# vim: set fileencoding=utf-8 :
# Copyright (C) 2020 Andrea Bastoni, License: Apache-2.0, see License file
import json
from collections import deque

class RegioneENC(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Regione):
            return o.json_enc()
        return json.JSONEncoder.default(self, o)

class Regione(object):
    def __init__(self, name, pop):
        self.pop = int(pop)
        self.name = name
        self.case_by_date = {} # { date : (total cases, active cases) }
        self.avg_pop = {}  # { interval : (avg new cases x days /pop*100000, avg active cases x days/pop*100000, total cases/pop*100000, max cases) }

    def add_case(self, date, tot, active):
        self.case_by_date[date] = (tot, active)

    def __str__(self):

        s = "[%s, pop: %d, (" % (self.name, self.pop)
        el = ''.join(" %s: %s;" % (d,n) for d,n in sorted(self.case_by_date.items()))
        return s + el + ')]'

    def json_enc(self):
        d = {}
        d['pop'] = self.pop
        d['name'] = self.name
        avg_pop = {}
        for k,v in sorted(self.avg_pop.items()):
            avg_pop[k] = v
        d['avg_pop'] = avg_pop
        return d

    def _avg_win(self, win, mavg_a, wsize):
        rg = "%s - %s" % (win[0][0], win[-1][0])
        # For the total number of cases
        # use maximum and minimum seen values in the interval
        # the data for some province is highly unstable.
        (lt, _) = min(win, key=lambda x: x[1])[1]
        (mt, _) = max(win, key=lambda x: x[1])[1]
        # compute average of _new_ cases
        avg_win = float(int(mt) - int(lt))/wsize
        cur = float(avg_win / self.pop) * 100000
        # store the active cases of the current
        self.avg_pop[rg] = (cur, (mavg_a/self.pop * 100000), ((mt/self.pop) * 100000), mt)
        return cur

    def do_avg(self, wsize):
        win = deque([])
        prmax = float(0)
        mavg_active = float(0)
        for d,c in sorted(self.case_by_date.items()):
            if len(win) < wsize:
                (tot, active) = c
                mavg_active = (mavg_active + active/wsize)
                win.append([d,c])
            else:
                _max = self._avg_win(win, mavg_active, wsize)
                if (_max > prmax):
                    prmax = _max
                # for the active cases, we need proper moving average
                l = win.popleft()
                win.append([d,c])
                (_, na) = c
                (_, oa) = l[1]
                mavg_active = (mavg_active + na/wsize - oa/wsize)

        if len(win) < wsize:
            print(self.name + " not enough data for avg of " + str(wsize) + " elements")
        else:
            _max = self._avg_win(win, mavg_active, wsize)
            if (_max > prmax):
                prmax = _max

        # (maximum new cases, last active average)
        return (prmax, (mavg_active/self.pop * 100000))
