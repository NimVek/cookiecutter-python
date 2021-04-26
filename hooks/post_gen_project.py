import getpass
import glob
import os
import subprocess

from typing import OrderedDict

import git
import incremental.update
import requests


class Hook:
    def __init__(self):
        self.__cookiecutter = {{cookiecutter}}  # noqa: F821

    def keys(self):
        return [x for x in self.__cookiecutter.keys() if not x.startswith("_")]

    def __getattr__(self, key):
        result = self.__cookiecutter.get(key)
        if key.startswith("do_") or key.startswith("use_") or key.startswith("with_"):
            result = (
                result
                if isinstance(result, bool)
                else result.lower() in ["y", "yes", "true", "on"]
            )
        return result


class PostGenProjectHook(Hook):
    def _remove_file(self, filename):
        os.remove(filename)

    def _get_credential_store(self, username):
        result = None
        tmp_file = ".tmp_get_repository_password"
        with open(tmp_file, "w") as f:
            f.write(f"username={username}\nprotocol=https\nhost=github.com\n")
        with open(tmp_file, "r") as f:
            cmd = git.Git()
            output = cmd.credential_store("get", istream=f)
            for i in output.splitlines():
                if i.startswith("password="):
                    result = i[9:]
        self._remove_file(tmp_file)
        return result

    def _get_repository_password(self):
        password = self._get_credential_store(self.repository_user)
        if not password:
            password = self._get_credential_store(self.repository_user.lower())
        if not password:
            password = getpass.getpass(
                f"Password for 'https://{self.repository_user}@github.com': "
            )
        return password

    def __init__(self):
        super().__init__()
        self.repository_password = self._get_repository_password()

    def __git_file_download(self, host, items, filename):
        url = f"https://{host}/api/{','.join(items)}"
        response = requests.get(url)
        with open(filename, "w") as f:
            f.write(response.text)

    def _git_ignore(self):
        self.__git_file_download(
            "gitignore.io", ("git", "linux", "windows", "macos", "python"), ".gitignore"
        )

    def _git_attributes(self):
        self.__git_file_download(
            "gitattributes.io", ("common", "python"), ".gitattributes"
        )

    def _git_init(self):
        cmd = git.Git()
        cmd.init()
        cmd.config("user.email", self.author_email)
        cmd.config("user.name", self.author_name)
        cmd.add("--all", "--intent-to-add")

    def _git_commit(self):
        cmd = git.Git()
        cmd.commit("--all", "--message", "build: Initial Buildsystem")

    def _git_github(self):
        payload = {
            "name": self.repository_name,
            "description": self.project_description,
            "private": False,
            "has_issues": True,
            "has_projects": False,
            "has_wiki": False,
            "auto_init": False,
        }
        requests.post(
            "https://api.github.com/user/repos",
            json=payload,
            auth=(self.repository_user, self.repository_password),
        )

        url = f"https://github.com/{self.repository_user}/{self.repository_name}.git"
        cmd = git.Git()
        cmd.remote("add", "origin", url)
        cmd.push("--set-upstream", "origin", "main")
        cmd.remote("set-url", "origin", url)

    def _version(self):
        incremental.update._run(
            self.package_name,
            path=None,
            newversion=None,
            patch=False,
            rc=False,
            dev=False,
            create=True,
        )
        incremental.update._run(
            self.package_name,
            path=None,
            newversion=self.package_version,
            patch=False,
            rc=False,
            dev=False,
            create=False,
        )

    def _pre_commit(self):
        for i in ["commit-msg", "pre-commit"]:
            subprocess.run(["pre-commit", "install", "--hook-type", i])

    def _template_file(self, filename):
        with open(filename, "r") as f:
            content = f.read()
        for key in self.keys():
            content = content.replace(f"###{key.upper()}###", str(getattr(self, key)))
        with open(filename, "w") as f:
            f.write(content)

    def _template(self):
        for g in self._copy_without_render:
            for f in glob.iglob(g):
                self._template_file(f)

    def _update(self):
        subprocess.run(["pre-commit", "run", "--all-files"])

    def _files(self):
        if not self.with_main:
            os.remove(f"src/{self.package_name}/__main__.py")
            os.remove(f"src/{self.package_name}/main.py")
            os.remove("tests/test_main.py")

    def run(self):
        self._version()
        self._template()
        self._git_ignore()
        self._git_attributes()
        self._files()
        self._git_init()
        self._update()
        self._git_commit()
        if self.do_github:
            self._git_github()
        self._pre_commit()


if __name__ == "__main__":
    PostGenProjectHook().run()
