"""Pytest-compatible replacement for unittest cleanup callbacks."""


class CleanupTestCase:
    """Provide unittest-style ``addCleanup`` in pytest classes."""

    def setup_method(self):
        self._cleanup_callbacks = []

    def addCleanup(self, callback, *args, **kwargs):  # noqa: N802
        self._cleanup_callbacks.append((callback, args, kwargs))

    def teardown_method(self):
        for callback, args, kwargs in reversed(self._cleanup_callbacks):
            callback(*args, **kwargs)
