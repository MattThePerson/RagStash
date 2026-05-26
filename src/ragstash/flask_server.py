from flask import Flask, request
from ragstash.rag_vault import RagVault

server = Flask(__name__)
_vault: RagVault

def create_server(vault: RagVault):
    global _vault
    _vault = vault
    return server

@server.route("/rag")
def rag():
    query = request.args.get("q", "")
    print(query)

    context = f"""
heading:
THIS IS AN EXAMPLE CONTEXT STRING

query:
{query}
"""
    return context, 200, {"Content-Type": "text/plain"}
