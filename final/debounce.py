import time

timers = {}


def debounce(fn, minTime):
    now = time.time()
    lastCalled = timers.get(fn, None)
    if lastCalled is not None and (now - lastCalled) < minTime:
        return
    timers[fn] = now
    fn()
