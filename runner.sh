for i in $(seq 1 50); do
  echo Starting to execute main.py
  warning=$(python3 main.py 2>&1)
  echo Executed main.py $i times.
done

echo Analysing the Results
python3 analysis.py
