---
name: ai-policy
description: |
  Generate an AI acceptable use policy for a UK business. Covers shadow AI,
  data protection, approved tools, staff responsibilities, and GDPR basics.
  Use when someone asks about AI policy, shadow AI, "what rules should we
  have for AI", acceptable use, or GDPR and AI tools in the workplace.
allowed-tools:
  - Read
  - Write
  - Edit
---

# AI Policy Generator

You generate a practical AI acceptable use policy for a UK business. Not a legal document. A clear, readable policy that staff will actually follow and management can enforce.

## When to Use This Skill

- "We need an AI policy"
- "What rules should we have for AI in the workplace?"
- "People are using ChatGPT with company data, what do we do?"
- "Shadow AI policy"
- "AI acceptable use policy"
- "GDPR and AI tools"

## What You Need From the User

1. **Company name** (for the policy header)
2. **Sector** (affects what data sensitivities to flag)
3. **Approximate size** (sole trader, 5-10, 10-50, 50-200, 200+)
4. **Which AI tools they already use or plan to use** (Claude, ChatGPT, Copilot, etc.)
5. **Any specific concerns** (data leaks, client confidentiality, regulated industry)

If the user does not provide all of these, generate a sensible default and note what they should customise.

## Workflow

### Step 1: Understand the Context

Based on the sector and size, determine:
- What types of sensitive data they likely handle (client data, financial, health, legal, personal)
- Whether they operate in a regulated industry (financial services, healthcare, legal, education)
- What level of detail the policy needs (a 5-person agency needs 2 pages, not 20)

### Step 2: Generate the Policy

Structure the policy as:

```
# [Company Name] AI Acceptable Use Policy

**Effective date:** [Today's date]
**Review date:** [6 months from today]
**Owner:** [Role, e.g. "Managing Director" or "Operations Manager"]

## Purpose

This policy sets out how [Company Name] staff may use AI tools in their work.
It exists to protect our clients, our data, and our reputation.

## Approved Tools

The following AI tools are approved for use at [Company Name]:

| Tool | Approved for | Not approved for |
|------|-------------|-----------------|
| [Tool 1] | [Permitted uses] | [Restricted uses] |
| [Tool 2] | [Permitted uses] | [Restricted uses] |

Any tool not on this list requires approval from [role] before use.

## What You Must Not Do

1. **Do not paste client data, personal data, or confidential information into any AI tool** unless it is on the approved list AND used within its approved scope.
2. **Do not use personal AI accounts** (e.g. your own ChatGPT subscription) for company work. This is shadow AI and creates data protection risk for the business.
3. **Do not rely on AI output without checking it.** AI tools can produce inaccurate, outdated, or fabricated information. You are responsible for the accuracy of your work.
4. **Do not use AI to generate content that is presented as your original professional opinion** without review (e.g. legal advice, medical guidance, financial recommendations).
5. **Do not upload client files, contracts, or documents** to AI tools without explicit approval.

## What You Should Do

1. **Use approved tools for approved purposes.** They are there to help you work faster and better.
2. **Check AI output before sending, publishing, or acting on it.** You own the output, not the tool.
3. **Tell your manager if you find a useful AI workflow.** We want to learn from what works.
4. **Ask before using a new tool.** If you have found something that could help, raise it. We will assess it.
5. **Report any data incident.** If you accidentally paste sensitive data into an unapproved tool, report it to [role] immediately. Early reporting is not punished.

## Data Protection (UK GDPR)

Under UK GDPR, [Company Name] is the data controller. This means:
- **We are responsible** for how personal data is processed, even if an AI tool does the processing.
- **The ICO enforces against us**, not against OpenAI or Anthropic.
- **Consent does not transfer.** A client consenting to share data with us does not mean they consent to that data being processed by a third-party AI service.

If you are unsure whether something counts as personal data, assume it does and ask.

## Shadow AI

Shadow AI is when staff use AI tools that the business has not approved, often with good intentions. This creates risk because:
- Data may be stored or used to train models outside our control
- We cannot audit what was shared
- We may breach client contracts or data protection obligations

If you are currently using a personal AI tool for work, tell [role]. You will not be in trouble. We want to find a way to support what is working while managing the risk.

## Review

This policy will be reviewed every 6 months or when:
- A new AI tool is adopted
- A data incident occurs
- Regulations change

## Staff Acknowledgement

I have read and understood this policy.

Name: ____________________
Date: ____________________
Signature: ____________________
```

### Step 3: Customise for Sector

Add sector-specific notes:

- **Legal:** Client legal privilege. AI-generated drafts must be reviewed by a qualified solicitor. Do not upload case files.
- **Financial services:** FCA requirements. AI cannot make regulated financial decisions without human oversight.
- **Healthcare:** Patient data is special category data under UK GDPR. Higher bar for processing.
- **Property:** Client financial information, AML obligations. Do not upload ID documents or proof of funds.
- **Education:** Student data, safeguarding considerations. Parental consent may be required.
- **General:** Focus on client confidentiality and commercial sensitivity.

### Step 4: Add Practical Guidance

After the formal policy, add a short "Quick Reference" section:

```
## Quick Reference

**Can I use [approved tool] to draft an email?** Yes.
**Can I paste a client contract into ChatGPT?** No.
**Can I use my personal ChatGPT account for work?** No.
**I found a useful AI tool. Can I use it?** Ask first.
**I accidentally pasted client data into an AI tool.** Report it to [role] immediately.
**Can I use AI to help with internal documents?** Yes, if no personal or client data is included.
```

## Output Rules

- Write in plain English. This is for staff, not lawyers.
- Keep it under 1,500 words for businesses under 50 people. Longer policies do not get read.
- Use "you" and "we" not "the employee" and "the organisation."
- Do not use legal jargon without explanation.
- Include the acknowledgement section. It matters for enforcement.
- Always include the review date. Policies without review dates become stale.
- British English throughout.
- Note at the end: "This policy is a starting point. For regulated industries or complex data environments, seek legal advice."

## What This Skill Does NOT Do

- Provide legal advice
- Replace a Data Protection Impact Assessment (DPIA)
- Cover AI procurement or vendor assessment
- Handle international data transfer considerations in detail
- Replace professional HR or legal review for regulated industries
