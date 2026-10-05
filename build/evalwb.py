"""Evaluate spec_v7 formulas in Python (same dialect the workbook uses) and dump values for the renderer.
Dialect: in_<id> names (and _lo/_hi), {key} row refs, + - * / ^, IF(c,a,b), MIN(), MAX(), comparisons, string literals."""
import re, json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import spec_v7 as spec

vals = {}
for i in spec.INPUTS:
    nm = "in_" + re.sub(r"[^A-Za-z0-9_]", "_", i["id"])
    vals[nm] = i.get("figure")
    if i.get("range_low") is not None:
        vals[nm + "_lo"] = i["range_low"]; vals[nm + "_hi"] = i["range_high"]

def _IF(c, a, b): return a if c else b

def to_py(f):
    f = f.replace("^", "**")
    f = re.sub(r"\bIF\(", "_IF(", f); f = re.sub(r"\bMIN\(", "min(", f); f = re.sub(r"\bMAX\(", "max(", f)
    f = re.sub(r"(?<![<>=!])=(?!=)", "==", f)
    return f

out = {}
errors = 0
for sh in spec.SHEETS:
    rows = {}
    rowvals = {}
    for row in sh["rows"]:
        if row.get("section"): continue
        f = row["excel"]
        f = re.sub(r"\{([A-Za-z0-9_]+)\}", lambda m: f"__row['{m.group(1)}']", f)
        try:
            v = eval(to_py(f), {"__builtins__": {}}, {"_IF": _IF, "min": min, "max": max, "__row": rowvals, **vals})
        except Exception as e:
            v = f"ERR {e}"; errors += 1
        if row.get("key"): rowvals[row["key"]] = v
        rows[(row.get("key") or f"r{len(rows)+1}") + " | " + row["label"]] = v
    out[sh["name"]] = rows
json.dump(out, open(os.path.join(os.path.dirname(__file__), "values_v7.json"), "w"), indent=1, default=str)
print("formula errors:", errors)
for name in ["WE_F1_Payments", "WE_F2_Lending", "WE_F3_Insurance", "WE_F4_Wealth", "WE_F5_Fraud_identity", "WE_AF2_Voice", "WE_AF1_Finance_agents", "EX2_Fee_ladder", "EX4_Exits", "EX7_Fund_maths"]:
    print("==", name)
    for k, v in out[name].items():
        s = f"{v:,.4f}" if isinstance(v, float) else str(v)
        print(f"  {k[:60]:60} {s:>16}")
