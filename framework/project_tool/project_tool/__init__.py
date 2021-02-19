import os, re
from glob import glob


class Header:
    def __init__(self, path, basedir, require_pattern=None):
        self.path = path
        self.basedir = basedir
        self.headers = []
        self.require_pattern = require_pattern
        self.relevant = require_pattern is None

    def __repr__(self):
        return "{} ({})".format(self.path, self.basedir)

    def analyze(self, tool):
        cpp_code = open(os.path.join(self.basedir, self.path)).read()
        if self.require_pattern is not None:
            if re.search(self.require_pattern, cpp_code, re.MULTILINE):
                self.relevant = True

        for m in re.finditer(
            r'^\s*#\s*include\s*(?:"([^"]+)"|<([^>]+)>)', cpp_code, re.MULTILINE
        ):
            try:
                if m.group(1) is not None:
                    self.headers.append(tool.lookup(m.group(1), self))
                elif m.group(2) is not None:
                    self.headers.append(tool.lookup(m.group(2), self))
            except:
                pass  # ok, file not requested for SWIG
        # print("HEADER {}".format(self.path))
        # for h in self.headers:
        #    print("  -- {}".format(h))


class SwigTool:
    def __init__(self, paths, require_pattern=None):
        self.paths = paths
        self.headers = []
        self.require_pattern = require_pattern

    def analyze(self):
        files = []
        for p in self.paths:
            # f = glob.glob(p,recursive=True)
            f1 = [os.path.relpath(x, p) for x in glob(p + "/**/*.h", recursive=True)]
            f2 = [os.path.relpath(x, p) for x in glob(p + "/**/*.hpp", recursive=True)]
            files += map(lambda a: (a, p), f1)
            files += map(lambda a: (a, p), f2)
        # print(files)
        for f in files:
            self.headers.append(Header(*f, self.require_pattern))
        for h in self.headers:
            h.analyze(self)

    def lookup(self, path, header=None):
        if header is not None:
            mypath = os.path.dirname(header.path)
            tmp = filter(
                lambda h: h.basedir == header.basedir and h.path.startswith(mypath),
                self.headers,
            )
            hit = list(filter(lambda h: h.path == os.path.join(mypath, path), tmp))
            if len(hit) > 0:
                return hit[0]

            tmp = filter(lambda h: h.basedir == header.basedir, self.headers)
            hit = list(filter(lambda h: h.path == path, tmp))
            if len(hit) > 0:
                return hit[0]

        hit = list(filter(lambda h: h.path == path, self.headers))
        if len(hit) > 0:
            return hit[0]
        raise Exception("error, {} not found from {}.", path, str(header))

    def get_sorted(self):
        result = []
        input = set(self.headers)
        while len(input) > 0:
            tmp = set(
                filter(
                    lambda h: len(set(filter(lambda i: i in input, h.headers))) == 0,
                    input,
                )
            )
            if len(tmp) == 0:
                raise Exception("detection circular dependency...")
            input = input - tmp
            result += tmp
        return result
