import requests
from retry import Retry, stop_after_attempt, wait_exponential

# Define a function to make an HTTP request
@Retry(
    # stop_condition=stop_after_attempt(5),  # Retry up to 5 times
    # wait_condition=wait_exponential(multiplier=1, min_wait=1, max_wait=10),  # Exponential backoff
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
