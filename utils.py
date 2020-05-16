import sys


class ProgressBar:
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.printed = 0

    def update(self):
        self.current += 1
        while self.printed + 1 <= (self.current / self.total) * 10:
            sys.stdout.write(u'\u2588')
            sys.stdout.flush()
            self.printed += 1
