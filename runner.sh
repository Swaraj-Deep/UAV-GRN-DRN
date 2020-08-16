#!/bin/bash
read -p "Which process you want to run (bruteforce/q_learn): " type_input
read -p "Enter number of times to run simulation: " number
if [[ ! $number =~ ^[0-9]+$ ]]; then
  echo "Enter only integers"
  exit
fi
read -p "Do you want to delete previous output files (y/n): " input
if [ ${input,,} = y ]; then
  echo "Removing previous output files"
  bash fresh_analysis.sh
  echo "Removed"
fi
if [ ${type_input,,} == bruteforce ]; then
  echo "Updating to bruteforce"
  python3 __update.py bruteforce
  for i in $(seq 1 $number); do
    echo Generating user location
    python3 user_scenario_cluster.py
    echo Generated user location
    echo Starting to execute main.py
    warning=$(python3 main.py 2>&1)
    echo Executed main.py $i times.
  done
else
  echo "Updating to q_learn"
  python3 __update.py q_learn
  echo Generating user location
  python3 user_scenario_cluster.py
  echo Generated user location
  for i in $(seq 1 $number); do
    echo Starting to execute main.py
    warning=$(python3 main.py 2>&1)
    echo Executed main.py $i times.
  done
fi
echo Analysing the Results
python3 analysis.py
