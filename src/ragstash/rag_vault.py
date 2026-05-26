# from langchain_community.document_loaders import PyPDFLoader, TextLoader
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
import os
from sentence_transformers import SentenceTransformer
import sqlite3
import sqlite_vec
import numpy as np

class RagVault:
    """
    RAG Vault


    """

    def __init__(
        self,
        path: str,
        name: str="",
        verbose=False,
    ):
        self.name = name
        name_str = ".ragstash" if name=="" else f".ragstash_{name}"
        self.path = path + os.sep + name_str
        self.verbose = verbose

        self.tokenizer: str
        self.chunk_size: int
        self.chunk_overlap: int
        self.model: SentenceTransformer
        self.conn: sqlite3.Connection

    def getRAGMessage(self, query: str, k: int=5) -> str:
        """  """
        return "TEMP RAG MESSAGE"

    def init(
        self,
        docs: list[str],
        metadatas: list[dict]|None = None,
        tokenizer="sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int=400,
        chunk_overlap: int=50,
    ):
        """
        1. check that vault doesn't exist
        2. split docs into chunks
        3. load tokenizer
        4. encode chunks
        5. create DB & save chunks+vectors
        """

    def load(self, redo=False):
        """
        1. check that vault exists
        2. load tokenizer
        3. load DB connection
        """
        ...

    def close(self):
        # self.conn.close()
        ...

    def _docsToChunks(self) -> list[str]:
        """  """
        ...

    def _getSimilarChunks(self, query: str, k: int=5) -> list[str]:
        """  """
        ...
        # results = self.db.similarity_search(query, k=k)
        # self._print("\nRESULTS:")
        # for i, r in enumerate(results):
        #     self._print(f"\n--- Result {i+1} ---")
        #     self._print(r.page_content)

    def _print(self, args, end='\n'):
        if self.verbose:
            print(*args, end=end)
