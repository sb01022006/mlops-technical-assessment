
import argparse, json, logging, time, yaml, pandas as pd, numpy as np

def write_error(output, version, msg):
    with open(output, "w") as f:
        json.dump({"version": version, "status": "error", "error_message": msg}, f, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)
    args = parser.parse_args()

    logging.basicConfig(filename=args.log_file, level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    start = time.time()
    version = "v1"

    try:
        logging.info("Job started")

        with open(args.config) as f:
            cfg = yaml.safe_load(f)

        for k in ["seed","window","version"]:
            if k not in cfg:
                raise ValueError(f"Missing config field: {k}")

        version = cfg["version"]
        np.random.seed(cfg["seed"])
        logging.info(f"Config validated: {cfg}")

        df = pd.read_csv(args.input)
        if df.empty:
            raise ValueError("Empty file")
        if "close" not in df.columns:
            raise ValueError("Missing required column: close")

        logging.info(f"Rows loaded: {len(df)}")

        df["rolling_mean"] = df["close"].astype(float).rolling(cfg["window"]).mean()
        df["signal"] = ((df["close"].astype(float) > df["rolling_mean"]) &
                        df["rolling_mean"].notna()).astype(int)

        signal_rate = float(df["signal"].mean())
        latency_ms = int((time.time() - start) * 1000)

        metrics = {
            "version": version,
            "rows_processed": int(len(df)),
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": int(cfg["seed"]),
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=2)

        logging.info(f"Metrics summary: {metrics}")
        logging.info("Job completed successfully")
        print(json.dumps(metrics))

    except Exception as e:
        logging.exception("Job failed")
        write_error(args.output, version, str(e))
        print(json.dumps({"version": version, "status":"error","error_message":str(e)}))
        raise

if __name__ == "__main__":
    main()
