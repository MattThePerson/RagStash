from tap import Tap
from importlib.metadata import version

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
    redo: bool=False

    # serve
    unload_timeout: int = 0

    # get
    chunks: int = 5
    retrieval_query: str
    message: str = ""
    file: str = ""
    ip_addr: str = "localhost"
    chunks_as_json: bool=False

    # init serve
    name: str = ""

    # serve get
    port: int = 32123

    def configure(self):
        self.add_argument("mode", help="mode of operation [init|serve|get|help]")
        self.add_argument("arg1", nargs="?", help="Path (init|serve) or Query (get)")

        self.add_argument( "--version", "-V", action="version", version=f"%(prog)s {version('ragstash')}")

        # init
        self.add_argument("--sentence-transformer", default="sentence-transformers/all-MiniLM-L6-v2", help="")
        self.add_argument("--chunk-size", type=int, default=500, help="")
        self.add_argument("--chunk-overlap", type=int, default=50, help="")
        self.add_argument("--redo", action="store_true", default=False, help="")

        # serve
        ...

        # get
        self.add_argument("--retrieval-query", "-rq", default="", help="")
        self.add_argument("--ip-addr", "-ip", default="localhost", help="")
        self.add_argument("--chunks-as-json", action="store_true", default=False, help="")

        # init serve
        self.add_argument("--name", "-n",               help="Give name to vault")

        # serve get
        self.add_argument("--port",                     help="RAG Stash server port")

    def check(self):
        self.mode = self.mode.lower()
        if self.mode == "help":
            self.print_help()
            self.exit()
        self.check_mode()
        self.check_arg1()

        # check unimplemented
        if self.file != "":
            raise NotImplementedError("argument --file not yet implemented")
        if self.unload_timeout != 0:
            raise NotImplementedError("argument --unload-timeout not yet implemented")
        if self.chunks_as_json:
            raise NotImplementedError("argument --chunks-as-json not yet implemented")

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
            self.path = self.arg1
            del self.arg1

    @staticmethod
    def _exit(msg="", status_code=0):
        import sys
        if msg != "":
            print(msg)
        sys.exit(status_code)
