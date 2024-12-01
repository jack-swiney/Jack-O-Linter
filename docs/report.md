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

This project aims to investigate the usefulness of popular static analysis tools **Pylint**, **Flake8**, and **MyPy**. These tools aim to solve varying challenges of static analysis in Python. This project then will take the three tools and combines them into an all-in-one static analysis tool called `Jack-O-Linter`. After its implementation, `Jack-O-Linter` will run against a popular Python library `requests`. "Requests is an elegant and simple HTTP library for Python, built for human beings,"[[2]]() created and maintained by the Python Software Foundation. Finally, this project will analyze the results, make recommendations for updates to the `requests` library, and suggest further improvements for `Jack-O-Linter`.

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

### Raw Outcomes

### Adjustments to `Jack-O-Linter` Configuration

### Static Analysis Results

#### Flake8

#### PyLint

#### MyPy

### Future Work and Recommendations

#### `Requests`

#### `Jack-O-Linter`

## VI. Conclusion

# Bibliography

- [[1]](https://www.tiobe.com/tiobe-index/) TIOBE Index for November 2024
- [[2]](https://requests.readthedocs.io/en/latest/) Requests read-the-docs
- [[3]](https://dl.acm.org/doi/pdf/10.1145/1646353.1646374) A few billion lines of code later
- [[4]](https://epub.fh-joanneum.at/obvfhjhs/content/titleinfo/9603356/full.pdf) Code Analysis and Data Collection Using Python Static Analysis Tools and SQLite
- [[5]](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9610640) Unambiguity of Python Language Elements for Static Analysis
- [[6]](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5590990) Mapping of Dynamic Language Constructs into Static Abstract Syntax Trees
- [[7]](https://ceur-ws.org/Vol-2508/paper-gul.pdf) Survey on Static Analysis Tools of Python Programs
- [[8]](https://scan.coverity.com/) Coverity Scan
- [[9]](https://pylint.readthedocs.io/en/stable/user_guide/messages/messages_overview.html) Pylint messages overview
- [[10]](https://flake8.pycqa.org/en/latest/user/options.html) Flake8 Configuration
- [[11]](https://mypy.readthedocs.io/en/stable/config_file.html) MyPy Configuration

<!-- TODO regex = "\[\[\d\]\]" -->
<!-- TODO fix inline citations -->
<!-- TODO add IEEE citation format -->