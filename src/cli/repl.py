from cli import clicommands
from cli.handlers.exit import handle_exit
from config import Config


def start(config: Config) -> None:
    commands = clicommands.get_commands()

    print("Choose action:")

    while True:
        print(">", end=" ")

        try:
            line = input()
        except (EOFError, KeyboardInterrupt):
            # ^D and ^C should end the session, not dump a traceback.
            print()
            handle_exit(config)
            return

        ipt = line.strip().split(" ")

        if ipt == [""]:
            continue

        command = ipt[0]
        args = []
        if len(ipt) > 1:
            args = ipt[1:]

        if command in commands:
            handler = commands[command].handler_function
            handler(config, *args)
        else:
            print("command unknown")
        continue
