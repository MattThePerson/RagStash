# Notes

## Publishing workflow

uv build          # produces dist/
uv publish        # uploads to PyPI (uses ~/.pypi token or env var)

## Tap idiosyncracy

For multi-word arguments where you also use .add_argument() and use dash (-) as separator, use `default=""` to prevent it being required.

## Files

|-- __init__.py
|-- app.py          // 
|-- cli.py          // cli entry
|-- cli_args.py     // cli args
|-- server.py       // flask server
|-- rag_vault.py    // class RAGVault, initiated by
