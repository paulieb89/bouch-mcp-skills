# VAT, MTD, and trading-address signals

VAT registration data is more valuable for DD than people realise. The HMRC VAT database tells you:
- Whether the company is VAT-registered (threshold: £90k turnover from April 2024)
- The trading name it uses (may differ from Companies House name)
- The trading address it operates from (may differ from registered office)

Discrepancies between these and Companies House records are soft fraud / compliance signals.

## What `vat_validate` returns

Input: a VAT number. Accepted formats: `GB123456789`, `123456789`, or `GB 123 456 789`.

Output: `VATValidationResult` with:
- `valid` (bool) — the number exists and is active on HMRC's register
- `vat_number` — normalised to `GB123456789`
- `trading_name` — what HMRC has on file
- `registered_address` — what HMRC has on file as trading address
- `consultation_number` — HMRC's reference for the lookup (useful if you need to cite)

## When to use VAT validation

Three use cases:

1. **Counterparty asserts a VAT number** — validate before raising an invoice. Invalid VAT means no input VAT recovery for you.
2. **DD check** — validate VAT as a cross-reference to Companies House data.
3. **Fraud flag** — invalid VAT on an invoice while the seller claims registration is classic missing-trader fraud (MTIC).

## Three signals from VAT data

### 1. Invalid VAT number

- **If the company claims to be VAT-registered** → serious flag. Either the number is mistyped (harmless but embarrassing) or fabricated (fraudulent).
- **If no claim of registration** → no flag. Sub-threshold companies (<£90k turnover) are not required to register.

Ask the counterparty to confirm the number before escalating. Humans transpose digits constantly.

### 2. Trading-name / Companies House name mismatch

The VAT trading name is what HMRC has — often the "trading as" name, not the legal entity. Common patterns:

- **"Acme Widgets Ltd" (CH) / "Acme Widgets" (VAT)** — routine, just formatting.
- **"A1 Trading Ltd" (CH) / "Best Deals Online" (VAT)** — different branding for an online store. Normal.
- **"Acme Holdings Ltd" (CH) / "Acme Trading" (VAT)** — the VAT-registered entity is a trading name of something else. Worth understanding the group structure.
- **"Alpha Ltd" (CH) / "Omega Ltd" (VAT)** — major red flag. The VAT number may belong to a different legal entity entirely.

### 3. Trading-address / registered-office mismatch

More common than the name mismatch and usually benign:

- Registered office is the formation agent's address
- Trading address is the actual warehouse / office / shop

When it's NOT benign:

- Registered office is a formation agent, trading address is residential, and the company claims to be a commercial operation
- Trading address is overseas (HMRC will have this as UK — if overseas, the registration is likely incorrect)
- Both addresses are mail-forwarding / virtual offices — no real operational footprint

## MTD (Making Tax Digital) — the April 2026 angle

From 6 April 2026, Making Tax Digital for Income Tax applies to:
- Sole traders with >£50k gross income (£30k from April 2027)
- Landlords with >£50k gross rental income (£30k from April 2027)

MTD already applies to VAT-registered businesses (since April 2022). MTD-compliant software must be used to file quarterly returns.

For DD purposes:
- A company claiming VAT registration but unable to verify MTD enrollment → investigation warranted.
- The `hmrc_check_mtd_status` MCP tool does this check via OAuth. Requires `HMRC_CLIENT_ID` and `HMRC_CLIENT_SECRET` — not available in most deployments. Safe to skip unless the use case demands it.

## Trading above or below threshold

Current threshold: £90,000 turnover (rolling 12 months). Companies above threshold must register; those below may register voluntarily.

- **Voluntary registration** (common for B2B) — lets the company reclaim input VAT. Benign signal.
- **Mandatory registration missed** — if a company is trading above £90k and not registered, it's in breach. Detectable only if you have independent revenue evidence.

For most DD checks, you validate a number the counterparty provided. You don't forensically audit their revenue.

## VAT in due diligence reports

What to include:

- Validation result (valid / invalid)
- Trading name as registered with HMRC
- Trading address as registered with HMRC
- Any discrepancies noted with Companies House (name, address)

What NOT to conclude:

- Do not infer revenue from VAT registration (many small businesses register voluntarily).
- Do not infer non-compliance from a missing VAT number (sub-threshold is fine).
- Do not cite HMRC data that isn't from the validation response (no revenue figures, no VAT return history — that data isn't public).

## Edge cases

- **Group VAT registration**: a parent company registers on behalf of a group. The VAT number belongs to the group, not the individual subsidiary. `vat_validate` on that number will return the parent's trading name. This is legal and common.
- **Recently de-registered**: a company that was VAT-registered but has de-registered (turnover dropped, business winding down) will show `valid: false`. Not the same as fraud — check the company status on Companies House in parallel.
- **New registrations**: HMRC's VAT database can lag 2–4 weeks behind actual registration. A genuine new VAT number may come back invalid briefly. Retry after 4 weeks if suspicious.

## Scope

UK VAT only. Northern Ireland businesses trading EU goods use a separate XI-prefix VAT number (XI123456789). The HMRC API accepts both GB and XI numbers — validation logic is identical.
