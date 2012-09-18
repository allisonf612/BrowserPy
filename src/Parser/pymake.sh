#! /bin/bash

# For building a library to be used as a Python extension

if [ $# == 1 ]; then
  if [ $1 = "clean" ]; then
    rm -r -f build
    rm -f process.so
  fi
  if [ $1 = "test" ]; then
    python ../mvcApp/Model.py
  fi
elif [ $# == 0 ]; then
  python setup.py build
  cp build/lib.*/process.so ../mvcApp/process.so
  rm -r -f build
else
  echo "proper usage..."
fi
