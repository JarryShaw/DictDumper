---
name: Bug report
about: Create a report to help us improve
labels: bug

---

**Describe the bug**
A clear and concise description of what the bug is.

**Reproduction**
The shortest script that shows the problem, followed by the output you actually
got from running it. A reproduction that was executed is worth much more than one
written from memory, so please paste real output rather than describing it.

**Expected behavior**
A clear and concise description of what you expected to happen. Where a value is
simply wrong, the most useful form is the observed value next to the expected one.

**System information**
A clear and concise description of your system information.
 - OS Version: [e.g. macOS 15.3, Ubuntu 24.04, Windows 11]
 - Python Version: [e.g. 3.15, 3.13, 3.11]
 - Python Implementation: [e.g. CPython, PyPy]
 - `dictdumper` Version: [`python -c "import dictdumper; print(dictdumper.__version__)"`]
 - If you are working from a checkout rather than an installed release, please give
   the commit too [`git rev-parse --short HEAD`].

**Traceback stack**
If the bug raises, paste the full traceback. Plenty of defects are silent rather
than fatal -- if nothing is raised, say so and leave this section out.

**Additional context**
Add any other context about the problem here. If you have already found the
offending code, an exact `file:line` is the single most useful thing you can
include; so is a note on why the existing tests do not catch it.
