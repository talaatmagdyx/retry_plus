import time
from retry import Retry, stop_after_attempt, wait_exponential

try:
    with Retry(
            stop_condition=stop_after_attempt(3),
            wait_condition=wait_exponential(multiplier=1, min_wait=1, max_wait=5),
            retry_on_exceptions=(ValueError,)
    ):
        print("Trying block operation.")
        if time.time() % 2 < 1:
            raise ValueError("Simulated transient error.")
        print("Block operation succeeded.")
except Exception as e:
    print(f"Block operation failed after retries with exception: {e}")
