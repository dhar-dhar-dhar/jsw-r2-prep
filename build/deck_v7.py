"""Render the v7 reference deck (HTML to PDF). Every number is read from values_v7.json or the Inputs spec."""
import json, os, html, subprocess, sys
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
def lo(id): return INP[id]["range_low"]
def hi(id): return INP[id]["range_high"]
def pct(x, d=1): return f"{x*100:.{d}f}%"
def inr(x, d=0): return f"Rs {x:,.{d}f}"
def esc(s): return html.escape(str(s))
INK = "#12243E"; INK2 = "#52514e"; MUTED = "#898781"; GRID = "#e1e0d9"; BLUE = "#2a78d6"; PANEL = "#f3f4f6"; AMBER = "#fbe6b8"; TEAL = "#d4e5ea"

def slide(title, sub, body, foot, num):
    return f'<section class="slide"><h1>{esc(title)}</h1><p class="sub">{esc(sub)}</p>{body}<p class="foot">{esc(foot)}</p><p class="num">{num}</p></section>'
def table(headers, rows, widths=None, cls=""):
    th = "".join(f'<th style="width:{widths[i]}">{esc(h)}</th>' if widths else f"<th>{esc(h)}</th>" for i, h in enumerate(headers))
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
def box(title, text, bg=PANEL): return f'<div class="bx" style="background:{bg}"><b>{esc(title)}</b> {text}</div>'
def card(head, lines, bg="#fff"):
    return f'<div class="card"><div class="ch">{esc(head)}</div><div class="cb" style="background:{bg}">' + "".join(f"<p>{l}</p>" for l in lines) + "</div></div>"

F1 = lambda k: V("WE_F1_Payments", k); F2 = lambda k: V("WE_F2_Lending", k); F3 = lambda k: V("WE_F3_Insurance", k)
F4 = lambda k: V("WE_F4_Wealth", k); F5 = lambda k: V("WE_F5_Fraud_identity", k); AF2 = lambda k: V("WE_AF2_Voice", k)
AF1 = lambda k: V("WE_AF1_Finance_agents", k); EX7 = lambda k: V("EX7_Fund_maths", k)
pre_roa_thr = F2("p_y") - inp("L27") - inp("L29") - inp("L28")
JSW = "JSW facts (Mint, 25 Jun 2026): Fund III target Rs 400 to 500 cr, not yet closed; 14 to 16 companies; pre-Series A to Series A+; initial cheque Rs 10 to 20 cr with an equal reserve; Fund II about Rs 280 cr. Nothing else about JSW is assumed. Fundable calls are my reasoning."

S = []
# 1 Title and the view
S.append(slide("Fintech and AI, read through the P&L: the margin sits with the licensed risk-holder run by software",
 "Five fintech sub-sectors and the AI stack, one worked P&L each. The numbers first, then the claim, then what has to be true. Discussion document for JSW Ventures, 5 Oct 2026.",
 f'''<div class="cols"><div class="l2">
<p class="lead">In the last thirty days the state reset two tolls and the market paid for one profit. UPI merchant payments carry a {pct(inp("P1"),1)} fee above {inr(inp("P2"))}, capped at {inr(inp("P3"))}, from 15 October (NPCI). IRDAI proposed caps on what an insurance distributor may earn on 23 September, and PB Fintech lost {pct(inp("I7"),0)} in four sessions. Moneyview listed {pct(inp("L10"),0)} above issue on 1 October on a {pct(inp("L9"),2)} cost of borrowings. Read through the ladder, these say one thing: revenue that is a toll on distribution is granted and withdrawn by rule and collected by licensed players at scale; revenue that is a yield or a premium survives if credit cost and claims are controlled. The investable company holds the risk on a licensed book and runs the operation with software instead of branches and agents. The AI argument is the same test from the other side: software earns the margin only where it holds the outcome.</p>
<p class="lead2">What this rules out: standalone payments, consumer apps, broking, insurance and wealth distribution, unlicensed neobanks, per-seat software that makes a bank's process cheaper, horizontal AI tools.</p>
</div><div class="r2">
{table(["The last thirty days", "P&L line"], [(f"<b>{d}</b> {e}", p) for d, e, p, s in spec.LAST_30_DAYS], ["72%", "28%"], "small")}
</div></div>''', JSW, 1))

# 2 The ladder
S.append(slide("The ladder I use on every segment, and where AI touches it",
 "What is left after each cost, read top to bottom. CM1 to CM3 are my convention; companies define them differently, so ask which one a company means.",
 f'''<div class="cols"><div class="l2">
{table(["Line", "Meaning", "Quality looks like"], [
 ("<b>Revenue</b>", "What the customer pays", "Recurs, grows with use, priced on value not cost; net of pass-through (interchange, model bill)"),
 ("<b>Gross margin</b>", "Less the direct cost of delivering it", "Rises as volume grows; flat means a reseller"),
 ("<b>CM1</b>", "Less the variable cost of serving one unit", "Positive on day one"),
 ("<b>CM2</b>", "Less the cost of keeping the customer: support, onboarding, collections, review", "Falls per unit as software replaces people"),
 ("<b>CM3</b>", "Less the cost of winning the customer: sales, marketing, partner payouts", "Each new customer pays back inside 18 months"),
 ("<b>EBITDA</b>", "Less fixed cost: technology, risk, compliance, management", "Shows whether scale pays")], ["14%", "40%", "46%"])}
</div><div class="r2">
{box("Lender or insurer.", f"The first test is risk-adjusted: yield less cost of funds less credit cost; premium less claims. Bajaj Finance borrows at {pct(inp('L1'),2)}, Moneyview at {pct(inp('L9'),2)}; the gap is the rating, and a model edge that a higher cost of funds eats earns nothing.")}
{box("Pass-through businesses.", "Judge net revenue. A payment aggregator's gross revenue is mostly the bank's and the network's bill; an AI tooling company's gross revenue is mostly the model vendor's.")}
{box("Where AI touches the ladder.", "Cost side (CM2): AI removes work in support, review, collections, and a cheaper model hands that saving to the buyer. Revenue side: AI helps the customer approve, convert, retain, and protects price. In my task map of 96 cells, 58 are coded cost-side and 40 revenue-side, 21 both; these are my codes, not data. The line that matters is who carries the outcome: a vendor paid per call, or an owner holding the loan.", TEAL)}
</div></div>''', "Reasoning (ladder); Task_Map in the workbook (judgement). Definitions: yield = interest and fees as a share of loans; cost of funds = interest paid as a share of borrowings; credit cost = losses and provisions as a share of loans.", 2))

# 3 Fintech map
rows3 = [
 ("<b>F1 Payments</b>", f"A {inr(inp('P22'))} UPI payment: fee {inr(F1('fee'))}, acquirer keeps an assumed {inr(F1('acq'))}; the average ticket ({inr(F1('avg'))}) pays nothing", f"Net take rate 0.1 to 0.3% (assumption); {inr(inp('P23'))} cr of monthly net revenue needs Rs 333 to 1,000 cr of volume above the floor", "Fails standalone; passes as a wedge inside vertical software for Rs 2,000 to 75,000 tickets", "Payments above 40% of revenue by year three", "M&A by listed acquirers; Pine Labs trades 22% below issue"),
 ("<b>F2 Lending</b>", f"Rs 100 of loans: new lender earns {pct(F2('p_roa'))} on assets in year one ({pct(F2('p_roa_lo'))} to {pct(F2('p_roa_hi'))}); Bajaj earns {pct(F2('b_roa'))}", f"Cost of funds under {pct(inp('L27'),0)}, opex under {pct(inp('L28'),0)} of assets by year three, credit cost under {pct(inp('L29'),1)}; then the same yield earns {pct(pre_roa_thr)}", "Passes in one asset class where repayment is controlled by the rail and the first Rs 100 cr of debt is contracted at entry", "Opex to assets over 4% by year three; credit cost over 2.5%; no co-lending or DFI line in 12 months", f"IPO prices profit: Moneyview +{pct(inp('L10'),0)} on debut, Aye flat"),
 ("<b>F3 Insurance</b>", f"A {inr(inp('I1'))} health policy: first-year commission {inr(F3('fy'))}, half to marketing; year two {inr(F3('y2'))} at {pct(inp('I4'),0)} persistency", f"Renewal share above 50% of three-year commission (today {pct(F3('ren_share'))}); claims software at {inr(inp('I13'))} per claim against the insurer's {inr(inp('I14'))}", "Passes on claims and underwriting infrastructure and embedded covers; fails on distribution (IRDAI caps proposed 23 Sep)", "Renewals under 80%; revenue tied to a commission rate the regulator is capping", f"PB Fintech −{pct(inp('I7'),0)} in four sessions; Acko and InsuranceDekho planning IPOs"),
 ("<b>F4 Wealth</b>", f"Rs 5 lakh investor: trail {inr(F4('trail'))} a year, advice {inr(F4('adv'))}, alternatives {inr(F4('alt'))}; acquisition paid back in {F4('pb1'):.0f}, {F4('pb2'):.0f}, {F4('pb3'):.0f} months", f"Revenue at least {pct(inp('W19'),1)} of assets, recurring, payback inside {inp('W20')} months; execution is won (Groww Rs {inp('W6'):,} cr Q1 PAT), F&O traders −{pct(-inp('W12'),0)}", "Passes only on manufacturing alternatives (SIF Rs 31,175 cr in 18 months) with captive distribution; fails on execution, MF distribution, advice", "Revenue to assets under 0.6%; distribution rented from others", "Groww bought Fisdom (USD 150 mn); IPO"),
 ("<b>F5 Fraud, identity</b>", f"One check: price {inr(inp('F1'))} (range {inr(lo('F1'))} to {inr(hi('F1'))}), data fee {inr(inp('F3'))}, gross margin {pct(F5('gm_pct'),0)} and rising with volume if the company owns the data", f"A rule creating the budget: banks pay {pct(inp('F4'),0)} of coerced losses up to {inr(inp('F5'))} from 1 Jan 2027; DPDP 13 Nov 2026 and 13 May 2027; only {pct(inp('F6'),1)} of regulated entities used AI in 2025", "Passes for named modules with a regulatory deadline: fraud and mule detection, consent pipes, collections stacks, model-risk tooling", "Top five customers over 50%; price per call falling over 20% a year", "Perfios bought three companies in 2025; Setu bought Agya in 2026"),
]
S.append(slide("Fintech: five sub-sectors, one worked unit each, one test",
 "Does the sub-sector let a company that raises Rs 10 to 20 cr become a licensed risk-holder run by software, or sell a must-have to the ones that do?",
 table(["Sub-sector", "Worked unit (numbers)", "What has to be true", "Verdict (my reasoning)", "Kill test", "Exit evidence"], rows3, ["9%", "25%", "24%", "18%", "12%", "12%"], "small"),
 "Every figure traces to the workbook Inputs sheet with source and date; ranges are assumptions. Print pack Exhibits 2 to 5 carry the charts.", 3))

# 4 F1 and F2 worked
S.append(slide("Fintech P&Ls (1 of 2): payments and lending, with the numbers in the ladder",
 "Payments is a regulated toll; lending is a capital-stack bet. The one line I would judge each on is in the amber box.",
 f'''<div class="cols">
{card("Payments and money movement (F1)", [
 f"<b>Revenue.</b> MDR {pct(inp('P1'),1)} on merchant payments above {inr(inp('P2'))}, cap {inr(inp('P3'))} (binds at {inr(inp('P3')/inp('P1'))}), from 15 Oct 2026. On {inr(inp('P22'))}: {inr(F1('fee'))}. On the {inr(F1('avg'))} average ticket (NPCI Sept 2026: Rs 29.37 lakh cr over 24,068 mn): nothing. More than 95% of merchant transactions pay nothing (NPCI).",
 f"<b>Who keeps it.</b> Not published. Acquiring side assumed at {pct(inp('P19'),0)} (30 to 50%): {inr(F1('acq'))} on the example payment. Net take rate after pass-through 0.1 to 0.3% (assumption).",
 f"<b>Costs.</b> Interchange, scheme and bank fees passed through; fraud and chargebacks {pct(inp('P21'),2)} of value (assumption); risk, compliance, engineering.",
 f"<b>Scale needed.</b> {inr(inp('P23'))} cr of monthly net revenue needs Rs 333 to 1,000 cr of monthly volume above the floor. Paytm earns {pct(F1('paytm_m'),1)} PAT margin on Rs {inp('P13'):,} cr of quarterly revenue, most of it lending distribution and devices; PhonePe lost Rs {inp('P18'):,} cr in FY26.",
 f"<b>Fundable?</b> Only as a wedge inside vertical software for merchants with Rs 2,000 to 75,000 tickets, where the toll is largest in percentage terms."]) }
{card("Lending and credit infrastructure (F2)", [
 f"<b>Ladder, Rs 100 of loans.</b> New lender year one: yield {pct(inp('L15'),0)}, cost of funds {pct(inp('L16'),1)}, credit cost {pct(inp('L17'),1)}, opex {pct(inp('L18'),0)} of assets; return on assets {pct(F2('p_roa'))} ({pct(F2('p_roa_lo'))} to {pct(F2('p_roa_hi'))}). Bajaj Finance: cost of funds {pct(inp('L1'),2)} (FY26), ROA about {pct(F2('b_roa'))}. Small-ticket listed lender: about {pct(F2('s_roa'))}.",
 f"<b>Capital stack.</b> Rs {inp('L25')} cr of equity supports a Rs {F2('own'):.0f} cr own book at {inp('L26')}x debt, or Rs {F2('colent'):.0f} cr co-lent under the directions in force since 1 Jan 2026 (originator keeps {pct(inp('L19'),0)}, default loss guarantee capped at {pct(inp('L20'),0)}). Year-one loss on the own book: Rs {-F2('yr1loss'):.1f} cr.",
 f"<b>What has to be true.</b> Cost of funds under {pct(inp('L27'),0)} and opex under {pct(inp('L28'),0)} of assets by year three, credit cost under {pct(inp('L29'),1)} on a 12-month vintage. Then the same yield earns {pct(pre_roa_thr)}. Moneyview borrows at {pct(inp('L9'),2)} (DRHP); the first Rs 100 cr of debt, contracted at entry, decides mortality.",
 f"<b>Sector.</b> Unsecured retail GNPA {pct(inp('L21'),1)} against {pct(inp('L22'),1)} secured (RBI FSR, Mar 2026); gold loans doubled to Rs {inp('L24')/100000:.2f} lakh cr. Navi lost {pct(inp('L11')/inp('L12'),1)} of its book in FY26; slice, now a bank, made over Rs {inp('L13')} cr in Q1 FY27.",
 f"<b>Fundable?</b> Yes, in one asset class where repayment is controlled by the rail (device locks, employer or institution deduction, UPI autopay on receivables), not by people. StrideOne is the in-house precedent."]) }
</div>
<div class="cols"><div class="amber">Judge payments on net take rate and the share of revenue that is not volume. If net revenue grows faster than volume, the company sells something above the rail.</div><div class="amber">Judge lending on credit cost by vintage against cost of funds. A model edge that a higher cost of funds eats earns nothing.</div></div>''',
 "Inputs P1 to P23, L1 to L32. Ranges are assumptions; FY26 figures for Bajaj and the small-ticket lender beyond cost of funds are pending verification against the results presentations.", 4))

# 5 F3 F4 F5 worked
S.append(slide("Fintech P&Ls (2 of 2): insurance, wealth, fraud and identity",
 "Same ladder, different line decides each one.",
 f'''<div class="cols3">
{card("Insurance (F3)", [
 f"<b>Distributor, {inr(inp('I1'))} health policy.</b> First-year commission {pct(inp('I2'),1)} ({inr(F3('fy'))}), of which {pct(inp('I5'),0)} goes to marketing and payouts; renewal {pct(inp('I3'),1)} at {pct(inp('I4'),0)} persistency gives {inr(F3('y2'))} in year two. Renewal share of three-year commission: {pct(F3('ren_share'),0)}. All ranges are assumptions; the IRDAI paper of 23 Sep proposes to cap the first number.",
 f"<b>Carrier.</b> Premium less claims less expenses. Digit's Q1 FY27 profit fell {pct(-inp('I8'),0)} as claims rose; Acko turned profitable at Rs {inp('I10')} cr in FY26. Individual health premiums grew {pct(inp('I11'),1)} in Oct to Mar FY26 after GST went to zero.",
 f"<b>Claims software.</b> {inr(inp('I13'))} per claim (range {inr(lo('I13'))} to {inr(hi('I13'))}) against the insurer's own {inr(inp('I14'))}; price at {pct(F3('pc_share'),0)} of the insurer's cost.",
 "<b>Fundable?</b> Claims and underwriting infrastructure, embedded covers with retention economics. Not a distributor whose revenue is a commission rate under consultation."]) }
{card("Wealth and capital markets (F4)", [
 f"<b>Rs 5 lakh investor.</b> Trail {pct(inp('W2'),2)} of assets ({inr(F4('trail'))} a year), advice {pct(inp('W3'),2)} ({inr(F4('adv'))}), alternatives {pct(inp('W5'),1)} ({inr(F4('alt'))}). Acquisition at {inr(inp('W4'))} pays back in {F4('pb1'):.0f}, {F4('pb2'):.0f} and {F4('pb3'):.0f} months. Ranges are assumptions.",
 f"<b>Market.</b> Execution is won: Groww Rs {inp('W6'):,} cr of Q1 FY27 profit and {pct(inp('W7'),0)} above issue; Zerodha flat at a {pct(F4('zer_m'),0)} margin. {pct(inp('W11'),1)} of individual F&O traders lost money in FY26 and their number fell {pct(-inp('W12'),0)} (SEBI); STT up from 1 Apr 2026; MF Regulations 2026 halved brokerage caps. SIP Rs {inp('W15'):,} cr a month; SIF AUM Rs {inp('W16'):,} cr in 18 months.",
 f"<b>What has to be true.</b> Revenue at least {pct(inp('W19'),1)} of assets, recurring, payback inside {inp('W20')} months. No Indian firm found earning a profit on paid advice to the mass affluent.",
 "<b>Fundable?</b> Manufacturing of alternatives (SIF, AIF, PMS) with captive distribution. Not broking, not MF distribution, not advice."]) }
{card("Fraud, compliance and identity (F5)", [
 f"<b>One check.</b> Price {inr(inp('F1'))} (range {inr(lo('F1'))} to {inr(hi('F1'))}), data fee {inr(inp('F3'))}; gross margin {pct(F5('gm_pct'),0)}. A Rs {inp('F2')} cr bank contract is {F5('checks')/1e6:.1f} million checks a year.",
 f"<b>The budget, by rule.</b> Banks compensate {pct(inp('F4'),0)} of coerced-transaction losses up to {inr(inp('F5'))} from 1 Jan 2027; DPDP consent managers from 13 Nov 2026, full obligations 13 May 2027; mule-account procedure (SC Aug 2026, RBI draft Sep 2026); RBI model-risk draft (Jun 2026).",
 f"<b>Buyers.</b> Fewer than {inp('F11')} regulated entities matter (assumption); {pct(inp('F6'),1)} used or built AI in 2025 (RBI). Account Aggregator: {inp('F8')} data providers, {inp('F9'):,} data users, {inp('F7'):.0f} mn consents fulfilled (Sahamati, Jul 2026). Credgenics: Rs {inp('F10')} cr FY25 revenue.",
 f"<b>Fundable?</b> Yes, for modules a regulated entity must have on a date in the calendar, with net revenue retention above {inp('F12')}x and no customer above 20% of revenue. Resellers of others' data do not fit."]) }
</div>
<div class="cols3"><div class="amber">Judge a distributor on renewal share of revenue; a carrier on loss ratio by cohort.</div><div class="amber">Judge wealth on revenue as a share of assets versus per trade; assets-based revenue survives a quiet market.</div><div class="amber">Judge fraud and identity on gross margin as checks grow; flat means a reseller.</div></div>''',
 "Inputs I1 to I16, W1 to W20, F1 to F13. Print pack Exhibits 4 and 5.", 5))

# 6 AI map and the test
S.append(slide("AI: the layers, the markets, and the one test that survives the efficiency counter",
 "Compute and models are not fundable at this cheque; tooling and apps are, selectively. Beyond efficiency has one meaning that holds.",
 f'''<div class="cols"><div class="l2">
{table(["Layer or market", "Revenue unit", "Judge on", "Fundable at Rs 10 to 20 cr?"], [
 ("Compute (AL1)", f"Price per GPU hour: IndiaAI portal Rs {inp('A30')} to {inp('A31')}; Neysa raised USD {inp('A32'):,} mn, half debt", "Contracted utilisation against cost of capital", "No"),
 ("Foundation models (AL2)", f"Price per million tokens: USD {inp('A35')} (small) to USD {inp('A34')} (mid-tier); Sarvam raised USD {inp('A33')} mn in 2026", "Gross margin after inference as prices fall; top-customer share", "No"),
 ("Tooling: orchestration, data (AL3)", f"Platform fee plus a share of routed model spend; Databricks claims {pct(inp('A25'),0)} routing saving (vendor, coding tasks)", "Net revenue after pass-through model spend", "Selective"),
 ("Tooling: security, audit (AL4)", f"Subscription Rs {lo('A26')} to {hi('A26')} cr per regulated buyer (assumption); RBI model-risk draft creates the budget", "Whether a rule or audit creates the budget", "Yes"),
 ("Consumer apps (AC)", f"{pct(inp('A27'),1)} of US households pay (a16z, Apr 2026); Emergent earns {pct(inp('A29'),1)} of USD {inp('A28')} mn in India", "Paying share; inference per heavy user against price", "Mostly no"),
 ("Enterprise apps (AE, AF1 to AF4, AV1)", "Per seat, per unit of work, or per outcome; see next slide", "Price tied to the job, not to tokens; gross margin rising with scale", "Yes, core fit"),
 ("Physical (AP)", f"Revenue per deployed unit; payback {lo('A36')} to {hi('A36')} months (assumption)", "Payback per unit; recurring share of revenue", "Selective")], ["22%", "40%", "24%", "14%"], "small")}
</div><div class="r2">
{box("The test.", "Efficiency: the same output at lower cost or time. The buyer keeps that saving, and a cheaper model hands more of it over every quarter. Per-outcome pricing is spreading (Intercom USD 0.99 per resolution, Agentforce USD 2 per conversation) and it is a contract; Genpact and EXL have sold gain-share for years without becoming software businesses. The one meaning of beyond efficiency that holds is that the software company becomes the operator and carries the outcome on its own account, visible as a loss ratio, a claims reserve or an SLA penalty in its own accounts, and the incumbent cannot follow because of a licence, data that holds through a cycle, or a structure it cannot cannibalise.", TEAL)}
{box("The Indian case.", f"SquadStack moved its voice agents to a base fee plus a success fee on disbursed loans for DMI Finance (CIOL, 14 Sep 2026). If those loans go bad the loss sits with DMI. A success fee is a vendor's price; a loss is an owner's. The balance sheet shows which one a company is, and that is the diligence test.")}
{box("Where the market is.", f"Bessemer (Aug 2026), Stellaris (Aug 2026) and Elevation (Sep 2026) all back AI-native services priced per outcome; Hang Ten raised USD {inp('A22')} mn in seed rounds for it. Direction agreed; the stopping point is too early. Bessemer's own warning: removing people does not by itself give software margins.")}
</div></div>''', "Inputs A4, A9 to A14, A22, A25 to A36. Spoken-panel figures are labelled; a16z figures are chart values from State of Markets II (30 Sep 2026).", 6))

# 7 AI worked examples
S.append(slide("AI P&Ls: four worked units with the numbers",
 "Voice and customer operations, finance agents, AI-native services, vertical AI. Human cost is the floor the price must sit under.",
 f'''<div class="cols">
{card("Customer operations and voice (AF2): one resolved call", [
 f"<b>Human.</b> Agent at {inr(inp('A1'))} a month ({inr(lo('A1'))} to {inr(hi('A1'))}), {inp('A2')} calls a day: {inr(AF2('hpc'),1)} per call ({inr(AF2('hpc_lo'),1)} to {inr(AF2('hpc_hi'),1)}). Assumption; the deck's v6 left this blank.",
 f"<b>AI.</b> {inp('A5'):,} tokens at USD {inp('A4')} per million (Ramp, Sep 2026) is {inr(AF2('mc'),2)}; telephony and speech {inr(inp('A6'),1)}; total {inr(AF2('ai'),2)} per call.",
 f"<b>Price.</b> {inr(inp('A8'))} per resolved call ({inr(lo('A8'))} to {inr(hi('A8'))}): gross margin {pct(AF2('gm'),0)}, buyer's saving {inr(AF2('saving'),1)} per call. Intercom charges USD 0.99 ({inr(inp('A9')*inp('A7'))}); India's cheap calls leave a thin price room.",
 f"<b>Must be true.</b> Resolution at or above the human benchmark; price per job, not per token; exception staff under {pct(inp('A37'),0)} of revenue. Stellaris: {pct(inp('A14'),0)} of 216 voice companies target an existing budget."]) }
{card("Finance and back-office agents (AF1): one invoice", [
 f"<b>Price.</b> {inr(inp('A15'))} per invoice ({inr(lo('A15'))} to {inr(hi('A15'))}); Hyperbots sells an unlimited-access licence (Inc42). The pricing path that grows with the work is seat, then usage, then per document.",
 f"<b>Costs.</b> Inference {inr(AF1('inf'),2)} per invoice; ERP integration Rs {inp('A17')} cr per enterprise ({lo('A17')} to {hi('A17')}); first-year contract Rs {inp('A18')} cr.",
 f"<b>Margin.</b> {pct(AF1('gm_inv'),0)} gross per invoice before integration; integration is {pct(AF1('sh'),0)} of the first-year contract against a {pct(inp('A19'),0)} threshold.",
 "<b>Must be true.</b> A per-document price that holds as the agent replaces seats; integration cost that falls with each customer. If each customer is a project, it is a services firm."]) }
</div><div class="cols">
{card("AI-native services (AF3): one finished job", [
 f"<b>Price.</b> Per finished job against the services budget; Sequoia counts USD {inp('A21')} of services spend per USD 1 of software (US). Hang Ten sells IT services with teams of 2 to 4 instead of about 30 (USD {inp('A22')} mn raised).",
 f"<b>Margin.</b> {pct(inp('A20'),0)} gross ({pct(lo('A20'),0)} to {pct(hi('A20'),0)}), assumption. Bessemer: removing people does not give software margins.",
 "<b>Must be true.</b> Human minutes per job fall every quarter; otherwise it is an agency with AI branding. The company that holds the outcome (prices the loss, not the task) is the one to fund."]) }
{card("Vertical AI (AV1): one site deployed", [
 f"<b>Price.</b> {inr(inp('A23'))} per site a month ({inr(lo('A23'))} to {inr(hi('A23'))}); deployment {inr(inp('A24'))} per site: {V('WE_AV1_Vertical','months'):.1f} months of revenue to recover.",
 "<b>Must be true.</b> Deployment repeats without a project (about one month of revenue or less), and the data gathered improves the product for the next site. Elevation (Sep 2026): Indian agents are 'judged on atoms', paired with on-the-ground fulfilment. Evidence in my set is thinnest here."]) }
</div>''', "Inputs A1 to A24. Print pack Exhibit 6 carries the pricing chart. JSW's listed companies (StrideOne, Hyperbots, Convin, Zvolv, Aereo, HealthPlix) are examples of applied vertical AI and licensed lending; my reading of jswvc.com, not Vikas's words.", 7))

# 8 What I would fund, fund maths
S.append(slide("What I would fund at JSW: five licensed risk-holders run by software, plus two or three suppliers they cannot do without",
 "Only the Mint facts about the fund, then arithmetic. The fund described needs low mortality and six outcomes at 5 to 8x; a 30x is not required.",
 f'''<div class="cols"><div class="l2">
{table(["Slot", "What", "Entry test (can fail)", "Exit route"], [
 ("1, 2", "Two licensed lenders: one secured retail class where repayment is controlled by the rail (EV fleets, education, LAP to GST filers); one embedded MSME lender that owns transaction data and settlement", f"First Rs 100 cr of debt contracted at entry; credit cost under {pct(inp('L29'),1)} on a 12-month vintage; opex under {pct(inp('L28'),0)} by year three", f"IPO on Rs 80 to 150 cr of PAT in year six or seven; Aye and Moneyview are the precedents"),
 ("3", "Claims and underwriting infrastructure for insurers, or an embedded cover with retention economics", "Price per claim under one fifth of the insurer's own cost; renewals above 80%", "Strategic or IPO; Acko and InsuranceDekho are filing"),
 ("4", "A manufacturer of alternatives (SIF, AIF, PMS) with captive distribution to the mass affluent and NRIs", f"Revenue above {pct(inp('W19'),1)} of assets; acquisition paid back inside {inp('W20')} months; distribution owned", "Strategic (Groww and Fisdom precedent) or IPO"),
 ("5", "A licensed cross-border or outcome-holder (exporter collections with FX and credit; an AI company that holds the loss)", "Take rate above 0.5%; a loss ratio line in its own accounts", "Strategic"),
 ("6 to 8", "Suppliers to the above: fraud and mule detection, consent pipes, collections stacks, model-risk tooling", f"Net revenue retention above {inp('F12')}x; top five customers under {pct(inp('F13'),0)}; a rule with a date behind the budget", "M&A by Perfios-type acquirers and listed fintechs")], ["6%", "40%", "32%", "22%"], "small")}
</div><div class="r2">
<div class="tiles"><div class="tile"><div class="tl">Fund III target, midpoint</div><div class="tv">Rs {EX7('f'):.0f} cr</div><div class="td">Mint; not yet closed</div></div><div class="tile"><div class="tl">Per name over life</div><div class="tv">Rs {EX7('life'):.0f} cr</div><div class="td">initial plus equal reserve</div></div><div class="tile"><div class="tl">Needed back for 3x</div><div class="tv">Rs {EX7('r3'):,.0f} cr</div><div class="td">{EX7('r7'):.1f}x on every name if no zeros</div></div></div>
{box("The maths.", f"Three zeros, six names at 1 to 2x and six at 5 to 8x return about 3.2x. A software-run lender listing on Rs 80 to 150 cr of PAT at 15 to 25x returns 5 to 8x on a diluted 8 to 10% stake. The 10x candidates are the suppliers with pricing power. Early-stage fintech funding was USD {inp('X9')} mn in H1 2026 and seed USD {inp('X10')} mn (Tracxn): a Rs 15 cr lead cheque sets price.")}
{box("What would prove me wrong, by when.", f"If by FY28 the best software-run lenders do not show opex under {pct(inp('L28'),0)} of assets with credit cost within 50 basis points of the branch lenders, the operating-team claim fails. If RBI's AI rules come to require human sign-off on every credit decision, the economics revert to the branch model (the June 2026 draft asks for validation and kill switches, not sign-off). If the regulator grants distribution a durable margin again, the distribution rows change; in September it did the opposite.", AMBER)}
</div></div>''', JSW, 8))

# 9 Sources and glossary
gl = [("MDR", "Merchant discount rate: the fee deducted from what a merchant receives on a card or UPI payment."), ("P2M, P2P", "Person to merchant; person to person."), ("Take rate", "Revenue as a share of the money that flows through."), ("Interchange", "The slice of a card fee paid to the cardholder's bank; a US debit average of 0.73% in 2024 (Fed)."), ("Yield", "Interest and fees earned as a share of loans."), ("Cost of funds", "Interest paid as a share of borrowings."), ("Credit cost", "Loan losses and provisions as a share of loans."), ("Opex to assets", "Operating cost as a share of the loan book."), ("ROA", "Profit as a share of assets."), ("Vintage", "Loans grouped by the month they were made, so losses can be compared like for like."), ("Co-lending", "A bank funds most of a loan an originator sources; RBI directions from 1 Jan 2026 set 10% minimum retention and a 5% cap on the default loss guarantee."), ("Default loss guarantee", "A promise by the originator to cover the first losses on a pool of loans."), ("GNPA", "Gross non-performing assets: loans overdue more than 90 days as a share of all loans."), ("Persistency", "The share of insurance policies renewed."), ("Loss ratio", "Claims paid as a share of premium."), ("Trail", "Recurring commission on assets a distributor keeps while the money stays invested."), ("SIF", "Specialised investment fund: SEBI's category between mutual funds and PMS, Rs 10 lakh minimum."), ("STT", "Securities transaction tax."), ("Account Aggregator", "RBI-licensed consent system through which a customer shares bank and other data with a lender."), ("NRR", "Net revenue retention: this year's revenue from last year's customers over last year's."), ("Token", "A unit of text a model reads or writes; prices are quoted per million."), ("Inference", "Running a trained model to produce an answer; the per-use cost."), ("Forward-deployed engineer", "An engineer who sits with the customer to connect the product to its systems."), ("Per-outcome pricing", "Charging per resolved conversation, per claim or per filing rather than per seat."), ("DRHP", "Draft red herring prospectus: the document filed before an IPO.")]
S.append(slide("Glossary and sources",
 "Every term used, in plain English. Sources are listed in the workbook Inputs sheet with URL, date, claim type and confidence.",
 f'''<div class="cols"><div class="l2">{table(["Term", "Meaning"], gl, ["18%", "82%"], "small")}</div><div class="r2">
{box("Primary sources used.", "NPCI (MDR FAQ 15 Sep 2026; UPI statistics Oct 2026; app-wise data Aug 2026); RBI (Financial Stability Report 2026; co-lending directions; fraud liability directions Jun 2026; FREE-AI report Aug 2025; model-risk draft Jun 2026); SEBI (FY26 derivatives study); IRDAI (consultation 23 Sep 2026); AMFI; Sahamati; Federal Reserve (Reg II); company results (Paytm, Pine Labs, PB Fintech, Go Digit, Groww, Angel One, Bajaj Finance) and DRHPs (Moneyview); Lok Sabha replies; Budget 2026.")}
{box("Secondary and claims.", "Business Standard, Inc42, Entrackr, TechCrunch, INDmoney, Outlook Business, Medianama, CIOL; Ramp AI Index (measured on Ramp customers); a16z State of Markets II (chart values); Sequoia, Bessemer, Stellaris, Elevation (investors' own posts, labelled as claims).")}
{box("Assumptions.", "Every assumption carries a range on the Inputs sheet and is marked amber. Nothing on these pages is invented; where I could not source a figure it is blank or labelled.", AMBER)}
</div></div>''', "Workbook: JSW_R2_workbook_v7.xlsx (Inputs, WE_ sheets, EX_ sheets, Check). Print pack: JSW_R2_print_pack_v7.pdf.", 9))

CSS = f'''<style>
@page {{ size: A4 landscape; margin: 10mm 12mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: system-ui, -apple-system, "Segoe UI", sans-serif; color: {INK}; margin: 0; font-size: 12px; line-height: 1.4; }}
.slide {{ page-break-after: always; position: relative; height: 188mm; overflow: hidden; }}
h1 {{ font-size: 20px; margin: 0 0 2px 0; font-weight: 700; }}
.sub {{ color: {INK2}; font-style: italic; margin: 0 0 10px 0; font-size: 12px; }}
.lead {{ font-size: 14px; line-height: 1.5; margin: 0 0 8px 0; }} .lead2 {{ font-size: 12px; color: {INK2}; }}
.cols {{ display: flex; gap: 12px; margin-bottom: 8px; }} .cols3 {{ display: flex; gap: 10px; margin-bottom: 8px; }}
.l2 {{ flex: 1.5; }} .r2 {{ flex: 1; }}
.card {{ flex: 1; border: 1px solid {GRID}; }} .ch {{ background: {INK}; color: #fff; font-weight: 600; padding: 6px 9px; font-size: 12.5px; }}
.cb {{ padding: 8px 10px; }} .cb p {{ margin: 0 0 7px 0; }}
.bx {{ padding: 9px 11px; margin-bottom: 9px; }}
.amber {{ flex: 1; background: {AMBER}; padding: 8px 10px; font-size: 12px; }}
.foot {{ color: {MUTED}; font-size: 9px; margin-top: 6px; position: absolute; bottom: 0; left: 0; right: 24px; }}
.num {{ position: absolute; right: 0; bottom: 0; color: {MUTED}; font-size: 9px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 11.5px; }} table.small {{ font-size: 10.5px; }}
th {{ background: {INK}; color: #fff; text-align: left; padding: 4px 6px; font-weight: 600; }}
td {{ padding: 4px 6px; border-bottom: 1px solid {GRID}; vertical-align: top; }}
.tiles {{ display: flex; gap: 8px; margin-bottom: 7px; }} .tile {{ flex: 1; border: 1px solid {GRID}; padding: 6px 8px; }}
.tl {{ font-size: 9px; color: {INK2}; }} .tv {{ font-size: 22px; font-weight: 600; }} .td {{ font-size: 8.5px; color: {MUTED}; }}
</style>'''
doc = f'<!doctype html><html><head><meta charset="utf-8"><title>JSW R2 reference deck v7</title>{CSS}</head><body>{"".join(S)}</body></html>'
out_html = os.path.join(H, "..", "outputs", "JSW_R2_reference_deck_v7.html"); open(out_html, "w").write(doc)
out_pdf = os.path.abspath(os.path.join(H, "..", "outputs", "JSW_R2_reference_deck_v7.pdf"))
subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", "file://" + os.path.abspath(out_html)], check=True, capture_output=True, timeout=120)
print("wrote", out_pdf)
