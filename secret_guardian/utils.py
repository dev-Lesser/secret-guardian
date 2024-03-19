from contextlib import ContextDecorator


class process(ContextDecorator):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass
