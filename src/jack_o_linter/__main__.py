"""Jack-O-Linter CLI"""
import argparse
import os
from statistics import fmean
import sys

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from jack_o_linter import ConfigParser, Flake8, MyPy, PyLint


def print_results(console: Console,
                  mypy: MyPy,
                  flake8: Flake8,
                  pylint: PyLint,
                  threshold: float = 100.0) -> None:
    """Use Rich to output the Jack-O-Linter results.

    Args:
        console (Console): Rich console
        mypy (MyPy): MyPy client.
        flake8 (Flake8): Flake8 client.
        pylint (PyLint): PyLint client.
        threshold (float, optional): Minimum score to pass Jack-O-Linter.
            Defaults to 100.0.
    """
    # Initialize table
    table = Table(title="Jack-O-Linter Results", show_lines=True)

    # Add columns
    table.add_column("Tool", style="bold magenta")
    table.add_column("Score", style="bold green", justify="right")
    table.add_column("Errors", style="bold red")
    table.add_column("Warnings", style="bold yellow")

    # Add rows for each tool
    for row in [mypy, flake8, pylint]:
        table.add_row(
            row.__class__.__name__,
            f"{(row.score or 0):.2f}",
            "\n".join(row.errors) if row.errors else "No Errors",
            "\n".join(row.warnings) if row.warnings else "No Warnings"
        )

    # Print the table to stdout
    console.print(table)

    # Print the overall score
    overall_score = fmean(
        [_score or 0 for _score in [(mypy.score or 0), (flake8.score or 0), (pylint.score or 0)]]
    )
    if overall_score < threshold:
        console.print(f"[bold red]Error: Overall Score ({overall_score:.1f}) "
                      f"is below the threshold ({threshold}).[/bold red]")
        sys.exit(1)
    else:
        console.print(f"[bold green]Overall Score: {overall_score:.1f}[/bold green]")


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

    # Initialize Rich
    console = Console()

    # Run Jack-O-Linter
    flake8 = Flake8()
    pylint = PyLint()
    mypy = MyPy()

    with Progress(SpinnerColumn(),
                  TextColumn("[bold blue]Running Flake8...[/bold blue]"),
                  console=console) as progress:
        progress.add_task("run", total=None)
        flake8.run(args.path, config=flake8_config)
    with Progress(SpinnerColumn(),
                  TextColumn("[bold blue]Running PyLint...[/bold blue]"),
                  console=console) as progress:
        progress.add_task("run", total=None)
        pylint.run(args.path, rcfile=pylint_config)
    with Progress(SpinnerColumn(),
                  TextColumn("[bold blue]Running MyPy...[/bold blue]"),
                  console=console) as progress:
        progress.add_task("run", total=None)
        mypy.run(args.path, config_file=mypy_config)

    # Process the results
    print_results(console, mypy, flake8, pylint, args.fail_under)


if __name__ == "__main__":
    main()
