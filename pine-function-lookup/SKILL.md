---
name: pine-function-lookup
description: |
  Look up a Pine Script v6 function and get its signature, parameters, and a
  usage example. Use when someone asks "how do I use [function] in Pine Script?"
  or "what are the parameters for [function]?". Requires the PineScript MCP
  server to be connected.
---

# Pine Script Function Lookup

You look up Pine Script v6 functions and return the correct signature, parameters, and usage. This is a reference lookup, not a strategy builder.

## Required Setup

Connect the **PineScript MCP server**:

```json
{
  "mcpServers": {
    "pinescript": {
      "url": "https://pinescript-mcp.fly.dev/mcp"
    }
  }
}
```

## Workflow

1. Get the function name or trading concept from the user
2. If they give a function name, call `search_docs` to find it
3. Call `get_doc` to retrieve the full documentation
4. If they describe a concept (e.g. "moving average"), call `resolve_topic` first to find the right v6 functions
5. Present the function signature and a clean usage example

## Output

```
## [function_name]()

**Namespace**: [ta / strategy / math / etc.]

**Signature**:
`[function_name](param1, param2, ...)`

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| [name] | [type] | [default] | [description] |

**Returns**: [return type and description]

**Example**:
```pine
[clean usage example]
```
```

Keep it factual. This is a docs lookup, not a strategy.

## Want More?

For a complete Pine Script v6 strategy built from a plain-English trading idea — with validated syntax, linting, and a full explanation — see the **Pine Script Strategy Builder** at [bouch.dev/products/pine-strategy-builder](https://bouch.dev/products/pine-strategy-builder/).
