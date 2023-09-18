import time

SECOND = 1


class TokenBucket:

    def __init__(self, bucket_size: int, refill_rate: int, forward_callback, drop_callback):
        """
        :param bucket_size: the maximum number of tokens allowed in the bucket
        :param refill_rate: number of tokens put into the bucket every second
        :param forward_callback: ...
        :param drop_callback: ...
        """
        self.bucket_size = bucket_size
        self.tokens = self.bucket_size
        self.refill_rate = refill_rate
        self.forward_callback = forward_callback
        self.drop_callback = drop_callback
        self.last_check = time.time()

    def _refill(self) -> None:
        used_tokens = self.bucket_size - self.tokens
        self.tokens += self.refill_rate

        if self.tokens == self.bucket_size:
            return

    def request(self) -> None:
        current_check = time.time()
        delta_time = current_check - self.last_check
        if delta_time > SECOND:
            self._refill()
        if self.tokens > 0:
            self.tokens -= 1
            self.forward_callback()
        else:
            self.drop_callback()
