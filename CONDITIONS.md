# Retry Conditions

This document provides detailed explanations and examples for the various stop, wait, and retry conditions available in the `retry` package.

## Stop Conditions

### `stop_after_attempt`

Stops retrying after a specified number of attempts.

**Usage Example:**

```python
from retry import Retry, stop_after_attempt, wait_fixed
import time

@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_fixed(1),
    retry_on_exceptions=(ValueError,)
)
def unreliable_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

### `stop_after_delay`

Stops retrying after a specified delay in seconds.

**Usage Example:**

```python
from retry import Retry, stop_after_delay, wait_fixed
import time

@Retry(
    stop_condition=stop_after_delay(10),  # 10 seconds
    wait_condition=wait_fixed(1),
    retry_on_exceptions=(ValueError,)
)
def unreliable_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

### `stop_before_delay`

Stops retrying just before a specified delay in seconds.

**Usage Example:**

```python
from retry import Retry, stop_before_delay, wait_fixed
import time

@Retry(
    stop_condition=stop_before_delay(10),  # Stops at 9 seconds
    wait_condition=wait_fixed(1),
    retry_on_exceptions=(ValueError,)
)
def unreliable_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

### `combine_stop_conditions`

Combines multiple stop conditions using logical OR.

**Usage Example:**

```python
from retry import Retry, stop_after_attempt, stop_after_delay, combine_stop_conditions, wait_fixed
import time

@Retry(
    stop_condition=combine_stop_conditions(stop_after_attempt(5), stop_after_delay(10)),
    wait_condition=wait_fixed(1),
    retry_on_exceptions=(ValueError,)
)
def unreliable_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

## Wait Conditions

### `wait_fixed`

Fixed wait time between retries.

**Usage Example:**

```python
from retry import Retry, stop_after_attempt, wait_fixed
import time

@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_fixed(2),  # 2 seconds fixed wait time
    retry_on_exceptions=(ValueError,)
)
def unreliable_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

### `wait_random`

Random wait time between retries.

**Usage Example:**

```python
from retry import Retry, stop_after_attempt, wait_random
import time

@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_random(1, 3),  # Waits between 1 to 3 seconds randomly
    retry_on_exceptions=(ValueError,)
)
def unreliable_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

### `wait_random_exponential`

Random exponential backoff wait time between retries.

**Usage Example:**

```python
from retry import Retry, stop_after_attempt, wait_random_exponential
import time

@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_random_exponential(multiplier=1, max_seconds=10),
    retry_on_exceptions=(ValueError,)
)
def unreliable_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

### `wait_chain`

Chain of fixed wait times between retries.

**Usage Example:**

```python
from retry import Retry, stop_after_attempt, wait_chain
import time

@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_chain(1, 2, 5, 10),  # Waits 1s, 2s, 5s, and then 10s
    retry_on_exceptions=(ValueError,)
)
def unreliable_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

### `wait_exponential`

Exponential backoff wait time between retries.

**Usage Example:**

```python
from retry import Retry, stop_after_attempt, wait_exponential
import time

@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_exponential(multiplier=1, min_wait=2, max_wait=10),
    retry_on_exceptions=(ValueError,)
)
def unreliable_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

## Retry Conditions

### `retry_if_exception_type`

Retries if the exception is of a specified type.

**Usage Example:**

```python
from retry import Retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import time

@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_fixed(1),
    retry_on_exceptions=(ValueError,)
)
def unreliable_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

### `retry_if_not_exception_type`

Retries if the exception is not of a specified type.

**Usage Example:**

```python
from retry import Retry, stop_after_attempt, wait_fixed, retry_if_not_exception_type
import time

@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_fixed(1),
    retry_on_exceptions=(Exception,),
    retry_on_result=lambda result: result != "Success"
)
def unreliable_function():
    if time.time() % 2 < 1:
        raise RuntimeError("Simulated transient error.")
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

### `retry_if_result`

Retries if the result satisfies a specified predicate.

**Usage Example:**

```python
from retry import Retry, stop_after_attempt, wait_fixed, retry_if_result
import time

@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_fixed(1),
    retry_on_result=lambda result: result is None
)
def unreliable_function():
    if time.time() % 2 < 1:
        return None
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

### `retry_if_not_result`

Retries if the result does not satisfy a specified predicate.

**Usage Example:**

```python
from retry import Retry, stop_after_attempt, wait_fixed, retry_if_not_result
import time

@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_fixed(1),
    retry_on_result=lambda result: result != "Success"
)
def unreliable_function():
    if time.time() % 2 < 1:
        return "Failure"
    return "Success"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

### `combine_retry_conditions`

Combines multiple

 retry conditions using logical OR.

**Usage Example:**

```python
from retry import Retry, stop_after_attempt, wait_fixed, retry_if_result, retry_if_exception_type, combine_retry_conditions
import time

@Retry(
    stop_condition=stop_after_attempt(5),
    wait_condition=wait_fixed(1),
    retry_on_exceptions=(ValueError,),
    retry_on_result=combine_retry_conditions(
        retry_if_result(lambda result: result == "Failure"),
        retry_if_exception_type(ValueError)
    )
)
def unreliable_function():
    if time.time() % 2 < 1:
        raise ValueError("Simulated transient error.")
    return "Failure"

try:
    result = unreliable_function()
    print(f"Function succeeded with result: {result}")
except Exception as e:
    print(f"Function failed after retries with exception: {e}")
```

## Conclusion

This document provides comprehensive examples of how to use the various stop, wait, and retry conditions available in the `retry` package. By understanding and utilizing these conditions, you can customize the retry behavior of your functions to suit your specific needs.


