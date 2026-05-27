from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import sqlite3
import os
from pathlib import Path
import json
from datetime import datetime

from ragstash import vecdb

DB_NAME = "vecdb.sqlite"
CONFIG_NAME = "config.json"
HEADER_MESSAGE = "This query is being augmented with RAG"
SAVE_ATTRIBUTES = ["name", "path", "date_created", "tokenizer_name", "chunk_size", "chunk_overlap", "filenames"]

class RagVault:

    def __init__(
        self,
        path: str,
        name: str="",
        verbose=False,
    ):
        self.name = name
        name_str = ".ragstash" if name=="" else f".ragstash_{name}"
        self.path = str(Path(path).resolve() / name_str)
        self.verbose = verbose

        self.date_created: str
        self.tokenizer_name: str
        self.chunk_size: int
        self.chunk_overlap: int
        self.filenames: list[str]
        self.tokenizer: SentenceTransformer
        self.conn: sqlite3.Connection|None = None

    def getRAGMessage(self,
        query: str,
        k: int=5,
        retrieval_query: str="",
        message: str=HEADER_MESSAGE,
    ) -> str:
        """  """
        if self.conn is None:
            raise Exception("vault not loaded")
        if retrieval_query == "":
            retrieval_query = query
        print(f"performing search with query: \"{retrieval_query}\"")
        results = vecdb.similarity_search(self.conn, self.tokenizer, retrieval_query, k)
        print(f"found {len(results)} results")
        return self._formatRagMessage(query, results, message)

    def init(
        self,
        docs: list[str],
        filenames: list[str],
        tokenizer="sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int=500,
        chunk_overlap: int=50,
    ):

        if len(docs) == 0:
            print("cannot init with 0 documents")

        # check exists
        if self.exists():
            raise Exception(f"vault already exists: \"{self.path}\"")
        Path(self.path).mkdir(exist_ok=True, parents=True)

        # set config
        self.date_created = str(datetime.now())
        self.tokenizer_name = tokenizer
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.filenames = filenames

        # create chunks
        print(f"creating chunks of size={chunk_size} and overlap={chunk_overlap}")
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True)
        doc_metadatas = [ {"filename": fn} for fn in filenames ]
        chunks = splitter.create_documents(texts=docs, metadatas=doc_metadatas)
        ids = [ str(i) for i in range(len(chunks)) ]
        texts = [ c.page_content for c in chunks ]
        metadatas = [ c.metadata for c in chunks ]

        # load tokenizer
        print(f"loading tokenizer: {tokenizer}")
        self.tokenizer = SentenceTransformer(tokenizer)
        print(f"encoding {len(chunks)} texts")
        vectors = self.tokenizer.encode(texts, normalize_embeddings=True, convert_to_numpy=True)

        # create db
        self.conn = vecdb.create_db(
            self._getDBPath(),
            texts=texts,
            ids=ids,
            metadatas=metadatas,
            vectors=vectors,
            replace=True,
        )

        # save config
        self._saveConfig()

    def load(self, redo=False):
        if not self.exists():
            raise Exception(f"vault doesn't exist: \"{self.path}\"")

        # load config
        self._loadConfig()

        # load
        self.tokenizer = SentenceTransformer(self.tokenizer_name)
        self.conn = vecdb.load_db(self._getDBPath())

    def close(self):
        if self.conn:
            self.conn.close()

    def exists(self):
        return (Path(self.path) / DB_NAME).exists() and (Path(self.path) / CONFIG_NAME).exists()

    def _formatRagMessage(self, query: str, results: list[vecdb.ChunkResult], message: str=HEADER_MESSAGE):

        # format chunks
        chunks_fmt = ""
        for i, c in enumerate(results):
            chunks_fmt += f"""
--- result {i+1}: filename: {c.metadata['filename']}
{c.text}

"""

        return f"""
{message}

RAG CONTEXT:

{chunks_fmt}

QUERY:

{query}
"""

    def _saveConfig(self):
        data = {
            _attr: getattr(self, _attr)
            for _attr in SAVE_ATTRIBUTES
        }
        with open(self._getConfigPath(), "w") as f:
            json.dump(data, f, indent=4)

    def _loadConfig(self):
        with open(self._getConfigPath(), "r") as f:
            data = json.load(f)
        for _attr in SAVE_ATTRIBUTES:
            setattr(self, _attr, data[_attr])

    def _getConfigPath(self):
        return str(Path(self.path) / CONFIG_NAME)

    def _getDBPath(self):
        return str(Path(self.path) / DB_NAME)

    def _print(self, args, end='\n'):
        if self.verbose:
            print(*args, end=end)
