export const meta = {
  name: 'jsw-r2-deck-review',
  description: 'Review the JSW R2 deck, six exhibits and workbook with parallel lenses, verify numbers, refute ranked changes',
  phases: [
    { title: 'Review', detail: 'ten parallel reviewers: argument, partner lens, numbers, exhibits, workbook, language' },
    { title: 'Refute', detail: 'two adversarial refuters per ranked change' },
  ],
}

const COMMON = `
You are working for Kushal, who meets Vikas Chandak (Partner, JSW Ventures, Bengaluru; 20 years operating in banking and consumer fintech at ICICI Bank, ING, CRED; counters every answer once; tests for a view, not a list) at 5 pm today, Monday 5 October 2026. You have under 10 minutes. Be fast and blunt. READ-ONLY: do not write, edit or create any file. Return results ONLY through the StructuredOutput tool.

Files (read with the Read tool; for PDFs pass pages):
- Deck (9 pages): ${args.deck}
- Print pack (14 pages): ${args.exhibits}. The six exhibits are pages 3 to 8: E1 p3 Payments P&L, UPI merchant fee from 15 Oct vs card rates; E2 p4 AI spend is concentrated; E3 p5 Where AI fits, cost side or revenue side (task map); E4 p6 Profit pools; E5 p7 United States to India line by line; E6 p8 Fourteen sub-theses, evidence behind each. Pages 1 to 2 are maps, 9 to 14 reference tables.
- Workbook sheets: README, PL_Summary, Insights, Inputs, Concentration, Cost_and_Price, Profit_Pools, India_vs_US, Task_Map, Subthesis_Matrix, Open questions, PL_F1..PL_F5, PL_AL1..PL_AV1 (templates), What_sits_under_what. Derived sheets are formulas off the Inputs sheet (no typed numbers). The Inputs sheet (ID|metric|figure|unit|source|date|claim type|confidence|note) is reproduced here:
${args.inputs}

The deck's structure: a P&L spine. For each sub-segment: how it makes money (revenue drivers), gross margin, cost to serve (a ladder CM1, CM2, CM3, EBITDA), the one line to judge quality on, and whether it is fundable at JSW's stage. Judge the deck against that choice; do not re-plan it into a narrative deck. At most one insight line per sector may be added on top of the spine.

JSW facts allowed (Mint, 25 Jun 2026): Fund III target Rs 400 to 500 cr, not yet closed; initial cheque Rs 10 to 20 cr with an equal amount reserved for follow-ons; pre-Series A to Series A+; 14 to 16 companies; Fund II about Rs 280 cr. Assume nothing else about JSW.

Style rules for every rewrite you propose and for your own writing: no "it's not X, it's Y" or "not just X but Y"; no vague load-bearing words (massive, game-changer, transformational, paradigm shift); no em dashes; no tidy summary lines; no generic AI polish; every weight-bearing sentence carries a number, a source, or a stated assumption with a range; never invent a figure; if a line could be said by any AI about fintech, cut it or make it specific. Numbers first, then the claim, then what has to be true. Kushal has no engineering or corporate-finance background: define each term in plain English the first time you use it.
`

const FINDINGS = {
  type: 'object',
  properties: {
    verdict: { type: 'string', description: 'Three to five sentences. Blunt. Does the section hold with a partner who counters once?' },
    weakest_first: { type: 'array', items: { type: 'object', properties: {
      location: { type: 'string', description: 'slide number and box, or exhibit' },
      what_it_says: { type: 'string' },
      why_weak: { type: 'string' },
      what_must_be_true: { type: 'string' },
      what_breaks_first: { type: 'string' },
      rewrite: { type: 'string', description: 'replacement text Kushal can paste, following the style rules; or "no rewrite, flag as question"' },
      severity: { type: 'integer', description: '5 = loses the partner, 1 = cosmetic' }
    }, required: ['location','what_it_says','why_weak','rewrite','severity'] } },
    ranked_changes: { type: 'array', items: { type: 'object', properties: { change: { type: 'string' }, why: { type: 'string' }, rewrite: { type: 'string' } }, required: ['change','why','rewrite'] }, description: 'at most 6, most important first' },
    questions_to_flag: { type: 'array', items: { type: 'string' }, description: 'issues to raise as questions rather than change' },
    one_insight_line_per_sector: { type: 'array', items: { type: 'object', properties: { sector: { type: 'string' }, line: { type: 'string' } }, required: ['sector','line'] } }
  },
  required: ['verdict','weakest_first','ranked_changes','questions_to_flag']
}

const NUMBERS = {
  type: 'object',
  properties: {
    numbers: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, claim_as_used: { type: 'string' },
      status: { type: 'string', enum: ['verified','unverified','contradicted','stale'] },
      correct_figure: { type: 'string' }, primary_source: { type: 'string' }, url: { type: 'string' },
      note: { type: 'string' }, likely_tested: { type: 'integer', description: '5 = Vikas will certainly test it' },
      plain_english: { type: 'string', description: 'one sentence explaining what the number means to a non-finance reader' }
    }, required: ['id','claim_as_used','status','correct_figure','primary_source','likely_tested','plain_english'] } }
  },
  required: ['numbers']
}

const EXHIBITS = {
  type: 'object',
  properties: { exhibits: { type: 'array', items: { type: 'object', properties: {
    exhibit: { type: 'string' },
    earns_place: { type: 'string', enum: ['yes','no','conditional'] },
    correct: { type: 'string', enum: ['yes','partly','no'] },
    issues: { type: 'array', items: { type: 'string' } },
    generic_test: { type: 'string', description: 'could a VC get this from a generic AI answer or a fintech report? why or why not' },
    improvement: { type: 'string', description: 'the specific change that makes it better, or "drop"' },
    slide_tie: { type: 'string' }, takeaway_line: { type: 'string', description: 'one line Kushal can say out loud, with the number' },
    drill: { type: 'array', items: { type: 'object', properties: { q: { type: 'string' }, a: { type: 'string' } }, required: ['q','a'] }, description: 'two questions a partner would ask about this exhibit, with answers' }
  }, required: ['exhibit','earns_place','correct','issues','improvement','slide_tie','takeaway_line','drill'] } } },
  required: ['exhibits']
}

const NEWEX = {
  type: 'object',
  properties: {
    workbook_issues: { type: 'array', items: { type: 'string' } },
    drop: { type: 'array', items: { type: 'string' } },
    new_exhibits: { type: 'array', items: { type: 'object', properties: {
      title: { type: 'string' }, claim_it_supports: { type: 'string' }, slide_tie: { type: 'string' },
      takeaway_line: { type: 'string' }, why_a_vc_cares: { type: 'string' },
      inputs_needed: { type: 'array', items: { type: 'object', properties: {
        metric: { type: 'string' }, figure: { type: 'string' }, unit: { type: 'string' }, source: { type: 'string' }, url: { type: 'string' },
        status: { type: 'string', enum: ['verified','assumption','not_found'] }, range: { type: 'string' }
      }, required: ['metric','figure','unit','source','status'] } },
      formula_logic: { type: 'string', description: 'how the chart values derive from the inputs, as formulas' },
      chart_form: { type: 'string' }
    }, required: ['title','claim_it_supports','slide_tie','takeaway_line','why_a_vc_cares','inputs_needed','formula_logic','chart_form'] } }
  },
  required: ['workbook_issues','drop','new_exhibits']
}

const VIKAS = {
  type: 'object',
  properties: {
    verdict: { type: 'string' },
    loses_him_at: { type: 'string', description: 'the first slide or line where a partner stops reading charitably, and why' },
    ten_questions: { type: 'array', items: { type: 'object', properties: { q: { type: 'string' }, probes: { type: 'string' }, answer_hint: { type: 'string' } }, required: ['q','probes','answer_hint'] } },
    ranked_changes: { type: 'array', items: { type: 'object', properties: { change: { type: 'string' }, why: { type: 'string' }, rewrite: { type: 'string' } }, required: ['change','why','rewrite'] } },
    what_would_make_it_memorable: { type: 'string' }
  },
  required: ['verdict','loses_him_at','ten_questions','ranked_changes','what_would_make_it_memorable']
}

const GLOSSARY = {
  type: 'object',
  properties: {
    language_findings: { type: 'array', items: { type: 'object', properties: { location: { type: 'string' }, text: { type: 'string' }, rule_broken: { type: 'string' }, rewrite: { type: 'string' } }, required: ['location','text','rule_broken','rewrite'] } },
    flow_findings: { type: 'array', items: { type: 'string' } },
    glossary: { type: 'array', items: { type: 'object', properties: { term: { type: 'string' }, plain_english: { type: 'string' }, where_used: { type: 'string' } }, required: ['term','plain_english','where_used'] } }
  },
  required: ['language_findings','flow_findings','glossary']
}

const VERDICT = {
  type: 'object',
  properties: { refuted: { type: 'boolean' }, reason: { type: 'string' }, better_rewrite: { type: 'string' } },
  required: ['refuted','reason']
}

phase('Review')

const argFintech = () => agent(COMMON + `
TASK: Test the fintech argument: deck slides 1 to 5 and print pages 1, 3, 9, 13. For each of the five sub-sectors (payments, lending, insurance, wealth, fraud and identity) and each "Fundable by JSW?" call: what has to be true for the call to hold, what breaks first, and whether the "one line I would judge on" is the right line. Check the P&L ladder (slide 2) for errors in how gross margin, CM1 to CM3 and EBITDA are defined, especially for lenders (yield less cost of funds less credit cost) and pass-through businesses. Test whether "partly fundable", "fundable (core fit)", "fundable, selective", "mostly not fundable", "fundable (strong fit)" are earned by the numbers shown or merely asserted. Known facts you may use to test: UPI P2M MDR 0.4 percent above Rs 2,000 capped at Rs 300 from 15 Oct 2026 (NPCI FAQ); IRDAI consultation of 23 Sep 2026 proposing caps on insurance distributor commissions and expenses (PB Fintech fell about 43 percent in four sessions, Business Standard 29 Sep 2026); co-lending directions in force 1 Jan 2026 with default loss guarantee capped at 5 percent; Moneyview listed 1 Oct 2026 about 62 percent above issue; Groww Q1 FY27 PAT Rs 735 cr; Fi shut its banking services Mar 2026. Give the weakest claims first with rewrites, then at most six ranked changes, then questions to flag, then one insight line per sector (optional, only if it carries a number).`, { label: 'argument:fintech', phase: 'Review', schema: FINDINGS })

const argAI = () => agent(COMMON + `
TASK: Test the AI argument: deck slides 1, 2, 6 to 9 and print pages 2, 4, 5, 6, 7, 8, 10, 11, 14. Vikas asked in round 1, three times, for an AI use beyond efficiency and rejected process automation, document summarisation, call automation and collections automation as efficiency; his own framing was AI "holding of outcomes for the company". Test: does the deck's "cost side 71 percent, revenue side 49 percent" task map and the "price the finished job" line answer him, or does it restate efficiency? Does the layer-by-market map (compute, models, tooling, apps) earn its place for a Rs 10 to 20 cr fund that cannot fund compute or models, or does it spend two slides on cells marked not fundable? Test each "Fundable by JSW?" call and each "judge on" line (pricing unit, gross margin over cohorts, price per resolved conversation, human minutes per finished job, deployment cost per customer) for whether a partner can actually observe it in a pre-Series A company. Check the AI anchors: effective price per 1M tokens 0.68 vs 1.15 (Ramp), 80 percent of lab revenue from top 1 percent of customers, 99.5 percent top-10 share, $780B vs $416B capex (spoken claim), 2 percent of US households pay, 66 percent of voice deployments replaced an existing budget (Stellaris), 6:1 services to software (Sequoia), NIFTY IT minus 39 percent (Bessemer). Which of these would a partner call irrelevant to India at pre-Series A? Give the weakest claims first with rewrites, at most six ranked changes, questions to flag, and one insight line per AI section only if it carries a number.`, { label: 'argument:ai', phase: 'Review', schema: FINDINGS })

const vikas = () => agent(COMMON + `
TASK: Read the whole deck (9 pages) and print pages 1 to 8 as Vikas Chandak would, in the 15 minutes before the coffee. Then answer as him. Give: a blunt verdict; the first slide or line where you stop reading charitably and why; the ten questions you would ask in order, each with what it probes and a hint of the answer Kushal should have; at most six ranked changes with rewrites; and one paragraph on what would make the document memorable rather than competent (a document that maps segments is competent; one that makes a call and names what the author would be wrong about is memorable). Judge against the P&L spine the author chose; do not ask for a narrative deck.`, { label: 'partner-lens', phase: 'Review', schema: VIKAS })

const numbersFintech = () => agent(COMMON + `
TASK: Verify every fintech and India number the deck and exhibits use, against primary sources, with WebSearch and WebFetch (fast: at most 12 fetches). The list: D6 UPI P2M MDR 0.4 percent, S28 cap Rs 300, S29 threshold Rs 2,000, D7 flat Rs 5 for specified categories (not found in the FAQ by the author; confirm or mark unverified), D8 96 percent of transactions unaffected; D1 D2 UPI Sept 2026 24,068 mn transactions and Rs 29.37 lakh cr; D4 average ticket Rs 1,220 (derived; check arithmetic: 2937396.67 crore times 1e7 divided by 24068.38 million times 1e6); D5 86 percent UPI share of retail digital payment transactions; D9 card MDR 1.5 to 2.5 percent (NPCI FAQ); D11 US debit interchange 0.79 percent (Fed Reg II average); S17 three apps about 80 percent of UPI volume (check NPCI app-wise market share data for Sept 2026 and give the actual top-3 share); D14 Account Aggregator 538 mn consents fulfilled Jul 2026 (Sahamati); S12 to S14 Suryoday SFB with Paytm, over Rs 360 cr credit lines to over 5 lakh customers in 8 months, 90 percent score 725+; S18 S19 Moneyview cost of borrowings 14.4 percent vs Bajaj Finance 7.45 percent (check against Moneyview's DRHP or FY26 annual report and Bajaj Finance FY26 results); S10 MSME credit gap $530 bn (Kae) vs D21 IFC Rs 36.7 tn 2018; S11 TReDS Rs 3.47 lakh cr FY26; S20 S21 India wealthtech funding $560 mn Q1 2026 up 84 percent; S22 remittances $137 bn 2024 (check RBI or World Bank 2024 and FY26 figure); D20 NBFC gross NPA 2.4 percent Mar 2026; D22 India fintech funding H1 2026 nearly $2 bn (Tracxn); S26 S27 fraud growth 18 to 20 percent a year (spoken; mark as such); D19 India NBFC average cost of funds (not found by the author; try RBI FSR or rating agency data, give a sourced range or mark not found). For each: status, the correct figure, the primary source and URL, a plain-English sentence, and likely_tested 1 to 5 from Vikas's seat (an ex-ICICI, ex-CRED operator). Never invent a figure.`, { label: 'numbers:fintech', phase: 'Review', schema: NUMBERS })

const numbersAI = () => agent(COMMON + `
TASK: Verify every AI number the deck and exhibits use, against primary sources, with WebSearch and WebFetch (fast: at most 12 fetches). The list: A2 Ramp top 1 percent median AI spend per employee $7,976 July 2026 and A3 top 10 percent $650 and A4 median $11.95 (check the Ramp AI Index pages for the unit and period); B3 B4 effective price per 1M tokens $0.68 early Sept 2026 vs $1.15 March 2026 peak (Ramp); A5 80 percent of OpenAI and Anthropic enterprise revenue from the top 1 percent of customers (Ramp economist via PYMNTS; find the primary post); A6 to A9 top 10 percent of firms' share of spend: model serving 99.5, neocloud 99.0, non-AI SaaS 91.8, CRM 84.2 (Apollo citing Ramp); A11 A12 43.8 percent of Ramp businesses pay Anthropic and 39.8 percent pay OpenAI (Aug 2026); A15 A16 big-5 hyperscaler capex $780 bn 2026 vs $416 bn 2025 (spoken claim on an a16z panel; check against company guidance and give the best sourced figure); C1 to C5 Amazon advertising revenue 2025 quarters summing to $68.6 bn (check Amazon's releases); B9 about 2 percent of US households pay for AI subscriptions (spoken); B7 B8 69 percent of S&P 500 firms report live deployments and 30 percent quantified impact (spoken; find the survey if it exists); C6 30 percent of public software companies grow 20 percent or more; S1 NIFTY IT down 39 percent from Dec 2024 peak to May 2026 (check index levels); S2 $6 on services per $1 on software (Sequoia); S3 to S6 US insurance brokerage labour pool $140 to 200 bn and claims adjusting $50 to 80 bn (Sequoia); S25 66 percent of sampled voice AI deployments replaced an existing budget (Stellaris); B1 Databricks routing about 35 percent cheaper (vendor blog); S23 S24 India added data-centre spend $20 to 25 bn by 2030 (Bessemer); D24 40 percent of Indian enterprises with significant or full AI usage (Deloitte 2026). For each: status, the correct figure, the primary source and URL, a plain-English sentence, and likely_tested 1 to 5 from Vikas's seat. Mark every spoken-panel figure as a spoken claim with the best primary figure beside it. Never invent a figure.`, { label: 'numbers:ai', phase: 'Review', schema: NUMBERS })

const exhibitsA = () => agent(COMMON + `
TASK: Review E1 (print page 3, Payments P&L: UPI merchant fee vs card rates) and E2 (page 4, AI spend is concentrated). For each: does it earn its place with a VC who will test it, is it correct (check the chart values against the Inputs: E1 uses D6, D9a, D9b, D11; E2 uses A2, A3, A4, A5, A6 to A9), and what specific change makes it better. Apply the generic test: could a VC get this from any AI answer or a fintech report? Specific concerns to test: E1 mixes four different bases (a merchant fee on UPI, a US debit interchange average, an Indian card MDR range) on one bar chart and says so in the subtitle; is "shown together for scale only" acceptable to a partner, and what would a cleaner E1 show (for example the fee pool by ticket size under the Rs 300 cap, or who in the chain receives the 0.4 percent)? E2 shows three different denominators; is the chart honest, and does any of it bear on a Rs 10 to 20 cr India fund? Give the takeaway line Kushal can say out loud and two drill questions with answers per exhibit.`, { label: 'exhibits:E1-E2', phase: 'Review', schema: EXHIBITS })

const exhibitsB = () => agent(COMMON + `
TASK: Review E3 (print page 5, Where AI fits: cost side or revenue side of the P&L, the eight-by-twelve task map) and E4 (page 6, Profit pools: where AI moves profit away from and toward). For each: does it earn its place with a VC who will test it, is it correct (E3 is the author's own coding, C/R/V/P, with counts by formula in Task_Map; check the 71 percent and 49 percent arithmetic from the row counts shown: cost-side cells and revenue-side cells over fitting cells; E4 numbers are C5 Amazon ads $68.6 bn, C6 30 percent, S1 minus 39 percent, S2 6:1, A15 A16 capex), and what specific change makes it better. Apply the generic test: could a VC get this from any AI answer or a report? Specific concerns: E3 is labelled "judgement, not data" in its own footnote; does a matrix of the author's own codes carry weight with a partner, and if it stays, what would make it testable (for example, one named Indian company per cell with a public price)? Does E3 answer Vikas's round-1 challenge that automation of support, collections and summarisation is all efficiency, or does it restate it with colour? E4 lists US profit pools with no rupee pool sizes and says so; is it a slide for an Indian pre-Series A fund? Give the takeaway line and two drill questions with answers per exhibit.`, { label: 'exhibits:E3-E4', phase: 'Review', schema: EXHIBITS })

const exhibitsC = () => agent(COMMON + `
TASK: Review E5 (print page 7, United States to India line by line on the P&L: six ingredients) and E6 (page 8, Fourteen sub-theses on the new map, how much evidence stands behind each). For each: does it earn its place with a VC who will test it, is it correct (E5's India proof points: UPI MDR 0.4 percent, Bessemer AI-native firms, 538 mn AA consents, Digital Lending Directions May 2025 repayments direct to lender account, Hyperbots, Bolna; E6's headline figures and the evidence grades Strongest to Thin, which are the author's own grades), and what specific change makes it better. Apply the generic test. Specific concerns: E5's "India test" column is mostly reasoning without numbers (labour cheaper, banks run legacy systems, calls mix languages); which cells can be given a number from the Inputs or from a quick primary search, and which should be cut? E6 grades evidence depth qualitatively; is "Strongest" for lending with a single $530 bn credit-gap claim from a VC's own thesis defensible, and would a partner prefer a column showing the number of primary sources behind each sub-thesis? Give the takeaway line and two drill questions with answers per exhibit.`, { label: 'exhibits:E5-E6', phase: 'Review', schema: EXHIBITS })

const workbook = () => agent(COMMON + `
TASK: Audit the workbook and propose new exhibits. Read the workbook with Python (openpyxl is not installed; parse the xlsx with zipfile and xml.etree: sheet names from xl/workbook.xml, cells from xl/worksheets/sheetN.xml, formulas in <f>, values in <v>, shared strings in xl/sharedStrings.xml). Check: (1) every chart value on the six exhibits traces to an Inputs row by formula (the derived sheets have no typed numbers; confirm the chart data ranges on Concentration, Profit_Pools, India_vs_US, Task_Map point at formulas); (2) the Insights sheet's 22 live sentences: do any reference a blank input and render a broken sentence; (3) stale or weak inputs that carry a deck claim (D21 IFC 2018; S18 S19 from a newsletter; S17 three apps 80 percent not checked against NPCI; S11 S20 S23 with missing URLs; D7 Rs 5 flat fee not found in the FAQ); (4) unit errors (A3 per employee with no period; D11 0.79 stored as percent not fraction; D4 ticket derivation). Then propose five new exhibits that meet this standard: each means something to a VC who will test it and could not be copied from a generic AI answer; each ties to a named deck slide or claim with a one-line takeaway; every number traces to a sourced input or is marked assumption with a range; formulas off visible inputs. Candidates to consider and improve on: (a) the UPI fee pool by ticket band under the Rs 2,000 floor and Rs 300 cap, showing where the 0.4 percent actually lands and who in the chain receives it (needs NPCI ticket-size distribution or a stated assumption with range); (b) a lender P&L worked through the ladder with sourced inputs: yield, cost of funds, credit cost, opex to AUM for two listed Indian lenders (Bajaj Finance and a small-ticket lender such as Five Star or Aye Finance, from FY26 results) against a pre-Series A lender's likely numbers as assumptions with ranges; (c) exit evidence: 2025 to 2026 fintech IPOs with issue price, current price and PAT at listing (Groww, Pine Labs, Aye Finance, Kissht, Turtlemint, Moneyview), which prices profit; (d) the regulatory calendar 2026 to 2027 with the P&L line each item moves (MDR 15 Oct 2026, DPDP consent managers 13 Nov 2026 and full obligations 13 May 2027, RBI fraud liability 1 Jan 2027, IRDAI commission caps consultation); (e) price per resolved conversation versus human cost per call in India with a stated assumption range, since the author left it blank. Say which of the six existing exhibits to drop. Mark every figure you propose as verified (with URL) or assumption (with range). Never invent a figure.`, { label: 'workbook+new-exhibits', phase: 'Review', schema: NEWEX })

const language = () => agent(COMMON + `
TASK: Language, framing and flow pass on the deck (9 pages) and print pages 1 to 8. Find every instance that breaks the style rules: "not X but Y" constructions, vague load-bearing words with no number, em dashes, tidy summary lines, generic AI polish, sentences any AI would write about fintech or AI, claims with no number or source. Quote the text, name the rule, give the rewrite. Then flow: does the deck open with a claim or a method; is the "Hypotheses to test, not conclusions" line on slide 1 and the repeated "(correct me)" and "my reasoning" labels strength (humility in front of a 20-year operator) or weakness (no view); is nine slides the right length for a coffee; which slide should come first; is the order fintech then AI then US-pattern right. Finally, a plain-English glossary for Kushal, who has no engineering or corporate-finance background: every term in the deck and exhibits that a non-finance reader would not know (take rate, interchange, MDR, P2M, float, cost of funds, credit cost, vintage, first-loss guarantee, FLDG, NIM, yield, AUM, basis points, persistency, loss ratio, underwriting margin, MGA, Account Aggregator, sponsor bank, BaaS, TReDS, CM1 to CM3, EBITDA, gross margin, pass-through, inference, token, GPU, foundation model, orchestration, fine-tuning, forward-deployed engineer, per-outcome pricing, backlog, capex, interchange cap, Reg II, hyperscaler, neocloud, and any others), each in one plain sentence with where it is used. Be complete on the glossary.`, { label: 'language+glossary', phase: 'Review', schema: GLOSSARY })

// start the non-gating reviewers; do not await yet
const othersP = parallel([numbersFintech, numbersAI, exhibitsA, exhibitsB, language])

// change-producing reviewers flow straight into refutation, no barrier
const producers = [
  { key: 'fintech', run: argFintech },
  { key: 'ai', run: argAI },
  { key: 'vikas', run: vikas },
]

const refuted = await pipeline(
  producers,
  p => p.run(),
  async (result, p) => {
    if (!result) return null
    const changes = (result.ranked_changes || []).slice(0, 4)
    const checked = await parallel(changes.map((c, i) => () =>
      parallel([0, 1].map(k => () => agent(COMMON + `
You are a second, hostile reviewer. A colleague proposes this change to the deck:
CHANGE: ${c.change}
WHY: ${c.why}
REWRITE: ${c.rewrite}
Try to refute it (lens ${k === 0 ? 'is the proposed rewrite true and sourced, or does it smuggle in an unsourced number or a generic claim' : 'would Vikas, an ex-ICICI and ex-CRED operator who counters once, find the original stronger than the rewrite, or find the change beside the point for a Rs 10 to 20 cr pre-Series A fund'}). Read the relevant deck page (${args.deck}) if needed. Default to refuted=true if uncertain. If you refute, say why in two sentences and give a better rewrite if one exists.`, { label: `refute:${p.key}:${i + 1}:${k + 1}`, phase: 'Refute', schema: VERDICT, effort: 'medium' })))
        .then(vs => ({ ...c, votes: vs.filter(Boolean), survives: vs.filter(Boolean).filter(v => !v.refuted).length >= 1 }))))
    return { key: p.key, result, changes: checked.filter(Boolean) }
  }
)

const [numF, numA, exA, exB, lang] = await othersP

log(`review done: ${refuted.filter(Boolean).length}/3 argument lenses, ${[numF, numA, exA, exB, lang].filter(Boolean).length}/5 others`)

return {
  argument: refuted.filter(Boolean),
  numbers_fintech: numF, numbers_ai: numA,
  exhibits: [exA, exB].filter(Boolean).flatMap(x => x.exhibits),
  new_exhibits: null,
  language: lang,
}