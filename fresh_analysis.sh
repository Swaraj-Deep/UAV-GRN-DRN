#!/bin/bash
if [ -d "./output_files" ]; then
    echo "-----------------------------------------------------"
else
    mkdir output_files
    echo "Creating directory for output files"
fi
if [ -d "./graph_output_files" ]; then
    echo "-----------------------------------------------------"
else
    mkdir graph_output_files
    echo "Creating directory for Graph output files"
fi
# DIR = /output_files
if [ "$(ls -A ./output_files)" ]; then
    cd ./output_files/
    rm -r *.*
    cd ..
fi
# DIR = /graph_output_files
if [ "$(ls -A ./graph_output_files)" ]; then
    cd ./graph_output_files/
    rm -r *.*
fi

