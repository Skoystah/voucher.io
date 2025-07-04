import cli.repl as repl
import voucher.voucher as voucher
import config

def main():
    repl.start(config.Config(voucher.VoucherDB())
)    

if __name__ == "__main__":
    main()
