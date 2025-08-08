import threading
import time
from datetime import datetime

from dzmt.utils.console import console


class LogReader:
    _is_running = True
    _files = set()
    _labels = {}
    _lock = threading.Lock()

    def __init__(self):
        self._thread = threading.Thread(target=self._reader)
        self._thread.start()

    def push_log(self, log_file, label):
        with self._lock:
            self._files.add(log_file)
            self._labels[log_file] = label

    def pop_log(self, log_file):
        with self._lock:
            self._files.remove(log_file)
            self._labels.pop(log_file)

    def join(self):
        self._is_running = False
        self._thread.join()

    def _reader(self):
        while self._is_running:
            with self._lock:
                for file in self._files:
                    self._print_log(file)
            time.sleep(0.1)

    def _print_log(self, file):
        while True:
            line = file.readline()
            if not line:
                break

            prefix = f"{datetime.now().strftime('%H:%M:%S')} {self._labels[file]}"
            console.print(
                f"[{prefix}]: {bytearray(line, 'cp1251').decode('utf-8')}",
                end="",
            )
