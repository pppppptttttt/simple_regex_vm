import unittest
from vm import RegexVM


class TestRegexVM(unittest.TestCase):
    def test_regex(self):
        vm = RegexVM("a+b+")

        self.assertTrue((vm.run("aaabbb")))
        self.assertTrue(vm.run("aabbb"))
        self.assertTrue(vm.run("ab"))
        self.assertFalse(vm.run("a"))
        self.assertFalse(vm.run("bbb"))
        self.assertFalse(vm.run(""))

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
