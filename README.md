[![Software License](https://img.shields.io/badge/Licence-Licence%20Ouverte-orange.svg?style=flat-square)](https://github.com/AntoineAugusti/vacances-scolaires/blob/master/LICENSE.md)
[![goodtables.io](https://goodtables.io/badge/github/AntoineAugusti/vacances-scolaires.svg)](https://goodtables.io/github/AntoineAugusti/vacances-scolaires)

# Vacances scolaires
Recense les vacances scolaires en France de l'année scolaire 1990/1991 à l'année scolaire 2020/2021 dans un fichier CSV unique.

## Modèle de données

|Nom|Type|Description|Exemple|Propriétés|
|-|-|-|-|-|
|date|date (format `%Y-%m-%d`)|Date|2018-01-01|Valeur obligatoire|
|vacances_zone_a|booléen|Est-ce que la zone A est en vacances à cette date|true, false|Valeur obligatoire|
|vacances_zone_b|booléen|Est-ce que la zone B est en vacances à cette date|true, false|Valeur obligatoire|
|vacances_zone_c|booléen|Est-ce que la zone C est en vacances à cette date|true, false|Valeur obligatoire|
|nom_vacances|chaîne de caractères|Si au moins une des zones est en vacances, le nom des vacances|true, false|Valeurs autorisées : Vacances de la Toussaint, Vacances de Noël, Vacances d'hiver, Vacances de printemps, Vacances d'été, Pont de l'Ascension|

## Package Python
Si vous souhaitez utiliser ces données en Python le package suivant vous sera utile : https://github.com/AntoineAugusti/vacances-scolaires-france
