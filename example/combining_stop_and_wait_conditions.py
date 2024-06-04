from retry import Retry, stop_after_delay, wait_random_exponential
import time


@Retry(
    stop_condition=stop_after_delay(20),  # Stop after 20 seconds
    wait_condition=wait_random_exponential(multiplier=1, max_seconds=10),  # Exponential backoff with randomness
    retry_on_exceptions=(ValueError,)
)
def unreliable_function():
    print("Trying to perform an unreliable operation.")
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"


try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
