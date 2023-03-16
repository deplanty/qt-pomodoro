import time


class Chrono:
    def __init__(self):
        self._timer = float()
        self._start = float()
        self._end = float()
        self._pause_tot = float()
        self._pause_start = float()

    @property
    def duration(self) -> float:
        if self.is_running():
            return time.perf_counter() - self._start - self._pause_tot
        else:
            return self._end - self._start - self._pause_tot

    @property
    def remaining(self):
        return self._timer - self.duration

    def is_running(self) -> bool:
        return self._start >= self._end

    def set_timer(self, seconds:float):
        self._timer = seconds

    def start(self):
        self._start = time.perf_counter()
        self._pause_tot = float()

    def stop(self):
        self._end = time.perf_counter()

    def pause(self):
        self._pause_start = time.perf_counter()

    def resume(self):
        self._pause_tot += time.perf_counter() - self._pause_start
        self._pause_start = float()

    def restart(self):
        self.start()

    def reset(self):
        self.start()
        self.pause()
