# RAG Stash

_Perform RAG flexibly and easily with an LLM of your choice_

## About

Ragstash is a CLI utility to help retrieve RAG (Retrieval Augmented Generation) context from your documents which can then be fed into an LLM of your choice.

## Installation

__recommended:__

`pipx install ragstash` or `uv tool install ragstash`

You should then have `ragstash` command available. 

## Usage

First, cd into your documents folder, then: 

1. Use `ragstash init .` to initialize (processes documents, generates embeddings, and saves vector db)
2. Use `ragstash serve .` to start the server used for querying
3. (_In a separate terminal_) Use `ragstash query YOUR_QUERY` to print out the RAG context. This output can be piped (|) into an LLM or saved in a file.

## Example Usage

__Simple__:

```sh
> cd path/to/your/documents
> ragstash init .
> ragstash serve .

# In another terminal
> ragstash query "What do the files say about the doings of Celebrity Celebface?" | claude
```

__Advanced__:

```sh
> cd path/to/your/documents
> ragstash init . \
  --sentence-transformer "sentence-transformers/all-MiniLM-L6-v2" \
  --chunk-size 200 \
  --name "diff_model"
> ragstash serve . --name "diff_model"

# In another terminal
> ragstash query "What do the files say about the doings of Celebrity Celebface?" \
  --retrieval-query "Things Celebrity Celebface has done" \
  --chunks 10 \
  --message "Here is " \
  | claude
```

## Options

```sh

> init PTH
    --sentence-transformer  # model to use for embedding of chunks
    --chunk-size            # size of chunks (chars)
    --chunk-overlap         # 
    --redo                  # needed if init has already been done
    --name                  # name to give initialization (appended to folder name: ".rag_{NAME}")

> start PTH
    --name                  # which initialization to use
    --unload-timeout        # time after which sentence transformer mode unloads (0 means never unloads)
    --port

> query YOUR_QUERY
    --chunks            # number of chunks to fetch
    --retrieval-query   # query to use when doing "dumb" retrieval of data (given to sentence transformer)
    --message           # Message to give LLM
    --load-vault PTH    # Load local vault without server
    --port              # Port to fetch 
    --file              # File where to save retrieved context

> status

```

## About the server

The reason for using a server is to avoid having to load the sentence transformer model into memory for each query (may take a few seconds). You can bypass the server (`serve` command) by passing `--load-local PTH` along with your query.

## What initialization does

Initialization will create a `.rag/` folder which contains:
- a config file (stores init parameters)
- the Chroma vector database
- a list of files used to create the rag context
