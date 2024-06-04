# Retry Package

A generic retry package for Python.

## Features

- Generic Decorator API
- Specify stop condition (e.g., limit by number of attempts, time-based conditions)
- Specify wait condition (e.g., exponential backoff, fixed delay, random delay)
- Customize retrying on Exceptions
- Customize retrying on expected returned result
- Retry on coroutines
- Retry code block with context manager
- Logging and custom callbacks before/after retries and before sleep
- Retry statistics and dynamic arguments at runtime

## Installation

```bash
pip install retry_plus
```

## Usage

For detailed usage and examples, refer to the [Conditions Documentation](https://github.com/talaatmagdyx/retry-plus/blob/main/CONDITIONS.md).

### Synchronous Function

```python
from retry import Retry, stop_after_attempt, wait_exponential
import time

@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_exponential(multiplier=1, min_wait=1, max_wait=10),
    retry_on_exceptions=(ValueError,),
    retry_on_result=lambda result: result != "Success"
)
def unreliable_sync_function():
    print("Trying to perform an unreliable operation.")
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"

try:
    result = unreliable_sync_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

### Asynchronous Function

```python
import asyncio
from retry import Retry, stop_after_attempt, wait_exponential
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
```

### Context Manager

```python
from retry import Retry, stop_after_attempt, wait_exponential
import time

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
    print(f"Context manager failed after retries with exception: {e}")
```

### Advanced Usage

#### Combining Stop and Wait Conditions

```python
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
```

# Real Example for http requests

```python
import requests
from retry import Retry, stop_after_attempt, wait_exponential

# Define a function to make an HTTP request
@Retry(
    stop_condition=stop_after_attempt(5),  # Retry up to 5 times
    wait_condition=wait_exponential(multiplier=1, min_wait=1, max_wait=10),  # Exponential backoff
    retry_on_exceptions=(requests.RequestException,),  # Retry on any requests exception
    retry_on_result=lambda result: result.status_code != 200  # Retry if the status code is not 200
)
def fetch_data_from_api(url):
    print(f"Trying to fetch data from {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError on bad status
    return response

# Use the function with a simulated unreliable endpoint
try:
    # Simulating a service that returns 500 Internal Server Error 50% of the time
    data = fetch_data_from_api("https://httpbin.org/status/500")
    print("Data fetched successfully:", data)
except Exception as e:
    print(f"Failed to fetch data after retries. Error: {e}")

# Use the function with a simulated successful endpoint
try:
    # Simulating a service that returns 200 OK
    data = fetch_data_from_api("https://httpbin.org/status/200")
    print("Data fetched successfully:", data)
except Exception as e:
    print(f"Failed to fetch data after retries. Error: {e}")

```


## Tests

To run the tests, use `pytest`:

```bash
pytest
```

## These tests cover:

- **Synchronous and Asynchronous Functions:** Testing both sync and async functions with various retry conditions.
- **Fixed and Random Wait Conditions:** Verifying the correct behavior with fixed and random wait conditions.
- **Exponential Backoff:** Ensuring that the retry logic respects exponential backoff settings.
- **Combined Stop Conditions:** Combining multiple stop conditions and ensuring the retry logic works as expected.
- **Context Manager:** Testing the retry logic within a context manager.
- **Exception Type and Result Conditions:** Verifying that the retry logic correctly handles retries based on specific exception types and result values.

## Contribute

We welcome contributions to improve the retry package. Here are some ways you can contribute:

1. **Report Bugs**: If you find a bug, please report it using the GitHub issue tracker.
2. **Feature Requests**: If you have an idea for a new feature, please open an issue to discuss it.
3. **Submit Pull Requests**: If you have a fix or a new feature, please submit a pull request.

### How to Contribute

1. **Fork the repository**: Click the "Fork" button on the GitHub repository page.
2. **Clone your fork**: Clone your fork to your local machine.
   ```bash
   git clone https://github.com/talaatmagdyx/retry-plus.git
   ```
3. **Create a branch**: Create a new branch for your changes.
   ```bash
   git checkout -b my-new-feature
   ```
4. **Make your changes**: Make your changes to the code.
5. **Commit your changes**: Commit your changes with a descriptive commit message.
   ```bash
   git commit -am 'Add some feature'
   ```
6. **Push to the branch**: Push your changes to your fork.
   ```bash
   git push origin my-new-feature
   ```
7. **Create a pull request**: Go to the GitHub repository page and create a pull request from your fork.

## Changelog

All notable changes to this project will be documented in this section.

### [Unreleased]

#### Added
- Initial release of the retry package.
- Generic decorator API for retrying operations.
- Support for synchronous and asynchronous functions.
- Various stop conditions (e.g., number of attempts, time-based).
- Various wait conditions (e.g., exponential backoff, fixed delay, random delay).
- Customizable retry conditions based on exceptions and result values.
- Context manager support.
- Logging and custom callbacks before/after retries and before sleep.
- Retry statistics and dynamic arguments at runtime.
