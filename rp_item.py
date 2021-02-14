# vim: set fileencoding=utf-8 :
# Copyright (C) 2021 Andrea Bastoni, License: Apache-2.0, see License file
import json
from collections import deque
from datetime import datetime, timedelta

class RPItemENC(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, RPItem):
            return o.json_enc()
        return json.JSONEncoder.default(self, o)

# regione / provincia object item
# S: total cases (day)
# N: new cases (day)
# sum_W: sum of N in the last W days (absolute)
# avg_N: average of the new cases in the last W days
#     For S, N, avg_N, each element's position is ('date', value)
#     since values are produced on a daily basis, each element in the
#     lists encodes one day.
# reff: reproduction index in the last W days
#     reff(t) = avg_N(t) / avg_N(t-W)
# exp: expected day
#     exp_t = sum(day * N(t)) / total

class RPItem(object):
    def __init__(self, code, name, pop, area):
        self.code = int(code)
        self.name = name
        self.pop = int(pop)
        self.area = float(area)
        self.S = [] # total cases (day) (sum)
        self.N = [] # new cases (day)
        self.sum_W = [] # absolute sum of new cases in last W days
        self.avg_N = [] # avg new cases (day-range)
        self.reff = [] # reproducion index over W days
        self.exp = () # (now, expected day date, expected day)

    def __str__(self):
        s = "[%s, pop: %d, area: %f,\n ->(" % (self.name, self.pop, self.area)
        el = ''.join(" %s: %s;" % (d,n) for d,n in sorted(self.S))
        el1 = ''.join(" %s: %s;" % (d,n) for d,n in sorted(self.N))
        el2 = ''.join(" %s: %s;" % (d,n) for d,n in sorted(self.avg_N))
        return s + el + ')\n' + '->(' + el1 + ')\n' + '->(' + el2 + ')\n]'

    def json_enc(self):
        d = {}
        d['code'] = self.code
        d['name'] = self.name
        d['exp'] = self.exp
        stat = {}
        for (t,x) in sorted(self.S):
            stat[t] = {}
            stat[t]['tot'] = x
        for (t,x) in sorted(self.avg_N):
            stat[t]['avg_N'] = x
        for (t,x) in sorted(self.sum_W):
            stat[t]['lastW_pop'] = float(x / self.pop) * 100000
            stat[t]['lastW_area'] = float(x / self.area)
        for (t,x) in sorted(self.reff):
            stat[t]['reff'] = x
        d['stat'] = stat
        return d

    def last(self):
        d = {}
        d['code'] = self.code
        d['name'] = self.name
        d['exp'] = self.exp
        stat = {}
        (t, x) = self.S[-1]
        stat[t] = {}
        stat[t]['tot'] = x
        (t, x) = self.avg_N[-1]
        stat[t]['avg_N'] = x
        (t, x) = self.sum_W[-1]
        stat[t]['lastW_pop'] = float(x / self.pop) * 100000
        stat[t]['lastW_area'] = float(x / self.area)
        (t, x) = self.reff[-1]
        stat[t]['reff'] = x
        d['stat'] = stat
        return d

    def add_case(self, date, total):
        if (len(self.S) > 0):
            (_, p) = self.S[-1]
        else:
            p = 0

        tot = int(total)
        self.S.append((date, tot))

        # total should be non-decreasing, but data is not precise
        new = tot - p
        if new < 0:
            new = 0
        self.N.append((date, new))

    def _avg(self, win, W):
        wl = [e for (_, e) in win]
        m = float(sum(wl) / W)
        (d, _) = win[-1]
        return (d, m)

    def _sum(self, win, W):
        wl = [e for (_, e) in win]
        m = sum(wl)
        (d, _) = win[-1]
        return (d, m)

    def _reff(self, win, W):
        (d, rt) = win[-1]
        (_, ri) = win[0]
        if ri > 0:
            reff = float(rt/ri)
        else:
            reff = -1
        return (d, reff)

    def _expd(self, wsum):
        (now, tot) = self.S[-1]
        (begin, _) = self.S[0]
        expf = float(wsum / tot)
        # When is the expected day from the beginning
        b = datetime.fromisoformat(begin)
        n = datetime.fromisoformat(now)
        d = timedelta(days=int(expf))
        expd = b + d
        diff = expd - n
        return (expf, expd.isoformat(), diff.days)

    def stat(self, W):
        win = deque([])
        exp = 0
        for n in self.N:
            # weighted sum expected value
            (_, c) = n
            exp = exp + (self.N.index(n) * c)
            # windows-based statistics
            if len(win) < W:
                win.append(n)
            else:
                self.avg_N.append(self._avg(win, W))
                self.sum_W.append(self._sum(win, W))
                # update
                win.popleft()
                win.append(n)
        # last element
        self.avg_N.append(self._avg(win, W))
        self.sum_W.append(self._sum(win, W))

        # expexted value day
        self.exp = self._expd(exp)

        # reff
        win = deque([])
        for n in self.avg_N:
            if len(win) < W:
                win.append(n)
            else:
                self.reff.append(self._reff(win, W))
                # update
                win.popleft()
                win.append(n)
        # last element
        self.reff.append(self._reff(win, W))
