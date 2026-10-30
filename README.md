# dataset-samsung-device-updates

![collection status](badges/project.svg)

Samsung devices listed for regular security updates, with their update cadence, read daily
from Samsung Mobile Security's
[security updates scope](https://security.samsungmobile.com/workScope.smsb) page.

The data is in [`dataset/samsung_device_updates.csv`](dataset/samsung_device_updates.csv),
one row per model:

| Column | Example | Meaning |
| --- | --- | --- |
| `id` | `rec_02105a6ab430a0a15eb9` | Stable record id |
| `model` | `Galaxy S25 Ultra` | Device model as Samsung lists it |
| `series` | `Galaxy S Series` | Series heading the model is listed under |
| `cadence` | `Monthly` | `Monthly`, `Quarterly` or `Biannual`; empty when the heading names none |
| `group` | `Current Models for Monthly Security Updates` | The list heading |
| `_source`, `_source_url` | | Provenance |

A model can appear in more than one group. `exports/records.jsonl` holds the same rows as
JSON lines, and `dataherb.json` describes both files for the
[DataHerb](https://dataherb.github.io) catalog.

## How it is collected

This is a [gleanyard](https://github.com/kausalflow/gleanyard) project: the scheduled
`collect` workflow fetches the page, extracts the lists with the CSS mapping in `mappings/`,
checks every record against `schema.yaml`, and reports the source's health in `status.json`.
When the page changes shape, the run fails or flags the source as degraded and opens a
`repair` issue, instead of writing broken rows.

```
schema.yaml            the contract every record meets
sources/<id>.yaml      the source (delivery + extract + rights)
mappings/<id>.json     its CSS selector mapping
evidence/              terms evidence for the source
tests/fixtures/        a saved page that guards the mapping against regressions
status.json            health report, written by every scheduled run
CLAUDE.md              ground rules for an AI assistant
```
