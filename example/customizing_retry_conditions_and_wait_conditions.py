from retry import stop_after_attempt, stop_after_delay, stop_before_delay

# ###################################### Stop Conditions: #########################

# Stop after a certain number of attempts
stop_condition = stop_after_attempt(5)

# Stop after a certain amount of time
stop_condition = stop_after_delay(10)  # 10 seconds

# Stop just before a certain amount of time
stop_condition = stop_before_delay(10)  # Stop at 9 seconds

# ###################################### Wait Conditions: #########################

from retry import wait_fixed, wait_random, wait_exponential, wait_chain

# Fixed wait time between retries
wait_condition = wait_fixed(2)  # 2 seconds

# Random wait time between retries
wait_condition = wait_random(min_seconds=1, max_seconds=3)

# Exponential backoff
wait_condition = wait_exponential(multiplier=1, min_wait=1, max_wait=10)

# Chain of wait times
wait_condition = wait_chain(1, 2, 5, 10)  # 1s, 2s, 5s, 10s
