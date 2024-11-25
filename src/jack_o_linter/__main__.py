"""Jack-O-Linter CLI"""
import argparse
import os
from statistics import fmean
from jack_o_linter import ConfigParser, Flake8, MyPy, PyLint
from jack_o_linter.errors import JackOLinterError


def main() -> None:
    """Main entrypoint."""
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Jack-O-Linter Code Analysis")

    # Add an arg for the file/dir to analyze
    parser.add_argument("path",
                        type=str,
                        help="Path to a file or directory.")
    parser.add_argument("--fail-under",
                        type=float,
                        help="Specify a score threshold under which the program "
                             "will exit with error. (default: 100)",
                        default=100.0)
    parser.add_argument("--rcfile",
                        help="Specify a Jack-O-Linter RC file.",
                        default=None)

    # Parse the arguments
    args = parser.parse_args()

    # Validate the path
    if not os.path.exists(args.path):
        raise FileNotFoundError(f"Error: The path '{args.path}' does not exist.")

    # Get configuration
    config = ConfigParser(args.rcfile)
    flake8_config = config.flake8()
    pylint_config = config.pylint()
    mypy_config = config.mypy()

    # Run Jack-O-Linter
    flake8 = Flake8()
    pylint = PyLint()
    mypy = MyPy()

    flake8.run(args.path, config=flake8_config)
    pylint.run(args.path, rcfile=pylint_config)
    mypy.run(args.path, config_file=mypy_config)

    # Gather the results
    score = fmean([_score or 0 for _score in [flake8.score, pylint.score, mypy.score]])
    errors = (flake8.errors or []) + (pylint.errors or []) + (mypy.errors or [])
    warnings = (flake8.warnings or []) + (pylint.warnings or []) + (mypy.warnings or [])

    if errors:
        print("*************ERRORS*************")
        print("\n".join([f"    {err}" for err in errors]) + "\n")
    if warnings:
        print("************WARNINGS************")
        print("\n".join([f"    {warn}" for warn in warnings]) + "\n")
    print("********************************")
    print(f"Jack-O-Linter Score: {score:.2f}/100")
    print("********************************")

    if score < args.fail_under:
        raise JackOLinterError(
            f"Score of {score:.2f}/100 is below passing threshold of {args.fail_under}"
        )


if __name__ == "__main__":
    main()
