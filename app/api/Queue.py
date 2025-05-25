import time
import requests
from collections import deque

class RateLimitedAPIQueue:
    def __init__(self, max_requests_per_minute=8, wait_time_after_429=60):
        self.queue = deque()
        self.max_requests_per_minute = max_requests_per_minute
        self.wait_time_after_429 = wait_time_after_429
        self.last_request_times = []

    def _can_make_request(self):
        cutoff = time.time() - 60
        self.last_request_times = [t for t in self.last_request_times if t > cutoff]
        return len(self.last_request_times) < self.max_requests_per_minute

    def fetch(self, url, params=None):
        """
        Enqueue and process a single request, handle rate limits and retries.
        Returns the JSON response dict.
        """
        while True:
            if not self._can_make_request():
                wait_seconds = 60 - (time.time() - min(self.last_request_times))
                print(f"Rate limit reached, sleeping for {wait_seconds:.1f}s")
                time.sleep(wait_seconds + 1)  # +1 for safety

            response = requests.get(url, params=params)
            json_data = response.json()

            if "code" in json_data and json_data["code"] == 429:
                print(f"Received 429 - Too Many Requests. Waiting {self.wait_time_after_429}s before retrying.")
                time.sleep(self.wait_time_after_429)
                continue

            self.last_request_times.append(time.time())
            return json_data