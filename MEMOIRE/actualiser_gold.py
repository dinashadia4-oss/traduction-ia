"""Classe les exemples et conserve un exemplaire de chaque modèle répété.
Les originaux serv et les livrables ne sont jamais modifiés.
"""
from pathlib import Path
import hashlib,shutil,json,csv,sqlite3,sys
from datetime import datetime,timezone
from collections import defaultdict
ROOT=Path(__file__).resolve().parent.parent
def sha(p):
 with p.open('rb') as f:
  h=hashlib.sha256()
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 gold=ROOT/'gold';gold.mkdir(exist_ok=True)
 groups=defaultdict(list)
 for p in ([] if '--exemples-seuls' in sys.argv else (ROOT/'serv').rglob('*')):
  if p.is_file() and p.suffix.lower() in ('.doc','.docx') and not p.name.startswith('~$'):
   groups[sha(p)].append(p)
 recurring=json.loads((gold/'INDEX_MODELES_RECURRENTS.json').read_text(encoding='utf8')) if '--exemples-seuls' in sys.argv else []
 for digest,paths in sorted(groups.items()):
  if len(paths)<2:continue
  preferred=min(paths,key=lambda p:(len(str(p)),str(p)))
  dest=gold/'modeles_recurrents'/digest[:12]/preferred.name
  dest.parent.mkdir(parents=True,exist_ok=True)
  if not dest.exists():shutil.copy2(preferred,dest)
  recurring.append(dict(sha256=digest,exemplaire=str(dest.relative_to(ROOT)),nombre_copies=len(paths),sources=[str(p.relative_to(ROOT)) for p in paths],statut='modèle fourni, répétition identique vérifiée'))
 (gold/'INDEX_MODELES_RECURRENTS.json').write_text(json.dumps(recurring,ensure_ascii=False,indent=2),encoding='utf8')
 with (gold/'INDEX_MODELES_RECURRENTS.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f,delimiter=';');w.writerow(['SHA256','Nombre de copies','Exemplaire gold','Sources identiques'])
  for x in recurring:w.writerow([x['sha256'],x['nombre_copies'],x['exemplaire'],' | '.join(x['sources'])])
 examples=[]
 for p in (ROOT/'WORD_TRADUITS').glob('*/*.docx'):
  dest=gold/'exemples_traduits'/p.parent.name/p.name
  dest.parent.mkdir(parents=True,exist_ok=True)
  if dest.exists() and sha(dest)!=sha(p):
   version=gold/'versions_exemples'/p.parent.name/p.stem/(datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')+'-'+sha(dest)[:10]+'.docx')
   version.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,version)
  shutil.copy2(p,dest)
  examples.append(dict(pdf=p.parent.name,word=str(p.relative_to(ROOT)),gold=str(dest.relative_to(ROOT)),sha256=sha(dest),statut='traduction de travail, validation utilisateur non reçue'))
 (gold/'INDEX_EXEMPLES.json').write_text(json.dumps(examples,ensure_ascii=False,indent=2),encoding='utf8')
 (gold/'LIRE_MOI.md').write_text('# Bibliothèque gold\n\nLes modèles répétés sont regroupés par empreinte SHA-256 : un original identique est conservé par groupe, sans supprimer les copies dans serv. Les variantes de contenu restent séparées. Les index indiquent toutes les provenances.\n\nLes traductions sont classées par PDF dans exemples_traduits. Leur présence dans gold ne signifie pas qu’elles ont été approuvées par vous. Vos corrections explicites seront enregistrées dans MEMOIRE/HISTORIQUE_MODIFICATIONS.jsonl et utilisées pour mettre à jour les règles et les exemples concernés.\n\nLa mémoire est locale à ce projet. AGENTS.md demande de la consulter lors des prochaines séances dans ce dossier.\n',encoding='utf8')
 print(json.dumps({'modeles_fournis':sum(map(len,groups.values())),'modeles_uniques':len(groups),'groupes_recurrents_gold':len(recurring),'exemples_traduits_gold':len(examples)},ensure_ascii=False))
if __name__=='__main__':main()
