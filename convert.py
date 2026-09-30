
import csv
import json
from pathlib import Path

INPUT  = "raa_clean.csv"
OUTPUT = "json/raa.json"
Path("json").mkdir(exist_ok=True)

# ---------- Départements → région ----------
REGIONS = {
    "01":"Auvergne-Rhône-Alpes","03":"Auvergne-Rhône-Alpes","07":"Auvergne-Rhône-Alpes",
    "15":"Auvergne-Rhône-Alpes","26":"Auvergne-Rhône-Alpes","38":"Auvergne-Rhône-Alpes",
    "42":"Auvergne-Rhône-Alpes","43":"Auvergne-Rhône-Alpes","63":"Auvergne-Rhône-Alpes",
    "69":"Auvergne-Rhône-Alpes","73":"Auvergne-Rhône-Alpes","74":"Auvergne-Rhône-Alpes",
    "21":"Bourgogne-Franche-Comté","25":"Bourgogne-Franche-Comté","39":"Bourgogne-Franche-Comté",
    "58":"Bourgogne-Franche-Comté","70":"Bourgogne-Franche-Comté","71":"Bourgogne-Franche-Comté",
    "89":"Bourgogne-Franche-Comté","90":"Bourgogne-Franche-Comté",
    "22":"Bretagne","29":"Bretagne","35":"Bretagne","56":"Bretagne",
    "18":"Centre-Val de Loire","28":"Centre-Val de Loire","36":"Centre-Val de Loire",
    "37":"Centre-Val de Loire","41":"Centre-Val de Loire","45":"Centre-Val de Loire",
    "2A":"Corse","2B":"Corse",
    "08":"Grand Est","10":"Grand Est","51":"Grand Est","52":"Grand Est",
    "54":"Grand Est","55":"Grand Est","57":"Grand Est","67":"Grand Est",
    "68":"Grand Est","88":"Grand Est",
    "02":"Hauts-de-France","59":"Hauts-de-France","60":"Hauts-de-France",
    "62":"Hauts-de-France","80":"Hauts-de-France",
    "75":"Île-de-France","77":"Île-de-France","78":"Île-de-France",
    "91":"Île-de-France","92":"Île-de-France","93":"Île-de-France",
    "94":"Île-de-France","95":"Île-de-France",
    "14":"Normandie","27":"Normandie","50":"Normandie","61":"Normandie","76":"Normandie",
    "16":"Nouvelle-Aquitaine","17":"Nouvelle-Aquitaine","19":"Nouvelle-Aquitaine",
    "23":"Nouvelle-Aquitaine","24":"Nouvelle-Aquitaine","33":"Nouvelle-Aquitaine",
    "40":"Nouvelle-Aquitaine","47":"Nouvelle-Aquitaine","64":"Nouvelle-Aquitaine",
    "79":"Nouvelle-Aquitaine","86":"Nouvelle-Aquitaine","87":"Nouvelle-Aquitaine",
    "09":"Occitanie","11":"Occitanie","12":"Occitanie","30":"Occitanie","31":"Occitanie",
    "32":"Occitanie","34":"Occitanie","46":"Occitanie","48":"Occitanie","65":"Occitanie",
    "66":"Occitanie","81":"Occitanie","82":"Occitanie",
    "44":"Pays de la Loire","49":"Pays de la Loire","53":"Pays de la Loire",
    "72":"Pays de la Loire","85":"Pays de la Loire",
    "04":"Provence-Alpes-Côte d'Azur","05":"Provence-Alpes-Côte d'Azur",
    "06":"Provence-Alpes-Côte d'Azur","13":"Provence-Alpes-Côte d'Azur",
    "83":"Provence-Alpes-Côte d'Azur","84":"Provence-Alpes-Côte d'Azur",
    # Outre-mer
    "971":"Guadeloupe","972":"Martinique","973":"Guyane","974":"La Réunion","976":"Mayotte",
}

# ---------- Noms officiels des départements ----------
DEP_NOMS = {
    "01":"Ain","02":"Aisne","03":"Allier","04":"Alpes-de-Haute-Provence",
    "05":"Hautes-Alpes","06":"Alpes-Maritimes","07":"Ardèche","08":"Ardennes",
    "09":"Ariège","10":"Aube","11":"Aude","12":"Aveyron","13":"Bouches-du-Rhône",
    "14":"Calvados","15":"Cantal","16":"Charente","17":"Charente-Maritime",
    "18":"Cher","19":"Corrèze","2A":"Corse-du-Sud","2B":"Haute-Corse",
    "21":"Côte-d'Or","22":"Côtes-d'Armor","23":"Creuse","24":"Dordogne",
    "25":"Doubs","26":"Drôme","27":"Eure","28":"Eure-et-Loir","29":"Finistère",
    "30":"Gard","31":"Haute-Garonne","32":"Gers","33":"Gironde","34":"Hérault",
    "35":"Ille-et-Vilaine","36":"Indre","37":"Indre-et-Loire","38":"Isère",
    "39":"Jura","40":"Landes","41":"Loir-et-Cher","42":"Loire","43":"Haute-Loire",
    "44":"Loire-Atlantique","45":"Loiret","46":"Lot","47":"Lot-et-Garonne",
    "48":"Lozère","49":"Maine-et-Loire","50":"Manche","51":"Marne",
    "52":"Haute-Marne","53":"Mayenne","54":"Meurthe-et-Moselle","55":"Meuse",
    "56":"Morbihan","57":"Moselle","58":"Nièvre","59":"Nord","60":"Oise",
    "61":"Orne","62":"Pas-de-Calais","63":"Puy-de-Dôme","64":"Pyrénées-Atlantiques",
    "65":"Hautes-Pyrénées","66":"Pyrénées-Orientales","67":"Bas-Rhin",
    "68":"Haut-Rhin","69":"Rhône","70":"Haute-Saône","71":"Saône-et-Loire",
    "72":"Sarthe","73":"Savoie","74":"Haute-Savoie","75":"Paris",
    "76":"Seine-Maritime","77":"Seine-et-Marne","78":"Yvelines",
    "79":"Deux-Sèvres","80":"Somme","81":"Tarn","82":"Tarn-et-Garonne",
    "83":"Var","84":"Vaucluse","85":"Vendée","86":"Vienne","87":"Haute-Vienne",
    "88":"Vosges","89":"Yonne","90":"Territoire de Belfort",
    "91":"Essonne","92":"Hauts-de-Seine","93":"Seine-Saint-Denis",
    "94":"Val-de-Marne","95":"Val-d'Oise",
    "971":"Guadeloupe","972":"Martinique","973":"Guyane","974":"La Réunion",
    "976":"Mayotte",
}

# ---------- Catégories valides ----------
TYPES_VALIDES = {"recueil", "arrete", "decision", "deliberation",
                 "special", "nominatif", "autre"}

def infer_type(row) -> str:
    """Renvoie le type déjà calculé par load_raa.py, ou le recalcule."""
    t = (row.get("type") or "").strip().lower()
    if t in TYPES_VALIDES:
        return t

    # Fallback : recalcul à partir du titre
    titre = (row.get("titre") or "").lower()
    titre = (titre.replace("é", "e").replace("è", "e").replace("ê", "e")
                  .replace("à", "a").replace("â", "a"))
    if "nominatif" in titre:
        return "nominatif"
    if "special" in titre:
        return "special"
    if "recueil" in titre and "actes administratifs" in titre:
        return "recueil"
    if "arrete" in titre:
        return "arrete"
    if "decision" in titre:
        return "decision"
    if "deliberation" in titre:
        return "deliberation"
    return "autre"

def infer_annee(row) -> int | None:
    for field in ("date_publication", "mise_a_jour", "titre"):
        v = row.get(field) or ""
        for token in v.replace("_", " ").replace("-", " ").split():
            if len(token) == 4 and token.isdigit() and 2000 <= int(token) <= 2100:
                return int(token)
    return None

def main():
    records = []
    seen    = set()

    with open(INPUT, encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f)):
            url = (row.get("url") or "").strip()
            if not url or url in seen:
                continue
            seen.add(url)

            dep = (row.get("departement") or "").strip()
            if not dep:
                continue

            titre = (row.get("titre") or "").strip()
            typ   = infer_type(row)

            rec = {
                "id":              f"raa-{dep}-{i:06d}",
                "departement":     dep,
                "nom_departement": DEP_NOMS.get(dep, row.get("nom") or dep),
                "region":          REGIONS.get(dep, "—"),
                "titre":           titre,
                "type":            typ,
                "numero":          (row.get("numero") or "").strip(),
                "date_publication":(row.get("date_publication") or "").strip(),
                "url":             url,
                "mise_a_jour":     (row.get("mise_a_jour") or "").strip(),
                "annee":           infer_annee(row),
                "description":     f"Recueil des actes administratifs du département {DEP_NOMS.get(dep, dep)}",
                "tags":            [dep, typ],
            }
            records.append(rec)

    # Tri : département puis date
    records.sort(key=lambda r: (r["departement"], r["date_publication"] or ""))

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump({"results": records, "count": len(records)},
                  f, ensure_ascii=False, indent=1)

    # Rapport
    from collections import Counter
    by_dep  = Counter(r["departement"] for r in records)
    by_type = Counter(r["type"] for r in records)

    print(f"✅ {len(records)} documents écrits dans {OUTPUT}")
    print(f"   Départements : {len(by_dep)}")
    print(f"   Répartition par type :")
    for t, n in by_type.most_common():
        print(f"      {t:14s} : {n}")
    print(f"   974 La Réunion : {by_dep.get('974', 0)} documents")
    print(f"   23  Creuse     : {by_dep.get('23', 0)} documents")
    print(f"   28  Eure-et-L. : {by_dep.get('28', 0)} documents")
    print(f"   74  Haute-Sav. : {by_dep.get('74', 0)} documents")

if __name__ == "__main__":
    main()