# MCP Error Handling

## Tool Failures

The uk-due-diligence MCP can return errors for individual tools without taking the whole server down. Handle these gracefully.

**One tool fails, others work:** Continue the workflow with what you have. Note the gap in the brief's "Sources checked" section. For example: "Companies House profile and PSC retrieved. Officers API unavailable (server error) — director list not verified."

**Never fabricate to fill a gap.** If officers data is missing, do not invent directors from web search alone. Say it is missing.

**Transient errors:** If a tool fails on first call, try once more before giving up. If the first error is a 5xx from the upstream API (application-layer, e.g. 500 "API request failed") and the retry returns a 502 from the proxy (transport-layer), that is a mixed failure — try once more before giving up. Three attempts is the hard ceiling. Never retry beyond three.

**Whole server unreachable:** Tell the user the UK Due Diligence MCP appears to be disconnected, and offer to fall back to web-only research with a clear caveat that the structural register data will not be available.

**Critical gaps for the brief:** If you lost `company_profile` entirely, you do not have enough structural data to proceed. Tell the user and stop.

The goal is partial output with honest gaps, not a clean-looking brief that invented what it could not retrieve.
