import time

timers = {}


def debounce(fn, minTime=0.25):
    now = time.time()
    lastCalled = timers.get(fn, None)
    if lastCalled is not None and (now - lastCalled) < minTime:
        return
    fn()
    timers[fn] = now
