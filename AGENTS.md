# Traductions PDF en italien

Avant chaque travail dans ce dossier, lire `MEMOIRE/CONSIGNES.md`, puis `MEMOIRE/HISTORIQUE_MODIFICATIONS.jsonl` et les index de `gold`.

L'utilisateur demande de choisir le modèle Word correspondant à chaque acte du PDF, de conserver exactement sa structure, sa mise en page et sa terminologie, et de remplacer uniquement les données propres à l'acte. Rechercher d'abord dans `gold/MODELES`, puis dans les bases de `INDEX` et les fichiers de `serv`. Ne pas substituer un modèle approximatif lorsqu'un modèle correspondant existe.

Créer un Word séparé pour chaque acte, avec son apostille. Le numéroter selon l'ordre dans le PDF, mettre le nom de la personne concernée dans le nom du fichier et classer les Word par PDF. Classer aussi les copies des PDF sources par dossier. Conserver les originaux.

Enregistrer les nouvelles corrections explicitement demandées par l'utilisateur dans l'historique, avec date, portée, ancien et nouveau choix. Mettre à jour les consignes seulement quand une correction exprime une règle générale. Ne pas inventer de préférence ou de validation.

Conserver les exemples traduits dans `gold/EXEMPLES_TRADUITS`. Indiquer séparément leur statut de validation ; une traduction produite par l'assistant n'est pas automatiquement validée par l'utilisateur. Conserver les modèles choisis dans `gold/MODELES`, leur provenance et leur empreinte SHA-256. Une variante distincte doit rester distincte ; ne pas fusionner des modèles au seul motif qu'ils traitent le même type d'acte.

Vérifier les données contre toutes les pages sources, puis rendre et contrôler toutes les pages des Word. Signaler les passages illisibles et les contradictions sans inventer de données. Ne pas attribuer les anciens noms, dates, numéros ou signatures du traducteur du modèle aux nouvelles traductions.
