"""Recherche dans l'index fourni, sans modification de la base source.
Usage : python MEMOIRE/rechercher_modeles.py "presa carico" --limite 10
"""
from pathlib import Path
import argparse,sqlite3,json
ROOT=Path(__file__).resolve().parent.parent
def chemin_local(old):
 parts=old.replace('\\','/').split('/serv/',1)
 return ROOT/'serv'/parts[-1] if len(parts)==2 else Path(old)
def rechercher(query,limite=10):
 con=sqlite3.connect((ROOT/'INDEX/index_modeles.db').as_uri()+'?mode=ro',uri=True)
 words=query.split();fts=' AND '.join('"'+w.replace('"','""')+'"' for w in words)
 rows=con.execute('SELECT d.nom,d.chemin,d.titre,d.texte,bm25(recherche_modeles) FROM recherche_modeles JOIN documents d ON d.chemin=recherche_modeles.chemin WHERE recherche_modeles MATCH ? AND d.extension IN (\'.doc\',\'.docx\') ORDER BY bm25(recherche_modeles) LIMIT 1000',(fts,)).fetchall()
 found=[]
 for nom,old,titre,texte,score in rows:
  p=chemin_local(old)
  if p.exists():found.append(dict(nom=nom,chemin=str(p),titre=titre,score=score,extrait=texte[:400]))
 con.close();return found[:limite]
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('recherche');parser.add_argument('--limite',type=int,default=10)
 a=parser.parse_args();print(json.dumps(rechercher(a.recherche,a.limite),ensure_ascii=False,indent=2))
