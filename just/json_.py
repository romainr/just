import warnings
import gzip


def read(fn, warn=False):
    from preconvert.output import json

    if isinstance(fn, gzip.GzipFile):
        return json.load(fn)
    if fn.endswith(".jsonl"):
        if warn:
            warnings.warn("Reading streaming format at once.")
        return list(iread(fn))
    with open(fn) as f:
        return json.load(f)


def append(obj, fn):
    from preconvert.output import json

    if isinstance(fn, gzip.GzipFile):
        raise TypeError("Cannot append to gzip")
    with open(fn, "a+") as f:
        f.write(json.dumps(obj) + "\n")


def write(obj, fn):
    from preconvert.output import json

    if isinstance(fn, gzip.GzipFile):
        fn.write(bytes(json.dumps(obj), encoding="utf8"))
    else:
        with open(fn, "w") as f:
            json.dump(obj, f, indent=4)


def iread(fn):
    from preconvert.output import json

    if isinstance(fn, gzip.GzipFile):
        raise TypeError("Cannot iteratively read gzip")
    with open(fn) as f:
        for i, line in enumerate(f):
            try:
                yield json.loads(line)
            except StopIteration:
                raise
            except:
                msg = "JSON-L parsing error in line number {} in the jsonl file".format(i)
                raise Exception(msg, line)


def iwrite(obj, fn):
    from preconvert.output import json

    if isinstance(fn, gzip.GzipFile):
        raise TypeError("Cannot iteratively write gzip")
    with open(fn, "w") as f:
        for chunk in obj:
            f.write(json.dumps(chunk) + "\n")
