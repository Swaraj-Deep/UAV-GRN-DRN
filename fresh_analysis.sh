#!/bin/bash
if [ -d "./output_files" ]; then
    echo "-----------------------------------------------------"
else
    mkdir output_files
    echo "Creating directory for output files"
fi
# DIR = /output_files
if [ "$(ls -A ./output_files)" ]; then
    cd ./output_files/
    rm -r *.*
fi
