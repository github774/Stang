# Directives

This folder contains **Standard Operating Procedures (SOPs)** written in Markdown.

## Purpose

Directives are the "what to do" layer of the 3-layer architecture. Each directive defines:

- **Objective** — What this process accomplishes
- **Inputs** — What data/parameters are required
- **Tools/Scripts** — Which `execution/` scripts to call
- **Outputs** — Expected deliverables
- **Edge Cases** — Known failure modes and how to handle them

## Rules

- Directives are **living documents** — update them when you learn something new
- Do **not** create or overwrite directives without asking unless explicitly instructed
- Every major workflow should have a corresponding directive

## Naming Convention

```
directives/
├── scrape_website.md
├── send_email_report.md
├── process_data.md
└── ...
```

## Template

```markdown
# [Directive Name]

## Objective
One-sentence description of what this directive achieves.

## Inputs
- `param_name` (type) — description

## Tools
- `execution/script_name.py` — what it does

## Outputs
- description of expected output / deliverable location

## Edge Cases
- **Rate limits**: ...
- **Missing data**: ...
```
