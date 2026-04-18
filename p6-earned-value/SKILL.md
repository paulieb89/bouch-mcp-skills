---
name: p6-earned-value
description: |
  Produce an earned value management (EVM) report from a Primavera P6 XER file.
  Calculates PV, EV, AC, CPI, SPI, and forecasts, with progress breakdown
  by WBS and resource utilisation. Use when someone says "earned value report",
  "EVM analysis", "is this project on budget", "CPI/SPI", or needs cost and
  schedule performance metrics from a P6 file.
  Requires the PyP6Xer MCP server (pyp6xer-mcp) to be connected.
---

# P6 Earned Value Report

You produce earned value management (EVM) reports from Primavera P6 XER schedule files. You calculate the standard EVM metrics, interpret what they mean in plain language, and break down performance by work package and resource.

The person you are helping is typically a QS, commercial manager, or project controls analyst who needs to report on cost and schedule performance. Give them the numbers they need in a format they can present.

## When to Use This Skill

- "Run an earned value analysis"
- "What's the CPI and SPI?"
- "Is this project on budget?"
- "EVM report for this schedule"
- "How's the project performing against plan?"
- Any request for cost/schedule performance metrics from a P6 file

## Required Setup

This skill requires the **PyP6Xer MCP server** (pyp6xer-mcp) to be connected.

Live server: https://pyp6xer-mcp.fly.dev/mcp

**Tools you will use (in order):**

1. `pyp6xer_load_file` — load and parse the XER file
2. `pyp6xer_earned_value` — core EVM metrics (PV, EV, AC, CPI, SPI, CV, SV)
3. `pyp6xer_progress_summary` — completion rates by count and duration
4. `pyp6xer_resource_utilization` — resource allocation and overallocation
5. `pyp6xer_work_package_summary` — progress by activity code prefix
6. `pyp6xer_wbs_analysis` — WBS hierarchy with activity counts

## Workflow

### Step 1: Load the XER File

Same as the health check — accept URL, local path, or base64. Note the cache_key.

If the file contains multiple projects, call `pyp6xer_list_projects` and ask the user which one to analyse, or default to the largest.

### Step 2: Run Earned Value Analysis

Call `pyp6xer_earned_value` with the cache_key and project_id.

This returns:
- **Planned Value (PV/BCWS)**: the budgeted cost of work scheduled
- **Earned Value (EV/BCWP)**: the budgeted cost of work performed
- **Actual Cost (AC/ACWP)**: the actual cost of work performed
- **Cost Variance (CV)**: EV - AC (positive = under budget)
- **Schedule Variance (SV)**: EV - PV (positive = ahead of schedule)
- **Cost Performance Index (CPI)**: EV / AC (>1 = under budget)
- **Schedule Performance Index (SPI)**: EV / PV (>1 = ahead of schedule)

**Important:** XER files often have incomplete cost data (resources not assigned, or costs at zero). If PV, EV, and AC are all zero or very low, flag this clearly — the schedule may not have cost-loaded resources. In that case, focus the report on schedule performance (progress, float, slippage) rather than cost metrics.

### Step 3: Get Progress Summary

Call `pyp6xer_progress_summary` for:
- Activity count by status (complete, in progress, not started)
- Completion rate by count
- Completion rate by duration (weighted — more meaningful)
- Average physical % complete

### Step 4: Check Resource Utilisation

Call `pyp6xer_resource_utilization` for:
- Resources assigned
- Overallocated resources (working beyond capacity)
- Underutilised resources
- Resource distribution across the programme

If no resources are assigned in the file, note this and skip the resource section.

### Step 5: Break Down by Work Package

Call `pyp6xer_wbs_analysis` to understand the programme structure.

Then call `pyp6xer_work_package_summary` with the top-level WBS prefixes to get per-package metrics:
- Activity count per package
- Completion % per package
- Critical activities per package
- Remaining duration per package

This shows where the programme is on track and where it's falling behind.

### Step 6: Calculate Forecasts

From the EVM metrics, calculate:

- **Estimate at Completion (EAC)**: BAC / CPI (what we expect the total cost to be)
- **Variance at Completion (VAC)**: BAC - EAC (expected cost overrun/underrun)
- **To Complete Performance Index (TCPI)**: (BAC - EV) / (BAC - AC) (what CPI needs to be from now on to finish on budget)

Where BAC = total Planned Value (budget at completion).

If CPI is below 0.9, flag that the project is unlikely to recover without intervention. If TCPI exceeds 1.2, recovery is very difficult historically.

## Output Format

```
# Earned Value Report: [Project Name]

## Executive Summary
- **Cost Status**: [Under/Over budget] by [£X] (CPI: [X])
- **Schedule Status**: [Ahead/Behind schedule] (SPI: [X])
- **Overall Progress**: [X]% complete (weighted by duration)
- **Forecast**: [One sentence on where this is heading]

## EVM Dashboard

| Metric | Value | Status |
|--------|-------|--------|
| Planned Value (PV) | £[X] | Budget baseline |
| Earned Value (EV) | £[X] | Work completed |
| Actual Cost (AC) | £[X] | Actual spend |
| Cost Variance (CV) | £[X] | [Under/Over] budget |
| Schedule Variance (SV) | £[X] | [Ahead/Behind] schedule |
| CPI | [X] | [Good/Caution/Poor] |
| SPI | [X] | [Good/Caution/Poor] |

## Forecasts

| Metric | Value |
|--------|-------|
| Budget at Completion (BAC) | £[X] |
| Estimate at Completion (EAC) | £[X] |
| Variance at Completion (VAC) | £[X] |
| To Complete Performance Index (TCPI) | [X] |

## Progress Breakdown

| Status | Count | % |
|--------|-------|---|
| Complete | [N] | [X]% |
| In Progress | [N] | [X]% |
| Not Started | [N] | [X]% |

**Weighted completion** (by duration): [X]%

## Work Package Performance

| Package | Activities | % Complete | Critical | Remaining (days) |
|---------|-----------|------------|----------|-------------------|
| [WBS 1] | [N] | [X]% | [N] | [X] |
| [WBS 2] | [N] | [X]% | [N] | [X] |

## Resource Utilisation
[Summary of resource allocation, any overallocation flags]

## Interpretation and Recommendations
1. [Cost finding and recommendation]
2. [Schedule finding and recommendation]
3. [Resource or work package specific recommendation]
```

## Key Principles

- **Flag missing cost data.** Many XER files don't have resources cost-loaded. If the EVM numbers look empty, say so and pivot to schedule-only metrics.
- **CPI and SPI are the headline.** Everything else supports these two numbers.
- **Context the indices.** CPI of 0.95 on a £10M project means £500K overrun. State the pound value, not just the ratio.
- **Forecasts are projections, not predictions.** EAC assumes current performance continues. Say so.
- **Work package breakdown is where the insight is.** The overall CPI might look fine but one package could be hemorrhaging. Break it down.
