# JSW Ventures R2 prep

Owner: Kushal Shankar Joka. Deadline: Monday 5 Oct 2026, 4:30 pm, coffee with Vikas Chandak
(Partner, JSW Ventures) near Trinity Circle, Bangalore.

## The ask (verbatim from Vikas, 30 Sep)
"Come prepped with your views on Fintech (all segments), what kind of investments would you make.
Same for AI. And why. Docs/ppt/pdf whatever u r comfortable with as anchor to the discussion."

## Read first
- inputs/brief_jsw.md: the fund, portfolio, Vikas's profile, and what he asked and pushed back on in R1.
- rules/WORKING_PRINCIPLES.md: how Kushal works. Sections 1, 2, 3 and 7 matter most here.

## What this is and is not
- A point-of-view document that anchors a conversation. Not a company analysis, not a market report.
- Vikas tests for a view, not a list. He asked "AI beyond efficiency" three times and rejected
  three efficiency answers. Every thesis must name what changes in a business, not what gets cheaper.
- His lane is fintech plus enterprise AI, not consumer. JSW backs applied, vertical AI with a
  business outcome; cheques Rs 10-20cr, pre-Series A to Series A+, 14-16 names a fund.
- Deliverable: format is flexible. Current set (v7): a reference deck (PDF), a print pack of exhibits (PDF), a
  workbook with every figure as a sourced input and every derived number as a formula, and a private talk
  track. Formal voice, Kushal's own, no slop. Every claim sourced and dated; facts in the brief marked
  UNCERTAIN stay that way.

## Repo layout
- inputs/: the brief and any uploaded data. research/: fact base, reviews, worked examples, talk track.
- build/: spec_v7.py (every input with source, URL, date, claim type, confidence, status, range),
  build_workbook.py (workbook from the spec), evalwb.py (computes every formula in Python and dumps
  values_v7.json), render_pack.py and deck_v7.py (HTML to PDF via headless Chromium). Rebuild order:
  evalwb, build_workbook, render_pack, deck_v7.
- outputs/: JSW_R2_workbook_v7.xlsx, JSW_R2_print_pack_v7.pdf, JSW_R2_reference_deck_v7.pdf.

## Rules
- Commit and push after each step. Plan mode first: agree the theses before any drafting.
