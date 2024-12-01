<div style="text-align: center;">
  <h1 style="margin: 0;">Jack-O-Linter</h1>
  <p>Static-Analysis All-In-One Tool</p>
  <h4 style="margin: 0;">Final Project Report</h4>
  <h4 style="margin: 0;">CS-6315: Automated Verification</h4>
  <h4 style="margin: 0;">Jack Swiney &lt;jackson.swiney@vanderbilt.edu&gt;</h4>
  <h4 style="margin: 0;">4 December, 2024</h4>
</div>

## I. Introduction

Static analysis is a key practice in modern software engineering. It enables developers and companies to identify bugs early, enforce coding standards, and improve source code maintainability without the need to execute code or write tests. According to the TIOBE index, Python is the most popular programming language as of November 2024[[1]](). Python has a plethora of static analysis tools for organizations and developers to choose from.

### Project Objective

This project aims to investigate the usefulness of popular static analysis tools **Pylint**, **Flake8**, and **MyPy**. These tools aim to solve varying challenges of static analysis in Python. This project then will take the three tools and combine them into an all-in-one static analysis tool called `Jack-O-Linter`. After its implementation, `Jack-O-Linter` will run against a popular Python library `requests`. "Requests is an elegant and simple HTTP library for Python, built for human beings,"[[2]]() created and maintained by the Python Software Foundation. Finally, this project will analyze the results, make recommendations for updates to the `requests` library, and suggest further improvements for `Jack-O-Linter`.

### Impacts and Benefits of Static Analysis

Static analysis offers numerous advantages that make it a crucial part of software engineering, the developer workflow, and CI/CD:

- **Error Detection**: Static analysis detects a broad spectrum of errors, including logical bugs, type mismatches, and adherence to coding standards, during early development phases.
- **Code Maintainability**: Tools like Pylint and Flake8 help enforce coding standards and measure code complexity, resulting in cleaner, more maintainable codebases. As highlighted, by measuring cyclomatic complexity, static analysis tools can pinpoint code sections that may be difficult to test or prone to errors.
- **Scalability**: Static analysis tools can process large codebases efficiently. For instance, scaling up from academic prototypes to industry tools required analyzing billions of lines of code, as demonstrated by the commercialization of Coverity[[3]]().
- **Security**: Static analysis often detects vulnerabilities such as improper input validation or insecure configurations, enhancing software security in critical applications.
- **Team Collaboration**: By enforcing consistent coding practices, static analysis fosters better collaboration among team members, especially in large projects.

### Challenges of Static Analysis with Dynamic Languages

Dynamic languages like Python pose several unique challenges for static analysis:

- **Type Ambiguity**: Python's lack of static type declarations makes it difficult to determine variable types and function signatures during analysis. Even tools like MyPy require explicit type annotations for effective analysis.
- **Dynamic Constructs**: Python allows features like dynamic method definitions and runtime attribute additions, complicating static analysis by making some constructs unpredictable.
- **Performance Overhead**: Handling Python’s flexibility often demands advanced techniques like AST traversal and runtime inference, which can impact performance and scalability
- **False Positives and Negatives**: Dynamic behavior can lead to inaccuracies in static analysis tools, with some errors being flagged incorrectly (false positives) or missed altogether (false negatives).

Despite these challenges, advancements like mapping dynamic constructs into static ASTs have improved the feasibility of static analysis in dynamic languages (Mapping of Dynamic Language Constructs into Static Abstract Syntax Trees).

## II. Literature Review

### A Few Billion Lines of Code Later[[3]]()

The popular commercial static analysis tool Coverity began as an academic research project. The tool was designed to find memory corruption, data races, mutex deadlocks, and other issues without needing to execute the code and write tests.

Coverity prioritizes finding as many bugs as possible, limiting false negatives. However, the paper emphasizes the importance of minimizing false positives, stating that as users detect false positives, they start to "ignore the tool. True bugs get lost in the false. A vicious cycle starts where low trust causes complex bugs to be labeled false positives, leading to yet lower trust"[[3]]().

When scaling the project from a research tool to a commercial product, the developers encountered several challenges handling large, diverse codebases. They found that many organizations used different build systems, including custom or undocumented ones that were hard to make integrate Coverity. Optimization issues became apparent as they started running against large codebases to improve runtime. They also noted that there was resistance from users, who were skeptical of using new tools that disrupted their workflow.

Coverity's key to success: focus on user experience. They prioritized ease-of-use to combat the resistance mentioned above. Additionally, they emphasized the importance of easy-to-read errors and output. After resolving the issues above and building trust with users, Coverity has grown to be used by over 50,000 users[[8]]().

### Code Analysis and Data Collection Using Python Static Analysis Tools and SQLite[[4]]()

This study explores the integration of Python static analysis tools — Pylint, Flake8, and Radon—to evaluate code quality. It employs SQLite for centralized storage and analysis of metrics generated by these tools.

- **Pylint**: Focuses on enforcing coding standards and identifying errors.
- **Flake8**: Integrates style checking and error detection.
- **Radon**: Provides metrics on code complexity (Cyclomatic Complexity, Maintainability Index, Halstead Metrics).

They were combined to deliver a holistic view of code quality. The analysis pipeline begins with running tools on the MyPy library, generating detailed reports. These reports are processed using Pandas for organization into structured data (DataFrames). Processed data is stored in an SQLite database, enabling advanced querying and insights into code trends.

Analysis of the MyPy library showcased practical insights, such as common coding violations and areas of high complexity. Managing and processing diverse outputs from different tools required significant effort in standardization. Complex queries for in-depth analysis pushed the database capabilities to their limits.

### Unambiguity of Python Language Elements for Static Analysis[[5]]()

This paper evaluates the feasibility and limitations of static analysis in Python. The authors developed a plugin for the CodeCompass framework to test the effectiveness of static analysis on real-world Python projects. Python, as a dynamically-typed language, presents the following issues highlighted in the paper:

- **Type Ambiguity**: Determining the type of variables and functions is inherently challenging due to Python's dynamic typing.
- **Symbol Definitions**: Identifying the declaration or definition of symbols can be ambiguous, especially when dependent on runtime conditions.
- **Dynamic Constructs**: Features like `getattr`, dynamic method calls, or class attribute assignments introduce complexity.
- **C Extensions**: Python functions implemented in C often lack sufficient metadata for analysis, making type deduction difficult.

After analyzing popular Python projects like Numpy, TensorFlow, and the Python Standard Library, over 60% of variables and function argument types could be determined statically. Less than 3% of variables or functions could be multiple types, suggesting that type ambiguity is less of an issue in Python than originally assumed.

### Mapping of Dynamic Language Constructs into Static Abstract Syntax Trees[[6]]()

It's important to note that the Python static analysis tools used by several of the previously mentioned papers are designed using Abstract Syntax Trees using a library called `Astroid`. This paper aims to investigate Abstract Syntax Trees (ASTs) and how they're used in static analysis of dynamic programming languages like Python or PHP. Constructs from the dynamic languages are mapped to static ASTs enabling static analysis tools to succeed.

Dynamic languages define and redefine constructs at runtime, making type information and variable declarations unavailable during static analysis. Constructs like variable types, dynamically added class members, and runtime expressions require special handling to estimate their behavior. The paper proposes a two-step solution to these issues:

1. **Syntactic Analysis**: Creates an initial AST based on the static elements of the code.
1. **Semantic Analysis**: Adds dynamic constructs and inferred information into the AST, converting it into a static representation suitable for further analysis.

These static analysis tools can then apply the following patterns to perform the static analysis:

- **Dynamic Constructs Mapping**: Dynamic constructs like variable declarations, assignments, and function calls are analyzed and represented statically in the AST.
- **Lazy Mapping**: Only parts of the AST are processed initially, with additional details added on demand to optimize performance.
- **Visitor Pattern**: Traverses the AST nodes to apply specific transformations or gather metadata.

### Survey on Static Analysis Tools of Python Programs[[7]]()

All of the following tools use `Astroid` to generate Abstract Syntax Trees for static analysis. This paper compares and contrasts a few of the most popular Python static analysis tools. Below are summaries for the chosen tools, `Pylint`, `Flake8`, and `MyPy`.

#### `Pylint`

`Pylint` is the most popular Python static analysis tool. It is free and capable of catching logical errors, warning about coding standards, offering details about code complexity, and suggesting refactoring opportunities.

##### Features

- Uses an Abstract Syntax Tree (AST), built with the help of the Astroid library, for its analysis.
- Supports custom plugins, enabling developers to extend the tool for specific checks.
Integrated into many popular IDEs and frameworks (e.g., PyCharm, VSCode, Django, Eclipse with PyDev).
- Widely used by tech leaders like Google, where it is part of Python codebase maintenance despite some known imperfections.

##### Strengths

- Identifies a broad range of logical errors, including: too many positional arguments and closure bugs.
- Generates descriptive and detailed output reports.

##### Limitations

- Can produce verbose and noisy output, especially with large codebases.
- Not as effective in handling type annotation-related bugs compared to MyPy.

#### `Flake8`

Flake8 is a wrapper that combines `Pyflakes` (for logical errors), `pycodestyle` (for style checks), and `McCabe` (for code complexity).

##### Features

- Focused on checking PEP8 compliance alongside logical errors.
- Designed for developers who want lightweight logical error detection combined with stylistic checks.

##### Strengths

- Covers some logical errors detected by `Pyflakes`.
- Simpler to use and configure for quick PEP8 validation.

##### Limitations

- Does not extend significantly beyond `Pyflakes`' capabilities in detecting logical errors.
- Limited detection of complex logical issues compared to tools like `Pylint` or `MyPy`.

#### `MyPy`

`MyPy` is an experimental and optional static checker with a strong focus on type checking.

##### Features

- Combines the benefits of dynamic and static typing.
- Particularly effective in analyzing type annotations, catching type-related bugs that other tools miss.

##### Strengths

- Detected type annotation errors in test cases where other tools failed, such as Passing parameters of a different type than intended.
- Essential for projects that rely heavily on type annotations for better clarity and error prevention.

##### Limitations

- Still considered experimental and not as mature or comprehensive in general-purpose static analysis as `Pylint`.
- Focuses solely on type-related issues, leaving broader logical error checks to other tools.

#### Comparison

- `Pylint`: Most versatile and descriptive but noisy for large projects.
- `Flake8`: Lightweight with stylistic checks but limited logical error detection.
- `MyPy`: Exceptional for type-related issues but experimental and specialized.

## III. Requirements

1. `Pylint`
    1. `Jack-O-Linter` must "wrap" the API for execution.
    1. `Jack-O-Linter` must compile errors and warnings from static analysis.
    1. `Jack-O-Linter` must generate a score out of 100 from the results of static analysis.
1. `Flake8`
    1. `Jack-O-Linter` must "wrap" the API for execution.
    1. `Jack-O-Linter` must compile errors and warnings from static analysis.
    1. `Jack-O-Linter` must generate a score out of 100 from the results of static analysis.
1. `MyPy`
    1. `Jack-O-Linter` must "wrap" the APIs for execution.
    1. `Jack-O-Linter` must compile errors and warnings from static analysis.
    1. `Jack-O-Linter` must generate a score out of 100 from the results of static analysis.
1. `Jack-O-Linter` must have a common configuration platform to configure all three APIs via a single config file.
1. `Jack-O-Linter` must have a Command Line Interface (CLI) to execute the tool and generate a report.

## IV. Implementation

### Implementing Requirements 1.x for `Pylint`

#### 1.1: `Jack-O-Linter` must "wrap" the API for `Pylint`

`Pylint`'s API defines a class `pylint.lint.Run()`. This class is the equivalent of the entrypoint to the `Pylint` CLI tool. The `jack_o_linter.pylint.PyLint.run(target, *args, **kwargs)` function formats the provided positional and keyword arguments for the `Run` class from pylint, sets the tool to raise no exceptions if the static analysis contains errors, and executes `Pylint`.

#### 1.2: `Jack-O-Linter` must compile errors and warnings from `Pylint`

The `Run` class also takes an IO buffer as one of its constructor arguments. This IO buffer stores the output from Pylint, similar to what a user would see in standard output if using the Pylint CLI directly.

Pylint "error" messages have a code specifying the issue. Each of these codes contains a character to signal the category of issue and an integer to point to the specific issue. The categories are as follows[[9]]():

- **F** - Fatal
- **E** - Error
- **W** - Warning
- **C** - Convention
- **R** - Refactor
- **I** - Information

The `Pylint` messages go into more specificity than required by `Jack-O-Linter`, so they are organized as follows:

- Fatal, Error, Convention, and Refactor are mapped to `Jack-O-Linter` "errors".
- Warning and Information are mapped to `Jack-O-Linter` "warnings".

`Jack-O-Linter` uses regular expressions to parse the error codes from the IO buffer and store the error and warnings from the raw static analysis results.

#### 1.3: `Jack-O-Linter` must generate a score out of 100 from the results of static analysis

`Pylint` already generates a score from [0, 10], where 10 is a perfect score. `Jack-O-Linter` simply multiplies the provided score by 10 to get a score out of 100.

### Implementing Requirements 2.x for `Flake8`

#### 2.1: `Jack-O-Linter` must "wrap" the API for `Flake8`

Unlike `Pylint`, recent versions of `Flake8` do not provide an API. `Jack-O-Linter` implements requirement 2.1 by using the Python standard library's `subprocess.run` to shell out to the `Flake8` CLI.

#### 2.2: `Jack-O-Linter` must compile errors and warnings from `Flake8`

`subprocess.run` gives access to the standard output from executing the `flake8` CLI. All `Flake8` error messages have a code similar to `PyLint`, with the category "F" for fatal. Other plugins include their own error message codes. `PyCodeStyle`, which is bundled with `Flake8`, has "E" for error and "W" for warning. `McCabe`, the code complexity plugin provided with `Flake8`, only has "C" for complexity.

"E" and "F" are processed by `Jack-O-Linter` as errors, while "W" and "C" are processed as warnings.

`Jack-O-Linter` had a stretch goal to implement docstring linting. By bundling the `Flake8` extension `Pydoclint` with this package, docstring linting is also available. `Pydoclint` use the error message prefix "DOC" for docstring issues. This is processed as an warning as well.

#### 2.3: `Jack-O-Linter` must generate a score out of 100 from the results of static analysis

The score for `Flake8` is calculated with the following equation:

```python
points_lost_for_errors = 100 * (number_of_errors / source_lines_of_code)
points_lost_for_warnings = 50 * (number_of_errors / source_lines_of_code)

score = max(0, 100 - points_lost_for_errors - points_lost_for_warnings)
```

### Implementing Requirements 3.x for `MyPy`

#### 3.1: `Jack-O-Linter` must "wrap" the API for `MyPy`

`MyPy` provides a convenient API that requires significantly less configuration than the other tools. `mypy.api.run(*args)` will execute the `MyPy` tool programmatically.

#### 3.2: `Jack-O-Linter` must compile errors and warnings from `MyPy`

`mypy.api.run` returns the standard output from the `MyPy` run, the same as what a user would see if running the `MyPy` CLI. Error lines from standard out contain the word "error". Warnings contain the word "note". Regular expressions can categorize the output into errors and warnings.

The "note" keyword unfortunately contains literal notes as well as warnings, so this implementation causes some false positives. E.g. `note: Hint: "python3 -m pip install types-simplejson"`.

#### 3.3: `Jack-O-Linter` must generate a score out of 100 from the results of static analysis

The score for `MyPy` is calculated with the following equation:

```python
points_lost_for_errors = 100 * (number_of_errors / source_lines_of_code)
points_lost_for_warnings = 50 * (number_of_errors / source_lines_of_code)

score = max(0, 100 - points_lost_for_errors - points_lost_for_warnings)
```

### Implementing Requirement 4: `Jack-O-Linter` must have a common configuration platform to configure all three APIs via a single config file.

`Jack-O-Linter` comes with a default YAML file with organized configuration for the included static analysis tools. The defaults for `Pylint` come from the output of `pylint --generate-rcfile` which creates a config with all possible options for pylint. The default settings for `Flake8` come from the official documentation[[10]]() as does `MyPy`[[11]]().

Users can provide their own configuration file to override the provided defaults and use the CLI to point to their configuration.

### Implementing Requirement 5: `Jack-O-Linter` must have a Command Line Interface (CLI) to execute the tool and generate a report.

`Jack-O-Linter` is built with Python Package Authority (PyPA)'s `build` package. This bundles the source code, default configuration, and main entrypoint `__main__.py`. When executing `Jack-O-Linter` as a module script via `python -m jack_o_linter`, the `__main__.py` module runs by default.

`__main__.py` uses the Python standard library's `argparse` to add the following arguments:

```
usage: python -m jack_o_linter [-h] [--fail-under FAIL_UNDER] [--rcfile RCFILE] path

Jack-O-Linter Code Analysis

positional arguments:
  path                  Path to a file or directory.

options:
  -h, --help            show this help message and exit
  --fail-under FAIL_UNDER
                        Specify a score threshold under which the program will exit with error. (default: 100)
  --rcfile RCFILE       Specify a Jack-O-Linter RC file.
```

## V. Experiment - `Requests`

### Overview

This experiment aims to test `Jack-O-Linter` against one of the top-10 most popular python libraries, `requests`. "The request library allows you to send HTTP requests extremely easily. It is widely used for interacting with the web APIs"[[12]]().

`requests` is maintained by the Python Software Foundation (PSF). "The Python Software Foundation is an organization devoted to advancing open source technology related to the Python programming language"[[12]](). They "support and maintain python.org, The Python Package Index, Python Documentation, and many other services the Python Community relies on"[[12]]().

Due to the nature of the Python Software Foundation and their impact on the Python community, as well as the popularity of the `requests` library, it is expected to follow PEP 8 standards thoroughly and be written with minimal static analysis findings. Hopefully, executing `Jack-O-Linter` against will have the following outcomes:

1. Provide insights on how `requests` can be improved.
1. Highlight any issues with `Jack-O-Linter` or room for improvement.

### Raw Outcomes

The first portion of the test is to run `Jack-O-Linter` against `requests` by cloning the repository locally and executing `python -m jack_o_linter src/requests` without any custom configuration. This will provide a baseline and show all issues with `requests`, including some the PSF may not care about. The raw results are as follows:

| Static Analysis Tool | Score (Out of 100) | Errors | Warnings |
| -------------------- | ------------------ | ------ | -------- |
| `Pylint` | 70.83 | 287 | 207 |
| `Flake8` | 94.62 | 98 | 101 |
| `MyPy` | 90.15 | 265 | 14 |

### Adding Configuration from `Requests` Project

The next portion of the test is to run against `requests` with custom configuration, gathered from the project. Inline comments below show the purpose of each setting.

```yaml
flake8:
  ignore:
    # These are explicitly ignored per the requests configuraiton.
    # See here: https://github.com/psf/requests/blob/main/setup.cfg
    - E203
    - E501
    - W503
    - W504
    # According to Pycodestyle's documentation, W505 is not enforced
    # by default, so this re-disables it.
    # See here: https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes
    - W505
    # Requests does not use Pydoclint to lint their docstrings
    - DOC
  # The requests configuration also explicitly disables these errors
  # on a per-file basis
  per-file-ignores:
    - src/requests/__init__.py:E402, F401
    - src/requests/compat.py:E402, F401
    - tests/compat.py:F401
  # Flake8 does not run McCabe by default, only if max-complexity is
  # set. This re-disables it.
  max-complexity: ""

mypy:
  # This setting was a stretch goal of Jack-O-Linter: to enforce
  # type hints in the source code. Most projects, including requests,
  # do not adhere to this requirement.
  disallow_untyped_defs: false
```

The updated results are as follows:

| Static Analysis Tool | Score (Out of 100) | Errors | Warnings |
| -------------------- | ------------------ | ------ | -------- |
| `Pylint` | 70.83 | 287 | 207 |
| `Flake8` | 100| 0 | 0 |
| `MyPy` | 98.93 | 28 | 3 |

### Recommending Additional Configuration

In addition to the project settings from `requests`, the following settings will help filter out the errors PSF clearly ignores during implementation. In addition, the dependency `types-pyOpenSSL` was installed per the recommendation of `MyPy` which adds type hints for OpenSSL.

```yaml
pylint:
  messages-control:
    disable:
      # Defaults of Pylint
      - raw-checker-failed
      - bad-inline-option
      - locally-disabled
      - file-ignored
      - suppressed-message
      - useless-suppression
      - deprecated-pragma
      - use-symbolic-message-instead
      - use-implicit-booleaness-not-comparison-to-string
      - use-implicit-booleaness-not-comparison-to-zero
      # PSF does not require docstrings for every function and module
      - missing-function-docstring
      - missing-module-docstring
      # PSF does not adhere to Pylint's preferred order of imports
      - wrong-import-position
      - wrong-import-order
      - ungrouped-imports
      # PSF does not adhere to Pylint's naming conventions (camel case, snake case, etc.)
      - invalid-name
      # PSF does not adhere to Pylint's limits for public methods, arguments, branches, etc.
      - too-many-arguments
      - too-many-positional-arguments
      - too-many-lines
      - too-many-statements
      - too-many-locals
      - too-many-branches
      - too-few-public-methods
      # PSF ignores line length warnings in Flake8, so ignore them in Pylint as well
      - line-too-long
      # Requests has many TODO/FIXMEs that PSF allows in-code
      - fixme
      # Requests has many unused imports
      - unused-import
      # Pylint recommends to raise custom exceptions from the originals to get the full stack
      # trace, but PSF does not adhere to this recommendation
      - raise-missing-from
      # Requests access protected members of classes they maintain often. They are likely
      # protected to prevent users from accidentally accessing them, but PSF needs access.
      - protected-access
      # Pylint has error messages specific to usage of the requests library to protect
      # users from unintentional behavior. PSF ignores these errors given the nature.
      - missing-timeout
```

The updated results are as follows:

| Static Analysis Tool | Score (Out of 100) | Errors | Warnings |
| -------------------- | ------------------ | ------ | -------- |
| `Pylint` | 87.23 | 81 | 52 |
| `Flake8` | 100| 0 | 0 |
| `MyPy` | 98.93 | 28 | 3 |

### Static Analysis Results

#### Flake8

##### Default Configuration:

The majority of errors came from imports, with many cases of unused imports or imports in the wrong location within the Python files. There were also 17 cases of lines over 100 characters long (note that the default for Flake8 is 79 but `Jack-O-Linter` uses 100 by default to match `Pylint`). Warnings were primarily from docstring/comment lines being over 80 characters long. There were also a couple complexity warnings from `McCabe`.

> **NOTE**: The raw output from Flake8 has a few `DOC` error codes on the error side, and a few `F` error codes on the warning side, suggesting that the regular expressions to separate warnings from errors are not working with 100% accuracy.

##### Project Configuration:

The `Requests` project uses "Pre-Commit" to execute various static analysis tools during CI/CD, including `Flake8`. Pre-Commit is "a framework for managing and maintaining multi-language pre-commit hooks"[[13]](). By applying PSF's `Flake8` configuration from the repository, all `Flake8` errors and warnings were eliminated.

##### Recommended Configuration:

No additional recommendations were needed because Flake8 was already at a score of 100.

#### PyLint

##### Default Configuration:

`Pylint` has many varying issues. Import errors and missing function/method docstrings are among the most frequent. There are also cases of non-conforming variable names, functions with too many statementso or branches, functions with too many arguments, line-length issues, and issues of variables or modules missing an expected member. Among the warnings are warnings of improperly named variables (i.e. reusing the name of an import for a variable later), accessing protected members, "FIXME"/"TODO" comments left in the code, and warnings about handling exceptions.

##### Project Configuration:

The `Requests` project does not use `Pylint`, so there were no updates from the default, resulting in the same issues as above.

##### Recommended Configuration:

`Pylint` found hundreds of errors and warnings in requests. Pylint has error and warning codes specific to users who use the requests library, so some of the messages like `missing-timeout` or `protected-access` were removed due to the nature of PSF bending the rules to write the library itself. The library was also missing many function and module docstrings, which are not a requirement of other linters like `Flake8`. `Requests` also handles errors themselves rather than using the `from` keyword to raise an error using the stacktrace of another. According to `Pylint` standards, the correct order of imports is "Python standard library imports", "third-party imports", then "first-party imports"[[15]](). Finally, `requests` does not adhere to Pylint's standards for maintainability standards like lines of code in a file, branches in a function, number of arguments for a function, etc.

By ignoring all of these errors (along with the default ignores), The score for `Pylint` increased dramatically from 70.83 to 87.23

#### MyPy

##### Default Configuration:

`MyPy` errors were mostly from missing type annotations. `Jack-O-Linter` requires type annotations in all functions by default as a personal preference of the project owner. The second largest sources of error were type incompatibilities, assigning the null `NoneType` to variables. `MyPy` expects the type of variables to be type-hinted as `Optional[<some-type>]` if they can be null. The other errors included a few imports of C libraries without type stubs (*.pyi files) or reusing variable names. Warnings were primarily from functions without return type annotations (or false positives like "Hint: python3 -m pip install types-pyOpenSSL")

##### Project Configuration:

`Jack-O-Linter` defaults the `MyPy` setting for `disallow_untyped_defs` to true. This was a stretch goal to force the Python code under test to use type hints. According to Pouya Hallaj, "Type hints serve as documentation for function parameters and return types, making it easier for developers to understand and use APIs. Instead of relying on external documentation or guessing the expected types, developers can refer to the type hints directly in the code. This results in better API design, as the expected input and output types are explicitly defined"[[14]]().

However, most Python projects do not adhere to this requirement. By disabling this check, the `MyPy` score significantly improved, going from 90.15 to 98.93.

##### Recommended Configuration:

Installing the recommended type hint dependencies increased the score for MyPy from 98.13 to 99.00.

### Future Work and Recommendations

#### `Requests`

While some of the errors and warnings from `Requests` can be safely ignored by PSF, there are a few that were ignored in the recommended settings that serve a valuable purpose in static analysis:

1. The standards like `max-line-length`, `too-many-arguments`, `too-many-statements`, etc. should not be ignored. These standards are to improve readability and maintainability of the software. Minimizing the amount of code in a function, method, or file promotes better organization of code and keeps developers accountable for the scope of each function, method, and file.
1. `Requests` does not follow `Pylint`'s naming conventions for functions, variables, or constants. While they may seem arbitrary, naming conventions are important in Python due to it's dynamic nature. Well-named variables help provide information about the variable, since types aren't always provided. Naming styles (uppercase, camel case, snake case, etc.) help distinguish between variables, constants, and classes.

There are still over 100 errors and warnings from `Pylint`, despite ignoring a large list of error codes. These are errors that are unsafe to ignore, and should be prioritized by PSF to resolve.

1. The `redefined-argument-from-local` error is raised several times. This error occurs when a local variable in a function or method is redefining an argument. This makes the code harder to read and opens the door for potential bugs from unintended behavior.
1. The `no-member` error is raised over 30 times. This error occurs when attempting to access a function or variable of a class that does not exist. 24 of these errors occur because `requests` defines a custom class that extends the builtin Python dictionary which dynamically creates an attribute for each key in the dictionary. The other 10 are from the `pypy` library which dynamically adds the attribute `pypy_version_info` to the standard library `sys`. The `no-member` error should not be blanket-ignored, by adding in-line comments to ignore these errors where they occur would be helpful for improving the linter's score.
1. The import errors suggest `Pylint` is unable to lint a C library or the developer requirements.txt file is missing dependencies.

Finally, there are various errors with minimal impacts:

1. The `consider-using-f-string` suggests users should use the Python 3.x f-string to format strings. Some repositories use the Python 2.x formatting syntax which is still acceptable and has not been deprecated.
1. Return statement errors like `inconsistent-return-statement` and `too-many-returns` signal a readability issue in the code, but nothing more. For example, if a function returns an optional string, it should explicitly return a string or explicitly return a null.

Warnings from `Pylint`, which have a much lower impact, include the following:

1. There are 20 `redefining-builtin` errors which all come from `requests` creating variables to point to builtins with the same name. This seems redundant, but perhaps there was a reason for this.
1. There are 10 `redefining-outer-name` errors. Each of these comes from a function argument where an import ("outer name" variable) is intended to be the function argument. Assuming developers understand variable scope in Python, these errors could be ignored.
1. There are 10 occurrences of `unused-argument` and `unused-variable` which should be cleaned up.

#### `Jack-O-Linter`

1. **Minimize False Positives**: The paper "A Billion Lines of Code Later" emphasized the importance of minimizing false positives, suggesting that they severely impact user trust[[3]](). The regular expression to find warnings in the `MyPy` results creates false positives and needs to be adjusted to filter out the literal notes and only provide the warnings.
1. **Fix Flake8 Error/Warning Distinction**: The regular expressions used to separate warnings from errors had some inaccuracies. Though the warnings and errors were still being reported, this suggests there could be additional false positives or false negatives by improperly handling the output of `Flake8`.
1. **Create Common Configuration**: There are several settings of the static analysis tools that could be made common. E.g. `Pylint` and `Flake8` both have settings for the maximum length of a line. These types of settings should be set from a common configuration rather than forcing users to set them in both places. This would have minimized the amount of confiugration required for `Requests`.
1. **Improve Scoring Algorithm**: The scores from `Pylint`, `Flake8`, and `MyPy` were drastically different, even when the number of errors and warnings was similar across the different static analysis tools. `Pylint` is the only tool that provides its own score metric, so it should be set as the baseline. The other two tools' scores were inflated in comparison, so the algorithm for those should be tweaked to be proportional to `Pylint`.

## VI. Conclusion

The development and evaluation of `Jack-O-Linter` have highlighted both the potential and challenges of creating a unified static analysis tool for Python. By combining `Pylint`, `Flake8`, and `MyPy`, `Jack-O-Linter` provides developers with a comprehensive platform to improve code quality, enforce coding standards, and identify bugs efficiently. The experimental application to the `Requests` library revealed key insights into both the effectiveness of the tool and the current limitations of popular Python static analysis practices.

`Jack-O-Linter` demonstrated the ability to consolidate outputs and configurations, improving usability and scalability for large projects. However, discrepancies in scoring, false positives, and limitations in tool integrations underline the need for further refinement. Addressing these issues, particularly harmonizing configurations across tools and improving output accuracy, will enhance user trust and adoption.

For the `Requests` library, the results emphasized areas for improvement, including adherence to naming conventions, managing complexity in functions, and addressing type ambiguity. Incorporating such recommendations will ensure greater maintainability and readability in codebases, aligning with Python's principles of simplicity and clarity.

Ultimately, `Jack-O-Linter` has proven to be a valuable asset for Python developers, streamlining static analysis processes. With continued enhancements, it has the potential to set a new standard for multi-tool static analysis, empowering teams to deliver cleaner, more reliable code while maintaining flexibility to adapt to specific project requirements.

# Bibliography

[1] TIOBE, “TIOBE Index | TIOBE - The Software Quality Company,” Tiobe.com, 2024. https://www.tiobe.com/tiobe-index/ (accessed Dec. 01, 2024).

[2] “Requests: HTTP for HumansTM — Requests 2.32.3 documentation,” Readthedocs.io, 2024. https://requests.readthedocs.io/en/stable/ (accessed Dec. 01, 2024).

[3] A. Bessey et al., “A few billion lines of code later,” Communications of the ACM, vol. 53, no. 2, pp. 66–75, Feb. 2010, doi: https://doi.org/10.1145/1646353.1646374.

[4] “Code Analysis and Data Collection using Python Static Analysis Tools and SQLite.” Available: https://epub.fh-joanneum.at/obvfhjhs/content/titleinfo/9603356/full.pdf

[5] B. Nagy, T. Brunner, and Zoltan Porkolab, “Unambiguity of Python Language Elements for Static Analysis,” Sep. 2021, doi: https://doi.org/10.1109/scam52516.2021.00017.

[6] J. Misek and F. Zavoral, “Mapping of Dynamic Language Constructs into Static Abstract Syntax Trees,” pp. 625–630, Aug. 2010, doi: https://doi.org/10.1109/icis.2010.100.

[7] H. Gulabovska and Z. Porkoláb, “Survey on Static Analysis Tools of Python Programs.” Available: https://ceur-ws.org/Vol-2508/paper-gul.pdf

[8] “Coverity Scan - Static Analysis,” scan.coverity.com. https://scan.coverity.com/

[9] “Messages overview - Pylint 3.3.2 documentation,” Readthedocs.io, 2024. https://pylint.readthedocs.io/en/stable/user_guide/messages/messages_overview.html (accessed Dec. 01, 2024).

[10] “Full Listing of Options and Their Descriptions — flake8 7.1.0 documentation,” Pycqa.org, 2020. https://flake8.pycqa.org/en/latest/user/options.html (accessed Dec. 01, 2024).

[11] “The mypy configuration file - mypy 1.13.0 documentation,” Readthedocs.io, 2022. https://mypy.readthedocs.io/en/stable/config_file.html (accessed Dec. 01, 2024).

[12] “Top 20 Python Libraries To Know in 2024,” GeeksforGeeks, Jan. 26, 2024. https://www.geeksforgeeks.org/python-libraries-to-know/ (accessed Dec. 01, 2024).

[13] “pre-commit,” pre-commit.com. https://pre-commit.com/ (accessed Dec. 01, 2024).

[14] Pouya Hallaj, “Mastering Type Hints in Python | By Pouya Hallaj | Medium,” Medium, Jun. 03, 2023. https://medium.com/@pouyahallaj/type-hints-in-python-why-you-should-embrace-static-typing-11cddf7036c2 (accessed Dec. 01, 2024).

[15] “wrong-import-order / C0411 - Pylint 3.3.2 documentation,” Readthedocs.io, 2024. https://pylint.readthedocs.io/en/stable/user_guide/messages/convention/wrong-import-order.html (accessed Dec. 01, 2024).


<!-- TODO regex = "\[\[\d\]\]" -->
<!-- TODO fix inline citations -->
<!-- TODO add IEEE citation format -->