import unittest
from cli import clicommands


class TestCommands(unittest.TestCase):
    def test_get_commands(self):
        commands = clicommands.get_commands()

        self.assertIsInstance(commands, dict)

    def test_check_commands(self):
        commands = clicommands.get_commands()

        self.assertIn("help", commands)
        self.assertIn("exit", commands)
        self.assertIn("add", commands)
        self.assertIn("add-file", commands)
        self.assertIn("list", commands)
        self.assertIn("use", commands)


if __name__ == "__main__":
    unittest.main()
