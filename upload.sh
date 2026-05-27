#!/usr/bin/env bash

set -e

rm dist/*
uv build
twine upload dist/*
