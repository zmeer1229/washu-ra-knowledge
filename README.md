# WashU RA knowledge

Unofficial, public reference guide compiled from the WashU Resident Advisors website on **2026-10-22**. Organized for human reading, search, and AI retrieval.

This collection includes **14 page text extracts, 50 document text extracts, 20 embedded images, 14 topic guides, 83 links, and 57 document catalog entries**. Start with the [actual extracted content](CONTENT.md), or search the AI retrieval index. Source text and OCR include explicit provenance and extraction limits.

## Start here

| Need | Guide |
| --- | --- |
| Duty shifts, phone expectations, duty forms | [Duty](topics/duty.md) |
| Find incident, lockout, maintenance, or mediation reference | [Policies](topics/policies.md), [document finder](DOCUMENTS.md) |
| Plan programs and intentional conversations | [Programming](topics/programming.md), [program lists](topics/program-planning.md) |
| Create or review a bulletin board | [Bulletin boards](topics/bulletin-boards.md) |
| Run floor or seasonal meetings | [Community meetings](topics/community-meetings.md), [meeting agendas](topics/meeting-agendas.md) |
| Use branding or manage community social media | [Branding](topics/branding.md) |
| Find expense-report instructions | [Expenses](topics/expense-reports.md) |
| Find training presentations and calendars | [Training](topics/training.md) |
| Follow communication standards | [Role expectations](topics/about-ra.md) |
| Find student support | [Campus directory](topics/campus-resources.md) |
| Understand Residential Life's mission | [Mission and team](topics/team.md) |
| Nominate an OTM award | [Recognition](topics/home.md) |

## Search locally

Python 3.10+; standard library only:

```sh
python tools/search.py "roommate mediation"
python tools/search.py "winter meeting" --limit 5
python tools/search.py "maintenance" --json
python tools/validate.py
```

Use [LINKS.md](LINKS.md) for clickable resources and [DOCUMENTS.md](DOCUMENTS.md) for exact file titles. JSON and JSONL data live in `data/`. AI tools should read [AGENTS.md](AGENTS.md) and [llms.txt](llms.txt).

## Coverage and access

All 15 entries in the Site Pages inventory were opened. One is a default SharePoint template and another duplicates the landing-page content. Word files from the five document-library categories and four duty guides were extracted; six access-control files are withheld. Videos, historical schedules, external sites, and Teams messages are **not** fully exported. The Anchor, Passive, and Active program-list targets reported unavailable in the current session. [Coverage metadata](data/coverage.json) describes these limits precisely.

Some original sources require WashU authorization. This repository does not grant it. Access codes, personal records, contact details, accounting values, and shared access links are omitted. Keep private resident information out of issues, pull requests, and AI prompts.

The original website and current supervisor guidance take priority. This guide is unofficial and is not an emergency procedure manual. Document titles alone do not establish a procedure.

## Updating

Review the original page, update the relevant topic and its observation date, and record any access or coverage limits. Update structured data consistently, then run `python tools/build_index.py` and `python tools/validate.py`. Do not add account tokens or raw browser captures.

Original WashU material remains attributable to its source owners. No blanket license is asserted over third-party materials.
