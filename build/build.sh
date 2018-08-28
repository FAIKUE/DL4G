#!/bin/bash

# pack sources
mkdir -p dist
tar cfv ./dist/libs.tar --exclude .git -C source/ .
