# vim: set fileencoding=utf-8 :
import json
from collections import deque

class ProvinciaENC(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Provincia):
            return o.json_enc()
        return json.JSONEncoder.default(self, o)

class Provincia(object):
    def __init__(self, code, pop, name):
        self.code = code
        self.pop = int(pop)
        self.name = name
        self.case_by_date = {} # { date : cases }
        self.avg_pop = {}  # { interval : (avg, max cases) }
        self.area = 0
        self.avg_area = {} # { interval : avg }

    def add_case(self, date, num):
        self.case_by_date[date] = num

    def add_area(self, area):
        self.area = float(area)

    def __str__(self):

        s = "[%s, pop: %d, (" % (self.name, self.pop)
        el = ''.join(" %s: %s;" % (d,n) for d,n in sorted(self.case_by_date.items()))
        return s + el + ')]'

    def json_enc(self):
        d = {}
        d['code'] = self.code
        d['pop'] = self.pop
        d['name'] = self.name
        avg_pop = {}
        for k,v in sorted(self.avg_pop.items()):
            avg_pop[k] = v
        d['avg_pop'] = avg_pop
        if self.avg_area is not {}:
            d['area'] = self.area
            aa = {}
            for k,v in sorted(self.avg_area.items()):
                aa[k] = v
            d['avg_area'] = aa
        return d

    def do_avg(self, avg, area):
        win = deque([])
        prmax = float(0)
        for d,c in sorted(self.case_by_date.items()):
            if len(win) < avg:
                win.append([d,c])
            else:
                rg = "%s - %s" % (win[0][0], win[-1][0])
                # Use maximum and minimum seen values in the interval
                # the data for some province is highly unstable.
                l = min(win, key=lambda x: int(x[1]))[1]
                m = max(win, key=lambda x: int(x[1]))[1]
                avg_win = float(int(m) - int(l))/avg
                cur = float(avg_win / self.pop) * 100000
                if (cur > prmax):
                    prmax = cur
                self.avg_pop[rg] = (cur, m)
                if area:
                    cur_a = float(avg_win / self.area)
                    self.avg_area[rg] = cur_a
                # print("%s: %s : %s %s %s" % (self.code, rg, avg_win, self.pop, self.avg_pop[rg]))
                l = win.popleft()
                win.append([d,c])

        if len(win) < avg:
            print("Not enough data for avg of " + avg + " elements")
        else:
            # last element
            rg = "%s - %s" % (win[0][0], win[-1][0])
            l = min(win, key=lambda x: int(x[1]))[1]
            m = max(win, key=lambda x: int(x[1]))[1]
            avg_win = float(int(m) - int(l))/avg
            cur = float(avg_win / self.pop) * 100000
            if (cur > prmax):
                prmax = cur
            self.avg_pop[rg] = (cur, m)
            if area:
                cur_a = float(avg_win / self.area)
                self.avg_area[rg] = cur_a

        return prmax
