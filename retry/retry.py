import time
import asyncio  # Importing asyncio module for asynchronous programming
import functools  # Importing functools module for higher-order functions
from typing import Callable, Type, Optional, Tuple, Any  # Importing typing module for type annotations


class RetryError(Exception):
    """
    Exception raised when the retrying operation fails after the maximum number of attempts.
    """

    def __init__(self, last_attempt):
        self.last_attempt = last_attempt  # Storing the last attempt when the error occurred


class TryAgain(Exception):
    """
    Exception that can be raised to explicitly retry the operation.
    """
    pass  # No additional functionality needed, serves as a marker exception


class Retry:
    """
    Retry decorator and context manager to retry operations based on specified conditions.

    Args:
        stop_condition: Callable that determines when to stop retrying. Default stop condition: stops after 3 attempts.
        wait_condition: Callable that determines how long to wait between attempts. Default wait condition: waits 1 second between attempts.
        retry_on_exceptions: Tuple of exception types that trigger a retry.
        retry_on_result: Callable that determines if the result should trigger a retry.
        before: Callable executed before each attempt.
        after: Callable executed after each attempt.
        before_sleep: Callable executed before sleeping between attempts.
        reraise: Boolean indicating whether to reraise the last exception if the stop condition is met.
    """

    def __init__(self,
                 stop_condition: Callable[[int, Optional[Exception], Optional[Any]], bool] = None,
                 wait_condition: Callable[[int], float] = None,
                 retry_on_exceptions: Tuple[Type[Exception], ...] = (Exception,),
                 retry_on_result: Optional[Callable[[Any], bool]] = None,
                 before: Optional[Callable] = None,
                 after: Optional[Callable] = None,
                 before_sleep: Optional[Callable] = None,
                 reraise: bool = False):
        self.stop_condition = stop_condition if stop_condition is not None else self.default_stop_condition
        self.wait_condition = wait_condition if wait_condition is not None else self.default_wait_condition
        self.retry_on_exceptions = retry_on_exceptions  # Storing the exceptions that trigger a retry
        self.retry_on_result = retry_on_result  # Storing the result-based retry condition
        self.before = before  # Storing the before attempt callback
        self.after = after  # Storing the after attempt callback
        self.before_sleep = before_sleep  # Storing the before sleep callback
        self.reraise = reraise  # Storing the reraise flag

    def default_stop_condition(self, attempt: int, exception: Optional[Exception], result: Optional[Any]) -> bool:
        """Default stop condition: stops after 3 attempts."""
        return attempt >= 3

    def default_wait_condition(self, attempt: int) -> float:
        """Default wait condition: waits 1 second between attempts."""
        return 1.0

    def __call__(self, func: Callable):
        """
        Wraps the function with retry logic.
        """
        if asyncio.iscoroutinefunction(func):  # Check if the function is asynchronous
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await self._retry_async(func, *args, **kwargs)  # Wrap with async retry logic

            return async_wrapper  # Return the wrapped async function
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                return self._retry_sync(func, *args, **kwargs)  # Wrap with sync retry logic

            return sync_wrapper  # Return the wrapped sync function

    def _retry_sync(self, func: Callable, *args, **kwargs):
        """
        Retry logic for synchronous functions.
        """
        attempt = 0  # Initialize attempt counter
        while True:
            try:
                if self.before:
                    self.before(self)  # Call before callback if provided
                result = func(*args, **kwargs)  # Execute the function
                if self.retry_on_result and self.retry_on_result(result):
                    attempt += 1  # Increment attempt counter
                    if self.stop_condition(attempt, None, result):
                        return result  # Stop condition met, return result
                    if self.before_sleep:
                        self.before_sleep(self)  # Call before sleep callback if provided
                    time.sleep(self.wait_condition(attempt))  # Wait before next attempt
                else:
                    if self.after:
                        self.after(self)  # Call after callback if provided
                    return result  # Return result if no retry needed
            except self.retry_on_exceptions as e:
                attempt += 1  # Increment attempt counter
                if self.stop_condition(attempt, e, None):
                    if self.reraise:
                        raise e  # Reraise the last exception
                    else:
                        raise RetryError(e)  # Raise RetryError with the last exception
                if self.before_sleep:
                    self.before_sleep(self)  # Call before sleep callback if provided
                time.sleep(self.wait_condition(attempt))  # Wait before next attempt

    async def _retry_async(self, func: Callable, *args, **kwargs):
        """
        Retry logic for asynchronous functions.
        """
        attempt = 0  # Initialize attempt counter
        while True:
            try:
                if self.before:
                    self.before(self)  # Call before callback if provided
                result = await func(*args, **kwargs)  # Execute the async function
                if self.retry_on_result and self.retry_on_result(result):
                    attempt += 1  # Increment attempt counter
                    if self.stop_condition(attempt, None, result):
                        return result  # Stop condition met, return result
                    if self.before_sleep:
                        self.before_sleep(self)  # Call before sleep callback if provided
                    await asyncio.sleep(self.wait_condition(attempt))  # Wait before next attempt
                else:
                    if self.after:
                        self.after(self)  # Call after callback if provided
                    return result  # Return result if no retry needed
            except self.retry_on_exceptions as e:
                attempt += 1  # Increment attempt counter
                if self.stop_condition(attempt, e, None):
                    if self.reraise:
                        raise e  # Reraise the last exception
                    else:
                        raise RetryError(e)  # Raise RetryError with the last exception
                if self.before_sleep:
                    self.before_sleep(self)  # Call before sleep callback if provided
                await asyncio.sleep(self.wait_condition(attempt))  # Wait before next attempt

    def __enter__(self):
        """
        Enter the runtime context related to this object.
        """
        return self  # Return the current instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context related to this object.
        """
        if exc_type is not None and issubclass(exc_type, self.retry_on_exceptions):
            return not self.stop_condition(1, exc_val, None)  # Determine if the exception should be suppressed
