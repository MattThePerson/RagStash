from ragstash import (
    cli_args,
)

def main(args: cli_args.CLIArgs):

    mode = args.mode.lower()

    match mode:
        case "get":     get(args)
        case "serve":   serve(args)
        case _:         raise Exception(f"bro, no such mode '{mode}' implemented")

# ====================================================================================================
# Get
# ====================================================================================================

def get(args: cli_args.CLIArgs):
    print("retrieve chunks using query:", args.query)

# ====================================================================================================
# Serve
# ====================================================================================================

def serve(args: cli_args.CLIArgs):
    print("serving rag stash:", args.path)
