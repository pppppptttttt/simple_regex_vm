import unittest
from vm import RegexVM
import re


class TestRegexVM(unittest.TestCase):
    def test_regex(self):
        pattern = "a+b+"
        vm = RegexVM(pattern)
        strings = ["", "a", "aaabbb", "ab", "bbb", "aaabb"]

        for s in strings:
            self.assertEqual(vm.run(s), re.match(pattern, s) is not None)

    def test_another_regex(self):
        pattern = "a+b*"
        vm = RegexVM(pattern)
        strings = ["", "a", "aaabbb", "ab", "bbb", "aaabb"]

        for s in strings:
            self.assertEqual(vm.run(s), re.match(pattern, s) is not None)

    def test_another_another_regex(self):
        pattern = "ab*"
        vm = RegexVM(pattern)
        strings = ["", "a", "aaabbb", "ab", "bbb", "aaabb"]

        for s in strings:
            self.assertEqual(vm.run(s), re.match(pattern, s) is not None)

    def test_compilation(self):
        self.assertEqual(
            ["char a", "char b", "match"], RegexVM.compile_regex("ab")
        )
        self.assertEqual(
            ["char a", "split 0 2", "char b", "split 2 4", "match"],
            RegexVM.compile_regex("a+b+"))
        self.assertEqual(
            ["char a", "split 0 2", "split 3 5", "char b", "jmp 2", "match"],
            RegexVM.compile_regex("a+b*"))
        self.assertEqual(
            ["split 1 3", "char a", "jmp 4", "char b", "match"],
            RegexVM.compile_regex("a|b"))
        self.assertEqual(
            ["split 1 2", "char a", "match"],
            RegexVM.compile_regex("a?"))


if __name__ == "__main__":
    unittest.main()
