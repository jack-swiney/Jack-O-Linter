"""Flake8 Wrapper. Flake8 has not maintained an API since version 2.6.0, so
this module shells out to the CLI using subprocess"""
# Third-party imports
import subprocess
from pathlib import Path

# Local imports
from jack_o_linter.common import APIWrapper


class Flake8(APIWrapper):
    """Wrapper class for running Flake8 static analysis.

    Attributes:
        score (Optional[float]): Score out of 100 based on flake8 results.
        errors (Optional[List[str]]): List of errors.
        warnings (Optional[List[str]]): List of warnings.
    """

    def run(self, target: Path, *args, **kwargs):
        """Run Flake8 on the given target file or directory.

        Updates the class attributes for score, errors, and warnings.

        Args:
            target (Path): The file or directory to run Flake8 against.
        """

        # Run the Flake8 command
        result = subprocess.run(
            ["flake8", *self._convert_args_to_list(target, *args, **kwargs)],
            capture_output=True,
            text=True
        )

        # Process the output
        output = result.stdout.splitlines()
        self.errors = [line for line in output if "E" in line or "F" in line]
        self.warnings = [line for line in output if "W" in line or "C" in line]
        self._calculate_score(target)
