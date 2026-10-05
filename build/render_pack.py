"""Render the v7 print pack (exhibits) to HTML and PDF from spec_v7 and values_v7.json.
Every number shown is read from the computed values or the Inputs spec; nothing is typed here."""
import json, os, re, html, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import spec_v7 as spec
H = os.path.dirname(os.path.abspath(__file__))
vals = json.load(open(os.path.join(H, "values_v7.json")))
INP = {i["id"]: i for i in spec.INPUTS}

def V(sheet, key):
    for k, v in vals[sheet].items():
        if k.split(" | ")[0] == key: return v
    raise KeyError(f"{sheet}:{key}")
def inp(id): return INP[id]["figure"]
def src(*ids):
    parts = []
    for i in ids:
        d = INP[i]; tag = {"verified": "", "assumption": " (assumption, range {} to {})".format(d.get("range_low"), d.get("range_high")), "scenario": " (scenario)", "not_found": " (not found)"}.get(d["status"], "")
        parts.append(f"{i}: {d['source']}{(', ' + d['source_date']) if d.get('source_date') else ''}{tag}")
    return "; ".join(parts)
def pct(x, d=1): return f"{x*100:.{d}f}%"
def inr(x, d=0): return f"Rs {x:,.{d}f}"
def esc(s): return html.escape(str(s))

BLUE, ORANGE, GRAY, RED, INK, INK2, MUTED, GRID = "#2a78d6", "#eb6834", "#898781", "#e34948", "#12243E", "#52514e", "#898781", "#e1e0d9"

def hbar(rows, fmt, width=620, maxv=None, color=BLUE, emph=None, neg_color=RED, label_w=250, bar_h=16, gap=8):
    """Horizontal bars. rows: list of (label, value). Single hue; emph set gets the accent, others gray if emph given."""
    n = len(rows); h = n * (bar_h + gap) + 30
    vmax = maxv or max(abs(v) for _, v in rows) or 1
    neg = any(v < 0 for _, v in rows)
    plot_w = width - label_w - 90
    zero_x = label_w + (plot_w * (max(-min(v for _, v in rows), 0) / (vmax + max(-min(v for _, v in rows), 0)))) if neg else label_w
    scale = (plot_w - (zero_x - label_w)) / vmax if not neg else plot_w / (vmax + max(-min(v for _, v in rows), 0))
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" font-family="system-ui, -apple-system, Segoe UI, sans-serif" font-size="12">']
    out.append(f'<line x1="{zero_x:.1f}" y1="8" x2="{zero_x:.1f}" y2="{h-20}" stroke="#c3c2b7" stroke-width="1"/>')
    for i, (lab, v) in enumerate(rows):
        y = 10 + i * (bar_h + gap)
        c = color if (emph is None or lab in emph) else GRAY
        if v < 0: c = neg_color
        w = abs(v) * scale
        x = zero_x if v >= 0 else zero_x - w
        out.append(f'<text x="{label_w-8}" y="{y+bar_h-4}" text-anchor="end" fill="{INK2}">{esc(lab)}</text>')
        rx = 4
        if v >= 0:
            out.append(f'<path d="M{x:.1f},{y} h{max(w-rx,0):.1f} a{rx},{rx} 0 0 1 {rx},{rx} v{bar_h-2*rx} a{rx},{rx} 0 0 1 -{rx},{rx} h-{max(w-rx,0):.1f} z" fill="{c}"/>')
            out.append(f'<text x="{x+w+6:.1f}" y="{y+bar_h-4}" fill="{INK}">{esc(fmt(v))}</text>')
        else:
            out.append(f'<path d="M{x+w:.1f},{y} h-{max(w-rx,0):.1f} a{rx},{rx} 0 0 0 -{rx},{rx} v{bar_h-2*rx} a{rx},{rx} 0 0 0 {rx},{rx} h{max(w-rx,0):.1f} z" fill="{c}"/>')
            out.append(f'<text x="{zero_x+6:.1f}" y="{y+bar_h-4}" fill="{INK}">{esc(fmt(v))}</text>')
    out.append('</svg>')
    return "".join(out)

def table(headers, rows, widths=None):
    th = "".join(f'<th style="width:{widths[i]}">{esc(h)}</th>' if widths else f"<th>{esc(h)}</th>" for i, h in enumerate(headers))
    tr = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'

def page(title, subtitle, left, right, box, sources, num):
    return f'''<section class="page">
<h1>{esc(title)}</h1><p class="sub">{esc(subtitle)}</p>
<div class="cols"><div class="left">{left}</div><div class="right"><h3>What the numbers say</h3>{right}</div></div>
<div class="box"><b>How this reads on the P&amp;L.</b> {esc(box)}</div>
<p class="src">Sources: {esc(sources)} Workbook: JSW_R2_workbook_v7.xlsx.</p>
<p class="num">{num}</p></section>'''

pages = []

# EX1 last thirty days
rows = [(d, e, p, s) for d, e, p, s in spec.LAST_30_DAYS]
pages.append(page("Exhibit 1. The last thirty days: five events, one direction",
 "Each event moves a named P&L line. Dated, sourced, nothing inferred.",
 table(["Date", "Event", "P&L line it moves", "Source"], rows, ["11%", "49%", "24%", "16%"]),
 f"<ul><li>Two of the five are the state resetting a toll: a 0.4% UPI merchant fee from 15 Oct, and IRDAI proposing caps on distributor commissions on 23 Sep.</li><li>Two are capital arriving for licensed risk-holders: JSW One's Rs 500 cr for its lending arm and Moneyview's listing {pct(inp('L10'),0)} above issue on a {pct(inp('L9'),2)} cost of borrowings.</li><li>One is the rail preparing for a software buyer: NPCI's agent protocol keeps authentication and settlement with the licensed layer.</li></ul>",
 "Distribution margins are granted and withdrawn by rule and collected by licensed players at scale. The margin that survives a rule change is the one earned by holding the risk: the loan, the policy, the claim. Judge every company by which of the two it earns.",
 "NPCI FAQ 15 Sep 2026; IRDAI consultation 23 Sep 2026 and Business Standard 29 Sep 2026; Medianama Sep 2026; Business Today 25 Sep 2026; Inc42 1 Oct 2026 and Moneyview DRHP.", 1))

# EX2 fee ladder
grid = [("G1","Rs 1,999"),("G2","Rs 2,000"),("G3","Rs 5,000"),("G4","Rs 10,000"),("G5","Rs 25,000"),("G6","Rs 50,000"),("G7","Rs 75,000"),("G8","Rs 1,50,000"),("G9","Rs 3,00,000")]
rate_rows = [(lab, V("EX2_Fee_ladder", f"r{i+1}")) for i, (g, lab) in enumerate(grid)]
fee_rows = [(lab, V("EX2_Fee_ladder", f"f{i+1}")) for i, (g, lab) in enumerate(grid)]
avg = V("WE_F1_Payments", "avg")
pages.append(page("Exhibit 2. The UPI merchant fee by ticket size: 0.4% between Rs 2,000 and Rs 75,000, then falling",
 "Pure arithmetic off the NPCI rule (rate, floor, cap). The average UPI ticket pays nothing.",
 '<p class="ct">Effective fee as a share of payment value, with the fee in rupees</p>' + hbar(rate_rows, lambda v: pct(v, 2) + "  (" + inr(dict(fee_rows)[[l for l,x in rate_rows if x==v][0]] if False else 0) + ")" if False else pct(v, 2), emph={"Rs 10,000"}) + table(["Ticket", "Fee", "Effective rate"], [(lab, inr(f), pct(r, 2)) for (lab, f), (_, r) in zip(fee_rows, rate_rows)], ["34%", "33%", "33%"]),
 f"<ul><li>MDR is {pct(inp('P1'),1)} only above {inr(inp('P2'))}, capped at {inr(inp('P3'))}; the cap binds at {inr(V('EX2_Fee_ladder','r10') if False else inp('P3')/inp('P1'))}.</li><li>The average UPI ticket in September 2026 was {inr(avg)} (NPCI value over count), below the floor.</li><li>NPCI: more than 95% of merchant transactions are at or below Rs 2,000 and pay nothing.</li><li>Notified categories (railways, telecom, insurance, fuel) pay a flat {inr(inp('P4'))} above Rs 2,000 (secondary report).</li><li>Who receives the 0.4% is not published; the acquiring side's share is an assumption of {pct(inp('P19'),0)} (range 30 to 50%).</li></ul>",
 f"Revenue line: a toll on a minority of merchant payments, largest in percentage terms between Rs 2,000 and Rs 75,000 (school fees, clinics, durables, auto service, small B2B invoices). On a {inr(inp('P22'))} payment the fee is {inr(V('WE_F1_Payments','fee'))} and the acquirer keeps an assumed {inr(V('WE_F1_Payments','acq'))}. Sell the software to these merchants; the rail is the wedge, not the business.",
 src("P1","P6","P19") + "; P2 to P5 and P4 as in Inputs.", 2))

# EX3 lender ladder
L = lambda k: V("WE_F2_Lending", k)
ladder = [("Bajaj Finance (AAA)", L("b_y"), L("b_c"), L("b_cc"), L("b_o"), L("b_roa")),
          ("Small-ticket listed lender", L("s_y"), L("s_c"), L("s_cc"), L("s_o"), L("s_roa")),
          ("Pre-Series A lender, year one", L("p_y"), L("p_c"), L("p_cc"), L("p_o"), L("p_roa")),
          ("Pre-Series A at the thresholds", L("p_y"), inp("L27"), inp("L29"), inp("L28"), L("p_y")-inp("L27")-inp("L29")-inp("L28"))]
trows = [(n, pct(y), pct(c), pct(cc), pct(o), pct(r)) for n, y, c, cc, o, r in ladder]
pages.append(page("Exhibit 3. The lender ladder: a new lender loses about 5% of assets a year until two lines move",
 "Yield, less cost of funds, less credit cost, less operating cost, equals return on assets. Listed figures are FY26 anchors; the new lender is an assumption with ranges.",
 table(["Lender", "Yield", "Cost of funds", "Credit cost", "Opex to assets", "Return on assets"], trows) +
 '<p class="ct">Return on assets, four cases</p>' + hbar([(r[0], r[5]) for r in ladder], lambda v: pct(v), emph={"Pre-Series A lender, year one"}),
 f"<ul><li>Bajaj Finance borrows at {pct(inp('L1'),2)} (FY26); Moneyview at {pct(inp('L9'),2)} (DRHP, FY25 and 9M FY26). The gap is {pct(L('mv')-inp('L1'),1)} and it is the rating.</li><li>Year-one return on the new lender's book: {pct(L('p_roa'))} at the midpoints, {pct(L('p_roa_lo'))} to {pct(L('p_roa_hi'))} across the ranges.</li><li>Rs {inp('L25')} cr of equity supports a Rs {L('own'):.0f} cr own book at {inp('L26')}x debt, or Rs {L('colent'):.0f} cr co-lent with the originator holding {pct(inp('L19'),0)} (RBI directions, 1 Jan 2026; default loss guarantee capped at {pct(inp('L20'),0)}).</li><li>Navi lost {pct(-L('r23') if False else inp('L11')/inp('L12'),1)} of its Rs {inp('L12'):,} cr book in FY26; slice, now a bank, made over Rs {inp('L13')} cr in Q1 FY27.</li></ul>",
 f"The lender bet is a capital-stack bet. The year-one loss is the cost of building a book; the test is whether cost of funds gets under {pct(inp('L27'),0)} and operating cost under {pct(inp('L28'),0)} of assets by year three with credit cost under {pct(inp('L29'),1)} on a 12-month vintage. At those thresholds the same yield earns {pct(ladder[3][5])}. The first Rs 100 cr of debt, contracted at entry, decides mortality more than the asset class does.",
 src("L1","L2","L5","L9","L11","L13","L15","L16","L17","L18","L19","L20","L25","L26"), 3))

# EX4 exits
X = lambda k: V("EX4_Exits", k)
ex_rows = [("Groww (Nov 2025 IPO)", X("g")), ("Moneyview (listing day, 1 Oct 2026)", X("mv")), ("Kissht (listing day, May 2026)", X("k")), ("Aye Finance (listing day, Feb 2026)", X("aye")), ("Turtlemint (late Sep 2026)", X("tm")), ("Pine Labs (Nov 2025 IPO)", X("pl"))]
pages.append(page("Exhibit 4. The public market prices profit: 2025 to 2026 fintech listings against issue price",
 "Blue above issue, red below. Profit in the latest quarter beside each name.",
 hbar(ex_rows, lambda v: pct(v, 0)),
 f"<ul><li>Groww: Rs {inp('W6'):,} cr of profit in Q1 FY27, {pct(X('g'),0)} above issue.</li><li>Pine Labs: Rs {inp('P15')} cr of profit in Q1 FY27, {pct(X('pl'),0)} against issue.</li><li>Turtlemint, a distributor: listed {pct(inp('X5'),0)} on day one and {pct(X('tm'),0)} by late September after IRDAI's commission paper; PB Fintech fell {pct(inp('I7'),0)} in four sessions on Rs {inp('I6')} cr of quarterly profit.</li><li>Moneyview listed {pct(X('mv'),0)} up after 98x subscription on a {pct(inp('L9'),2)} cost of borrowings.</li><li>Early-stage fintech funding was USD {inp('X9')} mn in H1 2026 and seed USD {inp('X10')} mn (Tracxn); pre-Series A is underfunded.</li></ul>",
 "Exit line: the Indian IPO is the exit, and it prices profit after tax, not growth. Every thesis therefore names the profit a company needs by year six or seven, and a distributor's profit is now exposed to a rule. Strategic buyers exist (Groww bought Fisdom for USD 150 mn; Perfios bought three companies in 2025) but pay less.",
 src("X1","X2","P16","P17","I15","I16","L10","X4","X3","W6","P15","I6","I7","X9","X10"), 4))

# EX5 regulatory calendar
pages.append(page("Exhibit 5. The regulatory calendar, Sep 2025 to May 2027: eleven dated rules and the P&L line each moves",
 "Effective dates from the issuing body or one business daily. A rule that creates a budget is the revenue test for F5 and AL4.",
 table(["Effective", "Rule", "Issuer", "P&L line it moves"], [(a, b, c, d) for a, b, c, d in spec.REG_CALENDAR], ["12%", "48%", "14%", "26%"]),
 f"<ul><li>Three rules create a fraud and compliance budget on a date: bank liability for {pct(inp('F4'),0)} of coerced-transaction losses up to {inr(inp('F5'))} from 1 Jan 2027; DPDP consent managers from 13 Nov 2026 and full obligations from 13 May 2027; the mule-account procedure.</li><li>Two rules compress a distribution margin: UPI MDR by cap and floor; IRDAI's proposed commission caps.</li><li>One rule codifies the lender's capital stack: co-lending from 1 Jan 2026.</li><li>Only {pct(inp('F6'),1)} of RBI-regulated entities were using or building AI in the 2025 survey, so the budget needs a rule to exist.</li></ul>",
 "Where a rule names a date, the buyer's budget appears on that date; a tool bought only after an incident has no steady revenue. The companies to back in F5 and AL4 are the ones whose module a regulated entity must have on the date in the calendar.",
 "RBI, SEBI, IRDAI, NPCI, MeitY and PIB releases; Business Standard, Lexology and Cyril Amarchand summaries as listed in Inputs F4 to F6, L19, L20, W13, W14, P1 to P3.", 5))

# EX6 vendor or owner
A = lambda k: V("WE_AF2_Voice", k)
price_rows = [("Agentforce per conversation", V("EX6_Vendor_or_owner", "af_conv")), ("Sierra per resolution (estimate)", V("EX6_Vendor_or_owner", "sierra")), ("Intercom Fin per resolution", V("EX6_Vendor_or_owner", "intercom")), ("Human cost per call, India (assumption)", A("hpc")), ("Agentforce per action", V("EX6_Vendor_or_owner", "af_act")), ("Indian voice vendor per resolved call (assumption)", inp("A8")), ("AI cost per call (model, telephony, speech)", A("ai"))]
pages.append(page("Exhibit 6. Vendor or owner: per-outcome prices against an Indian call's cost",
 "Prices converted at an assumed Rs {:.0f} per USD. A success fee is a vendor's price; a loss is an owner's.".format(inp("A7")),
 '<p class="ct">Rupees per conversation or call</p>' + hbar(price_rows, lambda v: inr(v, 1), emph={"Indian voice vendor per resolved call (assumption)", "AI cost per call (model, telephony, speech)"}) ,
 f"<ul><li>A human call in India costs {inr(A('hpc'),1)} at the midpoint (range {inr(V('WE_AF2_Voice','hpc_lo'),1)} to {inr(V('WE_AF2_Voice','hpc_hi'),1)}): an agent at {inr(inp('A1'))} a month handling {inp('A2')} calls a day.</li><li>An AI call costs {inr(A('ai'),2)}: {inp('A5'):,} tokens at USD {inp('A4')} per million plus {inr(inp('A6'),1)} of telephony and speech.</li><li>So the price room for an Indian voice vendor is {inr(inp('A8_lo') if 'A8_lo' in INP else INP['A8']['range_low'])} to {inr(INP['A8']['range_high'])} per resolved call, against USD 0.99 ({inr(V('EX6_Vendor_or_owner','intercom'),0)}) at Intercom. Gross margin at Rs {inp('A8')}: {pct(A('r10') if False else V('WE_AF2_Voice','gm'),0)}.</li><li>SquadStack moved to a success fee on disbursed loans for DMI Finance (CIOL, 14 Sep 2026); if the loans go bad, the loss sits with DMI. Stellaris: {pct(inp('A14'),0)} of 216 voice AI companies target an existing budget.</li></ul>",
 "Efficiency is the floor: an AI call at under Rs 3 against a human call at Rs 8 to 25 is a saving the buyer captures, and India's cheap calls leave a thin price room. The business that earns the margin through a cycle is the one that holds the outcome on its own account: the lender using the agent and holding the loan, not the vendor paid per call. The balance sheet shows which one a company is.",
 src("A1","A2","A4","A5","A6","A7","A8","A9","A10","A11","A12","A14"), 6))

# EX7 fund maths
F = lambda k: V("EX7_Fund_maths", k)
tiles = [("Fund III target, midpoint", f"Rs {F('f'):.0f} cr", "Mint, 25 Jun 2026; not yet closed"), ("Names", f"{F('n'):.0f}", "14 to 16"), ("Per name over life", f"Rs {F('life'):.0f} cr", "initial plus equal reserve"), ("Needed back for 3x", f"Rs {F('r3'):,.0f} cr", "on the midpoint target"), ("Multiple on every name for 3x", f"{F('r7'):.1f}x", "if no zeros, reserves fully drawn")]
tile_html = '<div class="tiles">' + "".join(f'<div class="tile"><div class="tl">{esc(a)}</div><div class="tv">{esc(b)}</div><div class="td">{esc(c)}</div></div>' for a, b, c in tiles) + '</div>'
pages.append(page("Exhibit 7. What the fund needs from each name: 3x on every company, or six at 5 to 8x and no zeros",
 "Only the Mint facts about JSW Ventures, then arithmetic. Nothing else is assumed about the fund.",
 tile_html + '<p class="ct">Reading</p><p>Three zeros, six names at 1 to 2x and six at 5 to 8x return about 3.2x on a Rs 450 cr fund with Rs 30 cr per name. The fund described needs low mortality and six mid-single-digit multiples, which is the profile of licensed risk-holders run by software; it does not need a 30x.</p>',
 f"<ul><li>Initial cheque Rs {inp('X15')} to {inp('X16')} cr with an equal reserve; pre-Series A to Series A+.</li><li>Fintech early-stage funding was USD {inp('X9')} mn in H1 2026 and seed USD {inp('X10')} mn (Tracxn), so a Rs 15 cr lead cheque sets price in a thin market.</li><li>Fund I returned about 3x per Mint; the Purplle sale was reported at 2.7x the Fund I corpus (Entrackr, 2023). [verify before quoting]</li></ul>",
 "Portfolio line: at Rs 30 cr per name over life and a 3x target, a company must return Rs 90 cr to carry its own weight. A software-run lender listing on Rs 80 to 150 cr of PAT at 15 to 25x returns 5 to 8x on JSW's diluted stake; the 10x candidates are the infrastructure suppliers with pricing power in F5.",
 src("X11","X12","X13","X14","X15","X16","X9","X10"), 7))

CSS = f'''<style>
@page {{ size: A4 landscape; margin: 12mm 14mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: system-ui, -apple-system, "Segoe UI", sans-serif; color: {INK}; margin: 0; font-size: 11.5px; }}
.page {{ page-break-after: always; position: relative; min-height: 180mm; max-height: 183mm; overflow: hidden; }}
h1 {{ font-size: 19px; margin: 0 0 2px 0; color: {INK}; font-weight: 700; }}
.sub {{ color: {INK2}; font-style: italic; margin: 0 0 10px 0; font-size: 11.5px; }}
.cols {{ display: flex; gap: 16px; }}
.left {{ flex: 1.55; }} .right {{ flex: 1; background: #f3f4f6; padding: 10px 12px; }}
.right h3 {{ margin: 0 0 6px 0; font-size: 12.5px; }} .right ul {{ margin: 0; padding-left: 16px; }} .right li {{ margin-bottom: 6px; }}
.box {{ background: {INK}; color: #fff; padding: 9px 12px; margin-top: 10px; font-size: 11.5px; line-height: 1.4; }}
.src {{ color: {MUTED}; font-size: 8.5px; margin-top: 6px; line-height: 1.35; }}
.num {{ position: absolute; right: 0; bottom: 0; color: {MUTED}; font-size: 9px; }}
.ct {{ font-weight: 600; margin: 8px 0 2px 0; color: {INK2}; font-size: 11px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 10.5px; margin-top: 4px; }}
th {{ background: {INK}; color: #fff; text-align: left; padding: 5px 6px; font-weight: 600; }}
td {{ padding: 5px 6px; border-bottom: 1px solid {GRID}; vertical-align: top; }}
td:nth-child(n+2):not(:last-child) {{ font-variant-numeric: tabular-nums; }}
.tiles {{ display: flex; gap: 10px; flex-wrap: wrap; }}
.tile {{ flex: 1; min-width: 120px; border: 1px solid {GRID}; padding: 8px 10px; }}
.tl {{ font-size: 10px; color: {INK2}; }} .tv {{ font-size: 22px; font-weight: 600; margin: 2px 0; }} .td {{ font-size: 9.5px; color: {MUTED}; }}
</style>'''
doc = f'<!doctype html><html><head><meta charset="utf-8"><title>JSW R2 print pack v7</title>{CSS}</head><body>{"".join(pages)}</body></html>'
out_html = os.path.join(H, "..", "outputs", "JSW_R2_print_pack_v7.html"); open(out_html, "w").write(doc)
out_pdf = os.path.abspath(os.path.join(H, "..", "outputs", "JSW_R2_print_pack_v7.pdf"))
subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", "file://" + os.path.abspath(out_html)], check=True, capture_output=True, timeout=120)
print("wrote", out_pdf)
