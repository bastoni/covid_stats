# vim: set fileencoding=utf-8 :
import csv
import re
from provincia import *
from regione import *

# mapping ISTAT province.code - province.name
# mapping ISTAT provincia Bolzano/Bozen and Trento to regioni P.A. Bolzano/Bozen, P.A. Trento

MAP_REG = {
        'Piemonte' : 'Piemonte',
        "Valle d'Aosta/Vallée d'Aoste" : "Valle d'Aosta",
        'Lombardia' : 'Lombardia',
        'Trentino-Alto Adige' : 'Trentino-Alto Adige',
        'Veneto' : 'Veneto',
        'Friuli-Venezia Giulia' : 'Friuli Venezia Giulia',
        'Liguria' : 'Liguria',
        'Emilia-Romagna' : 'Emilia-Romagna',
        'Toscana' : 'Toscana',
        'Umbria' : 'Umbria',
        'Marche' : 'Marche',
        'Lazio' : 'Lazio',
        'Abruzzo' : 'Abruzzo',
        'Molise' : 'Molise',
        'Campania' : 'Campania',
        'Puglia' : 'Puglia',
        'Basilicata': 'Basilicata',
        'Calabria' : 'Calabria',
        'Sicilia' : 'Sicilia',
        'Sardegna' :'Sardegna',
        "P.A. Bolzano" : "Bolzano/Bozen",
        "P.A. Trento" : "Trento",
        }

MAP_PROV = {
        "Chieti" : "CH",
        "L'Aquila" : "AQ",
        "Pescara" : "PE",
        "Teramo" : "TE",
        "Matera" : "MT",
        "Potenza" : "PZ",
        "Bolzano" : "BZ",
        "Bolzano/Bozen" : "BZ",
        "Catanzaro" : "CZ",
        "Cosenza" : "CS",
        "Crotone" : "KR",
        "Reggio di Calabria" : "RC",
        "Vibo Valentia" : "VV",
        "Avellino" : "AV",
        "Benevento" : "BN",
        "Caserta" : "CE",
        "Napoli" : "NA",
        "Salerno" : "SA",
        "Bologna" : "BO",
        "Ferrara" : "FE",
        "Forlì-Cesena" : "FC",
        "Modena" : "MO",
        "Parma" : "PR",
        "Piacenza" : "PC",
        "Ravenna" : "RA",
        "Reggio nell'Emilia" : "RE",
        "Rimini" : "RN",
        "Gorizia" : "GO",
        "Pordenone" : "PN",
        "Trieste" : "TS",
        "Udine" : "UD",
        "Frosinone" : "FR",
        "Latina" : "LT",
        "Rieti" : "RI",
        "Roma" : "RM",
        "Viterbo" : "VT",
        "Genova" : "GE",
        "Imperia" : "IM",
        "La Spezia" : "SP",
        "Savona" : "SV",
        "Bergamo" : "BG",
        "Brescia" : "BS",
        "Como" : "CO",
        "Cremona" : "CR",
        "Lecco" : "LC",
        "Lodi" : "LO",
        "Mantova" : "MN",
        "Milano" : "MI",
        "Monza e della Brianza" : "MB",
        "Pavia" : "PV",
        "Sondrio" : "SO",
        "Varese" : "VA",
        "Ancona" : "AN",
        "Ascoli Piceno" : "AP",
        "Fermo" : "FM",
        "Macerata" : "MC",
        "Pesaro e Urbino" : "PU",
        "Campobasso" : "CB",
        "Isernia" : "IS",
        "Alessandria" : "AL",
        "Asti" : "AT",
        "Biella" : "BI",
        "Cuneo" : "CN",
        "Novara" : "NO",
        "Torino" : "TO",
        "Verbano-Cusio-Ossola" : "VB",
        "Vercelli" : "VC",
        "Bari" : "BA",
        "Barletta-Andria-Trani" : "BT",
        "Brindisi" : "BR",
        "Foggia" : "FG",
        "Lecce" : "LE",
        "Taranto" : "TA",
        "Cagliari" : "CA",
        "Nuoro" : "NU",
        "Oristano" : "OR",
        "Sassari" : "SS",
        "Sud Sardegna" : "SU",
        "Agrigento" : "AG",
        "Caltanissetta" : "CL",
        "Catania" : "CT",
        "Enna" : "EN",
        "Messina" : "ME",
        "Palermo" : "PA",
        "Ragusa" : "RG",
        "Siracusa" : "SR",
        "Trapani" : "TP",
        "Arezzo" : "AR",
        "Firenze" : "FI",
        "Grosseto" : "GR",
        "Livorno" : "LI",
        "Lucca" : "LU",
        "Massa Carrara" : "MS",
        "Massa-Carrara" : "MS",
        "Pisa" : "PI",
        "Pistoia" : "PT",
        "Prato" : "PO",
        "Siena" : "SI",
        "Trento" : "TN",
        "Perugia" : "PG",
        "Terni" : "TR",
        "Valle d'Aosta/Vallée d'Aoste" : "AO",
        "Aosta" : "AO",
        "Belluno" : "BL",
        "Padova" : "PD",
        "Rovigo" : "RO",
        "Treviso" : "TV",
        "Venezia" : "VE",
        "Verona" : "VR",
        "Vicenza" : "VI"
        }

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


# test
#load_istat_province('./tavola_bilancio_mensile_2019_province_tot.csv')
#load_istat_regioni('./tavola_bilancio_mensile_2019_regioni_tot.csv')
