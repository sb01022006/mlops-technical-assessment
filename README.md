# MLOps Technical Assessment

A minimal MLOps-style batch processing pipeline built in Python that demonstrates reproducibility, observability, validation, and deployment readiness.

## Features

- Configuration-driven execution using YAML
- Deterministic runs using a fixed random seed
- OHLCV dataset validation
- Rolling mean computation on close prices
- Binary signal generation
- Structured metrics output in JSON
- Detailed logging for observability
- Dockerized deployment
- Error handling and validation

---

## Project Structure

```text
.
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json
└── run.log
```

---

## Configuration

Configuration is provided through `config.yaml`.

Example:

```yaml
seed: 42
window: 5
version: "v1"
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| seed | Random seed for deterministic execution |
| window | Rolling mean window size |
| version | Pipeline version identifier |

---

## Dataset

The input dataset contains OHLCV market data.

Required column:

```text
close
```

The pipeline validates:

- Input file existence
- Readable CSV format
- Non-empty dataset
- Presence of required `close` column

---

## Processing Workflow

### 1. Load Configuration

The application loads and validates:

- seed
- window
- version

### 2. Load Dataset

The CSV dataset is loaded and validated.

### 3. Compute Rolling Mean

Rolling mean is calculated using:

```python
rolling_mean = close.rolling(window).mean()
```

### 4. Generate Signal

A binary signal is generated:

```python
signal = 1 if close > rolling_mean else 0
```

Rows without a valid rolling mean (initial window period) are handled consistently.

### 5. Generate Metrics

The following metrics are computed:

- rows_processed
- signal_rate
- latency_ms

### 6. Write Outputs

Generated outputs:

```text
metrics.json
run.log
```

---

## Local Setup

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Pipeline

```bash
python3 run.py \
--input data.csv \
--config config.yaml \
--output metrics.json \
--log-file run.log
```

---

## Example Metrics Output

```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4989,
  "latency_ms": 34,
  "seed": 42,
  "status": "success"
}
```

### Output Fields

| Field | Description |
|---------|-------------|
| version | Pipeline version |
| rows_processed | Number of rows processed |
| metric | Metric name |
| value | Signal rate |
| latency_ms | Runtime in milliseconds |
| seed | Random seed |
| status | Job status |

---

## Error Handling

If an error occurs, the application writes:

```json
{
  "version": "v1",
  "status": "error",
  "error_message": "Description of what went wrong"
}
```

Supported validation checks:

- Missing configuration file
- Invalid YAML structure
- Missing configuration fields
- Missing input file
- Invalid CSV format
- Empty dataset
- Missing close column

---

## Logging

Execution logs are written to:

```text
run.log
```

The log contains:

- Job start timestamp
- Configuration validation
- Dataset loading information
- Rolling mean computation
- Signal generation
- Metrics summary
- Job completion status
- Errors and exceptions

---

## Docker Support

### Build Docker Image

```bash
docker build -t mlops-task .
```

### Run Docker Container

```bash
docker run --rm mlops-task
```

The container:

- Loads configuration
- Processes the dataset
- Generates metrics.json
- Generates run.log
- Prints metrics JSON to stdout

---

## Example Docker Run

```bash
docker build -t mlops-task .

docker run --rm mlops-task
```

Example output:

```json
{
  "version":"v1",
  "rows_processed":10000,
  "metric":"signal_rate",
  "value":0.4989,
  "latency_ms":34,
  "seed":42,
  "status":"success"
}
```

---

## Reproducibility

Deterministic execution is achieved using:

```yaml
seed: 42
```

Given the same dataset and configuration, repeated executions produce identical results.

---

## Requirements

Python packages:

```text
pandas
numpy
pyyaml
```

Install using:

```bash
pip install -r requirements.txt
```

---

## Repository

Repository Name:

```text
mlops-technical-assessment
```

Repository Description:

```text
Dockerized MLOps pipeline that loads configuration from YAML, validates OHLCV data, computes rolling-mean trading signals, generates structured metrics, and provides detailed logging for reproducible batch processing.
```

---

## Author

**Syamantak Banerjee**

MLOps Technical Assessment Submission
