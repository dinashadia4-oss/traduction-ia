"""Journal append-only des corrections explicitement demandées.
Usage : python MEMOIRE/enregistrer_correction.py --demande "..." --portee "..." --ancien "..." --nouveau "..."
Ce script enregistre la correction ; il ne remplace pas la mise à jour du Word et son contrôle.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,uuid
p=argparse.ArgumentParser()
for key in ('demande','portee','ancien','nouveau'):p.add_argument('--'+key,required=True)
p.add_argument('--fichier');p.add_argument('--regle-generale',action='store_true')
a=p.parse_args()
record={'id':str(uuid.uuid4()),'date':datetime.now(timezone.utc).isoformat(),'demande_utilisateur':a.demande,'portee':a.portee,'ancien':a.ancien,'nouveau':a.nouveau,'fichier':a.fichier,'regle_generale':a.regle_generale,'statut':'demandée explicitement, application à vérifier'}
with Path(__file__).with_name('HISTORIQUE_MODIFICATIONS.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
print(record['id'])
