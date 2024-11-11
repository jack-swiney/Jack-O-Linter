"""MyPy Wrapper"""
# Standard imports
from pathlib import Path
import re

# Third-party imports
import mypy.api as mypy

# Local imports
from jack_o_linter.common import APIWrapper


class MyPy(APIWrapper):
    """Mypy is a static type checker for Python.

    Type checkers help ensure that you're using variables and functions in your
    code correctly. With mypy, add type hints
    ([PEP 484](https://peps.python.org/pep-0484/)) to your Python programs, and
    mypy will warn you when you use those types incorrectly.

    Python is a dynamic language, so usually you'll only see errors in your code
    when you attempt to run it. Mypy is a static checker, so it finds bugs in
    your programs without even running them!

    Attributes:
        score (Optional[float]): Score out of 100.
        errors (Optional[List[str]]): List of errors.
        self.warnings (Optional[List[str]]): List of warnings.
    """

    def run(self, target: Path, *args, **kwargs) -> None:
        """Run mypy on the given target file or directory.

        Args:
            target (Path): The file or directory to type check with mypy.
            *args: Additional arguments to be passed to mypy (strings).
            **kwargs: Additional keyword arguments to be converted to mypy
                command-line options.
        """
        # Run MyPy with the positional and keyword args against the target
        stdout, _, _ = mypy.run(self._convert_args_to_list(target, *args, **kwargs))

        # Parse results to get errors, warnings, and calculate score
        self.errors = re.compile(r"^.*error:.*$", re.MULTILINE).findall(stdout)
        self.warnings = re.compile(r"^.*note:.*$", re.MULTILINE).findall(stdout)
        self._calculate_score(target)
