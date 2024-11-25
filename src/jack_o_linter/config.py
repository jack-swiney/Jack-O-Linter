"""Helper classes/functions to parse the `jack.yaml` file for the
underlying analysis tools."""
# pylint: disable = consider-using-with
from collections.abc import Mapping
from pathlib import Path
import tempfile
from typing import Optional, Union
import yaml


def recursive_update(base: dict, overrides: Union[dict, Mapping]) -> dict:
    """
    Recursively merge two dictionaries.

    Parameters:
        base (dict): The base dictionary.
        overrides (Union[dict, Mapping]): The second dictionary, whose
            values take precedence.

    Returns:
        dict: A merged dictionary with combined values from base and
            overrides.
    """
    merged = base.copy()
    for key, value in overrides.items():
        if key in merged and isinstance(merged[key], Mapping) and isinstance(value, Mapping):
            # If both values are dictionaries, merge them recursively
            merged[key] = recursive_update(merged[key], value)
        else:
            # Otherwise, overwrite or add the value from overrides
            merged[key] = value
    return merged


class ConfigParser:
    """Parse default and provided overrides for analysis tools."""

    def __init__(self, config_file: Optional[Path] = None):
        # Read the default YAML configuration file
        with open(Path(__file__).parent / "jackrc.yaml", "r", encoding="utf-8") as file:
            self.config: dict = yaml.safe_load(file)

        if config_file is None:
            return

        # Update the default with the provided config overrides
        with open(config_file, "r", encoding="utf-8") as file:
            custom_config = yaml.safe_load(file)

        self.config = recursive_update(self.config, custom_config)

    def pylint(self) -> str:
        """Generate a temporary RC file for PyLint.

        Raises:
            TypeError: Configuration is misformatted.

        Returns:
            str: Path to temporary .pylintrc file.
        """
        # Get the pylint configuration
        pylint_config = self.config.get("pylint")

        if not isinstance(pylint_config, dict):
            raise TypeError("PyLint Configuration is misformatted. See documentation.")

        # Create a pylintrc temporary file
        pylint_rc_path = tempfile.NamedTemporaryFile(delete=True, suffix="_pylintrc").name
        with open(pylint_rc_path, "w", encoding="utf-8") as pylint_file:
            for section, options in pylint_config.items():
                pylint_file.write(f"[{section.upper()}]\n")
                for key, value in options.items():
                    if isinstance(value, list):
                        pylint_file.write(f"{key}={','.join(map(str, value))}\n")
                    else:
                        pylint_file.write(f"{key}={value}\n")
                pylint_file.write("\n")

        return pylint_rc_path

    def flake8(self) -> str:
        """Generate a temporary config file for Flake8.

        Raises:
            TypeError: Configuration is misformatted.

        Returns:
            str: Path to temporary .flake8 file.
        """
        # Get the flake8 configuration
        flake8_config = self.config.get("flake8")
        pydoclint_config = self.config.get("pydoclint")

        if not isinstance(flake8_config, dict):
            raise TypeError("Flake8 Configuration is misformatted. See documentation.")
        if not isinstance(pydoclint_config, dict):
            raise TypeError("PyDocLint Configuration is misformatted. See documentation.")

        # Combine pydoclint and flake8 configuration.
        # Give flake8 priority for overlapping settings.
        combined_configuration = recursive_update(pydoclint_config, flake8_config)

        # Create a .flake8 temporary file
        flake8_rc_path = tempfile.NamedTemporaryFile(delete=False, suffix="_flake8rc").name
        with open(flake8_rc_path, "w", encoding="utf-8") as flake8_file:
            flake8_file.write("[flake8]\n")
            for key, value in combined_configuration.items():
                if isinstance(value, list):
                    flake8_file.write(f"{key} =\n")
                    for item in value:
                        flake8_file.write(f"  {item}\n")
                else:
                    flake8_file.write(f"{key} = {value}\n")

        return flake8_rc_path

    def mypy(self) -> str:
        """Generate a temporary ini file for MyPy.

        Raises:
            TypeError: Configuration is misformatted.

        Returns:
            str: Path to temporary mypy.ini file.
        """
        # Get the mypy configuration
        mypy_config = self.config.get("mypy")

        if not isinstance(mypy_config, dict):
            raise TypeError("MyPy Configuration is misformatted. See documentation.")

        # Create a mypy.ini temporary file
        mypy_rc_path = tempfile.NamedTemporaryFile(delete=False, suffix="_mypy_ini").name
        with open(mypy_rc_path, "w", encoding="utf-8") as mypy_file:
            mypy_file.write("[mypy]\n")
            for key, value in mypy_config.items():
                if isinstance(value, list):
                    mypy_file.write(f"{key} =\n")
                    for item in value:
                        mypy_file.write(f"  {item}\n")
                else:
                    mypy_file.write(f"{key} = {value}\n")

        return mypy_rc_path
