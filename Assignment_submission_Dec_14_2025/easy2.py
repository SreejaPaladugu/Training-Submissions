from datetime import datetime

# --- Airflow-like mini orchestrator (toy) ---
def run_task(task_name, fn):
    print(f"[{datetime.now()}] START: {task_name}")
    result = fn()
    print(f"[{datetime.now()}] END:   {task_name}\n")
    return result

# --- ETL steps (toy) ---
def extract():
    # Toy "source"
    return [
        {"id": 1, "name": "alice", "amount": 100},
        {"id": 2, "name": "bob", "amount": 200},
        {"id": 3, "name": "alice", "amount": 50},
    ]

def transform(rows):
    # Clean + simple feature
    cleaned = []
    for r in rows:
        cleaned.append({
            "id": r["id"],
            "name": r["name"].title(),
            "amount": float(r["amount"]),
            "amount_with_tax": float(r["amount"]) * 1.08
        })
    return cleaned

def load(rows):
    # Toy "destination" = print + return
    print("Loaded rows:")
    for r in rows:
        print(r)
    return rows

def main():
    raw = run_task("extract_task", extract)
    transformed = run_task("transform_task", lambda: transform(raw))
    _ = run_task("load_task", lambda: load(transformed))

if __name__ == "__main__":
    main()
