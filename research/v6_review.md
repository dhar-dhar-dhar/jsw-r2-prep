# Review of the v6 deck, exhibits and workbook (5 Oct 2026)

Built from my own pass, two number-verification agents (every figure checked against a primary or reputable source), and exhibit reviewers for Exhibits 1 to 4. Sections marked PENDING fill in when the argument, partner-lens and language reviewers report. The v7 rebuild (deck, pack, workbook under `outputs/`) already applies the corrections below.

## (a) Deck review

### Verdict
The v6 deck is a method rather than a view. It opens with "Hypotheses to test, not conclusions", every segment box says "correct me", and nine slides of taxonomy and ladder never show one P&L with numbers in it; the workbook's P&L templates are empty. The spine is the right choice and the ladder is sound. What a partner who tests for a view will do is ask for one filled ladder per thesis, and v6 cannot give him one. The anchors skew to United States and spoken figures (a16z panel, Sequoia, Bessemer) while the Indian regulator numbers the deck already holds sit in footnotes. The two most relevant Indian facts of the last two weeks are absent: IRDAI's 23 Sep consultation on distributor commissions (PB Fintech minus 43 percent) and NPCI's agent-payments protocol. The "fundable" calls are asserted by fit to JSW's named themes rather than earned by a number.

### Weakest claims first, with the rewrite (ranked)
1. Slide 5, insurance anchor is a United States labour pool (Sequoia) and the IRDAI consultation is missing. Rewrite: "IRDAI's consultation of 23 Sep 2026 proposes caps on distributor commissions and insurer expenses; PB Fintech fell 43 percent in four sessions (Business Standard, 29 Sep). Individual health premiums grew 29.7 percent in Oct to Mar FY26 after GST went to zero (Lok Sabha reply). The carrier and the claims line gain; the distributor's revenue is a rate under consultation."
2. Slide 4, lending anchor "Moneyview 14.4 percent vs Bajaj 7.45 percent (TheGreySwan)" mixes periods. Rewrite: "Moneyview's cost of borrowings was 14.44 percent in FY25 and 9M FY26 (DRHP); Bajaj Finance's was 7.54 percent in FY26. The gap is the rating." Add one credit-cost number, since the judge-on line is credit cost by vintage.
3. Slide 4 and E1, "three apps carry about 80 percent of UPI volume (The Ken)". Contradicted: NPCI's August 2026 app-wise data gives PhonePe 45.9, Google Pay 32.4, Paytm 8.1 percent; top two about 78 percent, top three about 86 percent. Rewrite with the NPCI figures.
4. Slide 4 footer, Suryoday and Paytm: "over Rs 360 crore credit lines to over 5 lakh customers in 8 months". Rs 360 cr is the sanctioned limit (Rs 102 cr drawn), 5.3 lakh sanctioned, 2.4 lakh active (Business Standard, 23 Jun 2026). Rewrite accordingly.
5. Slide 5, wealth anchor "$560 mn wealthtech funding in Q1 2026, up 84 percent" is a funding flow, which the spine itself says is not a P&L fact; Tracxn puts all India fintech funding at $513 mn for the same quarter, so the two trackers classify differently. Rewrite with Groww Q1 FY27 PAT Rs 735 cr and SEBI's FY26 study (87.7 percent of individual F&O traders lost money; traders down 18 to 20 percent).
6. Slide 5, fraud anchor "fraud growing 18 to 20 percent a year (a16z video)" is a spoken United States estimate. Rewrite with RBI's fraud liability directions (banks compensate 85 percent of coerced-transaction losses up to Rs 25,000 from 1 Jan 2027), which is a rule creating the budget, the deck's own test for F5.
7. Slide 2 and E3, "cost side in 71 percent and revenue side in 49 percent of fitting cells". Arithmetic is right (58 and 40 of 82 fitting cells) but they sum to 120 percent because 21 cells count twice, and they are the author's codes. Rewrite: "Of 96 cells I coded, 37 are cost only, 19 revenue only, 21 both, 14 poorly targeted; the revenue cells sit in four columns."
8. Slides 6 and 7: two of nine slides on compute and foundation models, both marked not fundable. Collapse to two rows on the map and spend the slide on a worked AI P&L (voice cost per call, which v6 leaves "NOT FOUND"; v7 carries it as an assumption with a range).
9. Slide 9, "Vertical AI: fundable (named theme) because JSW names it (Mint)" is circular. Give it the deck's own test (deployment cost per new customer) with a threshold.
10. Slide 1 footer, "I am new to these sectors". Honest, and it lowers the bar before he reads. Keep the humility in the "correct me" labels and cut the sentence.
11. E1 bar "US debit interchange 0.79 percent (2024)". The Fed's 2024 all-transactions row is 0.73 percent. Correct or drop (the United States bar is interchange, a different cut from Indian MDR).
12. E6 and slide 4, "$530 bn MSME credit gap (Kae)". Traces to Avendus Capital's April 2023 modelled paper; the IFC 2018 figure is Rs 36.7 tn of demand with a Rs 25.8 tn gap. Cite "Avendus 2023, modelled" or drop.
13. Slide 9 footer, "66 percent of sampled voice deployments replaced an existing budget (Stellaris)". The source says 66 percent of 216 companies target existing spend. Rewrite to companies and "target".
14. Slide 7 and E4, "big-5 hyperscaler capex $780 bn vs $416 bn (spoken claim)". These are a16z chart figures (State of Markets II, 30 Sep 2026); relabel. Same for 69 percent live deployments, 30 percent quantified, 2.2 percent of households (as of April 2026).
15. E2 and slide 7, "80 percent of OpenAI and Anthropic enterprise revenue from the top 1 percent of customers". It is 80 percent of Ramp-observed business spend on the two labs, not the labs' revenue books. Rewrite the wording.

### Questions to flag rather than change
- Who receives the 0.4 percent UPI MDR (acquirer, issuer, NPCI)? The FAQ does not publish the split. Carry it as the open question.
- The flat Rs 5 fee for notified categories: two secondary sources quote it from the FAQ; the author's FAQ text may have been an earlier version. Keep Medium confidence.
- "86 percent UPI share of retail digital payments" is by count, not value. Change the wording to "by count".
- NBFC average cost of funds: no sector figure exists; show the two anchors (Bajaj AAA 7.54 percent, Moneyview A- 14.44 percent) as a range, never a midpoint.
- TReDS Rs 3.47 lakh cr for FY26 is a platform projection (RXIL), not an outturn. Say so or remove.

### PENDING: argument tests (what has to be true, what breaks first) from the fintech and AI argument reviewers, the partner-lens verdict and his ten questions, and the language and flow pass.

## (b) Exhibit-by-exhibit verdicts (v6 pack)

- E1 (p3, UPI fee vs card rates). Earns its place only because it is current. Four bases on one axis (interchange, MDR range, UPI MDR); the United States bar is 0.73 percent, not 0.79. Generic test fails as built: any AI produces this bar chart. Better: a fee-per-transaction ladder off the rule (Rs 0 at 1,999; Rs 8 at 2,000; Rs 40 at 10,000; Rs 300 from 75,000; 0.1 percent at 3,00,000) with the Rs 1,220 average ticket marked and NPCI's "more than 95 percent pay nothing". Takeaway: "From 15 October UPI merchants pay 0.4 percent only on payments above Rs 2,000, capped at Rs 300, so the cap binds at Rs 75,000 and the average ticket pays nothing." Done as v7 Exhibit 2.
- E2 (p4, AI spend concentration). Correct to its inputs but mixes periods (July revised top 1 percent against a July top 10 percent whose period is unclear) and overstates the lab-revenue panel. All B2B spend is concentrated (SaaS 91.8 percent, CRM 84.2 percent); AI is 8 points more so. Zero India data on a page for an India fund. Better: one panel with the SaaS baseline and the $11.95 median as the callout; or drop. Dropped in v7; the top-customer question survives as a diligence line.
- E3 (p5, task map). Arithmetic verified. It is the author's coding with a "judgement, not data" footnote; five of eight rows sit outside Vikas's lane; it restates the efficiency challenge with colour. Better: cut to Bank/NBFC and Insurer by the five contested columns and write the P&L line and test in each cell. Kept in v7 as a reference page with counts instead of percentages.
- E4 (p6, profit pools). Numbers transcribed correctly; lists unsourced and generic; United States pools on an India page; off-spine. Drop as a page; move NIFTY IT minus 39 percent and Sequoia's 6:1 under AI-native services. Dropped in v7; replaced by the last-thirty-days page.
- E5 (p7, US to India line by line). My pass: the best frame in the pack; the India test column is reasoning without numbers in four of six rows. Better: give three rows a number from the inputs. v7 keeps the frame inside slides 6 and 7 and the pricing exhibit.
- E6 (p8, fourteen sub-theses). My pass: evidence grades are the author's; "Strongest" for lending rests on one VC's $530 bn claim that traces to Avendus 2023. Better: a count of primary sources per sub-thesis. Replaced in v7 by sourced worked examples per sub-sector.

## (c) New exhibits
See `outputs/JSW_R2_print_pack_v7.pdf` (seven exhibits) and `outputs/JSW_R2_workbook_v7.xlsx` (Inputs with source, URL, date, claim type, confidence, status and ranges; WE_ and EX_ sheets as formulas; Check sheet).

## (d) The ten numbers Vikas is most likely to test
See `research/talk_track_v7.md`.

## (e) Five-question drill
See `research/talk_track_v7.md`.

## Number corrections table (v6 figure, status, correct figure, source)
| v6 figure | Status | Correct | Source |
|---|---|---|---|
| Three apps about 80% of UPI volume | Contradicted | Top two about 78%, top three about 86% (PhonePe 45.9, GPay 32.4, Paytm 8.1) | NPCI app-wise, Aug 2026 |
| Suryoday-Paytm: Rs 360 cr credit to 5 lakh customers | Partly wrong | Rs 360 cr sanctioned, Rs 102 cr drawn; 5.3 lakh sanctioned, 2.4 lakh active | Business Standard, 23 Jun 2026 |
| 96% of UPI transactions unaffected | Wording | More than 95% of merchant (P2M) volume by count | NPCI FAQ |
| US debit interchange 0.79% (2024) | Contradicted | 0.73% all transactions, 2024 | Federal Reserve Reg II table |
| Moneyview 14.4% vs Bajaj 7.45% | Period mismatch | 14.44% (FY25, 9M FY26) vs 7.54% (FY26) | Moneyview DRHP; Bajaj results |
| $530 bn MSME credit gap (Kae) | Stale, modelled | Avendus Capital, Apr 2023 | KNN India |
| TReDS Rs 3.47 lakh cr FY26 | Unverified | RXIL projection "more than Rs 3.5 lakh cr" | Outlook Business |
| Stellaris 66% of deployments replaced a budget | Wording | 66% of 216 companies target existing spend | Stellaris post |
| Hyperscaler capex $780 bn / $416 bn (spoken) | Relabel | a16z chart figures, 30 Sep 2026 | a16z State of Markets II |
| 2% of US households pay for AI (spoken) | Relabel | 2.2%, as of April 2026 (a16z chart) | a16z State of Markets II |
| 80% of lab revenue from top 1% of customers | Wording | 80% of Ramp-observed business spend on the two labs | Ara Kharazian post, Sep 2026 |
| UPI 86% of retail digital payments | Wording | By count; by value far lower | RBI Annual Report 2025-26 |
| Fraud growing 18 to 20% a year | Unverified | Spoken, United States; no regulator data | a16z video |
| NBFC average cost of funds | Not found | Range with anchors: AAA 7.54%, A- 14.44% | ICRA; DRHP |
