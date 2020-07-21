"""Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

You might be tempted to import things from __main__ later, but that will cause
problems: the code will get executed twice:

  - When you run `python -m {{ cookiecutter.package_name }}` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``{{ cookiecutter.package_name }}.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``{{ cookiecutter.package_name }}.__main__`` in ``sys.modules``.

Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse

from typing import List, Optional

import {{ cookiecutter.package_name }}


def main(args: Optional[List[str]] = None) -> int:
    """Console script for {{ cookiecutter.package_name }}.

    Args:
        args: Commandline arguments to parse

    Returns:
        exit code
    """
    parser = argparse.ArgumentParser(description={{ cookiecutter.package_name }}.__summary__)
    parser.add_argument(
        "--version",
        action="version",
        version=f"{ {{ cookiecutter.package_name }}.__name__ } { {{ cookiecutter.package_name }}.__version__ }",
    )
    parser.add_argument("_", nargs="*")

    parsed = parser.parse_args(args=args)

    print(f"Arguments: {parsed._}")
    print(f"Replace this message by putting your code into {__name__}.main")

    return 0
