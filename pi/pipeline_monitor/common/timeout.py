import sys
import time


def func_with_timeout(func, result_validator, timeout_seconds=None, interval_ms=None):
    timeout_seconds = timeout_seconds or sys.maxsize
    start_timestamp = time.time()
    while True:
        result = func()
        if result_validator(result):
            return result
        current_stamp = time.time()
        if current_stamp - start_timestamp >= timeout_seconds:
            raise TimeoutError("Function run timeout")
        if interval_ms:
            time.sleep(0.001 * interval_ms)
