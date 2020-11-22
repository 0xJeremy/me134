import time

timers = {}


def debounce(fn, minTime):
    now = time.time()
    lastCalled = timers.get(fn, None)
    if (now - lastCalled) < minTime:
        return
    timers[fn] = now
    fn()
