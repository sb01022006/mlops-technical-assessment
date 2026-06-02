# MLOps Technical Assessment

## Local Run

pip install -r requirements.txt

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

## Docker

docker build -t mlops-task .

docker run --rm mlops-task

## Output

metrics.json contains:
- rows_processed
- signal_rate
- latency_ms
- seed
- status