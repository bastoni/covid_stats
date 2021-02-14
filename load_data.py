# vim: set fileencoding=utf-8 :
# Copyright (C) 2020 Andrea Bastoni, License: Apache-2.0, see License file
import csv
import re
from rp_item import *
from provincia import *
from regione import *
from mapping import *

# length: how many bytes to sniff ahead to detect dialect type
def csv_reader(infile, mode, length):
    f = open(infile, mode, newline='')
    try:
        dialect = csv.Sniffer().sniff(f.read(length))
    except csv.Error as err:
        # print("ERR: Dialect: " + str(err))
        f.seek(0)
        # detection failed, best effort detection
        return (csv.reader(f, delimiter=','), f)

    f.seek(0)
    return (csv.reader(f, dialect), f)

def csv_close(f):
    f.close()

# ISTAT-based data
def load_istat_regioni(infile):
    reg_pop = {}
    (spam, f) = csv_reader(infile, 'r', 2048)
    anum = re.compile("^[0-9]")
    for s in spam:
        if anum.match(s[0]):
            r = Regione(MAP_REG[s[1]], s[2])
            reg_pop[r.name] = r
    csv_close(f)
    return reg_pop

def load_istat_province(infile):
    prov = {}
    (spam, f) = csv_reader(infile, 'r', 2048)
    anum = re.compile("^[0-9]")
    for s in spam:
        if anum.match(s[0]):
            p = Provincia(MAP_PROV[s[1]], s[2], s[1])
            prov[p.code] = p
    csv_close(f)
    return prov

# Load consolidated CSV data for regioni and province
def load_data(infile, type):
    d = {}
    anum = re.compile("^[0-9]")
    (spam, f) = csv_reader(infile, 'r', 2048)
    # Skip description lines
    anum = re.compile("^[0-9]")
    for s in spam:
        if anum.match(s[0]):
            # code, name, population, area
            if type is 'provincia':
                el = RPItem(s[0], s[1], s[3], s[4])
            else:
                el = RPItem(s[0], s[1], s[2], s[3])
            d[el.code] = el
    csv_close(f)
    return d

# test
#d = load_regioni('./data/regioni.csv')
#d = load_province('./data/province.csv')
#for el in d.values():
#    print(el)
#load_istat_province('./tavola_bilancio_mensile_2019_province_tot.csv')
#load_istat_regioni('./tavola_bilancio_mensile_2019_regioni_tot.csv')
