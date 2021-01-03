#!/usr/bin/env python3
import sys
import time
import threading


class Main:
    _lastBeat = None
    _timer = None
    _abortVibingEvent = threading.Event()
    _debug = False

    def run(self):
        for line in sys.stdin:
            if self._lastBeat is not None:
                # Calculate time since last beat:
                sinceLastBeat = time.monotonic() - self._lastBeat

                # Start “vibing” after half a beat passes:
                untilVibeStart = sinceLastBeat / 2.

                # Calculate “down“ and “up“ duration:
                downDuration = sinceLastBeat / 2.
                upDuration = sinceLastBeat / 2.

                # Print message:
                if self._debug:
                    print(f'beat! ({sinceLastBeat:.2f}s since last, assuming '
                          f'{untilVibeStart:.2f}s until next one starts)')

                # Start timer if not already running:
                self._timer = threading.Timer(
                    untilVibeStart, self.vibeStart,
                    [downDuration, upDuration])
                self._timer.start()

            # Remember time of last beat:
            self._lastBeat = time.monotonic()

    def vibeStart(self, downDuration, upDuration):
        # Abort old vibing:
        self._abortVibingEvent.set()
        self._abortVibingEvent.clear()

        # Vibe!:
        self.llamaNormal()
        if self._abortVibingEvent.wait(downDuration):
            return
        self.llamaVibe()
        if self._abortVibingEvent.wait(upDuration):
            return
        self.llamaNormal()

    def llamaNormal(self):
        if not self._debug:
            print(chr(27) + "[2J")
        print("  \\/")
        print(" <'l")
        print("  ll")
        print("  llama~")
        print("  || ||")
        print("  '' ''")

    def llamaVibe(self):
        if not self._debug:
            print(chr(27) + "[2J")
        print(" \\/")
        print("<'l")
        print("  \\\\")
        print("  llama~")
        print("  || ||")
        print("  '' ''")


if __name__ == '__main__':
    Main().run()
