<div style="text-align: center;">
  <h1>Final Project Milestone Report</h1>
  <h4 style="margin: 0;">CS-6315: Automated Verification</h4>
  <h4 style="margin: 0;">Jack Swiney &lt;jackson.swiney@vanderbilt.edu&gt;</h4>
  <h4 style="margin: 0;">12 November, 2024</h4>
</div>

## Table of Contents

- [Completed Work](#completed-work)
    - [Initial Implementation](#initial-implementation)
    - [Implemented Static Analysis Tools](#implemented-static-analysis-tools)
        - [Flake8](#flake8)
        - [PyLint](#pylint)
        - [MyPy](#mypy)
- [Remaining Work](#remaining-work)
    - [Additional Static Analysis Tools](#additional-static-analysis-tools)
    - [Implement Dynamic Analysis Tools](#implement-dynamic-analysis-tools)
    - [Finish the Pipeline](#finish-the-pipeline)
- [Changes from Proposal](#changes-from-proposal)

## Completed Work

### Initial Implementation

- Created a repository. The source can be found on [GitHub](https://github.com/jack-swiney/Jack-O-Linter).
- Wrote an abstract base class for API wrappers. This will be used as a base for classes that wrap the API of the chosen analysis tools.

### Implemented Static Analysis Tools

Implemented API wrappers for the following static analysis tools:
#### [Flake8](https://flake8.pycqa.org/en/latest/index.html)

Flake8 is a static-analysis tool used to lint Python source code based on the PEP 8 standard. PEP 8 was derived from Guido von Rossum's (the original Python author) style guide, with some tweaks from Barry Warsaw (Python core engineer). Flake8 is a standard Python linter.

##### Issues Encountered

Flake8 has not maintained an API since v2.6 (now on v7.1+). The wrapper for Flake8 uses subprocess to shell out to the CLI. This isn't an ideal implementation since it relies on an additional shell.

#### [PyLint](https://pylint.readthedocs.io/en/stable/)

Pylint analyzes your code without actually running it. It checks for errors, enforces a coding standard, looks for code smells, and can make suggestions about how the code could be refactored.

##### Issues Encountered

PyLint has a convenient API for running the analysis tool and gathering stats. However, it doesn't have a great way to get the individual error/warning messages. The solution was to use a custom text reporter and parsing it with regular expressions.

#### [MyPy](https://mypy.readthedocs.io/en/stable/index.html)

MyPy is a static type checker for Python. Type checkers help ensure that you’re using variables and functions in your code correctly. With MyPy, add type hints (PEP 484) to your Python programs, and MyPy will warn you when you use those types incorrectly. Python is a dynamic language, so usually you’ll only see errors in your code when you attempt to run it. MyPy is a static checker, so it finds bugs in your programs without even running them! Typehinting is a contentious topic on Python. Python doesn't enforce any type checks, so adding typehints to functions, variables, etc., may seem like pointless extra work for some. I'm a big Pylance/Intellicode/Intellisense user, and adding typehints makes programming in Python much easier for more. Ergo, I wanted a static analysis tool to validate the typehints I provide.

##### Issues Encountered

Similar to PyLint, there's no easy way to parse the output of MyPy to get warnings and errors, so I used a regular-expression solution.

## Remaining Work

### Additional Static Analysis Tools

- Docstring linter
- Typehint enforcer

### Implement Dynamic Analysis Tools

- Following the proposal, implement Dynapyt, Typo, and research additional tools.

### Finish the Pipeline

- Add a Command-Line Interface (CLI).
- Add a common configuration. There are many command-line and config file options for each of the selected tools. I need to create a giant configuration schema with default values that will work for all the tools so users can just put their settings into a ".jackrc" file.
- Add unit tests
- Add GitHub actions

## Changes from Proposal

- Sonarlint requires a SonarQube server to be running, so this tool will not implement an interface for it.
- Added MyPy for typehinting.
- I'd like to add additional configuration for enforcing docstring styles (perhaps a flake8 plugin) and enforcing typehints (possibly a setting of MyPy).
