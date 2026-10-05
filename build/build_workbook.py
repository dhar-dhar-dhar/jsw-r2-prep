"""Build JSW_R2_workbook_v7.xlsx from spec_v7.py.

Rules enforced: typed numbers live only on the Inputs sheet (blue font); every other
cell with a number is a formula (black). Each input gets a defined name in_<id> so
formulas read as =in_L1-in_L2. The Check sheet counts typed numbers outside Inputs
(must be 0) and lists every input that is an assumption or not found.
"""
import json, re, sys, os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(__file__))
import spec_v7 as spec

BLUE = Font(name="Calibri", size=10, color="0000FF")
BLACK = Font(name="Calibri", size=10, color="000000")
BOLD = Font(name="Calibri", size=11, bold=True)
TITLE = Font(name="Calibri", size=14, bold=True, color="12243E")
SUB = Font(name="Calibri", size=10, italic=True, color="555555")
HEAD_FILL = PatternFill("solid", fgColor="12243E")
HEAD_FONT = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
ASSUME_FILL = PatternFill("solid", fgColor="FBE6B8")
NF_FILL = PatternFill("solid", fgColor="F4CCCC")
WRAP = Alignment(wrap_text=True, vertical="top")

def header(ws, row, cols):
    for j, h in enumerate(cols, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = HEAD_FONT; c.fill = HEAD_FILL; c.alignment = WRAP

def build():
    wb = Workbook()
    ws = wb.active; ws.title = "README"
    for i, line in enumerate(spec.README, 1):
        ws.cell(row=i, column=1, value=line).alignment = WRAP
    ws.column_dimensions["A"].width = 120

    # Inputs
    wi = wb.create_sheet("Inputs")
    wi["A1"] = "JSW R2 inputs v7. Blue = typed input. Every figure carries its source, URL, date, claim type and confidence. Status: verified, assumption (with range), derived, not_found (left blank)."
    wi["A1"].font = SUB
    cols = ["ID", "Metric", "Figure", "Unit", "Period", "Source", "URL", "Source date", "Claim type", "Confidence", "Status", "Range low", "Range high", "Note"]
    header(wi, 3, cols)
    widths = [7, 48, 12, 16, 14, 34, 40, 12, 12, 10, 11, 10, 10, 60]
    for j, w in enumerate(widths, 1):
        wi.column_dimensions[get_column_letter(j)].width = w
    name_row = {}
    r = 4
    for inp in spec.INPUTS:
        vals = [inp["id"], inp["metric"], inp.get("figure"), inp.get("unit", ""), inp.get("period", ""),
                inp.get("source", ""), inp.get("url", ""), inp.get("source_date", ""), inp.get("claim_type", ""),
                inp.get("confidence", ""), inp.get("status", ""), inp.get("range_low"), inp.get("range_high"), inp.get("note", "")]
        for j, v in enumerate(vals, 1):
            c = wi.cell(row=r, column=j, value=v)
            c.alignment = WRAP
            c.font = BLUE if (j in (3, 12, 13) and isinstance(v, (int, float))) else BLACK
        if inp.get("status") == "assumption":
            for j in (3, 11, 12, 13): wi.cell(row=r, column=j).fill = ASSUME_FILL
        if inp.get("status") == "not_found":
            wi.cell(row=r, column=11).fill = NF_FILL
        name = "in_" + re.sub(r"[^A-Za-z0-9_]", "_", inp["id"])
        wb.defined_names[name] = DefinedName(name, attr_text=f"Inputs!$C${r}")
        if inp.get("range_low") is not None:
            wb.defined_names[name + "_lo"] = DefinedName(name + "_lo", attr_text=f"Inputs!$L${r}")
            wb.defined_names[name + "_hi"] = DefinedName(name + "_hi", attr_text=f"Inputs!$M${r}")
        name_row[inp["id"]] = r
        r += 1
    wi.freeze_panes = "C4"

    # Calculation sheets
    for sh in spec.SHEETS:
        w = wb.create_sheet(sh["name"][:31])
        w["A1"] = sh["title"]; w["A1"].font = TITLE
        w["A2"] = sh.get("subtitle", ""); w["A2"].font = SUB
        header(w, 4, ["Line", "Value", "Unit", "Excel formula (what it does)", "Inputs used", "Note"])
        w.column_dimensions["A"].width = 46; w.column_dimensions["B"].width = 14
        w.column_dimensions["C"].width = 14; w.column_dimensions["D"].width = 48
        w.column_dimensions["E"].width = 18; w.column_dimensions["F"].width = 60
        rr = 5
        rowref = {}
        for row in sh["rows"]:
            if row.get("section"):
                c = w.cell(row=rr, column=1, value=row["section"]); c.font = BOLD; rr += 1; continue
            w.cell(row=rr, column=1, value=row["label"]).alignment = WRAP
            f = row["excel"]
            # resolve {ROWKEY} references to this sheet's cells
            f = re.sub(r"\{([A-Za-z0-9_]+)\}", lambda m: f"B{rowref[m.group(1)]}", f)
            c = w.cell(row=rr, column=2, value="=" + f); c.font = BLACK
            if row.get("fmt"): c.number_format = row["fmt"]
            w.cell(row=rr, column=3, value=row.get("unit", ""))
            w.cell(row=rr, column=4, value=row.get("explain", "")).alignment = WRAP
            w.cell(row=rr, column=5, value=", ".join(re.findall(r"in_([A-Za-z0-9_]+)", f)))
            w.cell(row=rr, column=6, value=row.get("note", "")).alignment = WRAP
            if row.get("key"): rowref[row["key"]] = rr
            rr += 1
        # optional chart data block and chart
        if sh.get("chart"):
            ch = sh["chart"]; r0 = rr + 2
            w.cell(row=r0, column=1, value=ch["title"]).font = BOLD
            header(w, r0 + 1, ["Category", ch["value_label"]])
            for k, (cat, key) in enumerate(ch["series"], 1):
                w.cell(row=r0 + 1 + k, column=1, value=cat)
                w.cell(row=r0 + 1 + k, column=2, value=f"=B{rowref[key]}").font = BLACK
            bar = BarChart(); bar.type = "bar"; bar.title = ch["title"]; bar.style = 10
            bar.y_axis.title = ch["value_label"]
            data = Reference(w, min_col=2, min_row=r0 + 1, max_row=r0 + 1 + len(ch["series"]))
            cats = Reference(w, min_col=1, min_row=r0 + 2, max_row=r0 + 1 + len(ch["series"]))
            bar.add_data(data, titles_from_data=True); bar.set_categories(cats)
            bar.height = 8; bar.width = 18
            w.add_chart(bar, f"D{r0}")

    # Check sheet
    wc = wb.create_sheet("Check")
    wc["A1"] = "Build checks"; wc["A1"].font = TITLE
    typed = 0
    for w in wb.worksheets:
        if w.title in ("Inputs", "Check"): continue
        for row in w.iter_rows():
            for c in row:
                if isinstance(c.value, (int, float)) and not isinstance(c.value, bool):
                    typed += 1
    wc["A3"] = "Typed numbers outside Inputs (must be 0)"; wc["B3"] = typed
    wc["A4"] = "Inputs marked assumption"; wc["B4"] = sum(1 for i in spec.INPUTS if i.get("status") == "assumption")
    wc["A5"] = "Inputs not found (left blank)"; wc["B5"] = sum(1 for i in spec.INPUTS if i.get("status") == "not_found")
    wc["A6"] = "Inputs verified"; wc["B6"] = sum(1 for i in spec.INPUTS if i.get("status") == "verified")
    wc["A8"] = "Assumptions and gaps"; wc["A8"].font = BOLD
    rr = 9
    for i in spec.INPUTS:
        if i.get("status") in ("assumption", "not_found"):
            wc.cell(row=rr, column=1, value=i["id"]); wc.cell(row=rr, column=2, value=i["metric"])
            wc.cell(row=rr, column=3, value=i.get("status")); wc.cell(row=rr, column=4, value=f"{i.get('range_low')} to {i.get('range_high')}" if i.get("range_low") is not None else "")
            rr += 1
    wc.column_dimensions["A"].width = 40; wc.column_dimensions["B"].width = 60
    out = os.path.join(os.path.dirname(__file__), "..", "outputs", "JSW_R2_workbook_v7.xlsx")
    wb.save(out)
    print("saved", os.path.abspath(out), "typed numbers outside Inputs:", typed)

if __name__ == "__main__":
    build()
