<div style="text-align: center;">
  <h1 style="margin: 0;">Jack-O-Linter</h1>
  <p>Static-Analysis All-In-One Tool</p>
  <h4 style="margin: 0;">Final Project Report</h4>
  <h4 style="margin: 0;">CS-6315: Automated Verification</h4>
  <h4 style="margin: 0;">Jack Swiney &lt;jackson.swiney@vanderbilt.edu&gt;</h4>
  <h4 style="margin: 0;">4 December, 2024</h4>
</div>

## I. Introduction

Static analysis is a key practice in modern software engineering. It enables developers and companies to identify bugs early, enforce coding standards, and improve source code maintainability without the need to execute code or write tests. According to the TIOBE index, Python is the most popular programming language as of November 2024[[1]](#tiobe-index). Python has a plethora of static analysis tools for organizations and developers to choose from.

### Project Objective

This project aims to investigate the usefulness of popular static analysis tools **Pylint**, **Flake8**, and **MyPy**. These tools aim to solve varying challenges of static analysis in Python. This project then will take the three tools and combines them into an all-in-one static analysis tool called `Jack-O-Linter`. After its implementation, `Jack-O-Linter` will run against a popular Python library `requests`. "Requests is an elegant and simple HTTP library for Python, built for human beings,"[[2]](#requests-rtd) created and maintained by the Python Software Foundation. Finally, this project will analyze the results, make recommendations for updates to the `requests` library, and suggest further improvements for `Jack-O-Linter`.

## II. Investigation

### Impacts and Benefits of Static Analysis

### Challenges of Static Analysis with Dynamic Languages

### Chosen Static Analysis Tools for `Jack-O-Linter`

#### Pylint

#### Flake8

#### PyDocLint

#### MyPy

## III. Implementation

### Software Design

### Parsing Output from Selected Tools

### Generating a Holistic `Jack-O-Linter` Score

## IV. Experiment - `Requests`

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

## V. Conclusion

# Bibliography

- [[1]](https://www.tiobe.com/tiobe-index/) TIOBE Index for November 2024
- [[2]](https://requests.readthedocs.io/en/latest/) Requests read-the-docs
