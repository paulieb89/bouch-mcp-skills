# Common UK Acts — Quick Reference

Use these when you know the Act but need to call `legislation_get_toc` or `legislation_get_section` directly.

Format for `legislation_get_section`: `type=ukpga, year=YYYY, number=NN, section=N`

## Property & Housing

| Act | Type | Year | Number |
|-----|------|------|--------|
| Housing Act 1988 | ukpga | 1988 | 50 |
| Housing Act 1996 | ukpga | 1996 | 52 |
| Housing Act 2004 | ukpga | 2004 | 34 |
| Landlord and Tenant Act 1985 | ukpga | 1985 | 70 |
| Landlord and Tenant Act 1987 | ukpga | 1987 | 31 |
| Leasehold Reform Act 1967 | ukpga | 1967 | 88 |
| Leasehold Reform, Housing and Urban Development Act 1993 | ukpga | 1993 | 28 |
| Commonhold and Leasehold Reform Act 2002 | ukpga | 2002 | 15 |
| Land Registration Act 2002 | ukpga | 2002 | 9 |
| Law of Property Act 1925 | ukpga | 1925 | 20 |

## Employment & Equality

| Act | Type | Year | Number |
|-----|------|------|--------|
| Equality Act 2010 | ukpga | 2010 | 15 |
| Employment Rights Act 1996 | ukpga | 1996 | 18 |
| National Minimum Wage Act 1998 | ukpga | 1998 | 39 |
| Working Time Regulations 1998 | uksi | 1998 | 1833 |
| TUPE Regulations 2006 | uksi | 2006 | 246 |

## Company & Commercial

| Act | Type | Year | Number |
|-----|------|------|--------|
| Companies Act 2006 ⚠️ | ukpga | 2006 | 46 |
| Insolvency Act 1986 | ukpga | 1986 | 45 |
| Sale of Goods Act 1979 | ukpga | 1979 | 54 |
| Consumer Rights Act 2015 | ukpga | 2015 | 15 |
| Unfair Contract Terms Act 1977 | ukpga | 1977 | 50 |
| Late Payment of Commercial Debts Act 1998 | ukpga | 1998 | 20 |

## Human Rights & Civil Liberties

| Act | Type | Year | Number |
|-----|------|------|--------|
| Human Rights Act 1998 | ukpga | 1998 | 42 |
| Data Protection Act 2018 | ukpga | 2018 | 12 |
| Freedom of Information Act 2000 | ukpga | 2000 | 36 |
| Police and Criminal Evidence Act 1984 | ukpga | 1984 | 60 |

## Criminal Law

| Act | Type | Year | Number |
|-----|------|------|--------|
| Theft Act 1968 | ukpga | 1968 | 60 |
| Fraud Act 2006 | ukpga | 2006 | 35 |
| Proceeds of Crime Act 2002 | ukpga | 2002 | 29 |
| Serious Crime Act 2007 | ukpga | 2007 | 27 |

## Tax

| Act | Type | Year | Number |
|-----|------|------|--------|
| Income Tax Act 2007 | ukpga | 2007 | 3 |
| Corporation Tax Act 2009 | ukpga | 2009 | 4 |
| Value Added Tax Act 1994 | ukpga | 1994 | 23 |
| Inheritance Tax Act 1984 | ukpga | 1984 | 51 |
| Capital Gains Tax Act 1979 (TCGA 1992 supersedes) | ukpga | 1992 | 12 |

## Known API Limitations

**Companies Act 2006 ⚠️** — both `legislation_get_toc` and `legislation_get_section` return "Document is empty" for this Act. The reference number ukpga/2006/46 is correct (confirmed via `legislation_search`) but the Act is not served by the legislation.gov.uk API. Use [legislation.gov.uk directly](https://www.legislation.gov.uk/ukpga/2006/46/contents) for Companies Act sections, or search by keyword with `fulltext=true`.

## Notes

- `ukpga` = UK Public General Act
- `uksi` = UK Statutory Instrument
- `ukla` = UK Local Act (rare)
- For Scottish Acts use `asp`, for Welsh use `anaw`/`asc`
- Use `legislation_search` when the Act number is not known
