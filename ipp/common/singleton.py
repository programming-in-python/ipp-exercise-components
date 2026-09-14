##
# MIT License
#
# Copyright (c) 2020 - 2025 Andrew D. King
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
Provide the Singleton metaclass used across the course code.
"""

import threading


class Singleton(type):
    """
    Metaclass for classes that must exist as a single shared instance.
    """

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """
        Return the existing instance for ``cls``, creating it on first use.

        The lock makes first-use construction safe when several threads race
        to create the instance at once: without it, two threads could both
        find no instance and each build one, defeating the singleton.
        """
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)

            return cls._instances[cls]

    def clear_instance(cls):
        """
        Evict the cached instance so the next construction rebuilds it.

        This exists so tests can reset shared singletons between cases, but
        it is a live operation with real side effects, so understand them
        before calling it outside a test.

        A singleton is meant to be the one shared instance for the life of
        the process, and callers hold references to it. Clearing the cache
        does not touch those existing references: they keep pointing at the
        old instance, still holding its old state. The next construction of
        ``cls`` then builds a brand-new instance with freshly loaded state,
        so after a clear the process can hold two live instances at once,
        the detached old one and the new one, which are no longer the same
        object and no longer share state. For ``ConfigUtil`` that means code
        still holding the pre-clear instance keeps reading the pre-clear
        configuration, while code constructed after the clear reads the new
        one. This is safe precisely because each instance's backing state is
        written once at construction and only read thereafter; clearing swaps
        which instance new callers receive rather than mutating a live one.

        The lock guards the eviction against a concurrent construction, but
        it cannot make an in-flight reconfiguration atomic across the many
        callers that may already hold the old instance. Reserve this for
        controlled moments, chiefly test setup and teardown, not for
        reconfiguring a running application.
        """
        with cls._lock:
            cls._instances.pop(cls, None)
