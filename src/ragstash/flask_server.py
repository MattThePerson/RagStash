from flask import Flask, request
from ragstash.rag_vault import RagVault

server = Flask(__name__)
_vault: RagVault

def create_server(vault: RagVault):
    global _vault
    _vault = vault
    return server

@server.route("/rag", methods=["POST"])
def rag():
    query = request.json.get("query", "")
    k = int(request.json.get("k", 5))
    rquery = request.json.get("retrieval_query", "")
    header_msg = request.json.get("message", "")
    msg = _vault.getRAGMessage(
        query=query,
        k=k,
        retrieval_query=rquery,
        message=header_msg,
    )

    return msg, 200, {"Content-Type": "text/plain"}
