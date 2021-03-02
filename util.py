import timeit


class codeTimer:
    def __init__(self, name=None, iters=None):
        self.name = " '"  + name + "'" if name else ''
        self.iters = iters if iters else 1

    def __enter__(self):
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_value, traceback):
        self.took = (timeit.default_timer() - self.start) * 1000.0
        if self.took > 5000:
            self.took = self.took/1000
            code = ' s'
        else:
            code = ' ms'
        print('Code block' + self.name + ' took: ' + str(self.took/self.iters) + code)


def pairs(seq):
    i = iter(seq)
    prev = next(i)
    for item in i:
        yield [prev, item]
        prev = item
