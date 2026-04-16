class Scheduler:
    def __init__(self, root, interval, callback):
        self.root = root
        self.interval = interval
        self.callback = callback
        self.running = False

    def start(self):
        self.running = True
        self._run()

    def _run(self):
        if self.running:
            self.callback()
            self.root.after(self.interval, self._run)

    def stop(self):
        self.running = False