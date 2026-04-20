---
name: legislation-lookup
description: |
  Look up a UK Act of Parliament or Statutory Instrument and retrieve a specific
  section. Returns the section text, in-force status, and territorial extent.
  Use when someone asks "what does the law say about X?" or "find me the section
  on X". Requires the UK Legal MCP server to be connected.
---

# Quick Legislation Lookup

You search UK legislation and retrieve the text of a specific section. This is a lookup, not a full legal brief.

## Required Setup

Connect the **UK Legal MCP server**:

```json
{
  "mcpServers": {
    "uk-legal": {
      "url": "https://uk-legal-mcp.fly.dev/mcp"
    }
  }
}
```

## Workflow

1. Get the legal topic or Act name from the user
2. Call `legislation_search` with keywords to find the relevant Act or SI
3. Call `legislation_get_toc` on the most relevant result to see its structure
4. Call `legislation_get_section` to retrieve the specific section text
5. Present the section with its status

## Output

```
## [Act Name], [Section Number]

**Status**: [In force / Not yet in force / Repealed]
**Extent**: [England and Wales / Scotland / Northern Ireland / UK-wide]

[Section text]

**Note**: [Any relevant context about amendments or commencement]
```

Keep it factual. This is a text lookup, not legal advice.

For common Acts and their type/year/number codes, see [references/common-acts.md](references/common-acts.md).
For search tips and edge cases, see [references/search-tips.md](references/search-tips.md).
Use the output template in [assets/output-template.md](assets/output-template.md).

## Want More?

For a full legal research brief with case law, OSCOLA citations, Hansard debates, and plain English analysis, see the **Legal Research Brief** at [bouch.dev/tools/legal-research](https://bouch.dev/tools/legal-research/).

For parliamentary landscape analysis on a policy topic, see the **Parliamentary Policy Briefing** at [bouch.dev/tools/policy-briefing](https://bouch.dev/tools/policy-briefing/).
