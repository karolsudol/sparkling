import os
import time
from datetime import datetime

import pandas as pd


def generate_batch(batch_id):
    # Create more "expressive" data with timestamps and amounts
    data = {
        "transaction_id": [f"TXN_{batch_id}_{i}" for i in range(10)],
        "user_id": [f"USER_{i%3}" for i in range(10)],
        "amount": [10.5 * (i + 1) * batch_id for i in range(10)],
        "status": ["COMPLETED" if i % 4 != 0 else "PENDING" for i in range(10)],
        "event_time": [datetime.now().isoformat() for _ in range(10)],
    }
    df = pd.DataFrame(data)

    filename = f"data/landing/batch_{batch_id}_{int(time.time())}.csv"
    df.to_csv(filename, index=False)
    print(f"Generated {filename}")


if __name__ == "__main__":
    # Generate an initial batch if none exists
    if not os.listdir("data/landing"):
        generate_batch(1)
    else:
        # Generate a subsequent batch
        generate_batch(2)
