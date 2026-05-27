from tap import Tap

RAGSTASH_MODES = ["init", "update", "serve", "get", "info", "help"]
RAGSTASH_USAGE_GET = "ragstash get <QUERY> [--args ...]"
RAGSTASH_USAGE_PATH = "ragstash %(MODE) <PATH> [--args ...]"

class CliArgs(Tap):
    """  """
    mode: str
    arg1: str

    # set from arg1
    path: str = ""
    query: str = ""

    # init
    sentence_transformer: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 500
    chunk_overlap: int = 50

    # serve
    unload_timeout: int = 0

    # query
    chunks: int = 5
    retrieval_query: str
    message: str = ""
    load_vault: str = ""
    file: str = ""
    ip_addr: str = "0.0.0.0" # if server exists not on localhost

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
        if self.mode not in RAGSTASH_MODES:
            self._exit(f"no such mode \"{self.mode}\", available modes are: {RAGSTASH_MODES}", 1)

    def check_arg1(self):
        if self.mode in ["get"]:
            if self.arg1 is None:
                self._exit(f"Please give a query (usage: {RAGSTASH_USAGE_GET}", 1)
            self.query = self.arg1
            del self.arg1
        else:
            if self.arg1 is None:
                self.arg1 = "."
                # usage = RAGSTASH_USAGE_PATH.replace("%(MODE)", self.mode)
                # self._exit(f"Please give path to vault (usage: {usage}", 1)
            self.path = self.arg1
            del self.arg1

    @staticmethod
    def _exit(msg="", status_code=0):
        import sys
        if msg != "":
            print(msg)
        sys.exit(status_code)
