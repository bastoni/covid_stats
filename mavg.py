#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :
# Copyright (C) 2020 Andrea Bastoni, License: Apache-2.0, see License file

import argparse
import sys
from load_istat import *
from load_dpc_cases import *
from load_area import *
from regione import *

## main ##
OFILE = {
        'avg_prov' : 'avg_province.json',
        'avg_reg'  : 'avg_regioni.json'
        }

IFILE = {
        'dpc_prov' : '../COVID-19/dati-json/dpc-covid19-ita-province.json',
        'prov': './tavola_bilancio_mensile_2019_province_tot.csv',
        'prov_area': '../Comuni-Italiani-2018-Sql-Json-excel/italy_provincies.json',
        'dpc_reg'  : '../COVID-19/dati-json/dpc-covid19-ita-regioni.json',
        'reg' : './tavola_bilancio_mensile_2019_regioni_tot.csv'
        }

AVG = 7
DBPROV = {}
DBREG = {}

lp = argparse.ArgumentParser(description="Moving average of DPC cases on Italian Province/Regioni")
lp.add_argument('--in-dpc-prov', help="Input DPC COVID 19 data per-provincia")
lp.add_argument('--in-prov', help="Input statistical data per-provincia")
lp.add_argument('--in-prov-area', help="Input statistical area per-provincia")
lp.add_argument('--out-prov', help="Output file per-provincia")
lp.add_argument('--in-dpc-reg', help="Input DPC COVID 19 data per-regione")
lp.add_argument('--in-reg', help="Input statistical data per-regione")
lp.add_argument('--out-reg', help="Output file per-region")
lp.add_argument('--wsize', help="Window size (default 7 days)")
lp.add_argument('--area', action="store_true", help="Compute moving average cases / provincia-area")
lp.add_argument('--verbose', action="store_true", help="Verbose: print stats max cases/7days avg")

args = lp.parse_args()

if args.in_dpc_prov is not None:
    IFILE['dpc_prov'] = args.in_dpc_prov
if args.in_prov is not None:
    IFILE['prov'] = args.in_prov
if args.in_prov_area is not None:
    IFILE['prov_area'] = args.in_prov_area
if args.out_prov is not None:
    OFILE['avg_prov'] = args.out_prov
if args.in_dpc_reg is not None:
    IFILE['dpc_reg'] = args.in_dpc_reg
if args.out_reg is not None:
    OFILE['avg_reg'] = args.out_reg
if args.wsize is not None:
    AVG = args.wsize

print('Infiles:\n%s' % ('\n'.join(str(k) + ' ' + str(v) for (k,v) in IFILE.items())))
print('Outfile:\n%s' % ('\n'.join(str(k) + ' ' + str(v) for (k,v) in OFILE.items())))

# prime Province DB with population data
DBPROV = load_istat_province(IFILE['prov'])
load_prov_case(IFILE['dpc_prov'], DBPROV)
if args.area:
    load_area(IFILE['prov_area'], DBPROV)

# Moving average for each provincia
provmax = []
for k,v in sorted(DBPROV.items()):
    _max = v.do_avg(AVG, args.area)
    provmax.append([k,_max])

if args.verbose:
    print("Max cases/7days * 100000 pop per-provincia")
    print(sorted(provmax, key=lambda x: x[1]))

with open(OFILE['avg_prov'], 'w') as f:
    f.write(json.dumps(DBPROV, indent=4, sort_keys=True, cls=ProvinciaENC))

# prime Regioni DB with population data
DBREG = load_istat_regioni(IFILE['reg'])
# add province autonome (mismatch ISTAT regioni/province and DPC)
r = Regione(DBPROV['BZ'].name, DBPROV['BZ'].pop)
DBREG[r.name] = r
r = Regione(DBPROV['TN'].name, DBPROV['RN'].pop)
DBREG[r.name] = r
# add cases
load_reg_case(IFILE['dpc_reg'], DBREG)

regmax = []
for k,v in sorted(DBREG.items()):
    _max = v.do_avg(AVG)
    regmax.append([k,_max])

if args.verbose:
    print("Max cases/7days * 100000 pop per-regione")
    print(sorted(regmax, key=lambda x: x[1]))

with open(OFILE['avg_reg'], 'w') as f:
    f.write(json.dumps(DBREG, indent=4, sort_keys=True, cls=RegioneENC))
