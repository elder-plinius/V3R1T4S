# SPDX-License-Identifier: AGPL-3.0-or-later
"""C++ source files must count as code when checking saved run evidence.

    python3 -m unittest discover -s kit/tests -p 'test_cpp_sources.py' -v
"""
import os
import shutil
import unittest
from test_check_run import Base, w


CPP = '#include <cstdio>\nint main() { std::puts("1"); }\n'


class CppSources(Base):
    def cpp_attempts(self, extension, output=True):
        self.attack()
        for lens in ("lens0", "lens1"):
            code = os.path.join(self.R, "attempts", lens, "code")
            shutil.rmtree(code)
            w(os.path.join(code, "try" + extension), CPP)
            if output:
                w(os.path.join(code, "try.out"), "1\n")

    def test_cpp_sources_and_headers_are_code(self):
        for extension in (".cc", ".cxx", ".hh", ".hxx", ".CC", ".CXX"):
            with self.subTest(extension=extension):
                self.cpp_attempts(extension)
                self.assertPass(self.W, "--no-exec")

    def test_cpp_sources_still_need_saved_output(self):
        for extension in (".cc", ".cxx"):
            with self.subTest(extension=extension):
                self.cpp_attempts(extension, output=False)
                self.assertFail("at least one program it ran and that program's saved output", self.W, "--no-exec")

    def test_plain_text_is_not_program_evidence(self):
        self.cpp_attempts(".txt")
        self.assertFail("at least one program it ran and that program's saved output", self.W, "--no-exec")


if __name__ == "__main__":
    unittest.main(verbosity=2)
