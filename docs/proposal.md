<div style="text-align: center;">
  <h1>Final Project Proposal</h1>
  <h4 style="margin: 0;">CS-6315: Automated Verification</h4>
  <h4 style="margin: 0;">Jack Swiney &lt;jackson.swiney@vanderbilt.edu&gt;</h4>
  <h4 style="margin: 0;">8 October, 2024</h4>
</div>

## Table of Contents

- [Introduction](#introduction)
- [Project Objective](#project-objective)
- [Project Scope](#project-scope)
  - [Research](#research)
    - [Static Analysis Tools](#static-analysis-tools)
    - [Dynamic Analysis Tools](#dynamic-analysis-tools)
  - [Tool Design and Implementation](#tool-design-and-implementation)
    - [Requirements](#requirements)
    - [Features of `Jack-o-Linter`](#features-of-jack-o-linter)
- [Methodology](#methodology)
  - [Phase 1: Research and Tool Selection](#phase-1-research-and-tool-selection)
  - [Phase 2: Tool Integration and Pipeline Design](#phase-2-tool-integration-and-pipeline-design)
  - [Phase 3: Validation and Testing](#phase-3-validation-and-testing)
  - [Phase 4: Report](#phase-4-report)
- [Conclusion](#conclusion)

## Introduction

In software development, both static and dynamic analysis play critical roles in ensuring code quality. Static analysis tools evaluate code without executing it, detecting potential issues such as syntax errors, “code smells”, and style inconsistencies. Dynamic analysis tools, on the other hand, inspect the behavior of code during execution, identifying runtime issues like unhandled exceptions, performance bottlenecks, and potential security vulnerabilities. This project aims to create a unified tool, `Jack-o-Linter`, which integrates both static and dynamic analysis methods to assess Python codebases for maintainability, complexity, type safety, and security concerns.

## Project Objective

The first objective of this project is to research off-the-shelf static and dynamic analysis tools and develop a pipeline that combines selected tools into a single utility, `Jack-o-Linter`, that can:

- Analyze readability and maintainability metrics.
- Measure code complexity and identify areas for refactoring.
- Assess type safety and ensure the proper use of type annotations where applicable.
- Detect potential security vulnerabilities in the code.

This tool will allow developers to run a single command to perform comprehensive code analysis, combining the strengths of both static and dynamic methods. At the end of the project, `Jack-o-Linter` will be tested on my personal code as well as larger open-source Python repositories.

The second objective is to write a report on `Jack-o-Linter`, including detailed analysis of:

- The various analysis tools researched
- Software design
- Product testing and outcomes
- Areas for future improvement

## Project Scope

### Research

Research into various off-the-shelf analysis tools is required before making choices on which to use and integrate into `Jack-o-Linter`. Research will include, but is not limited to, the following tools.

#### Static Analysis Tools

- **Sonarlint**: A tool that detects “code smells”, bugs, and potential vulnerabilities.
- **Pylint**: Used for code linting, enforcing coding standards, and evaluating code complexity.
- **Flake8**: A simple tool for checking the style guide compliance of Python code, often used in conjunction with other static analysis tools.

#### Dynamic Analysis Tools

- **Dynapyt**: A tool for dynamic analysis, focusing on capturing runtime behaviors and helping developers understand how their code behaves in real-world conditions.
- **Typo**: A tool for catching potential errors in Python by analyzing type hints and ensuring consistency in type annotations.
- Explore additional dynamic analysis tools that provide insights into runtime performance, memory management, and security vulnerabilities.

### Tool Design and Implementation

#### Requirements

- Provide a simple interface to run all selected analysis tools in one go.
- Generate reports on various metrics including code readability/maintainability, complexity, type safety, and security.
- Be flexible enough to allow users to select which checks they want to run.

#### Features of `Jack-o-Linter`

- Readability and Maintainability: Tools like Pylint will help identify areas of the code that are difficult to read or maintain, flagging issues like code reusability and poor naming conventions.
- Code Complexity: `Jack-o-Linter` will report on code complexity, with metrics such as cyclomatic complexity being derived from static analysis tools like Sonarlint.
- Type Safety: By integrating Typo and similar tools, `Jack-o-Linter` will check type annotations for correctness and consistency, helping ensure that run-time type errors are mitigated and Python’s type hinting system is used effectively.
- Security and Vulnerabilities: Static and dynamic analysis tools, such as Sonarlint and Dynapyt, will scan the code for potential vulnerabilities like unsafe function calls, improper exception handling, and unvalidated inputs.

## Methodology

### Phase 1: Research and Tool Selection

- Investigate the capabilities of static analysis tools like Pylint, Sonarlint, and Flake8.
- Research dynamic analysis tools, like Dynapyt and and Typo.
- Select the most appropriate tools based on the desired metrics (readability, complexity, type safety, security).

### Phase 2: Tool Integration and Pipeline Design

- Develop the structure for `Jack-o-Linter`, integrating the selected tools into a single pipeline.
- Create a unified interface that allows users to run multiple specified tools at once.
- Implement functionality for generating reports that summarize the findings of each analysis tool.

### Phase 3: Validation and Testing

- Run `Jack-o-Linter` on small Python codebases, including DoctoPi, to test functionality and accuracy.
- Validate the tool on larger, open-source Python repositories to ensure it can handle larger codebases and complex projects.
- Compare the tool’s output with existing tools to assess its effectiveness and reliability.

### Phase 4: Report

- Document research and tool selection.
- Discuss software design, problems, and solutions from implementation phase.
- Analyze results from testing phase.
- Draw conclusions from results, room for improvement, and retrospective.

## Conclusion

`Jack-o-Linter` will serve as a valuable asset for Python developers, combining the power of multiple static and dynamic analysis tools into a single, easy-to-use interface. With the ability to assess readability, complexity, type safety, and security, the tool will streamline the code review and refactoring process, ensuring that Python projects are not only functional but also maintainable, secure, and robust.