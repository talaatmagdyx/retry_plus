import time
import pytest
import asyncio
from retry import (
    Retry, RetryError, TryAgain,
    stop_after_attempt, stop_after_delay, stop_before_delay, combine_stop_conditions,
    wait_fixed, wait_random, wait_random_exponential, wait_chain, wait_exponential,
    retry_if_exception_type, retry_if_not_exception_type, retry_if_result, retry_if_not_result, combine_retry_conditions
)


# Synchronous function example with fixed wait
@Retry(
    stop_condition=stop_after_attempt(3),
    wait_condition=wait_fixed(1),
    retry_on_exceptions=(ValueError,),
    retry_on_result=lambda result: result != "Success"
)
def fixed_wait_sync_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"


# Asynchronous function example with random wait
@Retry(
    stop_condition=stop_after_attempt(3),
    wait_condition=wait_random(1, 2),
    retry_on_exceptions=(ValueError,),
    retry_on_result=lambda result: result != "Success"
)
async def random_wait_async_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"


# Synchronous function example with exponential backoff
@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_exponential(multiplier=1, min_wait=2, max_wait=5),
    retry_on_exceptions=(ValueError,),
    retry_on_result=lambda result: result != "Success"
)
def exponential_backoff_sync_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"


# Test retry with a combination of stop conditions
@Retry(
    stop_condition=combine_stop_conditions(stop_after_attempt(3), stop_after_delay(10)),
    wait_condition=wait_fixed(1),
    retry_on_exceptions=(ValueError,)
)
def combined_stop_conditions_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"


# Test context manager with stop_before_delay
def test_context_manager_stop_before_delay():
    try:
        with Retry(
                stop_condition=stop_before_delay(5),
                wait_condition=wait_fixed(1),
                retry_on_exceptions=(ValueError,)
        ):
            if time.time() % 2 < 1:
                raise ValueError("Simulated transient error.")
    except Exception:
        pytest.fail("Context manager failed after retries.")


# Test retry with exception type condition
@Retry(
    stop_condition=stop_after_attempt(3),
    wait_condition=wait_fixed(1),
    retry_on_exceptions=(ValueError,),
    retry_on_result=lambda result: result != "Success"
)
def exception_type_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"


# Test retry if result is None
@Retry(
    stop_condition=stop_after_attempt(3),
    wait_condition=wait_fixed(1),
    retry_on_result=lambda result: result is None
)
def result_is_none_function():
    if time.time() % 2 < 1:
        return None
    return "Success"


# Test sync retry
def test_sync_retry():
    try:
        result = fixed_wait_sync_function()
        assert result == "Success"
    except Exception:
        pytest.fail("Synchronous function failed after retries.")


# Test async retry
@pytest.mark.asyncio
async def test_async_retry():
    try:
        result = await random_wait_async_function()
        assert result == "Success"
    except Exception:
        pytest.fail("Asynchronous function failed after retries.")


# Test exponential backoff
def test_exponential_backoff():
    try:
        result = exponential_backoff_sync_function()
        assert result == "Success"
    except Exception:
        pytest.fail("Exponential backoff function failed after retries.")


# Test combined stop conditions
def test_combined_stop_conditions():
    try:
        result = combined_stop_conditions_function()
        assert result == "Success"
    except Exception:
        pytest.fail("Combined stop conditions function failed after retries.")


# Test result is None condition
def test_result_is_none():
    try:
        result = result_is_none_function()
        assert result == "Success"
    except Exception:
        pytest.fail("Result is None function failed after retries.")


# Test context manager
def test_context_manager():
    try:
        with Retry(
                stop_condition=stop_after_attempt(3),
                wait_condition=wait_exponential(multiplier=1, min_wait=1, max_wait=5),
                retry_on_exceptions=(ValueError,)
        ):
            if time.time() % 2 < 1:
                raise ValueError("Simulated transient error.")
    except Exception:
        pytest.fail("Context manager failed after retries.")


# Test exception type condition
def test_exception_type():
    try:
        result = exception_type_function()
        assert result == "Success"
    except Exception:
        pytest.fail("Exception type function failed after retries.")


# Test wait_exponential min_wait and max_wait
def test_wait_exponential():
    wait_time_fn = wait_exponential(multiplier=1, min_wait=2, max_wait=10)
    assert wait_time_fn(1) == 2  # min_wait should be applied
    assert wait_time_fn(2) == 2  # max(min_wait, multiplier * (2 ** (1))) = 2
    assert wait_time_fn(3) == 4  # 2 ** (3 - 1) = 4
    assert wait_time_fn(4) == 8  # 2 ** (4 - 1) = 8
    assert wait_time_fn(5) == 10  # max_wait should be applied
    assert wait_time_fn(6) == 10  # max_wait should be applied
