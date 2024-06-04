## [released]

## [1.0.0] - 2024-06-04
- Initial release of the retry package.
- Generic decorator API for retrying operations.
- Support for synchronous and asynchronous functions.
- Various stop conditions (e.g., number of attempts, time-based).
- Various wait conditions (e.g., exponential backoff, fixed delay, random delay).
- Customizable retry conditions based on exceptions and result values.
- Context manager support.
- Logging and custom callbacks before/after retries and before sleep.
- Retry statistics and dynamic arguments at runtime.