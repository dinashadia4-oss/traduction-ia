# Traductions PDF en italien

Avant chaque travail dans ce dossier, lire `MEMOIRE/CONSIGNES.md`, puis `MEMOIRE/HISTORIQUE_MODIFICATIONS.jsonl` et les index de `gold`.

L'utilisateur demande de choisir le modèle Word correspondant à chaque acte du PDF, de conserver exactement sa structure, sa mise en page et sa terminologie, et de remplacer uniquement les données propres à l'acte. Rechercher d'abord dans `gold/MODELES`, puis dans les bases de `INDEX` et les fichiers de `serv`. Ne pas substituer un modèle approximatif lorsqu'un modèle correspondant existe.

Créer un Word séparé pour chaque acte, avec son apostille. Le numéroter selon l'ordre dans le PDF, mettre le nom de la personne concernée dans le nom du fichier et classer les Word par PDF. Classer aussi les copies des PDF sources par dossier. Conserver les originaux.

Enregistrer les nouvelles corrections explicitement demandées par l'utilisateur dans l'historique, avec date, portée, ancien et nouveau choix. Mettre à jour les consignes seulement quand une correction exprime une règle générale. Ne pas inventer de préférence ou de validation.

Conserver les exemples traduits dans `gold/EXEMPLES_TRADUITS`. Indiquer séparément leur statut de validation ; une traduction produite par l'assistant n'est pas automatiquement validée par l'utilisateur. Conserver les modèles choisis dans `gold/MODELES`, leur provenance et leur empreinte SHA-256. Une variante distincte doit rester distincte ; ne pas fusionner des modèles au seul motif qu'ils traitent le même type d'acte.

Vérifier les données contre toutes les pages sources, puis rendre et contrôler toutes les pages des Word. Signaler les passages illisibles et les contradictions sans inventer de données. Ne pas attribuer les anciens noms, dates, numéros ou signatures du traducteur du modèle aux nouvelles traductions.


## Commande courte permanente : « traduit »

Quand l'utilisateur joint un ou plusieurs PDF et écrit seulement **« traduit »** (ou « traduire »), exécuter automatiquement le workflow complet de traduction sans lui redemander les consignes.

Ordre des sources :
1. Si des PDF sont joints à la tâche, traiter ces PDF.
2. Sinon, utiliser Google Drive et prendre les PDF présents dans le dossier `A_TRADUIRE` (folder ID : `16jPAMH_BXoo5L14dmO5H63TFH9M_JAjb`).

Workflow automatique pour chaque PDF :
- Lire et appliquer `AGENTS.md`, `MEMOIRE/CONSIGNES.md`, `MEMOIRE/HISTORIQUE_MODIFICATIONS.jsonl` et les index de `gold`.
- Utiliser `INDEX/index_modeles.db`, `gold/MODELES` et `serv` pour retrouver le modèle Word exact ou le plus pertinent ; ne jamais remplacer un modèle exact par un modèle approximatif.
- Traduire en italien en respectant strictement la terminologie et la mise en page du modèle : structure, tableaux, marges, polices, tailles, gras/italique, alignements, sauts, apostille et ordre des éléments.
- Remplacer uniquement les données propres au nouvel acte et ne jamais conserver par erreur des noms, dates, numéros ou signatures provenant du modèle.
- Vérifier toutes les pages sources ; signaler les éléments réellement illisibles et ne jamais inventer d'information.
- Créer un Word séparé par acte, numéroté dans l'ordre du PDF, avec le nom de la personne concernée dans le nom du fichier, et classer les résultats par PDF.
- Rendre les Word en PDF et effectuer un contrôle visuel de toutes les pages avant livraison.
- Conserver les PDF sources inchangés et ne jamais modifier les modèles originaux.

Livraison par défaut :
- Déposer les fichiers Word finaux dans Google Drive, dossier `TRADUITS` (folder ID : `1fWrT-ai_dJehp7_niBhnflvxanNQ4HB3`).
- Déposer aussi les PDF de contrôle dans ce dossier si le contrôle visuel a été généré.
- Si Google Drive n'est pas disponible dans la tâche, fournir les résultats dans la conversation et regrouper les Word dans un ZIP lorsque plusieurs fichiers sont produits.
- À la fin, répondre brièvement avec la liste des fichiers terminés et signaler uniquement les documents nécessitant une vérification manuelle.

Ne demander une précision à l'utilisateur que si une ambiguïté empêche réellement de choisir le bon document, le bon modèle ou de produire une traduction fiable.
