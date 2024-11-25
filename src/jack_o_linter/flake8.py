"""Flake8 Wrapper. Flake8 has not maintained an API since version 2.6.0, so
this module shells out to the CLI using subprocess"""
# Standard imports
from typing import Any

# Third-party imports
import subprocess
from pathlib import Path

# Local imports
from jack_o_linter.common import APIWrapper


class Flake8(APIWrapper):
    """Wrapper class for running Flake8 static analysis."""

    def run(self, target: Path, *args: Any, **kwargs: Any) -> None:
        """Run Flake8 on the given target file or directory.

        Updates the class attributes for score, errors, and warnings.

        Args:
            target (Path): The file or directory to run Flake8 against.
            *args (Any): Additional arguments to be passed to Flake8.
            **kwargs (Any): Additional keyword arguments to be converted to
                Flake8 command-line options.
        """

        # Run the Flake8 command
        result = subprocess.run(
            ["flake8", *self._convert_args_to_list(target, *args, **kwargs)],
            capture_output=True,
            text=True,
            check=False
        )

        # Process the output
        output = result.stdout.splitlines()
        self.errors = [line for line in output if "E" in line or "F" in line or "DOC" in line]
        self.warnings = [line for line in output if "W" in line or "C" in line]
        self._calculate_score(target)
