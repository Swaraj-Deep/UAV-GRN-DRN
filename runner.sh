for i in $(seq 1 50); do
  python3 main.py 2
  echo Executed main.py $i times.
done

python3 analysis.py
