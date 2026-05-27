# Notes

## Publishing workflow

uv build                # produces dist/
uv publish              # uploads to PyPi
twine upload dist/*     # uploads to PyPi (uses ~/.pypirc)

## TAP idiosyncracy

For multi-word arguments where you also use .add_argument() and use dash (-) as separator, use `default=""` to prevent it being required.
