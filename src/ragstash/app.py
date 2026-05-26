from ragstash.args import CliArgs

def main():

    # args
    args = CliArgs().parse_args()
    args.check()

    # mode
    match args.mode:
        case "init":
            init(args)
        case "serve":
            serve(args)
        case "get":
            get(args)
        case _:
            raise Exception(f"bro, no such mode '{args.mode}' implemented")

# ====================================================================================================
# Init
# ====================================================================================================

def init(args: CliArgs):
    from ragstash.rag_vault import RagVault
    """

    """
    vault = RagVault(args.path, name=args.name)
    vault.init([])
    print("initializing with path:", args.path)

# ====================================================================================================
# Get
# ====================================================================================================

def get(args: CliArgs):
    msg: str

    if args.load_vault == "":
        import requests
        r = requests.get(
            f"http://localhost:{args.port}/rag",
            params={"q": args.query}
        )
        msg = r.text
    else:
        from ragstash.rag_vault import RagVault
        vault = RagVault(args.path, name=args.name)
        vault.load()
        msg = vault.getRAGMessage(args.query)
        vault.close()

    # output msg
    print(msg)

# ====================================================================================================
# Serve
# ====================================================================================================

def serve(args: CliArgs):
    from ragstash.rag_vault import RagVault
    from ragstash.flask_server import create_server
    vault = RagVault(args.path, name=args.name)
    vault.load()
    server = create_server(vault)
    try:
        print(f"serving ragstash on: http://localhost:{args.port}")
        server.run(port=args.port)
    except KeyboardInterrupt:
        print("\n... closing server")
    finally:
        vault.close()
