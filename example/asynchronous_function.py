import asyncio
from retry import Retry, stop_after_attempt, wait_exponential, wait_fixed, retry_if_exception_type, retry_if_result
import time


@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_exponential(multiplier=1, min_wait=1, max_wait=10),
    retry_on_exceptions=(ValueError,),
    retry_on_result=lambda result: result != "Success"
)
async def unreliable_async_function():
    print("Trying to perform an unreliable operation.")
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"


async def main():
    try:
        result = await unreliable_async_function()
        print(f"Function succeeded with result: {result}")
    except Exception as e:
        print(f"Function failed after retries with exception: {e}")


asyncio.run(main())
