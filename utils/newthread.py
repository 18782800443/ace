import threading


class newThread(threading.Thread):

    def __init__(self, target, args, kwargs):
        threading.Thread.__init__(self)
        self.exception = None
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            self.target(*self.args, **self.kwargs)
        except Exception as e:
            self.exception = e

