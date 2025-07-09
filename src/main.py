import cli.repl as repl
from config import Config

def main():
    
    #todo - use config file?
    config = Config(db="voucher.db")
    print("config db", config.db)
    repl.start(config)

if __name__ == "__main__":
    main()
