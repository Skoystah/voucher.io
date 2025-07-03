import unittest
from context import command

class TestCommands(unittest.TestCase):
    def test_get_commands(self):
        
        commands = command.get_commands()

        self.assertIsInstance(commands, dict)

