# RAG Stash

_Perform RAG flexibly and easily with an LLM of your choice_

## About

Ragstash is a CLI utility to help retrieve RAG (Retrieval Augmented Generation) context from your documents which can then be fed into an LLM of your choice. It is a simple tool meant to be integrated into your RAG workflow. You could even ask a local LLM (that you trust) to fetch RAG context by using the tool itself while a server is running.

## Installation

Available on [PyPI](https://pypi.org/project/ragstash/)

__recommended:__

`pipx install ragstash` or `uv tool install ragstash`

You should then have `ragstash` command available. 

## Usage

First, cd into your documents folder, then: 

1. Use `ragstash init` to initialize (processes documents, generates embeddings, and saves vector db)
2. Use `ragstash serve` to start the server used for querying
3. (_In a separate terminal_) Use `ragstash get <QUERY>` to print out the RAG context. This output can be piped (|) into an LLM or saved in a file.

### Example Usage

__Simple__:

```sh
> cd path/to/your/documents
> ragstash init
> ragstash serve

# In another terminal
> ragstash get "What do the leaked files say about the doings of Celebrity Celebface?" | claude
```

__Advanced__:

```sh
> cd path/to/your/documents
> ragstash init \
  --sentence-transformer "sentence-transformers/all-MiniLM-L6-v2" \
  --chunk-size 1000 \
  --name "LargeChunks"
> ragstash serve --name "LargeChunks"

# In another terminal
> ragstash get "What do the leaked files say about the doings of Celebrity Celebface?" \
  --retrieval-query "Things Celebrity Celebface has done" \
  --chunks 10 \
  --message "I am doing RAG, here are some chunks of info ^^" \
  | claude
```

## Options

```sh

> init PTH
    --sentence-transformer  # model to use for embedding of chunks
    --chunk-size            # size of chunks (chars)
    --chunk-overlap         # overlap of chunks (chars)
    --redo                  # overwrite existing vault
    --name                  # name to give initialization (appended to folder name: ".rag_{NAME}")

> serve PTH
    --name                  # which initialization to use
    --unload-timeout        # time after which sentence transformer mode unloads (0 means never unloads)
    --port

> get YOUR_QUERY
    --chunks                # number of chunks to fetch
    --retrieval-query       # query to use when doing "dumb" retrieval of data (given to sentence transformer)
    --message               # message to give LLM
    --port                  # port to fetch
    --ip-addr               # default `localhost`
    --chunks-as-json        # instead of getting RAG formatted message, get retireved chunks as json
    --file                  # file where to save retrieved context

> update PTH
    --name                  # name of vault

```

## Upcoming features

- `update` mode so that you can add or update documents and only scan the changes.
