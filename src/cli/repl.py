import cli.clicommands as clicommands
from config import Config

def start(config: Config):

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
            handler = commands[command].handler_function
            handler(config, args)
        else:
            print("command unknown")
        continue

