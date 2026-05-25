from ragstash import (
    cli_args,
    app,
)

def main():
    args = cli_args.CLIArgs().parse_args()
    args.check()
    app.main(args)
