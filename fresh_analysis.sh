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
if [ -d "./node_failures_plots" ]; then
    echo "-----------------------------------------------------"
else
    mkdir node_failures_plots
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
    cd ..
fi

# DIR = /node_failures_plots
if [ "$(ls -A ./node_failures_plots)" ]; then
    cd ./node_failures_plots/
    rm -r *.*
    cd ..
fi

