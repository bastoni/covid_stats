# vim: set fileencoding=utf-8 :

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
def load_prov(infile):
    with open(infile, 'r') as f:
        prov = json.load(f)

    for p in prov:
        if (p['sigla'] != "") and (p['sigla'] != "Total"):
            pr = Provincia(p['sigla'], p['residenti'], p['superficie'], p['provincia'])
            DBPROV[pr.code] = pr
