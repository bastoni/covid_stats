# vim: set fileencoding=utf-8 :
# Copyright (C) 2020 Andrea Bastoni, License: Apache-2.0, see License file
from rp_item import *
import json
import sys

# COVID-19/dati-json/dpc-covid19-ita-province.json
#[
#    {
#        "data": "2020-02-24T18:00:00",
#        "stato": "ITA",
#        "codice_regione": 13,
#        "denominazione_regione": "Abruzzo",
#        "codice_provincia": 69,
#        "denominazione_provincia": "Chieti",
#        "sigla_provincia": "CH",
#        "lat": 42.35103167,
#        "long": 14.16754574,
#        "totale_casi": 0,
#        "note_it": "",
#        "note_en": ""
#    },

# COVID-19/dati-json/dpc-covid19-ita-regioni.json lines
# [
#     {
#         "data": "2020-02-24T18:00:00",
#         "stato": "ITA",
#         "codice_regione": 13,
#         "denominazione_regione": "Abruzzo",
#         "lat": 42.35122196,
#         "long": 13.39843823,
#         "ricoverati_con_sintomi": 0,
#         "terapia_intensiva": 0,
#         "totale_ospedalizzati": 0,
#         "isolamento_domiciliare": 0,
#         "totale_positivi": 0,
#         "variazione_totale_positivi": 0,
#         "nuovi_positivi": 0,
#         "dimessi_guariti": 0,
#         "deceduti": 0,
#         "totale_casi": 0,
#         "tamponi": 5,
#         "casi_testati": null,
#         "note_it": "",
#         "note_en": ""
#     },

MAP = {
        'provincia' : 'codice_provincia',
        'regione'   : 'codice_regione',
    }

def load_case(infile, db, type):
    with open(infile, 'r') as f:
        dpc = json.load(f)

    code = MAP[type]

    for p in dpc:
        try:
            pr = db[p[code]]
            pr.add_case(p['data'], p['totale_casi'])
        except:
            # print(str(p) + ' not found', file=sys.stderr)
            None

