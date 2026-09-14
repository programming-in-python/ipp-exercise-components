# Linting and Formatting

Style in this repository is enforced with [Ruff](https://github.com/astral-sh/ruff), an MIT-licensed linter and formatter maintained by Astral. Ruff is a development-only tool: it is listed in `requirements-dev.txt`, not `requirements.txt`, so it is never needed to run the exercises or the test suite. The configuration lives in `ruff.toml` and targets canonical, teaching-style PEP 8, so students learn idiomatic Python they can carry into any project.

## Running it

Install the development dependency and run Ruff from the command line. Do **not** install the Ruff editor extension; editor integration stays on the Microsoft Python and Pylance extensions, and Ruff runs from the terminal or CI.

```
pip install -r requirements-dev.txt
ruff check .          # report style issues
ruff check --fix .    # apply the safe fixes
ruff format .         # normalize formatting
```

`ruff check` reports rule violations; `ruff format` reflows code to a consistent shape (quote style, spacing, line wrapping, trailing whitespace). The two are independent, so run both.

## Why `select` and not `extend-select`

The config pins its rule set explicitly with `select` rather than adding to Ruff's built-in default with `extend-select`:

```toml
[lint]
select = ["E4", "E7", "E9", "F", "N", "D"]
ignore = ["D200", "D212"]
```

The reason is reproducibility. Ruff's default rule set has broadened across releases, and `extend-select` inherits whatever that moving default happens to be. On Ruff 0.16, inheriting the default pulled in roughly fifty extra findings the course never opted into, dominated by `LOG015` (using the root logger), plus `DTZ` (timezone-naive datetimes), `BLE` (blind except), `PLR` (pylint refactors), and `RUF` rules. Pinning with `select` fixes the exact set the course intends, so a `ruff check` here reports the same findings today and a year from now, regardless of Ruff's evolving defaults.

## What each selected group covers

| Code | Group | What it catches |
|---|---|---|
| `E4` | pycodestyle | Import formatting, for example imports not at the top of the file. |
| `E7` | pycodestyle | Statement-level errors, for example a bare `except:` or a `== False` comparison. |
| `E9` | pycodestyle | Syntax and runtime errors Ruff can detect statically. |
| `F` | Pyflakes | Real defects: unused imports, unused variables, undefined names. |
| `N` | pep8-naming | Idiomatic naming: `snake_case` functions, `CapWords` classes, `cls` as a classmethod's first argument. |
| `D` | pydocstyle | PEP 257 docstring conventions, read in Google style so `Args:` / `Returns:` / `Raises:` sections are parsed. |

`E4`, `E7`, `E9`, and `F` are Ruff's own historical default; `N` and `D` are the two groups this course adds to hold student code to idiomatic naming and documented interfaces.

## The `ignore` and per-file-ignore values

```toml
ignore = ["D200", "D212"]   # always-multi-line docstrings; summary on line two

[lint.pydocstyle]
convention = "google"

[lint.per-file-ignores]
"tests/**" = ["D100", "D101", "D102", "D103", "D104", "D107"]
"**/__init__.py" = ["D104"]
```

- **`D200` and `D212`:** the house docstring form is always multi-line, with the opening and closing `"""` each on their own line and the summary beginning on the line after the opening quotes, even for a single-sentence docstring. `D200` (a one-line docstring should fit on one line) and `D212` (summary on the first physical line) both push the other way, so they are ignored; `D213` (summary on the second line) then holds and defines the form.
- **`convention = "google"`:** tells pydocstyle to parse Google-style sections, which keeps `D417` (undocumented parameter) working as a useful check rather than misfiring.
- **`tests/**`:** test scenarios are documented in their method names (`test_parse_input_returns_empty_string_for_none`), not in docstrings, so the "missing docstring" rules (`D100`–`D107`) are silenced for the test tree.
- **`**/__init__.py`:** empty package markers do not earn a package docstring, so `D104` (undocumented public package) is silenced for them.

## Linting is safe under the test-driven structure

Ruff performs static analysis: it parses source text and never imports or executes the modules under test. A test module that imports a not-yet-written solution still lints cleanly, because the import statement is valid Python regardless of whether the target exists on disk. A student working in `labmodule05` sees `labmodule06`'s tests lint without error, even though the `labmodule06` solution does not exist yet.

The "unresolved import" markers that may appear in the editor come from Pylance's type checker, which does resolve imports; Ruff does not. At runtime, the `try/except ImportError` guard with `@unittest.skipUnless` keeps the suite from breaking, and a skipped test names the exact file to write in its skip reason. Run the suite with `-v` to see those reasons:

```
python -m unittest discover -s tests -t . -v
```

One consequence of the guard pattern: a few test modules import a solution's prerequisite classes purely to check availability, without referencing them in the test body. Ruff flags those as unused imports (`F401`), so they carry an explicit `# noqa: F401  (prerequisite availability guard)` marker to document that the import's presence is the check, not an oversight.
