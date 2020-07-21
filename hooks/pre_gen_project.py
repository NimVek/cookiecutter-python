import re
import sys

from typing import OrderedDict

class Hook:
    def __init__(self):
        self.__cookiecutter = {{cookiecutter}}  # noqa: F821

    def __getattr__(self, key):
        result = self.__cookiecutter.get(key)
        if key.startswith("do_") or key.startswith("use_") or key.startswith("with_"):
            result = (
                result
                if isinstance(result, bool)
                else result.lower() in ["y", "yes", "true", "on"]
            )
        return result


class PreGenProjectHook(Hook):
    def test_package_name(self):
        MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
        if not re.match(MODULE_REGEX, self.package_name):
            print("ERROR: %s is not a valid Python module name!" % self.package_name)
            sys.exit(1)

    def run(self):
        self.test_package_name()


if __name__ == "__main__":
    PreGenProjectHook().run()
