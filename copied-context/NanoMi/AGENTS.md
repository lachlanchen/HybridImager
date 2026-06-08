# Repository Guidelines

## Project Structure & Modules
- Top-level directories contain CAD, electronics, documentation, and the main software repo under `NanoMi/`.
- The Python control software and tools live in `NanoMi/Software`, `NanoMi/STEM_Image_Generation_Code`, `NanoMi/RayOptics`, and `NanoMi/nanomi-optics`.
- Tests currently exist only for `nanomi-optics` under `NanoMi/nanomi-optics/tests`.
- Large CAD and electronics artifacts (for fabrication and reference) live in `CAD files`, `NanoMi electronics files`, and `2022 NanoMi paper`.

## Build, Test, and Development
- Use Python 3.9–3.10 for `nanomi-optics` (see `NanoMi/nanomi-optics/pyproject.toml`).
- From `NanoMi/nanomi-optics`, install deps with `poetry install` or `pip install -r` generated from `pyproject.toml`.
- Run optics tests from `NanoMi/nanomi-optics` with `pytest`.
- The main control application is launched from `NanoMi/Software/NANOmi.py` after installing its documented dependencies.

## Coding Style & Naming
- Use 4-space indentation for Python and follow PEP 8 where practical.
- Prefer descriptive snake_case for functions/variables and PascalCase for classes.
- Keep modules small and focused; mirror existing patterns in `nanomi-optics` and `Software/AddOnModules`.
- Do not reformat unrelated files; keep diffs minimal and focused on the feature or bug.

## Testing Guidelines
- Add or update tests in `NanoMi/nanomi-optics/tests` when touching that package.
- Name tests `test_<unit>.py` and use clear, behavior-focused test names.
- Run `pytest` before opening a pull request that changes `nanomi-optics`.
- For other Python areas, add lightweight tests where sensible, but avoid introducing new frameworks without discussion.

## Commit & Pull Request Practices
- Write concise commits with imperative subjects, e.g., `Add lens optimization helper` or `Fix STEM scanner config`.
- Group related changes into a single PR and avoid mixing refactors with behavior changes when possible.
- In PR descriptions, summarize the change, list key files (e.g., `Software/NANOmi.py`, `nanomi-optics/tests/...`), and reference any related issues.
- Include screenshots or short notes for UI-facing or optics-visualization changes when helpful for reviewers.

