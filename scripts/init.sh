#!/usr/bin/env bash

git submodule update --init --recursive
cd ./runs/
npm i
cd ../eoc/
npm i
