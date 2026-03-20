# TVIS MCH Director Scraper

Automatically scrapes state MCH Director contact data from
[mchb.tvisdata.hrsa.gov](https://mchb.tvisdata.hrsa.gov/Home/StateContacts)
and keeps two CSVs up to date in this repo.

## Output files

| File | Contents |
|------|----------|
| `data/tvis_mch_directors.csv` | Title V / MCH Directors only (one per state/territory) |
| `data/tvis_all_contacts.csv` | All contact types across all 59 states/territories |

### Contact types
| Type | Role |
|------|------|
| 1 | MCH Director |
| 2 | CSHCN Director |
| 3 | Family/Youth Leader |
| 4 | Youth Leader |
| 5 | SSDI Project Director |

## Schedule

Runs every **Monday at 7:00 AM UTC** via GitHub Actions.
The workflow only commits when contact data has actually changed,
so the git history gives you a clean record of director turnover over time.

## Manual run

Trigger a run any time from the **Actions** tab → **Weekly TVIS MCH Director Scrape** → **Run workflow**.

## Local run

```bash
python scrape_tvis.py
```

No dependencies beyond the Python standard library.

## Source API

```
GET https://mchb.tvisdata.hrsa.gov/api/Values/GetContactsByStateOrRegion?state=00
```

`state=00` returns all states/territories at once.
