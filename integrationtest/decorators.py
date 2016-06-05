from functools import wraps


def try_or_add_failure(failure_fn=None):

    def wrapped(fn):

        @wraps(fn)
        def _callable(ctxt, *a, **kw):
            try:
                return fn(ctxt, *a, **kw)
            except (ctxt.failureException, Exception) as e:
                setattr(ctxt.__class__, '_failures', getattr(
                    ctxt.__class__, '_failures', set()
                ) | {failure_fn or fn.__name__})
                raise e

        return _callable

    return wrapped


def depends_on(*fns):
    fns = set(fns)

    def wrapped(fn):
        setattr(fn, 'dependencies', fns)

        @wraps(fn)
        def _callable(ctxt, *a, **kw):
            if fns & getattr(ctxt.__class__, '_failures', set()):
                ctxt.skipTest('Because a dependency failed')

            return fn(ctxt, *a, **kw)
        return _callable

    return wrapped
