

import csv
import re
import unicodedata
from urllib.parse import urlparse
from datetime import datetime
from collections import Counter

INPUT  = "raa_flat.csv"
OUTPUT = "raa_clean.csv"


# ---------- Normalisation ----------
def strip_accents(s: str) -> str:
    """Retire les accents d'une chaîne."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", s or "")
        if not unicodedata.combining(c)
    )


def clean_text(s: str) -> str:
    """Nettoie un texte : supprime retours ligne, espaces multiples."""
    if s is None:
        return ""
    s = s.replace("\r", " ").replace("\n", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def clean_url(u: str) -> str | None:
    """Valide et normalise une URL. Retourne None si invalide."""
    if not u:
        return None
    u = u.strip().replace(" ", "%20")
    # Correction des URLs malformées du type "...gouv.frmailto:..."
    u = re.sub(r"gouv\.fr(mailto:)", r"gouv.fr/\1", u)
    try:
        p = urlparse(u)
        if p.scheme not in ("http", "https") or not p.netloc:
            return None
        return u
    except Exception:
        return None


def parse_date(s: str) -> str | None:
    """Renvoie la date ISO 8601 ou None."""
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).isoformat()
    except ValueError:
        return None


# ---------- Lecture CSV robuste ----------
def read_csv(path: str):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=",", quotechar='"')
        yield from reader


# ---------- Classification ----------
def classify(row: dict) -> str:
    """Détermine la catégorie du document à partir du titre.

    Catégories possibles :
      - nominatif    : contient « nominatif »
      - special      : contient « special » / « spécial »
      - recueil      : contient « recueil » + « actes administratifs »
      - arrete       : contient « arrêté » / « arrete »
      - decision     : contient « décision »
      - deliberation : contient « délibération »
      - autre        : tout le reste
    """
    t = strip_accents((row.get("titre") or "").lower())
    titre_brut = (row.get("titre") or "").lower()

    if "nominatif" in t:
        return "nominatif"
    if "special" in t or "spécial" in titre_brut:
        return "special"
    if "recueil" in t and "actes administratifs" in t:
        return "recueil"
    if "arrete" in t:
        return "arrete"
    if "decision" in t:
        return "decision"
    if "deliberation" in t:
        return "deliberation"
    return "autre"


# ---------- Extraction d'infos ----------
NUM_RE  = re.compile(r"(\d{2,3})[-_]?(\d{4})[-_]?(\d{1,3})")
DATE_RE = re.compile(r"(\d{1,2})[-/ ]?(\d{1,2})[-/ ]?(\d{4})")


def extract_meta(row: dict) -> dict:
    """Extrait un numéro et une date de publication depuis le titre."""
    titre  = row.get("titre") or ""
    t_norm = strip_accents(titre.lower())

    num_match = NUM_RE.search(t_norm)
    num = num_match.group(3) if num_match else None

    date_match = DATE_RE.search(t_norm)
    date_pub = None
    if date_match:
        d, m, y = date_match.groups()
        try:
            date_pub = f"{y}-{int(m):02d}-{int(d):02d}"
        except ValueError:
            pass

    return {"numero": num, "date_publication": date_pub}


# ---------- Programme principal ----------
def main():
    seen_urls = set()
    rows_out  = []

    for row in read_csv(INPUT):
        # Normalisation des champs
        row = {k: clean_text(v) for k, v in row.items() if k}

        # Champs obligatoires
        if not row.get("url") or not row.get("departement"):
            continue

        # Garde-fou : titre vide
        if not row.get("titre"):
            continue

        url = clean_url(row["url"])
        if not url:
            continue

        # Déduplication UNIQUEMENT par URL.
        # ⚠️  On ne déduplique PLUS par titre : deux documents différents
        #     peuvent partager un titre générique (« PV », « Arrêté DGF 2026… »)
        #     tout en ayant des URLs distinctes.
        key_url = url.lower()
        if key_url in seen_urls:
            continue
        seen_urls.add(key_url)

        meta = extract_meta(row)

        rows_out.append({
            "departement":      row["departement"],
            "nom":              row["nom"],
            "titre":            row["titre"],
            "type":             classify(row),
            "numero":           meta["numero"] or "",
            "date_publication": meta["date_publication"] or "",
            "url":              url,
            "mise_a_jour":      parse_date(row.get("mise_a_jour")) or "",
        })

    # Tri : département, puis date de mise à jour croissante
    rows_out.sort(key=lambda r: (r["departement"], r["mise_a_jour"]), reverse=False)

    # Écriture
    with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "departement", "nom", "titre", "type", "numero",
            "date_publication", "url", "mise_a_jour"
        ])
        writer.writeheader()
        writer.writerows(rows_out)

    # ---------- Rapport ----------
    by_dep  = Counter(r["departement"] for r in rows_out)
    by_type = Counter(r["type"] for r in rows_out)

    print(f"✅ {len(rows_out)} enregistrements écrits dans {OUTPUT}")
    print(f"   Départements : {len(by_dep)}")
    print(f"   Répartition par type :")
    for t, n in by_type.most_common():
        print(f"      {t:14s} : {n}")
    print()
    print(f"   Contrôle des départements récupérés :")
    for code, nom in [
        ("974", "La Réunion"),
        ("23",  "Creuse"),
        ("28",  "Eure-et-Loir"),
        ("74",  "Haute-Savoie"),
        ("16",  "Charente"),
        ("69",  "Rhône"),
        ("60",  "Oise"),
        ("61",  "Orne"),
        ("02",  "Aisne"),
        ("42",  "Loire"),
    ]:
        n = by_dep.get(code, 0)
        flag = "✅" if n > 0 else "❌"
        print(f"      {flag} {code:>3} {nom:18s} : {n} documents")


if __name__ == "__main__":
    main()