from cli import clicommands


def test_get_commands():
    commands = clicommands.get_commands()

    assert isinstance(commands, dict)


def test_check_commands():
    commands = clicommands.get_commands()

    assert "help" in commands
    assert "exit" in commands
    assert "add" in commands
    assert "add-file" in commands
    assert "list" in commands
    assert "use" in commands
    assert "add-user" in commands
