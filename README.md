# 🇫🇷 RAA Monitor

> **Explorateur des Recueils des Actes Administratifs des préfectures françaises**

[![Documents](https://img.shields.io/badge/Documents-22%20771-blue?style=flat-square)](https://github.com/gunout/raa-monitor-)
[![Départements](https://img.shields.io/badge/D%C3%A9partements-90-green?style=flat-square)](https://github.com/gunout/raa-monitor-)
[![Préfectures](https://img.shields.io/badge/Pr%C3%A9fectures-88-orange?style=flat-square)](https://github.com/gunout/raa-monitor-)
[![Catégories](https://img.shields.io/badge/Cat%C3%A9gories-6-purple?style=flat-square)](https://github.com/gunout/raa-monitor-)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)](https://developer.mozilla.org/fr/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)](https://developer.mozilla.org/fr/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/fr/docs/Web/JavaScript)
[![Licence MIT](https://img.shields.io/badge/Licence-MIT-yellow?style=flat-square)](https://github.com/gunout/raa-monitor-/blob/main/LICENSE)
[![Statut](https://img.shields.io/badge/Statut-Actif-brightgreen?style=flat-square)](https://github.com/gunout/raa-monitor-)

---

## 📖 Sommaire

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Arborescence](#-arborescence)
- [Base de données](#-base-de-données)
- [Interface web](#-interface-web)
- [Contrôle qualité](#-contrôle-qualité)
- [Stack technique](#-stack-technique)
- [Déploiement](#-déploiement)
- [Contribution](#-contribution)
- [Licence](#-licence)

---

## 🎯 Présentation

**RAA Monitor** est une application web 100 % statique pour explorer le corpus des Recueils des Actes Administratifs (RAA) publiés par les préfectures françaises.

L'application agrège les documents publiés au format PDF sur les sites des préfectures, les normalise, les catégorise et les expose dans une interface de recherche moderne.

**Points clés :**

- Couverture nationale : métropole, Corse et DROM
- Aucune dépendance externe
- Fonctionne hors ligne une fois la base générée
- Design conforme à la charte de l'État (DSFR)

---

## ✨ Fonctionnalités

### Côté utilisateur

- 🔍 **Recherche plein texte** — titre, numéro, préfecture, département, région
- 🎯 **Filtres combinables** — préfecture, département, type, année, tri
- 📊 **Statistiques temps réel** — répartition par type, top 10 préfectures
- 📥 **Export CSV** — téléchargement des résultats filtrés
- 📋 **Copie en masse** — toutes les URLs en un clic
- ⚡ **Pagination fluide** — 25, 50 ou 100 résultats par page
- ⌨️ **Raccourcis clavier** — navigation rapide sans souris

### Côté données

- 🧹 **Nettoyage automatique** — accents, espaces, retours ligne
- 🔗 **Validation d'URL** — rejet des liens invalides
- 🗓️ **Extraction de dates** — parsing automatique depuis les titres
- 🏷️ **Catégorisation intelligente** — 6 types de documents
- 🔍 **Déduplication** — basée sur l'URL unique
- ✅ **Contrôle qualité** — 8 vérifications automatiques

---

## 🚀 Installation

### Prérequis

- Python 3.10 ou supérieur
- Un navigateur moderne (Chrome, Firefox, Safari, Edge)
- Aucune dépendance Python externe

### Cloner le dépôt

    git clone https://github.com/gunout/raa-monitor-.git
    cd raa-monitor-

### Construire la base de données

    python3 load_raa.py
    python3 convert.py
    python3 verify.py

### Lancer l'interface web

    python3 -m http.server 8000

Puis ouvrir l'adresse locale sur le port 8000 dans un navigateur.

**Important** — ne pas ouvrir `index.html` par double-clic. En mode `file://`, le navigateur bloque la lecture du fichier JSON.

---

## 📁 Arborescence

    raa-monitor-/
    ├── raa_flat.csv              Source brute
    ├── raa_clean.csv             Source nettoyée
    ├── json/
    │   └── raa.json              Base finale
    ├── load_raa.py               Nettoyage CSV
    ├── convert.py                CSV vers JSON
    ├── verify.py                 Contrôle qualité
    ├── index.html                Front-end
    ├── prefecture.json           Données préfectures
    ├── prefectures_verified.json Préfectures vérifiées
    ├── prefectures_report.txt    Rapport préfectures
    ├── raa_index.json            Index RAA
    ├── README.md                 Documentation
    └── LICENSE                   Licence MIT

### Pipeline de données

`raa_flat.csv` → `load_raa.py` → `raa_clean.csv` → `convert.py` → `json/raa.json` → `index.html`

---

## 🗄️ Base de données

### Format JSON

Chaque enregistrement contient les champs suivants : `id`, `departement`, `nom_departement`, `region`, `titre`, `type`, `numero`, `date_publication`, `url`, `mise_a_jour`, `annee`, `description`, `tags`.

### Catégories de documents

| Icône | Catégorie | Description | Volume |
|:---:|---|---|---:|
| 📋 | `recueil` | Recueil complet des actes administratifs | 692 |
| 📜 | `arrete` | Arrêté préfectoral isolé | 668 |
| ⚖️ | `decision` | Décision administrative | 39 |
| ⚡ | `special` | Recueil spécial | 8 204 |
| 👤 | `nominatif` | Recueil nominatif | 2 429 |
| 📁 | `autre` | Autres documents | 10 739 |
| | | **Total** | **22 771** |

### Couverture géographique

| Zone | Départements | Statut |
|---|:---:|:---:|
| Métropole | 77 sur 88 | ✅ |
| Corse | 2 sur 2 (2A, 2B) | ✅ |
| DROM | 5 sur 5 (971, 972, 973, 974, 976) | ✅ |
| COM | 0 sur 7 | ⚠️ Non publié |

Départements manquants (scraping amont) : `17`, `38`, `51`, `54`, `55`, `57`, `67`, `75`, `79`, `85`, `95`

---

## 🖥️ Interface web

### Zones fonctionnelles

| Zone | Contenu |
|---|---|
| En-tête | Bande Marianne, devise, statut |
| Barre supérieure | Compteurs : statut, total, préfectures, affichés |
| Sidebar gauche | 6 types + top 8 préfectures |
| Centre | Recherche, filtres, pagination, résultats |
| Panneau droit | Statistiques, répartition, top 10, actions |

### Raccourcis clavier

| Touche | Action |
|:---:|---|
| `/` | Focus sur la barre de recherche |
| `Échap` | Retirer le focus |
| `Entrée` | Lancer la recherche |

### Actions disponibles

- 📥 **Export CSV** — télécharge les résultats filtrés
- 📋 **Copier les URLs** — copie en masse dans le presse-papier
- 🔄 **Réinitialiser** — efface tous les filtres

---

## 🧪 Contrôle qualité

`verify.py` effectue 8 vérifications automatiques :

1. Cohérence `count` vs `len(results)`
2. Validité des codes département
3. Présence des 101 départements
4. Couverture DROM
5. Validité des 6 catégories
6. Champs obligatoires non vides
7. Absence de doublons d'URL
8. Top 10 des départements

---

## 🛠️ Stack technique

| Couche | Technologie |
|---|---|
| Backend | Python 3.10+ (stdlib) |
| Traitement CSV | `csv`, `re`, `unicodedata` |
| Traitement JSON | `json`, `pathlib` |
| Front-end | HTML5, CSS3, JavaScript vanilla |
| Design system | DSFR 1.11.2 |
| Polices | Marianne |
| Couleurs | Bleu `#000091`, Rouge `#E1000F` |

Aucun framework JavaScript. Aucune dépendance Python.

---

## 📦 Déploiement

### GitHub Pages

1. Pousser `index.html` et `json/raa.json`
2. Activer GitHub Pages dans **Settings → Pages**
3. Sélectionner la branche `main`

### Netlify / Vercel

Glisser-déposer le dossier `raa-monitor-`.

### Nginx

Configuration type : servir le dossier en statique, ajouter un cache d'une heure sur `/json/`.

---

## 🤝 Contribution

1. Forker le projet
2. Créer une branche : `git checkout -b feature/x`
3. Commiter : `git commit -m 'Ajout X'`
4. Pousser : `git push origin feature/x`
5. Ouvrir une Pull Request

### Priorités

| Priorité | Tâche |
|:---:|---|
| 🔴 Haute | Scraper les 11 dépts manquants |
| 🟠 Moyenne | Accessibilité WCAG 2.1 AA |
| 🟠 Moyenne | Filtre par région |
| 🟡 Basse | Export JSON |
| 🟡 Basse | Tests pytest |

---

## 🐛 Problèmes connus

| # | Problème | Contournement |
|:---:|---|---|
| 1 | 11 dépts métropole absents | Corriger le scraper amont |
| 2 | `fetch()` bloqué en `file://` | Serveur HTTP local |
| 3 | Titres parfois tronqués | Source amont |

---

## 📜 Licence

MIT. Voir le fichier [LICENSE](https://github.com/gunout/raa-monitor-/blob/main/LICENSE).

---

<div align="center">

**🇫🇷 RAA Monitor** — *Liberté · Égalité · Fraternité*

Fait avec ❤️ pour la transparence administrative

</div>

---

---

<div align="center">

### 🇫🇷 Gunout · 2026

![Made in France](https://img.shields.io/badge/Made_in-France-002395?style=flat-square&labelColor=FFFFFF&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MDAgNjAwIj48cmVjdCB3aWR0aD0iOTAwIiBoZWlnaHQ9IjYwMCIgZmlsbD0iIzAwMjM5NSIvPjxyZWN0IHdpZHRoPSI5MDAiIGhlaWdodD0iNDAwIiB5PSIxMDAiIGZpbGw9IiNmZmYiLz48cmVjdCB3aWR0aD0iOTAwIiBoZWlnaHQ9IjIwMCIgeT0iNDAwIiBmaWxsPSIjZWQyOTM5Ii8+PC9zdmc+)
![GitHub](https://img.shields.io/badge/GitHub-gunout-181717?style=flat-square&logo=github&logoColor=white)
![Year](https://img.shields.io/badge/2026-ED2939?style=flat-square&labelColor=FFFFFF)

<sub>© 2026 <strong>Gunout</strong> — Tous droits réservés.</sub>

</div>
