from config import Config


def handle_help(config: Config, *args) -> None:
    # Imported here rather than at module level because clicommands imports
    # this handler, so a top-level import would be circular.
    from cli import clicommands

    commands = clicommands.get_commands()

    width = max(len(command.name) for command in commands.values())

    print("Available commands:")
    for command in commands.values():
        print(f"    {command.name.ljust(width)}  {command.description}")
    print()
