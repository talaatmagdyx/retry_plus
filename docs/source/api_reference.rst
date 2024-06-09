===============
 API Reference
===============

Retry Main API
--------------

.. autoclass:: retry.Retry
   :members:

.. autofunction:: retry.stop_after_attempt
   :noindex:

.. autofunction:: retry.stop_after_delay
   :noindex:

.. autofunction:: retry.stop_before_delay
   :noindex:

.. autofunction:: retry.combine_stop_conditions
   :noindex:

.. autofunction:: retry.wait_fixed
   :noindex:

.. autofunction:: retry.wait_random
   :noindex:

.. autofunction:: retry.wait_random_exponential
   :noindex:

.. autofunction:: retry.wait_chain
   :noindex:

.. autofunction:: retry.wait_exponential
   :noindex:

.. autofunction:: retry.retry_if_exception_type
   :noindex:

.. autofunction:: retry.retry_if_not_exception_type
   :noindex:

.. autofunction:: retry.retry_if_result
   :noindex:

.. autofunction:: retry.retry_if_not_result
   :noindex:

.. autofunction:: retry.combine_retry_conditions
   :noindex:

Retry Conditions
----------------

.. automodule:: retry.conditions
   :members:
