# vim: set fileencoding=utf-8 :
from provincia import *
from regione import *

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
def load_prov_case(infile, db):
    with open(infile, 'r') as f:
        dpc = json.load(f)

    for p in dpc:
        try:
            pr = db[p['sigla_provincia']]
            pr.add_case(p['data'], p['totale_casi'])
        except:
            # print(p['sigla_provincia'] + ' not found', file=sys.stderr)
            if (p['sigla_provincia'] != ""):
                quit()

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
def load_reg_case(infile, db):
    with open(infile, 'r') as f:
        dpc = json.load(f)

    for r in dpc:
        try:
            reg = db[r['denominazione_regione']]
            reg.add_case(r['data'], r['totale_casi'])
        except:
            if (MAP_REG[r['denominazione_regione']] != ""):
                reg = db[MAP_REG[r['denominazione_regione']]]
                reg.add_case(r['data'], r['totale_casi'])
            else:
                print("Error parsing regione " + r['denominazione_regione'])
                quit()