#!/bin/bash

uvicorn api.main:app \
  --reload \
  --reload-dir api \
