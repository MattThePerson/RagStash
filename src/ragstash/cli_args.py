from tap import Tap

class CLIArgs(Tap):
    mode: str
    arg1: str

    path: str = ""
    query: str = ""

    # init
    sentence_transformer: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 400
    chunk_overlap: int = 50

    # serve
    unload_timeout: int = 0

    # query
    chunks: int = 5
    retrieval_query: str
    message: str = ""
    load_vault: str = ""

    # init serve
    name: str = ""

    # serve get
    port: int = 32123

    def configure(self):
        self.add_argument("mode", help="mode of operation [init|serve|get|help]")
        self.add_argument("arg1", nargs="?", help="Path (init|serve) or Query (get)")

        self.add_argument("--port",                     help="RAG Stash server port")
        self.add_argument("--name", "-n",               help="Give name to vault")
        self.add_argument("--load-vault", default="",   help="Path to vault to load directly (without serve)")
        self.add_argument("--retrieval-query", default="", help="")

    def check(self):
        self.mode = self.mode.lower()
        self.check_mode()
        self.check_arg1()

    def check_mode(self):
        modes = ["init", "serve", "get", "help", "status"]
        if self.mode not in modes:
            print(f"no such mode \"{self.mode}\", available modes are: {modes}")
            import sys
            sys.exit(1)
        if self.mode in ["get"]:
            self.query = self.arg1
        else:
            self.path = self.arg1
        del self.arg1

    def check_arg1(self):
        ...
