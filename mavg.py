#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :
# Copyright (C) 2020 Andrea Bastoni, License: Apache-2.0, see License file

import argparse
import sys
from load_data import *
from load_dpc_cases import *
from rp_item import *

## main ##
OFILE = {
        'provincia' : 'avg_province.json',
        'regione'   : 'avg_regioni.json'
        }

IFILE = {
        'dpc_provincia' : '../COVID-19/dati-json/dpc-covid19-ita-province.json',
        'provincia': './data/province.csv',
        'dpc_regione'  : '../COVID-19/dati-json/dpc-covid19-ita-regioni.json',
        'regione' : './data/regioni.csv'
        }

AVG = 7
DBPROV = {}
DBREG = {}

lp = argparse.ArgumentParser(description="Moving average of DPC cases on Italian Province/Regioni")
lp.add_argument('--in-dpc-prov', help="Input DPC COVID 19 data per-provincia")
lp.add_argument('--in-prov', help="Input statistical data per-provincia")
lp.add_argument('--out-prov', help="Output file per-provincia")
lp.add_argument('--in-dpc-reg', help="Input DPC COVID 19 data per-regione")
lp.add_argument('--in-reg', help="Input statistical data per-regione")
lp.add_argument('--out-reg', help="Output file per-region")
lp.add_argument('--wsize', help="Window size (default 7 days)")
lp.add_argument('--verbose', action="store_true", help="Verbose: Print most recent Wsize average")

args = lp.parse_args()

if args.in_dpc_prov is not None:
    IFILE['dpc_provincia'] = args.in_dpc_prov
if args.in_prov is not None:
    IFILE['provincia'] = args.in_prov
if args.out_prov is not None:
    OFILE['provincia'] = args.out_prov
if args.in_dpc_reg is not None:
    IFILE['dpc_regione'] = args.in_dpc_reg
if args.in_reg is not None:
    IFILE['regione'] = args.in_reg
if args.out_reg is not None:
    OFILE['regione'] = args.out_reg
if args.wsize is not None:
    AVG = int(args.wsize)

print('Infiles:\n%s' % ('\n'.join(str(k) + ' ' + str(v) for (k,v) in IFILE.items())))
print('Outfile:\n%s' % ('\n'.join(str(k) + ' ' + str(v) for (k,v) in OFILE.items())))

# interesting codes
codes = [23, 5, 6, 30, 21]

for tp in ['provincia', 'regione']:
    # prime DB with population data
    DB = load_data(IFILE[tp], tp)
    # load cases
    fname = 'dpc_' + tp
    load_case(IFILE[fname], DB, tp)
    for k,v in sorted(DB.items()):
        v.stat(AVG)
        if args.verbose:
            if k in codes:
                print(v.last())

    with open(OFILE[tp], 'w+') as f:
        f.write(json.dumps(DB, indent=4, sort_keys=True, cls=RPItemENC))
quit()
