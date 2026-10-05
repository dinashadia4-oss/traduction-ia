#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Catalogue rapide des modèles italiens.
Méthode : lecture partielle, pas d'OCR massif, reprise possible.
"""

import os
import sys
import csv
import re
import time
from pathlib import Path
from datetime import datetime

# Extensions ciblées
EXT_CIBLE = {'.pdf', '.docx', '.doc', '.jpg', '.jpeg', '.png'}

# Fichiers/patterns à ignorer
IGNORE_PATTERNS = [
    r'~\$',
    r'Thumbs\.db',
    r'\.DS_Store',
    r'__pycache__',
    r'\.tmp$',
    r'\.temp$',
    r'\.cache',
    r'\.crdownload',
    r'\.part$',
]

# Chemin du catalogue
BASE_DIR = Path(r'C:\Users\hatta\Desktop\serv')
CSV_PATH = BASE_DIR / 'CATALOGUE_MODELES.csv'
PROGRESS_PATH = BASE_DIR / 'CATALOGUE_MODELES.progress.json'

# En-têtes CSV
HEADERS = [
    'nom_fichier',
    'chemin_complet',
    'nom_dossier',
    'extension',
    'taille_octets',
    'date_modification',
    'nb_pages',
    'titre_italien',
    'type_document',
    'sous_titres',
    'autorite_emettrice',
    'noms_signataires',
    'fonctions_signataires',
    'expressions_italiennes',
    'apostille',
    'tableau',
    'cadre',
    'etat_document',
    'date_analyse',
]

# Mots-clés de classification
CLASSIF_KEYWORDS = [
    (r'\b(estratto\s+dell?[\']?\s*atto\s+di\s+nascita|atto\s+di\s+nascita|nascita)\b', "Estratto dell'atto di nascita"),
    (r'\b(estratto\s+dell?[\']?\s*atto\s+di\s+matrimonio|atto\s+di\s+matrimonio|matrimonio)\b', "Estratto dell'atto di matrimonio"),
    (r'\b(estratto\s+dell?[\']?\s*atto\s+di\s+morte|atto\s+di\s+morte|morte|decesso)\b', "Estratto dell'atto di morte"),
    (r'\b(certificato\s+di\s+residenza|residenza)\b', "Certificato di residenza"),
    (r'\b(attestazione\s+di\s+stipendio|stipendio|busta\s+paga)\b', "Attestazione di stipendio"),
    (r'\b(attestazione\s+di\s+reddito|reddito)\b', "Attestazione di reddito"),
    (r'\b(di\s*ploma|diploma\s+di\s+maturità|laurea|titolo\s+di\s+studio)\b', "Diploma"),
    (r'\b(certificato\s+degli\s+esami|esami\s+sostenuti|programma\s+degli\s+esami)\b', "Certificato degli esami"),
    (r'\b(sentenza|tribunale|giudice|corte\s+d[\']?appello)\b', "Sentenza"),
    (r'\b(procura\s+speciale|procura|mandato|power\s+of\s+attorney)\b', "Procura"),
    (r'\b(casellario\s+giudiziale|certificato\s+penale|fedina\s+penale)\b', "Casellario giudiziale"),
    (r'\b(apostill[ae]|hague\s+convention)\b', "Apostille"),
    (r'\b(certificato\s+anagrafico|anagrafe|stato\s+civile|certificato\s+amministrativo)\b', "Certificato amministrativo"),
    (r'\b(attestazione\s+di\s+lavoro|contratto\s+di\s+lavoro|dichiarazione\s+di\s+lavoro)\b', "Attestazione di lavoro"),
]

AUTORITA_KEYWORDS = [
    (r'\b(Comune\s+di\s+[A-Z][a-zàèéìòù]+)', 'Comune'),
    (r'\b(Prefettura\s+-?\s*[A-Z][a-zàèéìòù]+)', 'Prefettura'),
    (r'\b(Tribunale\s+di\s+[A-Z][a-zàèéìòù]+)', 'Tribunale'),
    (r'\b(Ufficio\s+[A-Z][a-zàèéìòù]+)', 'Ufficio'),
    (r'\b(Agenzia\s+delle\s+[A-Z][a-zàèéìòù]+)', 'Agenzia'),
    (r'\b(Regione\s+[A-Z][a-zàèéìòù]+)', 'Regione'),
    (r'\b(Consolato\s+[A-Za-z\s]+)', 'Consolato'),
    (r'\b(Ministero\s+della?\s+[A-Za-z\s]+)', 'Ministero'),
    (r'\b(Istituto\s+[A-Za-z\s]+)', 'Istituto'),
    (r'\b(Scuola\s+[A-Za-z\s]+)', 'Scuola'),
    (r'\b(Università\s+[A-Za-z\s]+)', 'Università'),
]

SIGNATAIRE_PATTERNS = [
    (r'\b(Il\s+Sindaco\s+[A-Z][A-Z\s]+)', 'Il Sindaco'),
    (r'\b(Il\s+Dirigente\s+[A-Z][A-Z\s]+)', 'Il Dirigente'),
    (r'\b(Il\s+Responsabile\s+[A-Z][A-Z\s]+)', 'Il Responsabile'),
    (r'\b(Il\s+Commissario\s+[A-Z][A-Z\s]+)', 'Il Commissario'),
    (r'\b(Il\s+Funzionario\s+[A-Z][A-Z\s]+)', 'Il Funzionario'),
    (r'\b(L[\']?Assessore\s+[A-Z][A-Z\s]+)', "L'Assessore"),
    (r'\b(Il\s+Presidente\s+[A-Z][A-Z\s]+)', 'Il Presidente'),
    (r'\b(Il\s+Segretario\s+[A-Z][A-Z\s]+)', 'Il Segretario'),
    (r'\b(L[\']?Ufficiale\s+[A-Z][A-Z\s]+)', "L'Ufficiale"),
    (r'\b(Il\s+Notaio\s+[A-Z][A-Z\s]+)', 'Il Notaio'),
    (r'\b(Il\s+Giudice\s+[A-Z][A-Z\s]+)', 'Il Giudice'),
    (r'\b(L[\']?Avvocato\s+[A-Z][A-Z\s]+)', "L'Avvocato"),
]


def should_ignore(filename):
    for pat in IGNORE_PATTERNS:
        if re.search(pat, filename, re.IGNORECASE):
            return True
    return False


def load_progress():
    """Charge les fichiers déjà catalogués : dict chemin -> (taille, mtime)"""
    processed = {}
    if CSV_PATH.exists():
        try:
            with open(CSV_PATH, 'r', encoding='utf-8-sig', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    chemin = row.get('chemin_complet', '').strip()
                    if chemin:
                        try:
                            taille = int(row.get('taille_octets', 0))
                            mtime = row.get('date_modification', '')
                            processed[chemin] = (taille, mtime)
                        except ValueError:
                            processed[chemin] = (0, '')
        except Exception as e:
            print(f"[!] Erreur lecture CSV existant: {e}")
    return processed


def init_csv():
    if not CSV_PATH.exists():
        with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(HEADERS)
        print(f"[+] CSV créé : {CSV_PATH}")
    else:
        print(f"[*] CSV existant trouvé : {CSV_PATH}")


def safe_text(text):
    if not text:
        return ''
    # Normaliser les espaces et retours chariot
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def detect_type_document(text, filename, folder_name):
    combined = f"{filename} {folder_name} {text}".lower()
    for pattern, label in CLASSIF_KEYWORDS:
        if re.search(pattern, combined, re.IGNORECASE):
            return label
    return "Autre"


def detect_autorite(text):
    if not text:
        return ''
    found = []
    for pattern, prefix in AUTORITA_KEYWORDS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            found.append(m.strip())
    return ' | '.join(list(dict.fromkeys(found))[:3])


def detect_signataires(text):
    if not text:
        return '', ''
    noms = []
    fonctions = []
    for pattern, fonction in SIGNATAIRE_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            noms.append(m.strip())
            fonctions.append(fonction)
    return ' | '.join(list(dict.fromkeys(noms))[:3]), ' | '.join(list(dict.fromkeys(fonctions))[:3])


def detect_expressions_italiennes(text):
    if not text:
        return ''
    # Expressions typiques de documents administratifs italiens
    expressions = []
    patterns = [
        r'\b(certifico\s+che)\b',
        r'\b(sotto\s+scritto)\b',
        r'\b(presso\s+l[\']?ufficio)\b',
        r'\b(ai\s+sensi\s+della\s+legge)\b',
        r'\b(in\s+qualità\s+di)\b',
        r'\b(dichiara\s+che)\b',
        r'\b(atti\s+dello\s+stato\s+civile)\b',
        r'\b(registro\s+degli\s+atti)\b',
        r'\b(parte\s+[I1V]+)\b',
        r'\b(serie\s+[A-Z])\b',
        r'\b(numero\s+d\s+ordine)\b',
        r'\b(annotazione\s+marginali)\b',
        r'\b(in\s+data)\b',
        r'\b(in\s+fede)\b',
        r'\b(presso\s+il\s+comune\s+di)\b',
        r'\b(a\s+richiesta\s+di)\b',
        r'\b(visto\s+il\s+decreto)\b',
        r'\b(visto\s+il\s+testo\s+unico)\b',
        r'\b(visto\s+il\s+regolamento)\b',
    ]
    for pat in patterns:
        matches = re.findall(pat, text, re.IGNORECASE)
        expressions.extend(matches)
    return ' | '.join(list(dict.fromkeys(expressions))[:8])


def detect_apostille(text, filename):
    combined = f"{filename} {text}".lower()
    if re.search(r'\b(apostill[ae]|hague\s+convention|apostilla)\b', combined, re.IGNORECASE):
        return 'OUI'
    return 'NON'


def detect_tableau_docx(doc):
    try:
        return 'OUI' if len(doc.tables) > 0 else 'NON'
    except Exception:
        return 'NON'


def detect_cadre(text):
    # Détection simplifiée : présence de mots liés à des cadres légaux
    if text and re.search(r'\b(visto|considerato|decreto|legge|regolamento|art\.?\s*\d+)\b', text, re.IGNORECASE):
        return 'PROBABLE'
    return 'NON'


# ============================================================
# EXTRACTEURS PAR TYPE DE FICHIER
# ============================================================

def extract_pdf_info(path):
    """Extrait infos d'un PDF : nb_pages, texte page 1, texte dernière page."""
    try:
        import PyPDF2
    except ImportError:
        return {'nb_pages': '?', 'texte': '', 'etat': 'ERREUR_IMPORT'}

    result = {'nb_pages': '?', 'texte': '', 'etat': 'TEXTE_LISIBLE'}
    try:
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            nb = len(reader.pages)
            result['nb_pages'] = str(nb)

            # Page 1
            page1_text = ''
            if nb > 0:
                try:
                    page1_text = reader.pages[0].extract_text() or ''
                except Exception:
                    page1_text = ''

            # Dernière page (signatures ?)
            last_text = ''
            if nb > 1:
                try:
                    last_text = reader.pages[-1].extract_text() or ''
                except Exception:
                    last_text = ''

            combined = page1_text + '\n' + last_text
            result['texte'] = combined

            # Si aucun texte extrait -> probablement scanné
            if not combined.strip():
                result['etat'] = 'OCR_NECESSAIRE'
            else:
                # Vérifier si c'est majoritairement du texte ou des caractères bizarres
                printable = sum(1 for c in combined if c.isprintable() or c.isspace())
                if len(combined) > 0 and printable / len(combined) < 0.7:
                    result['etat'] = 'OCR_NECESSAIRE'

    except Exception as e:
        result['etat'] = f'ERREUR_LECTURE: {str(e)[:50]}'

    return result


def extract_docx_info(path):
    """Extrait infos d'un DOCX."""
    try:
        from docx import Document
    except ImportError:
        return {'nb_pages': '?', 'texte': '', 'tableau': 'NON', 'etat': 'ERREUR_IMPORT'}

    result = {'nb_pages': '?', 'texte': '', 'tableau': 'NON', 'etat': 'TEXTE_LISIBLE'}
    try:
        doc = Document(path)

        # Texte des premiers paragraphes (~première page)
        paras = [p.text for p in doc.paragraphs if p.text.strip()]
        # Texte des derniers paragraphes (~signatures)
        debut = paras[:30]
        fin = paras[-15:] if len(paras) > 15 else []
        combined = '\n'.join(debut + ['---FIN---'] + fin)
        result['texte'] = combined
        result['tableau'] = detect_tableau_docx(doc)

        if not combined.strip():
            result['etat'] = 'OCR_NECESSAIRE'

    except Exception as e:
        result['etat'] = f'ERREUR_LECTURE: {str(e)[:50]}'

    return result


def extract_doc_info(path):
    """Extrait infos d'un DOC ancien (Word 97-2003). Essai de lecture brute."""
    result = {'nb_pages': '?', 'texte': '', 'etat': 'DOC_ANCIEN'}
    try:
        # Tentative de lecture brute UTF-16 (souvent présent dans les .doc)
        with open(path, 'rb') as f:
            raw = f.read()
        # Chercher des blocs UTF-16
        text_utf16 = ''
        try:
            text_utf16 = raw.decode('utf-16-le', errors='ignore')
        except Exception:
            pass
        # Nettoyer
        text_utf16 = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', ' ', text_utf16)
        # Filtrer les lignes qui ont du sens
        lines = [l.strip() for l in text_utf16.split('\n') if len(l.strip()) > 3 and len(l.strip()) < 200]
        if len(lines) > 3:
            combined = '\n'.join(lines[:40] + ['---FIN---'] + lines[-10:])
            result['texte'] = combined
            result['etat'] = 'TEXTE_LISIBLE'
        else:
            # Essai latin-1
            text_latin = raw.decode('latin-1', errors='ignore')
            text_latin = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', ' ', text_latin)
            lines = [l.strip() for l in text_latin.split('\n') if len(l.strip()) > 3 and len(l.strip()) < 200]
            if len(lines) > 5:
                combined = '\n'.join(lines[:40] + ['---FIN---'] + lines[-10:])
                result['texte'] = combined
                result['etat'] = 'TEXTE_LISIBLE'
            else:
                result['etat'] = 'OCR_NECESSAIRE'
    except Exception as e:
        result['etat'] = f'OCR_NECESSAIRE (erreur: {str(e)[:30]})'
    return result


def extract_image_info(path):
    """Pour les images : OCR_NECESSAIRE par défaut, mais on note les métadonnées."""
    return {'nb_pages': '1', 'texte': '', 'etat': 'OCR_NECESSAIRE'}


def analyze_file(path):
    ext = path.suffix.lower()
    if ext == '.pdf':
        return extract_pdf_info(path)
    elif ext == '.docx':
        return extract_docx_info(path)
    elif ext == '.doc':
        return extract_doc_info(path)
    elif ext in {'.jpg', '.jpeg', '.png'}:
        return extract_image_info(path)
    else:
        return {'nb_pages': '?', 'texte': '', 'etat': 'IGNORE'}


# ============================================================
# BOUCLE PRINCIPALE
# ============================================================

def main():
    print("=" * 60)
    print(" CATALOGUE MODELES ITALIENS")
    print("=" * 60)
    print(f"Dossier base : {BASE_DIR}")
    print(f"CSV sortie   : {CSV_PATH}")
    print()

    init_csv()
    processed = load_progress()
    print(f"[*] Fichiers déjà catalogués : {len(processed)}")
    print()

    # Lister tous les fichiers à traiter
    all_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # Ignorer certains dossiers
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'__pycache__', 'node_modules'}]
        for fname in files:
            if should_ignore(fname):
                continue
            ext = Path(fname).suffix.lower()
            if ext not in EXT_CIBLE:
                continue
            full = Path(root) / fname
            rel = full.relative_to(BASE_DIR)
            all_files.append(rel)

    total = len(all_files)
    print(f"[+] Total fichiers à traiter : {total}")
    print()

    traites_session = 0
    nouveaux = 0
    skips = 0
    erreurs = 0

    t_start = time.time()

    for idx, rel_path in enumerate(all_files, 1):
        full_path = BASE_DIR / rel_path
        try:
            stat = full_path.stat()
            taille = stat.st_size
            mtime_iso = datetime.fromtimestamp(stat.st_mtime).isoformat()
        except Exception:
            continue

        chemin_str = str(full_path)
        ext = full_path.suffix.lower().lstrip('.')
        nom_dossier = full_path.parent.name

        # Vérifier si déjà traité et inchangé
        if chemin_str in processed:
            old_taille, old_mtime = processed[chemin_str]
            if old_taille == taille and old_mtime == mtime_iso:
                skips += 1
                if idx % 500 == 0:
                    print(f"  [{idx}/{total}] skip (déjà catalogué) : {rel_path}")
                continue

        # Analyse rapide
        info = analyze_file(full_path)

        texte = safe_text(info.get('texte', ''))
        etat = info.get('etat', 'INCONNU')
        nb_pages = info.get('nb_pages', '?')

        # Détections
        type_doc = detect_type_document(texte, full_path.name, nom_dossier)
        autorite = detect_autorite(texte)
        noms_sign, fonc_sign = detect_signataires(texte)
        expressions = detect_expressions_italiennes(texte)
        apostille = detect_apostille(texte, full_path.name)
        tableau = info.get('tableau', 'NON')
        cadre = detect_cadre(texte)

        # Titre italien : première ligne significative ou nom de fichier si pas de texte
        titre = ''
        if texte:
            lines = [l.strip() for l in texte.split('\n') if len(l.strip()) > 5]
            if lines:
                titre = lines[0][:200]
        if not titre:
            titre = full_path.name

        # Sous-titres : lignes 2-4 significatives
        sous_titres = ''
        if texte:
            lines = [l.strip() for l in texte.split('\n') if len(l.strip()) > 5]
            if len(lines) > 1:
                sous_titres = ' | '.join(lines[1:4])[:300]

        row = [
            full_path.name,
            chemin_str,
            nom_dossier,
            ext,
            taille,
            mtime_iso,
            nb_pages,
            titre,
            type_doc,
            sous_titres,
            autorite,
            noms_sign,
            fonc_sign,
            expressions,
            apostille,
            tableau,
            cadre,
            etat,
            datetime.now().isoformat(),
        ]

        # Écriture immédiate (append)
        with open(CSV_PATH, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(row)

        traites_session += 1
        if chemin_str not in processed:
            nouveaux += 1

        # Progression
        if idx % 100 == 0 or idx == total:
            elapsed = time.time() - t_start
            rate = traites_session / elapsed if elapsed > 0 else 0
            print(f"  [{idx}/{total}] {rel_path} -> {type_doc} | {etat} | {rate:.1f} fichiers/s")

    print()
    print("=" * 60)
    print(" RÉSUMÉ")
    print("=" * 60)
    print(f"Total fichiers trouvés    : {total}")
    print(f"Déjà catalogués (inchangés): {skips}")
    print(f"Traités cette session     : {traites_session}")
    print(f"Nouveaux                  : {nouveaux}")
    print(f"Erreurs                   : {erreurs}")
    print(f"Catalogue final           : {CSV_PATH}")
    print("=" * 60)


if __name__ == '__main__':
    main()
