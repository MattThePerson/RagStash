from ragstash.args import CliArgs

def main():

    # args
    args = CliArgs().parse_args()
    args.check()

    # mode
    match args.mode:
        case "init":
            init(args)
        case "update":
            update(args)
        case "serve":
            serve(args)
        case "get":
            get(args)
        case _:
            raise Exception(f"bro, no such mode: '{args.mode}'")

# ====================================================================================================
# Init
# ====================================================================================================

def init(args: CliArgs):
    from ragstash.rag_vault import RagVault
    from ragstash import docs

    # get docs
    docs, files = docs.readFiles(".")
    print(f"scanned {len(docs)} docs")

    # init vault
    vault = RagVault(args.path, name=args.name)
    print("initializing vault")
    vault.init(
        docs=docs,
        filenames=files,
        tokenizer=args.sentence_transformer,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )
    print("done")

# ====================================================================================================
# Update
# ====================================================================================================

def update(args: CliArgs):
    from ragstash.rag_vault import RagVault
    from ragstash import docs
    ...

# ====================================================================================================
# Get
# ====================================================================================================

def get(args: CliArgs):
    import requests
    msg: str

    # get message
    params = {
        "query": args.query,
        "k": args.chunks,
        "retrieval_query": args.retrieval_query,
        "message": args.message,
    }
    r = requests.post(
        f"http://{args.ip_addr}:{args.port}/rag",
        json=params,
    )
    msg = r.text

    # output msg
    print(msg)

# ====================================================================================================
# Serve
# ====================================================================================================

def serve(args: CliArgs):
    from ragstash.rag_vault import RagVault
    from ragstash.flask_server import create_server

    # load
    vault = RagVault(args.path, name=args.name)
    print('loading vault')
    vault.load()
    print('creating server')
    server = create_server(vault)

    # run
    try:
        print(f"serving ragstash on: http://0.0.0.0:{args.port}")
        server.run(host="0.0.0.0", port=args.port)
    except KeyboardInterrupt:
        print("\n... closing server")
    finally:
        print('closing vault')
        vault.close()
