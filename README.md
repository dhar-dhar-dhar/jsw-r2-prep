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

## Repo layout and rebuild
- build/spec_v7.py holds every input (source, URL, date, claim type, confidence, status, range) and every
  sheet as formulas. Rebuild: `python3 build/evalwb.py && python3 build/build_workbook.py &&
  python3 build/render_pack.py && python3 build/deck_v7.py`. Outputs land in outputs/.
- research/: worked examples per sub-sector, the v6 review, the talk track.

## Rules
- Commit and push after each step. Plan mode first: agree the theses before any drafting.
