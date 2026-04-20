# Legislation Search Tips

## Getting good results from `legislation_search`

### Use the short popular name, not the full title
- Good: `"Housing Act 1988"`
- Bad: `"An Act to make further provision with respect to dwelling-houses let on assured tenancies"`

### For SIs, search by subject not full title
- Good: `"working time regulations"`
- Bad: `"The Working Time Regulations 1998 No. 1833"`

### Narrow by year when there are many Acts on a topic
- `"Data Protection Act 2018"` not just `"data protection"`
- The search returns many results — year narrows it fast

### The result gives you `legislation_type`, `year`, `number`
Feed these directly into `legislation_get_toc` then `legislation_get_section`. Do not search again.

## Getting the right section

### Always call `legislation_get_toc` first on unfamiliar Acts
Large Acts (Companies Act 2006, Equality Act 2010) have hundreds of sections. The TOC shows you Part and Schedule structure so you can target the right section number.

### For a known section number, skip the TOC
`legislation_get_section(type="ukpga", year=1988, number=50, section=21)` — goes direct.

### Sections vs schedules
- Sections are numbered: `section=21`
- Schedules need the schedule number: check TOC output for the exact reference format

## In-force status and territorial extent

The tool always returns:
- `in_force`: True/False — check this. Some sections are not yet commenced.
- `extent`: list of territories — England, Wales, Scotland, Northern Ireland

**Always report extent when citing.** A section may not apply in Scotland.

## Point-in-time legislation

For historic disputes or transactions, ask what the law said on a specific date.
The underlying API accepts a `date` parameter. Phrase the user query as:
`"What did section 21 Housing Act 1988 say on 1 October 2015?"`

The tool handles this automatically.

## Commencement orders

If `in_force` is False, the section exists in the Act but has not been brought into force by a commencement order. Note this explicitly. Do not cite it as current law.
