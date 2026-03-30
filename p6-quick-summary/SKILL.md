---
name: p6-quick-summary
description: |
  Load a Primavera P6 XER file and get a quick progress summary. Returns
  activity count, status breakdown, and completion percentage. Use when
  someone uploads an XER file or says "what's in this schedule?" or
  "quick look at this XER". Requires the PyP6Xer MCP server to be connected.
---

# Quick P6 Schedule Summary

You load a Primavera P6 XER file and present a quick overview of what is in it. This is a summary, not an audit.

## Required Setup

Connect the **PyP6Xer MCP server**:

```json
{
  "mcpServers": {
    "pyp6xer": {
      "url": "https://pyp6xer-mcp.fly.dev/mcp"
    }
  }
}
```

## Workflow

1. Get the XER file from the user (URL, local path, or upload)
2. Call `pyp6xer_load_file` with the file path or URL. Note the `cache_key`.
3. Call `pyp6xer_progress_summary` with the cache_key
4. Present the results

## Output

```
## Schedule Summary: [Project Name]

- **Total activities**: [N]
- **Completed**: [N] ([X]%)
- **In progress**: [N] ([X]%)
- **Not started**: [N] ([X]%)
- **Completion by duration**: [X]% (weighted)

[Progress bar]
```

Keep it brief. This is a quick look, not a health check.

## Want More?

For a full schedule health check with critical path analysis, float distribution, logic quality assessment, slipping activities, and prioritised recommendations, see the **P6 Schedule Health Check** at [bouch.dev/products/p6-health-check](https://bouch.dev/products/p6-health-check/).

For earned value analysis with CPI, SPI, forecasts, and WBS breakdown, see the **P6 Earned Value Report** at [bouch.dev/products/p6-earned-value](https://bouch.dev/products/p6-earned-value/).
