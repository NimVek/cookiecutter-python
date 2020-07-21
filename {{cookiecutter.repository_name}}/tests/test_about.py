import pytest

import {{ cookiecutter.package_name }}


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("title", "{{ cookiecutter.project_name }}"),
        ("summary", "{{ cookiecutter.project_description }}"),
        ("uri", "https://github.com/{{ cookiecutter.repository_user }}/{{ cookiecutter.repository_name }}/"),
        ("author", "{{ cookiecutter.author_name }}"),
        ("email", "{{ cookiecutter.author_email }}"),
        ("license", "GPL-3.0-or-later"),
    ],
)
def test_about(key, value):
    assert getattr({{ cookiecutter.package_name }}, f"__{key}__") == value
