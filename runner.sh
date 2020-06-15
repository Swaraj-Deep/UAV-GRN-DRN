for i in $(seq 1 15); do
  echo Starting to execute main.py
  python3 main.py 2
  echo Executed main.py $i times.
done

echo Analysing the Results
python3 analysis.py
