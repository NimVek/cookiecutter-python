"""Provides {{ cookiecutter.package_name }} various information."""
from ._version import __version__ as version


__all__ = [
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]

__title__ = "{{ cookiecutter.project_name }}"
__summary__ = "{{ cookiecutter.project_description }}"
__uri__ = "https://github.com/{{ cookiecutter.repository_user }}/{{ cookiecutter.repository_name }}/"

__version__ = version.short()

__author__ = "{{ cookiecutter.author_name }}"
__email__ = "{{ cookiecutter.author_email }}"

__license__ = "GPL-3.0-or-later"
