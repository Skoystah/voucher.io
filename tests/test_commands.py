import unittest
from cli import clicommands

class TestCommands(unittest.TestCase):
    def test_get_commands(self):
        
        commands = clicommands.get_commands()

        self.assertIsInstance(commands, dict)

if __name__ == "__main__":
    unittest.main()

