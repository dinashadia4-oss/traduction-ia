# Mémoire des traductions

Langue de sortie : italien, conformément aux modèles fournis.

## Règles demandées par l'utilisateur

1. Choisir le modèle qui correspond au PDF et conserver sa terminologie et sa présentation. Changer uniquement les données variables du nouvel acte.
2. Séparer les Word : un acte et son apostille par fichier.
3. Numéroter chaque Word et inclure le nom de la personne concernée, selon le PDF. Pour une prise en charge, identifier le garant et le bénéficiaire.
4. Classer les traductions et les PDF par dossier source. Garder les originaux disponibles.
5. Utiliser l'index et le dossier `serv` pour retrouver les modèles correspondants.
6. Conserver les exemples traduits et les modèles réutilisables dans le dossier `gold`, sans perdre les variantes distinctes.
7. Conserver l'historique de toutes les modifications demandées et appliquer les règles générales aux travaux suivants dans ce projet.

## Méthode de réutilisation

Consulter `gold/INDEX_MODELES.csv`, puis rechercher dans la base `INDEX/index_modeles.db` avec `MEMOIRE/rechercher_modeles.py`. Les anciens chemins de la base pointent vers `Desktop/serv` ; l'outil les résout vers le dossier `serv` présent ici, sans modifier la base originale.

Comparer le type d'acte, l'autorité, les rubriques, les tableaux, les pages et l'apostille. Une ressemblance de titre seule ne suffit pas. Conserver les termes du modèle retenu et documenter toute adaptation nécessaire si le modèle exact demeure absent.

Correction demandée le 05/10/2026 : les anciens Word présentent des différences. Rechercher la variante correspondante dans INDEX/serv et remplacer les données dans ses éléments existants. Ne pas reconstruire librement les paragraphes, reformuler les phrases fixes ni modifier les colonnes, polices ou marges du modèle. Un modèle correspondant disponible doit remplacer tout choix approximatif antérieur. La clarification ultérieure limite le travail aux nouveaux PDF 17 à 20 : ne pas corriger les 54 anciens Word sans nouvelle demande.

Pour tous les nouveaux documents : supprimer le numéro de traduction en tête. Dans la formule finale, choisir uniquement « lingua araba » ou « lingua francese » selon la langue du texte de l'acte. Remplacer la ligne finale de date par le texte exact demandé : « Rabat. il 08/10/2026.N ». Cette date est une instruction explicite de l'utilisateur, et non une date à déduire du jour courant. Conserver la police et les propriétés du pied de texte du modèle.

Correction explicite du 05/10/2026 : dans les nouveaux documents, inscrire uniquement les dates et années grégoriennes. Ne pas ajouter ni conserver les équivalents hégiriens, même lorsqu'ils figurent dans le PDF ou le modèle.

La mémoire est un ensemble de fichiers locaux. Elle peut être relue et enrichie lors des prochaines demandes dans ce dossier ; elle ne constitue pas un entraînement du modèle ni une promesse de mémorisation automatique dans tous les autres chats.

## État des exemples

Le lot antérieur PDF 5 à 10 contient 37 Word. Il est conservé comme exemples de travail, avec ses remarques de lecture. L'utilisateur n'a pas encore explicitement validé leur contenu ou leur mise en page ; ne pas les présenter comme des traductions certifiées ou définitivement approuvées.

Les nouveaux lots sont archivés séparément pour permettre les comparaisons et corrections ultérieures.

Le 05/10/2026, la demande « faire la même chose avec les nouveaux PDF » étend l’application des règles ci-dessus au lot PDF 21, 23, 24, 27, 29 et 33. Les corrections générales de dates et de formule finale restent applicables aux futurs nouveaux lots. Le détail de ce lot et les réserves figurent dans VERIFICATION_LOT_21_23_24_27_29_33.json et le relevé de remarques.


## Vocabulaire des mentions scolaires — correction du 05/10/2026
- Insuffisant → Insufficiente
- Passable → Sufficiente
- Assez bien → Buono
- Bien → Distinto
- Très bien → Ottimo
Appliquer aux mentions scolaires selon le texte source. Ne pas remplacer les adjectifs ordinaires par une mention. Référence : REFERENCES/vovabulaire.jpeg.
