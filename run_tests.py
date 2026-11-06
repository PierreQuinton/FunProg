#!/usr/bin/env python3
"""Run the Church encodings tests without installing pytest.

Students only need a standard Python interpreter:

    python run_tests.py          # short summary
    python run_tests.py -v       # one line per test case

What it does
------------
* discovers every `test_*.py` file inside `tests/church_encodings`,
* provides a tiny stand-in for the `pytest` module (the test files only use
  `mark.parametrize`),
* runs every test function, expanding the parametrized cases,
* replaces every exercise item still left as `...` in `src/church_encodings`
  by a function that raises `NotImplementedYet`, so that the report can tell
  "wrong answer" apart from "not implemented yet".

Report legend
-------------
OK      every test passes
FAIL    at least one test gives a wrong result
TODO    at least one test hits an item still left as `...`
ERROR   anything else (syntax error, unexpected crash, ...)

The exit code is 0 only when every test passes.
"""

from __future__ import annotations

import ast
import importlib
import importlib.util
import itertools
import sys
import types
from pathlib import Path
from typing import Any, Callable, Iterator, NamedTuple

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"
PACKAGE = "church_encodings"
PKG_DIR = SRC_DIR / PACKAGE
TESTS_DIR = ROOT / "tests" / PACKAGE

VERBOSE = any(arg in sys.argv[1:] for arg in ("-v", "--verbose"))

OK, FAIL, TODO, ERROR = "OK", "FAIL", "TODO", "ERROR"
ELLIPSIS_TYPEERROR = "an item left as `...`"


class NotImplementedYet(Exception):
    """Raised in place of any exercise item still left as `...`."""

    def __init__(self, module: str, name: str) -> None:
        super().__init__(f"{module}.{name} is not implemented yet")
        self.module = module
        self.name = name


# ---------------------------------------------------------------------------
# A tiny stand-in for the pytest module
# ---------------------------------------------------------------------------
class _Mark:
    """Just enough of ``pytest.mark`` for the exercise test files."""

    def parametrize(self, argnames, argvalues, *args, **kwargs):
        def decorator(func):
            specs = list(getattr(func, "_parametrize", []))
            specs.append((argnames, list(argvalues)))
            func._parametrize = specs
            return func

        return decorator

    def __getattr__(self, name: str) -> Callable[..., Callable[..., Any]]:
        # Any other mark (skip, slow, ...) is accepted and ignored.
        def decorator(*args, **kwargs):
            return lambda func: func

        return decorator


def install_pytest_stub() -> None:
    """Make ``from pytest import mark`` work without pytest installed."""
    stub = types.ModuleType("pytest")
    stub.mark = _Mark()
    stub.__version__ = "stand-in provided by run_tests.py"
    sys.modules["pytest"] = stub


# ---------------------------------------------------------------------------
# Static scan of the exercise files: what is still `...`?
# ---------------------------------------------------------------------------
def _is_ellipsis(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value is Ellipsis


def _is_stub_body(body: list[ast.stmt]) -> bool:
    """A body that is exactly `...`, `pass` or `return ...`."""
    if len(body) != 1:
        return False
    stmt = body[0]
    return (
        isinstance(stmt, ast.Pass)
        or (isinstance(stmt, ast.Expr) and _is_ellipsis(stmt.value))
        or (isinstance(stmt, ast.Return) and _is_ellipsis(stmt.value))
    )


def scan_module(path: Path) -> tuple[list[str], list[str]]:
    """Return (every top-level name, names still left as `...`)."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError):
        return [], []
    names: list[str] = []
    missing: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            value, targets = node.value, node.targets
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            value, targets = node.value, [node.target]
        else:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.append(node.name)
                if not isinstance(node, ast.ClassDef) and _is_stub_body(node.body):
                    missing.append(node.name)
            elif isinstance(node, ast.ImportFrom):
                names.extend(alias.asname or alias.name for alias in node.names)
            elif isinstance(node, ast.Import):
                names.extend((alias.asname or alias.name).split(".")[0] for alias in node.names)
            continue
        bound = [t.id for t in targets if isinstance(t, ast.Name)]
        names.extend(bound)
        if _is_ellipsis(value):
            missing.extend(bound)
    return names, missing


def _raiser(module: str, name: str) -> Callable[..., Any]:
    def not_implemented(*args, **kwargs):
        raise NotImplementedYet(module, name)

    return not_implemented


def patch_module(module: types.ModuleType, full_name: str, missing: list[str]) -> None:
    """Replace every item left as `...` by a function raising NotImplementedYet."""
    for name in missing:
        try:
            current = getattr(module, name)
        except AttributeError:
            continue
        if current is Ellipsis or isinstance(current, types.FunctionType):
            setattr(module, name, _raiser(full_name, name))


def make_stub(full_name: str, path: Path) -> types.ModuleType:
    """A module whose every top-level name raises NotImplementedYet.

    Used when a module cannot even be imported because it calls one of its
    own `...` items at import time (e.g. `i_one = i_succ(i_zero)`).
    """
    names, _ = scan_module(path)
    stub = types.ModuleType(full_name)
    stub.__file__ = str(path)
    for name in names:
        setattr(stub, name, _raiser(full_name, name))
    return stub


# ---------------------------------------------------------------------------
# Loading the exercise modules, in dependency order
# ---------------------------------------------------------------------------
def _chain(exc: BaseException) -> Iterator[BaseException]:
    seen: set[int] = set()
    while exc is not None and id(exc) not in seen:
        yield exc
        seen.add(id(exc))
        exc = exc.__cause__ or exc.__context__


def _not_implemented_signal(exc: BaseException):
    """A NotImplementedYet (or ellipsis TypeError) found in the chain, if any."""
    for e in _chain(exc):
        if isinstance(e, NotImplementedYet):
            return e
    for e in _chain(exc):
        if isinstance(e, TypeError) and "ellipsis" in str(e).lower():
            return e
    return None


def _raising_module(exc: BaseException) -> str | None:
    """Name of the module whose code raised `exc` (the deepest frame)."""
    tb = exc.__traceback__
    if tb is None:
        return None
    while tb.tb_next is not None:
        tb = tb.tb_next
    return tb.tb_frame.f_globals.get("__name__")


def _module_dependencies(path: Path) -> set[str]:
    """The modules of the package that the file at `path` imports from."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError):
        return set()
    deps: set[str] = set()
    prefix = PACKAGE + "."
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith(prefix):
            deps.add(node.module[len(prefix):].split(".")[0])
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(prefix):
                    deps.add(alias.name[len(prefix):].split(".")[0])
    return deps


def _dependency_order(deps: dict[str, set[str]]) -> list[str]:
    """Order module names so that dependencies are imported first.

    This way a module always binds the patched (or stubbed) version of every
    `...` item it imports, which keeps the "missing: <name>" messages precise.
    Ties and dependency cycles are broken alphabetically.
    """
    order: list[str] = []
    remaining = dict(deps)
    while remaining:
        ready = sorted(
            name
            for name, needs in remaining.items()
            if not needs & (set(remaining) - {name})
        )
        if not ready:  # dependency cycle: break it alphabetically
            ready = [min(remaining)]
        for name in ready:
            order.append(name)
            del remaining[name]
    return order


def load_source_modules() -> dict[str, str]:
    """Import every module of the package, patching or stubbing `...` items.

    Returns a {module: state} mapping with states:
      "ok"     imported, `...` items patched
      "stub"   import failed because of its own `...` -> replaced by a stub
      "blocked" import failed because a dependency is not implemented yet
      "broken" import failed for another reason (syntax error, ...)
    """
    states: dict[str, str] = {}
    files = sorted(p for p in PKG_DIR.glob("*.py") if p.name != "__init__.py")
    deps = {p.stem: _module_dependencies(p) for p in files}
    pending = _dependency_order(deps)
    while pending:
        progress = False
        still: list[str] = []
        for stem in pending:
            full = f"{PACKAGE}.{stem}"
            path = PKG_DIR / f"{stem}.py"
            try:
                module = importlib.import_module(full)
            except Exception as exc:
                signal = _not_implemented_signal(exc)
                if signal is None:
                    states[stem] = "broken"
                    progress = True
                else:
                    own = (
                        signal.module == full
                        if isinstance(signal, NotImplementedYet)
                        else _raising_module(signal) == full
                    )
                    if own:
                        stub = make_stub(full, path)
                        sys.modules[full] = stub
                        parent = sys.modules.get(PACKAGE)
                        if parent is not None:
                            setattr(parent, stem, stub)
                        states[stem] = "stub"
                        progress = True
                    else:
                        still.append(stem)  # retry once the dependency is stubbed
            else:
                _, missing = scan_module(path)
                patch_module(module, full, missing)
                states[stem] = "ok"
                progress = True
        if not progress:
            for stem in still:
                states[stem] = "blocked"
            break
        pending = still
    return states


# ---------------------------------------------------------------------------
# Running the test files
# ---------------------------------------------------------------------------
class CaseResult(NamedTuple):
    label: str  # e.g. "test_add[3-5]"
    status: str  # OK / FAIL / TODO / ERROR
    detail: str  # exercise item, or short error message


class FileResult(NamedTuple):
    name: str  # display name, e.g. "bool"
    status: str
    passed: int
    total: int
    detail: str
    cases: list[CaseResult]


def _load_by_path(name: str, path: Path) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _expand(func: Callable[..., Any]) -> list[tuple[dict[str, Any], str]]:
    """All cases of a test function, as (kwargs, label) pairs."""
    specs = getattr(func, "_parametrize", [])
    if not specs:
        return [({}, "")]
    per_mark: list[list[dict[str, Any]]] = []
    for argnames, argvalues in specs:
        names = [n.strip() for n in str(argnames).split(",") if n.strip()]
        if not names:
            continue
        if len(names) == 1:
            combos = [{names[0]: v} for v in argvalues]
        else:
            combos = [dict(zip(names, tuple(v))) for v in argvalues]
        if not combos:  # empty parameter list: the test never runs
            return []
        per_mark.append(combos)
    if not per_mark:
        return [({}, "")]
    cases: list[tuple[dict[str, Any], str]] = []
    for parts in itertools.product(*per_mark):
        kwargs: dict[str, Any] = {}
        values: list[str] = []
        for part in parts:
            for key, value in part.items():
                kwargs[key] = value
                values.append(_id_value(value))
        label = "[" + "-".join(values) + "]"
        cases.append((kwargs, label))
    return cases


def _id_value(value: Any) -> str:
    if callable(value):
        return "fn"
    text = repr(value)
    return text if len(text) <= 12 else text[:11] + "..."


def _short(text: str, width: int = 64) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= width else text[: width - 3] + "..."


def _classify(exc: BaseException) -> tuple[str, str]:
    signal = _not_implemented_signal(exc)
    if signal is not None:
        item = signal.name if isinstance(signal, NotImplementedYet) else ELLIPSIS_TYPEERROR
        return TODO, item
    if isinstance(exc, AssertionError):
        return FAIL, _short(exc) or "assertion failed"
    return ERROR, _short(f"{type(exc).__name__}: {exc}")


def _display_name(path: Path) -> str:
    stem = path.stem
    return stem[5:] if stem.startswith("test_") else stem


def _module_name(path: Path) -> str:
    relative = path.relative_to(ROOT).with_suffix("")
    return "_runner_" + ".".join(relative.parts)


def _join(items: list[str], limit: int = 3) -> str:
    items = list(dict.fromkeys(items))
    if len(items) > limit:
        return ", ".join(items[:limit]) + ", ..."
    return ", ".join(items)


def run_test_file(path: Path) -> FileResult:
    cases: list[CaseResult] = []
    try:
        module = _load_by_path(_module_name(path), path)
    except Exception as exc:
        signal = _not_implemented_signal(exc)
        if signal is not None:
            if isinstance(signal, NotImplementedYet):
                where = signal.module
                if where.startswith(PACKAGE + "."):
                    where = where[len(PACKAGE) + 1 :]
                detail = f"blocked by {where}.{signal.name}"
            else:
                detail = f"blocked by {ELLIPSIS_TYPEERROR}"
            return FileResult(_display_name(path), TODO, 0, 0, detail, cases)
        return FileResult(_display_name(path), ERROR, 0, 0, _short(f"{type(exc).__name__}: {exc}"), cases)

    functions = [
        (name, obj)
        for name, obj in vars(module).items()
        if name.startswith("test") and callable(obj)
    ]
    for func_name, func in functions:
        for kwargs, label in _expand(func):
            try:
                func(**kwargs)
            except Exception as exc:
                status, detail = _classify(exc)
            else:
                status, detail = OK, ""
            cases.append(CaseResult(func_name + label, status, detail))

    passed = sum(1 for c in cases if c.status == OK)
    failing = [c.label.split("[")[0] for c in cases if c.status == FAIL]
    errors = [c.label.split("[")[0] for c in cases if c.status == ERROR]
    missing = [c.detail for c in cases if c.status == TODO]

    if cases and passed == len(cases):
        status = OK
    elif errors:
        status = ERROR
    elif failing:
        status = FAIL
    elif missing:
        status = TODO
    else:
        status = OK

    parts: list[str] = []
    if failing:
        parts.append("failing: " + _join(failing))
    if errors:
        parts.append("error in: " + _join(errors))
    if missing:
        parts.append("missing: " + _join(missing))
    if errors:
        parts.append(_short(next(c.detail for c in cases if c.status == ERROR)))
    return FileResult(_display_name(path), status, passed, len(cases), "; ".join(parts), cases)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def print_report(results: list[FileResult]) -> int:
    print(f"Church encodings -- {TESTS_DIR.relative_to(ROOT)}")
    print()
    for result in results:
        counts = f"{result.passed}/{result.total}"
        print(f"  {result.name:<13} {result.status:<6} {counts:>7}   {result.detail}".rstrip())
        if VERBOSE:
            for case in result.cases:
                line = f"      {case.label:<40} {case.status}"
                if case.detail and case.status != OK:
                    line += f"  {case.detail}"
                print(line)
    print()
    ok_files = sum(1 for r in results if r.status == OK)
    passed = sum(r.passed for r in results)
    total = sum(r.total for r in results)
    print(f"{ok_files}/{len(results)} files OK -- {passed}/{total} tests passed")
    print("legend: OK = all pass | FAIL = wrong result | TODO = not implemented yet | ERROR = unexpected problem")
    return 0 if all(r.status == OK for r in results) else 1


def main() -> int:
    if not TESTS_DIR.is_dir():
        print(f"No test directory: {TESTS_DIR}", file=sys.stderr)
        return 2
    install_pytest_stub()
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))
    sys.setrecursionlimit(10_000)
    load_source_modules()
    test_files = sorted(TESTS_DIR.rglob("test_*.py"))
    if not test_files:
        print(f"No test files found in {TESTS_DIR}", file=sys.stderr)
        return 2
    results = [run_test_file(path) for path in test_files]
    return print_report(results)


if __name__ == "__main__":
    sys.exit(main())
