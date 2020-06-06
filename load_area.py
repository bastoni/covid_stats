# vim: set fileencoding=utf-8 :
# Copyright (C) 2020 Andrea Bastoni, License: Apache-2.0, see License file
from provincia import *

# Comuni-Italiani-2018-Sql-Json-excel/italy_provincies.json
# [
# 	{
# 		"sigla": "CH",
# 		"provincia": "Chieti",
# 		"superficie": "2588.35",
# 		"residenti": "389053",
# 		"num_comuni": "104",
# 		"id_regione": "1"
# 	},
def load_area(infile, db):
    with open(infile, 'r') as f:
        prov = json.load(f)

    for p in prov:
        if (p['sigla'] != "") and (p['sigla'] != "Total"):
            try:
                pr = db[p['sigla']]
                pr.add_area(p['superficie'])
            except:
                print(p['sigla'] + ' not found', file=sys.stderr)
