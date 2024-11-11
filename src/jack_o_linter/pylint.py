"""PyLint Wrapper"""
# Standard imports
import io
import re

# Third-party imports
from pathlib import Path
from pylint import lint
from pylint.reporters.text import TextReporter

# Local imports
from jack_o_linter.common import APIWrapper


class PyLint(APIWrapper):
    """Wrapper class for running PyLint static analysis.

    Attributes:
        score (Optional[float]): Score out of 100 based on pylint results.
        errors (Optional[List[str]]): List of errors.
        warnings (Optional[List[str]]): List of warnings.
    """

    def run(self, target: Path, *args, **kwargs):
        """Run PyLint on the given target file or directory.

        Updates the class attributes for score, errors, and warnings.

        Args:
            target (Path): The file or directory to run PyLint against.
        """
        # Set up Pylint with a custom string buffer to capture output
        pylint_output = io.StringIO()
        reporter = TextReporter(pylint_output)

        # Run pylint and get the score (convert to score / 100)
        results = lint.Run(self._convert_args_to_list(target, *args, **kwargs),
                              reporter=reporter,
                              exit=False)
        self.score = results.linter.stats.global_note * 10

        # Extract errors and warnings
        pylint_output.seek(0)
        output_lines = pylint_output.read().splitlines()
        self.errors = [
            # Extract pylint "Fatal", "Error", "Convention", and "Refactor" messages
            line for line in output_lines if re.search(r":\s+([FECR]\d{4}):", line) is not None
        ]
        self.warnings = [
            # Extract pylint "Warning" and "Information" messages
            line for line in output_lines if re.search(r":\s+([WI]\d{4}):", line) is not None
        ]
