# vim: set fileencoding=utf-8 :
# Copyright (C) 2021 Andrea Bastoni, License: Apache-2.0, see License file

# regione / provincia object item
# S: total cases (day)
# N: new cases (day)
# avg_N: average of the new cases in the last W days
#     For S, N, avg_N, each element's position is ('date', value)
#     since values are produced on a daily basis, each element in the
#     lists encodes one day.

# CSV reader (from consolidated data)

class RPItem(object):
    def __init__(self, code, name, pop, area):
        self.code = code
        self.name = name
        self.pop = int(pop)
        self.area = float(area)
        self.S = [] # total cases (day) (sum)
        self.N = [] # new cases (day)
        self.avg_N = [] # avg new cases (day-range)

    def __str__(self):
        s = "[%s, pop: %d, area: %f, (" % (self.name, self.pop, self.area)
        el = ''.join(" %s: %s;" % (d,n) for d,n in sorted(self.S))
        return s + el + ')]'


    def add_case(self, date, total):
        self.S.append((date, int(total)))
        (_, p) = self.S[-1]
        if p != 0:
            self.N.append((date, int(total) - p))
        else:
            self.N.append((date, 0))

    def _avg(self, win, W):
        wl = [e for (_, e) in win]
        m = float(sum(wl) / W)
        (d, _) = win[-1]
        return (d, m)

    def avgN(self, W):
        win = deque([])
        for n in self.N:
            if len(win) < W:
                win.append(n)
            else:
                self.avg_N.append(self._avg(win, W))
                # update
                win.popleft()
                win.append(n)

        # last element
        self.avg_N.append(self._avg(win, W))


