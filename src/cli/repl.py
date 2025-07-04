import cli.clicommands as clicommands
import config

def start(config: config.Config):

    commands = clicommands.get_commands()

    print("Choose action:")

    while True:
        print(">", end=" ")

        ipt = input().split(" ")

        command = ipt[0]
        args = []
        if len(ipt) > 1:
            args = ipt[1:]

        if command in commands:
            handler = commands[command].create_handler(config)
            handler.handle(*args)
        else:
            print("command unknown")
        continue

