"""
prepare_data.py
---------------
Reads the raw Navigate/Mastery Tracker assessment exports for two 4th-grade math
interim assessments, anonymizes student identities, and writes:

  data/interim1_anon.csv        - tidy per-student-per-item, names removed
  data/interim2_anon.csv
  data/standards_long.csv       - per-student, per-standard mastery (both interims)
  data/student_growth.csv       - matched Interim 1 -> Interim 2 growth per student
  data/item_analysis.csv        - per-question class correct% + standard (Interim 2)
  private/student_id_map.csv    - REAL name <-> anonymized id  (DO NOT COMMIT)

Run:  python prepare_data.py
"""
import csv
import hashlib
from pathlib import Path
from collections import defaultdict

RAW_INTERIM1 = "raw/14_Jun_20_25.csv"
RAW_INTERIM2 = "raw/14_Jun_20_36.csv"
RAW_ITEMS    = "raw/item_analysis_data_6150844_2026-06-14.csv"

META_COLS = ["district", "school", "teacher", "tracker", "tracker_status",
             "school_year", "assessment_name", "student_id", "state_number",
             "last_name", "first_name", "student_status", "created_at",
             "points_possible", "score", "percentage"]
N_META = len(META_COLS)

STD_NAMES = {
    "4.OA.A.1": "Multiplicative comparison",
    "4.OA.A.2": "Multiplicative comparison word problems",
    "4.OA.A.3": "Multistep word problems",
    "4.NBT.A.1": "Place value understanding",
    "4.NBT.A.2": "Read, write & compare multi-digit numbers",
    "4.NBT.A.3": "Rounding multi-digit numbers",
    "4.NBT.B.4": "Add & subtract multi-digit numbers",
    "4.NBT.B.5": "Multiply multi-digit numbers",
    "4.NBT.B.6": "Divide multi-digit numbers",
}


def load_assessment(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    standards_row = rows[0]
    data = [r for r in rows[2:] if any(c.strip() for c in r)]
    # answer columns come in (letter, score) pairs after the meta block
    item_standards = []
    for i in range(N_META, len(standards_row), 2):
        item_standards.append(standards_row[i])
    return item_standards, data


def anon_id(student_id, n):
    """Stable anonymous label like S07 from the real student_id."""
    return "S%02d" % n


def build():
    base = Path(".")
    (base / "data").mkdir(exist_ok=True)
    (base / "private").mkdir(exist_ok=True)

    stds1, data1 = load_assessment(RAW_INTERIM1)
    stds2, data2 = load_assessment(RAW_INTERIM2)

    # Stable ordering by last,first so anon ids are deterministic
    def key(r): return (r[9].strip().lower(), r[10].strip().lower())
    data1.sort(key=key)
    data2.sort(key=key)

    # Build the id map from the union of both rosters
    roster = {}
    n = 0
    for r in data1 + data2:
        sid = r[7].strip()
        if sid and sid not in roster:
            n += 1
            roster[sid] = anon_id(sid, n)

    # private mapping file
    with open("private/student_id_map.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["anon_id", "student_id", "last_name", "first_name"])
        seen = set()
        for r in data1 + data2:
            sid = r[7].strip()
            if sid and sid not in seen:
                seen.add(sid)
                w.writerow([roster[sid], sid, r[9].strip(), r[10].strip()])

    def write_anon(path_out, stds, data, assessment_label):
        with open(path_out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            header = ["anon_id", "assessment", "points_possible", "score", "percentage"]
            header += ["q%02d_%s" % (i + 1, stds[i]) for i in range(len(stds))]
            w.writerow(header)
            for r in data:
                sid = r[7].strip()
                row = [roster.get(sid, "S??"), assessment_label,
                       r[13], r[14], r[15]]
                # item correctness (the "1"/"0" score column of each pair)
                for i in range(len(stds)):
                    score_idx = N_META + i * 2 + 1
                    val = r[score_idx] if score_idx < len(r) else ""
                    row.append(val.strip() if val.strip() else "")
                w.writerow(row)

    write_anon("data/interim1_anon.csv", stds1, data1, "Interim 1")
    write_anon("data/interim2_anon.csv", stds2, data2, "Interim 2")

    # ---- standards_long: per student, per standard, per interim mastery ----
    def standard_scores(stds, data, label):
        out = []
        for r in data:
            sid = r[7].strip()
            by_std_correct = defaultdict(int)
            by_std_total = defaultdict(int)
            for i, std in enumerate(stds):
                score_idx = N_META + i * 2 + 1
                if score_idx < len(r) and r[score_idx].strip() in ("0", "1"):
                    by_std_total[std] += 1
                    by_std_correct[std] += int(r[score_idx].strip())
            for std in by_std_total:
                out.append({
                    "anon_id": roster.get(sid, "S??"),
                    "assessment": label,
                    "standard": std,
                    "skill": STD_NAMES.get(std, std),
                    "correct": by_std_correct[std],
                    "items": by_std_total[std],
                    "mastery_pct": round(100 * by_std_correct[std] / by_std_total[std], 1),
                })
        return out

    long_rows = standard_scores(stds1, data1, "Interim 1") + \
                standard_scores(stds2, data2, "Interim 2")
    with open("data/standards_long.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["anon_id", "assessment", "standard",
                                          "skill", "correct", "items", "mastery_pct"])
        w.writeheader()
        w.writerows(long_rows)

    # ---- student_growth: matched Interim1 -> Interim2 ----
    pct1 = {r[7].strip(): float(r[15]) for r in data1 if r[15].strip()}
    pct2 = {r[7].strip(): float(r[15]) for r in data2 if r[15].strip()}
    with open("data/student_growth.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["anon_id", "interim1_pct", "interim2_pct", "growth_pts"])
        for sid in sorted(set(pct1) & set(pct2), key=lambda s: roster.get(s, s)):
            g = round(pct2[sid] - pct1[sid], 1)
            w.writerow([roster.get(sid, "S??"), pct1[sid], pct2[sid], g])

    # ---- item analysis (Interim 2) ----
    with open(RAW_ITEMS, newline="", encoding="utf-8") as f:
        irows = list(csv.reader(f))
    labeled = {}
    for r in irows:
        if len(r) > 11 and r[11].strip():
            labeled[r[11].strip()] = r[12:]
    qn = labeled.get("question_number", [])
    std = labeled.get("standard", [])
    pc = labeled.get("percent_correct", [])
    ca = labeled.get("correct_answer", [])
    with open("data/item_analysis.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["question", "standard", "skill", "correct_answer", "class_correct_pct"])
        for i in range(len(qn)):
            s = std[i] if i < len(std) else ""
            w.writerow([qn[i], s, STD_NAMES.get(s, s),
                        ca[i] if i < len(ca) else "",
                        pc[i] if i < len(pc) else ""])

    print("Wrote anonymized data for %d students." % len(roster))
    print("Interim 1 standards:", sorted(set(stds1)))
    print("Interim 2 standards:", sorted(set(stds2)))


if __name__ == "__main__":
    build()
