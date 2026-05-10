---
name: p6-health-check
description: |
  Audit a Primavera P6 XER schedule file. Produces a health score, critical
  path analysis, float distribution, logic quality assessment, and prioritised
  recommendations. Use when someone uploads an XER or asks to check, audit,
  or review a schedule. Requires the PyP6Xer MCP server.
---

# P6 Schedule Health Check

Audit a Primavera P6 XER schedule and tell the project manager what's wrong, what's at risk, and what to fix first.

## Thinking Like a PM

The person asking has been handed a programme — usually by a contractor — and needs to know if it's credible. They're not looking for a data dump. They want answers to:

1. **Is this schedule healthy?** A single score they can put in a report or use in a meeting. Red, amber, green. A number out of 100.
2. **Where are the problems?** Missing logic, negative float, activities without predecessors or successors. These undermine the critical path and make the programme unreliable.
3. **What's at risk?** Which activities are slipping? Is the critical path continuous or broken? How much float buffer exists in the programme?
4. **What should they fix first?** Prioritised recommendations, not a list of 50 issues with equal weight. Negative float before missing successors. Logic gaps before long durations.

A healthy schedule typically has 10-20% of activities on the critical path. Below 5% suggests incomplete logic. Above 30% suggests over-constraining. These benchmarks matter — state them.

## What the Tools Give You

`schedule_health_check` returns an overall score (0-100) with component scores for completion, float health, logic quality, and slippage. This is the headline.

`schedule_quality` finds the specific issues — activities without predecessors, without successors, with negative float, with excessive float, and with long durations. These are the details behind the score.

`critical_path` returns activities with zero or negative float. The percentage of activities on the critical path tells you about schedule structure. A critical path with gaps (non-contiguous) means the logic is incomplete.

`float_analysis` shows how float is distributed — critical, near-critical (1-5 days), and healthy (>5 days). The shape of this distribution tells the story.

`slipping_activities` compares forecast finish to baseline finish. These are the activities that are actively causing the programme to overrun.

`progress_summary` gives completion rates by count and by duration (weighted). The duration-weighted figure is more meaningful — a programme can be 80% complete by activity count but only 40% complete by duration if the remaining activities are the big ones.

## How to Work

**Load the file first.** Accept URL, local path, or upload. Note the cache_key — you need it for every subsequent call. If there are multiple projects in the file, ask which one or default to the largest.

**Run the health check for the headline.** This gives you the overall score and component breakdowns in one call. Lead with this.

**Then dig into specifics.** Pull quality issues, critical path, and float distribution. You don't always need all of them — if the health score is 85+, a brief summary suffices. If it's below 60, the user needs the full breakdown with specific activities named.

**Slippage only matters if there's a baseline.** If the XER has no baseline dates, slipping_activities returns nothing useful. Note this rather than reporting "no slipping activities" as if it's good news.

## When Things Go Wrong

- **File won't load:** Check the URL is accessible. XER files from email attachments often need re-saving. Suggest the upload URL approach.
- **Zero activities:** The XER may contain only project-level data with no activities. Report this.
- **No critical path:** This is a finding, not an error. A schedule with no critical path has incomplete logic — the programme end date is not driven by the activity network. Flag it prominently.
- **All activities are critical:** Also a finding. The schedule is either over-constrained or every activity is on a single chain. This makes the programme extremely fragile.
- **Earned value shows zero:** The XER likely has no cost-loaded resources. Pivot to schedule-only metrics.

## Good vs Bad Output

**Good:** Opens with health score and one-sentence assessment. Groups issues by severity. Names specific activities. Explains why an issue matters ("12 activities without predecessors means the critical path may not reflect reality"). Recommendations are prioritised and actionable.

**Bad:** Dumps every metric without interpretation. Lists 50 activities with missing predecessors without explaining the impact. Gives recommendations like "improve schedule quality" without saying how. Reports "no slipping activities" without checking whether a baseline exists.

## Formatting

Programme, not project (UK context). Float, not slack. British spelling throughout. Health score as X/100 with a rating (Healthy/Caution/At Risk/Critical). Activity codes included in issue lists. Durations in days. Always include: schedule analysis, not programme assurance.
