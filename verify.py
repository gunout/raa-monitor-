
import json
import sys
from collections import Counter

JSON_PATH = "json/raa.json"

# Départements attendus (métropole + Corse + DOM + COM)
ATTENDUS_METRO = {f"{i:02d}" for i in range(1, 96)} - {"20"} | {"2A", "2B"}
ATTENDUS_DOM   = {"971", "972", "973", "974", "976"}
ATTENDUS_COM   = {"975", "977", "978", "984", "986", "987", "988"}
ATTENDUS       = ATTENDUS_METRO | ATTENDUS_DOM | ATTENDUS_COM

TYPES_CONNUS = {"recueil", "arrete", "decision", "deliberation",
                "special", "nominatif", "autre"}

def main():
    try:
        with open(JSON_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ {JSON_PATH} introuvable. Lance d'abord convert.py.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON invalide : {e}")
        sys.exit(1)

    results = data.get("results", [])
    count   = data.get("count", len(results))

    print("=" * 60)
    print(f"📊 RAPPORT DE VÉRIFICATION — {JSON_PATH}")
    print("=" * 60)

    # 1. Cohérence count / len
    print(f"\n1️⃣  Nombre d'enregistrements")
    print(f"   count déclaré : {count}")
    print(f"   results len   : {len(results)}")
    if count == len(results):
        print("   ✅ Cohérent")
    else:
        print("   ⚠️  Incohérent !")

    # 2. Départements présents
    deps = sorted(set(r["departement"] for r in results))
    print(f"\n2️⃣  Départements présents : {len(deps)}")

    inconnus = [c for c in deps if c not in ATTENDUS]
    if inconnus:
        print(f"   ⚠️  Codes inconnus : {inconnus}")
    else:
        print("   ✅ Tous les codes sont valides")

    manquants = sorted(ATTENDUS - set(deps))
    if manquants:
        print(f"   ⚠️  Départements absents ({len(manquants)}) : {manquants}")
    else:
        print("   ✅ Aucun département manquant")

    # 3. Vérification spéciale outre-mer
    print(f"\n3️⃣  Outre-mer")
    for code in sorted(ATTENDUS_DOM):
        n = sum(1 for r in results if r["departement"] == code)
        flag = "✅" if n > 0 else "❌"
        print(f"   {flag} {code} : {n} documents")

    # 4. Répartition par type
    print(f"\n4️⃣  Répartition par type")
    by_type = Counter(r.get("type", "?") for r in results)
    for t, n in by_type.most_common():
        flag = "✅" if t in TYPES_CONNUS else "⚠️ "
        print(f"   {flag} {t:14s} : {n}")

    types_inconnus = [t for t in by_type if t not in TYPES_CONNUS]
    if types_inconnus:
        print(f"   ⚠️  Types inconnus : {types_inconnus}")

    # 5. Vérification des champs obligatoires
    print(f"\n5️⃣  Champs obligatoires")
    champs = ["id", "departement", "titre", "type", "url"]
    for champ in champs:
        vides = sum(1 for r in results if not r.get(champ))
        flag = "✅" if vides == 0 else "⚠️ "
        print(f"   {flag} {champ:14s} : {vides} vide(s)")

    # 6. Doublons d'URL
    print(f"\n6️⃣  Doublons d'URL")
    urls   = [r["url"] for r in results if r.get("url")]
    doublons = len(urls) - len(set(urls))
    if doublons:
        print(f"   ⚠️  {doublons} doublon(s) détecté(s)")
    else:
        print("   ✅ Aucun doublon")

    # 7. Top 10 départements
    print(f"\n7️⃣  Top 10 départements")
    by_dep = Counter(r["departement"] for r in results)
    for dep, n in by_dep.most_common(10):
        nom = next((r["nom_departement"] for r in results
                    if r["departement"] == dep), dep)
        print(f"   {dep:>4} {nom:30s} : {n}")

    # 8. Résumé final
    print("\n" + "=" * 60)
    if not manquants and not inconnus and not types_inconnus:
        print("✅ BASE COMPLÈTE ET VALIDE")
    else:
        print("⚠️  BASE INCOMPLÈTE — voir les avertissements ci-dessus")
    print("=" * 60)

if __name__ == "__main__":
    main()