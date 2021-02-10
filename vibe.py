#!/usr/bin/env python3
import sys
import time
import threading
import serial


class Main:
    _lastBeat = None
    _timer = None
    _abortVibingEvent = threading.Event()
    _debug = False
    _angles = (10, 30)

    def __init__(self, argv):
        if len(argv) >= 2:
            print('Opening serial port %s ...' % argv[1])
            self._serial = serial.Serial(argv[1], 9600, timeout=0)
        else:
            self._serial = None

    def __del__(self):
        if self._serial is not None:
            print('Closing serial port ...')
            self._serial.close()

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
        self.serialSend("%d,%d\n" % (
            self._angles[0], round(downDuration * 1000)))
        self.llamaNormal()
        if self._abortVibingEvent.wait(downDuration):
            return
        self.serialSend("%d,%d\n" % (
            self._angles[1], round(upDuration * 1000)))
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

    def serialSend(self, msg):
        if self._debug:
            print(msg)
        if self._serial is not None:
            recvMsg = self._serial.readline()
            if self._debug:
                print(recvMsg.decode('ascii').strip())
            self._serial.write(msg.encode('ascii'))


if __name__ == '__main__':
    Main(sys.argv).run()
