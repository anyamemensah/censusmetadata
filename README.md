# censusmetadata

`censusmetadata` is a Python package that provides a simplified interface for accessing the United States (U.S.) Census Bureau’s API to retrieve metadata from publicly accessible datasets. With its two core functions,`get_census_apis()` and `get_census_metadata()`, you can easily retrieve a list of available datasets, filtering by survey, program, or vintage year, and obtain metadata such as variable names, variable labels, value codes, and value code labels for a specific dataset.

## Install

To install the package with uv, run:

```terminal
uv add git+https://github.com/anyamemensah/censusmetadata.git
```

## Using censusmetadata

1. Import libraries:

```python
from censusmetadata import get_census_apis, get_census_metadata
import polars as pl
```

2. Retrieve the complete list of publicly available datasets provided by the U.S. Census Bureau.

```python
all_apis = get_census_apis()
all_apis.head()

shape: (5, 10)
┌──────────┬──────────┬──────────┬─────────┬───┬─────────┬─────────┬─────────┬─────────┐
│ dataset  ┆ title    ┆ descript ┆ vintage ┆ … ┆ geograp ┆ api_url ┆ contact ┆ modifie │
│ ---      ┆ ---      ┆ ion      ┆ ---     ┆   ┆ hyLink  ┆ ---     ┆ ---     ┆ d       │
│ str      ┆ str      ┆ ---      ┆ i64     ┆   ┆ ---     ┆ str     ┆ str     ┆ ---     │
│          ┆          ┆ str      ┆         ┆   ┆ str     ┆         ┆         ┆ str     │
╞══════════╪══════════╪══════════╪═════════╪═══╪═════════╪═════════╪═════════╪═════════╡
│ timeseri ┆ Annual   ┆ The      ┆ null    ┆ … ┆ http:// ┆ http:// ┆ ewd.out ┆ 2025-04 │
│ es/aies/ ┆ Integrat ┆ Annual   ┆         ┆   ┆ api.cen ┆ api.cen ┆ reach@c ┆ -11 13: │
│ basic    ┆ ed       ┆ Integrat ┆         ┆   ┆ sus.gov ┆ sus.gov ┆ ensus.g ┆ 20:27.0 │
│          ┆ Economic ┆ ed Econo ┆         ┆   ┆ /data/t ┆ /data/t ┆ ov      ┆         │
│          ┆ Sur…     ┆ mic…     ┆         ┆   ┆ im…     ┆ im…     ┆         ┆         │
│ timeseri ┆ Annual   ┆ The      ┆ null    ┆ … ┆ http:// ┆ http:// ┆ Ewd.out ┆ 2018-12 │
│ es/asm/a ┆ Economic ┆ Annual   ┆         ┆   ┆ api.cen ┆ api.cen ┆ reach@c ┆ -13 00: │
│ rea2012  ┆ Surveys: ┆ Survey   ┆         ┆   ┆ sus.gov ┆ sus.gov ┆ ensus.g ┆ 00:00.0 │
│          ┆ Annua…   ┆ of Manuf ┆         ┆   ┆ /data/t ┆ /data/t ┆ ov      ┆         │
│          ┆          ┆ actu…    ┆         ┆   ┆ im…     ┆ im…     ┆         ┆         │
│ timeseri ┆ Economic ┆ The      ┆ null    ┆ … ┆ http:// ┆ http:// ┆ ewd.out ┆ 2020-03 │
│ es/asm/a ┆ Surveys: ┆ Annual   ┆         ┆   ┆ api.cen ┆ api.cen ┆ reach@c ┆ -17 00: │
│ rea2017  ┆ Annual   ┆ Survey   ┆         ┆   ┆ sus.gov ┆ sus.gov ┆ ensus.g ┆ 00:00.0 │
│          ┆ Surve…   ┆ of Manuf ┆         ┆   ┆ /data/t ┆ /data/t ┆ ov      ┆         │
│          ┆          ┆ actu…    ┆         ┆   ┆ im…     ┆ im…     ┆         ┆         │
│ timeseri ┆ Annual   ┆ The      ┆ null    ┆ … ┆ http:// ┆ http:// ┆ Ewd.out ┆ 2021-03 │
│ es/asm/b ┆ Economic ┆ Annual   ┆         ┆   ┆ api.cen ┆ api.cen ┆ reach@c ┆ -17 00: │
│ enchmark ┆ Surveys: ┆ Survey   ┆         ┆   ┆ sus.gov ┆ sus.gov ┆ ensus.g ┆ 00:00.0 │
│ 2017     ┆ Annua…   ┆ of Manuf ┆         ┆   ┆ /data/t ┆ /data/t ┆ ov      ┆         │
│          ┆          ┆ actu…    ┆         ┆   ┆ im…     ┆ im…     ┆         ┆         │
│ timeseri ┆ Annual   ┆ The      ┆ null    ┆ … ┆ http:// ┆ http:// ┆ ewd.out ┆ 2025-02 │
│ es/asm/b ┆ Economic ┆ Annual   ┆         ┆   ┆ api.cen ┆ api.cen ┆ reach@c ┆ -18 14: │
│ enchmark ┆ Surveys: ┆ Survey   ┆         ┆   ┆ sus.gov ┆ sus.gov ┆ ensus.g ┆ 11:28.0 │
│ 2022     ┆ Annua…   ┆ of Manuf ┆         ┆   ┆ /data/t ┆ /data/t ┆ ov      ┆         │
│          ┆          ┆ actu…    ┆         ┆   ┆ im…     ┆ im…     ┆         ┆         │
└──────────┴──────────┴──────────┴─────────┴───┴─────────┴─────────┴─────────┴─────────┘
```

3. Another option is to obtain a list of available datasets for a particular program. Below, we demonstrate how to fetch all datasets provided by the U.S. Census Bureau’s API for the 2022 American Community Survey (ACS).

```python
acs_2022_apis = get_census_apis(name = "acs", vintage = 2022)
acs_2022_apis.head()

shape: (5, 10)
┌──────────┬──────────┬──────────┬─────────┬───┬─────────┬─────────┬─────────┬─────────┐
│ dataset  ┆ title    ┆ descript ┆ vintage ┆ … ┆ geograp ┆ api_url ┆ contact ┆ modifie │
│ ---      ┆ ---      ┆ ion      ┆ ---     ┆   ┆ hyLink  ┆ ---     ┆ ---     ┆ d       │
│ str      ┆ str      ┆ ---      ┆ i64     ┆   ┆ ---     ┆ str     ┆ str     ┆ ---     │
│          ┆          ┆ str      ┆         ┆   ┆ str     ┆         ┆         ┆ str     │
╞══════════╪══════════╪══════════╪═════════╪═══╪═════════╪═════════╪═════════╪═════════╡
│ acs/acs1 ┆ American ┆ The      ┆ 2022    ┆ … ┆ http:// ┆ http:// ┆ acso.us ┆ 2023-04 │
│          ┆ Communit ┆ American ┆         ┆   ┆ api.cen ┆ api.cen ┆ ers.sup ┆ -24 14: │
│          ┆ y        ┆ Communit ┆         ┆   ┆ sus.gov ┆ sus.gov ┆ port@ce ┆ 51:53.0 │
│          ┆ Survey:  ┆ y Survey ┆         ┆   ┆ /data/2 ┆ /data/2 ┆ nsus.go ┆         │
│          ┆ 1-Y…     ┆ …        ┆         ┆   ┆ 02…     ┆ 02…     ┆ v       ┆         │
│ acs/acs1 ┆ American ┆ The      ┆ 2022    ┆ … ┆ http:// ┆ http:// ┆ acso.us ┆ 2023-04 │
│ /cprofil ┆ Communit ┆ American ┆         ┆   ┆ api.cen ┆ api.cen ┆ ers.sup ┆ -24 14: │
│ e        ┆ y        ┆ Communit ┆         ┆   ┆ sus.gov ┆ sus.gov ┆ port@ce ┆ 49:08.0 │
│          ┆ Survey:  ┆ y Survey ┆         ┆   ┆ /data/2 ┆ /data/2 ┆ nsus.go ┆         │
│          ┆ 1-Y…     ┆ …        ┆         ┆   ┆ 02…     ┆ 02…     ┆ v       ┆         │
│ acs/acs1 ┆ American ┆ The      ┆ 2022    ┆ … ┆ http:// ┆ http:// ┆ acso.us ┆ 2023-04 │
│ /profile ┆ Communit ┆ American ┆         ┆   ┆ api.cen ┆ api.cen ┆ ers.sup ┆ -24 14: │
│          ┆ y        ┆ Communit ┆         ┆   ┆ sus.gov ┆ sus.gov ┆ port@ce ┆ 49:41.0 │
│          ┆ Survey:  ┆ y Survey ┆         ┆   ┆ /data/2 ┆ /data/2 ┆ nsus.go ┆         │
│          ┆ 1-Y…     ┆ …        ┆         ┆   ┆ 02…     ┆ 02…     ┆ v       ┆         │
│ acs/acs1 ┆ 2022     ┆ The      ┆ 2022    ┆ … ┆ http:// ┆ http:// ┆ acso.us ┆ 2023-06 │
│ /pums    ┆ American ┆ American ┆         ┆   ┆ api.cen ┆ api.cen ┆ ers.sup ┆ -08 10: │
│          ┆ Communit ┆ Communit ┆         ┆   ┆ sus.gov ┆ sus.gov ┆ port@ce ┆ 03:42.0 │
│          ┆ y        ┆ y Survey ┆         ┆   ┆ /data/2 ┆ /data/2 ┆ nsus.go ┆         │
│          ┆ Survey…  ┆ …        ┆         ┆   ┆ 02…     ┆ 02…     ┆ v       ┆         │
│ acs/acs1 ┆ 2022     ┆ The      ┆ 2022    ┆ … ┆ http:// ┆ http:// ┆ acso.us ┆ 2023-06 │
│ /pumspr  ┆ American ┆ Public   ┆         ┆   ┆ api.cen ┆ api.cen ┆ ers.sup ┆ -08 10: │
│          ┆ Communit ┆ Use Micr ┆         ┆   ┆ sus.gov ┆ sus.gov ┆ port@ce ┆ 03:09.0 │
│          ┆ y        ┆ odata    ┆         ┆   ┆ /data/2 ┆ /data/2 ┆ nsus.go ┆         │
│          ┆ Survey…  ┆ Sampl…   ┆         ┆   ┆ 02…     ┆ 02…     ┆ v       ┆         │
└──────────┴──────────┴──────────┴─────────┴───┴─────────┴─────────┴─────────┴─────────┘
```

4. To retrieve a list of timeseries datasets, set the name argument to `timeseries`.

```python
timeseries_apis = get_census_apis(name = "timeseries")
timeseries_apis.head()

shape: (5, 9)
┌───────────┬───────────┬──────────┬──────────┬───┬──────────┬──────────┬──────────┬──────────┐
│ dataset   ┆ title     ┆ descript ┆ type     ┆ … ┆ geograph ┆ api_url  ┆ contact  ┆ modified │
│ ---       ┆ ---       ┆ ion      ┆ ---      ┆   ┆ yLink    ┆ ---      ┆ ---      ┆ ---      │
│ str       ┆ str       ┆ ---      ┆ str      ┆   ┆ ---      ┆ str      ┆ str      ┆ str      │
│           ┆           ┆ str      ┆          ┆   ┆ str      ┆          ┆          ┆          │
╞═══════════╪═══════════╪══════════╪══════════╪═══╪══════════╪══════════╪══════════╪══════════╡
│ timeserie ┆ Annual    ┆ The      ┆ Timeseri ┆ … ┆ http://a ┆ http://a ┆ ewd.outr ┆ 2025-04- │
│ s/aies/ba ┆ Integrate ┆ Annual   ┆ es       ┆   ┆ pi.censu ┆ pi.censu ┆ each@cen ┆ 11 13:20 │
│ sic       ┆ d         ┆ Integrat ┆          ┆   ┆ s.gov/da ┆ s.gov/da ┆ sus.gov  ┆ :27.0    │
│           ┆ Economic  ┆ ed Econo ┆          ┆   ┆ ta/tim…  ┆ ta/tim…  ┆          ┆          │
│           ┆ Sur…      ┆ mic…     ┆          ┆   ┆          ┆          ┆          ┆          │
│ timeserie ┆ Annual    ┆ The      ┆ Timeseri ┆ … ┆ http://a ┆ http://a ┆ Ewd.outr ┆ 2018-12- │
│ s/asm/are ┆ Economic  ┆ Annual   ┆ es       ┆   ┆ pi.censu ┆ pi.censu ┆ each@cen ┆ 13 00:00 │
│ a2012     ┆ Surveys:  ┆ Survey   ┆          ┆   ┆ s.gov/da ┆ s.gov/da ┆ sus.gov  ┆ :00.0    │
│           ┆ Annua…    ┆ of Manuf ┆          ┆   ┆ ta/tim…  ┆ ta/tim…  ┆          ┆          │
│           ┆           ┆ actu…    ┆          ┆   ┆          ┆          ┆          ┆          │
│ timeserie ┆ Economic  ┆ The      ┆ Timeseri ┆ … ┆ http://a ┆ http://a ┆ ewd.outr ┆ 2020-03- │
│ s/asm/are ┆ Surveys:  ┆ Annual   ┆ es       ┆   ┆ pi.censu ┆ pi.censu ┆ each@cen ┆ 17 00:00 │
│ a2017     ┆ Annual    ┆ Survey   ┆          ┆   ┆ s.gov/da ┆ s.gov/da ┆ sus.gov  ┆ :00.0    │
│           ┆ Surve…    ┆ of Manuf ┆          ┆   ┆ ta/tim…  ┆ ta/tim…  ┆          ┆          │
│           ┆           ┆ actu…    ┆          ┆   ┆          ┆          ┆          ┆          │
│ timeserie ┆ Annual    ┆ The      ┆ Timeseri ┆ … ┆ http://a ┆ http://a ┆ Ewd.outr ┆ 2021-03- │
│ s/asm/ben ┆ Economic  ┆ Annual   ┆ es       ┆   ┆ pi.censu ┆ pi.censu ┆ each@cen ┆ 17 00:00 │
│ chmark201 ┆ Surveys:  ┆ Survey   ┆          ┆   ┆ s.gov/da ┆ s.gov/da ┆ sus.gov  ┆ :00.0    │
│ 7         ┆ Annua…    ┆ of Manuf ┆          ┆   ┆ ta/tim…  ┆ ta/tim…  ┆          ┆          │
│           ┆           ┆ actu…    ┆          ┆   ┆          ┆          ┆          ┆          │
│ timeserie ┆ Annual    ┆ The      ┆ Timeseri ┆ … ┆ http://a ┆ http://a ┆ ewd.outr ┆ 2025-02- │
│ s/asm/ben ┆ Economic  ┆ Annual   ┆ es       ┆   ┆ pi.censu ┆ pi.censu ┆ each@cen ┆ 18 14:11 │
│ chmark202 ┆ Surveys:  ┆ Survey   ┆          ┆   ┆ s.gov/da ┆ s.gov/da ┆ sus.gov  ┆ :28.0    │
│ 2         ┆ Annua…    ┆ of Manuf ┆          ┆   ┆ ta/tim…  ┆ ta/tim…  ┆          ┆          │
│           ┆           ┆ actu…    ┆          ┆   ┆          ┆          ┆          ┆          │
└───────────┴───────────┴──────────┴──────────┴───┴──────────┴──────────┴──────────┴──────────┘
```
5. After selecting a dataset you're interested in exploring, use the `get_census_metadata()` function to obtain its metadata. For instance, the following code retrieves variable metadata for the 2021 dataset from the U.S. Census Bureau's Population Estimates Program (PEP).

```python
pep_2021 = get_census_metadata(
    name = "pep/population", 
    vintage = 2021,
    meta_type = "variables"
)
pep_2021.head()

shape: (5, 6)
┌──────────────────────┬──────────────────────┬────────────┬──────────┬───────────────┬───────┐
│ name                 ┆ label                ┆ concept    ┆ required ┆ predicateType ┆ group │
│ ---                  ┆ ---                  ┆ ---        ┆ ---      ┆ ---           ┆ ---   │
│ str                  ┆ str                  ┆ str        ┆ str      ┆ str           ┆ str   │
╞══════════════════════╪══════════════════════╪════════════╪══════════╪═══════════════╪═══════╡
│ for                  ┆ Census API FIPS      ┆ Census API ┆ null     ┆ fips-for      ┆ N/A   │
│                      ┆ 'for' clause         ┆ Geography  ┆          ┆               ┆       │
│                      ┆                      ┆ Specifica… ┆          ┆               ┆       │
│ in                   ┆ Census API FIPS 'in' ┆ Census API ┆ null     ┆ fips-in       ┆ N/A   │
│                      ┆ clause               ┆ Geography  ┆          ┆               ┆       │
│                      ┆                      ┆ Specifica… ┆          ┆               ┆       │
│ ucgid                ┆ Uniform Census       ┆ Census API ┆ null     ┆ ucgid         ┆ N/A   │
│                      ┆ Geography Ident…     ┆ Geography  ┆          ┆               ┆       │
│                      ┆                      ┆ Specifica… ┆          ┆               ┆       │
│ DESC_RANK_PPOPCHG_20 ┆ Description of       ┆ null       ┆ null     ┆ string        ┆ N/A   │
│ 21                   ┆ RANK_PPOPCHG_20…     ┆            ┆          ┆               ┆       │
│ DESC_POP_2021        ┆ Description of       ┆ null       ┆ null     ┆ string        ┆ N/A   │
│                      ┆ POP_2021 variab…     ┆            ┆          ┆               ┆       │
└──────────────────────┴──────────────────────┴────────────┴──────────┴───────────────┴───────┘
```

By default, datasets do not include variable values and value labels. To add this information, set `include_labels = True`. The example below demonstrates how to retrieve these details and filter out rows where this information is present.

```python
pep_2021_labels = get_census_metadata(
    name = "pep/population", 
    vintage = 2021,
    meta_type = "variables",
    include_labels = True
)
pep_2021_labels.filter(
    (pl.col("code").is_not_null()) & 
    (pl.col("code_label").is_not_null())
).select(["name", "code", "code_label"])

shape: (11, 3)
┌─────────────┬──────┬─────────────────────────────────┐
│ name        ┆ code ┆ code_label                      │
│ ---         ┆ ---  ┆ ---                             │
│ str         ┆ str  ┆ str                             │
╞═════════════╪══════╪═════════════════════════════════╡
│ UNIVERSE    ┆ R    ┆ Resident population             │
│ FUNCSTAT    ┆ A    ┆ identifies an active governmen… │
│ FUNCSTAT    ┆ B    ┆ identifies an active governmen… │
│ FUNCSTAT    ┆ C    ┆ identifies an active governmen… │
│ FUNCSTAT    ┆ S    ┆ identifies a statistical entit… │
│ …           ┆ …    ┆ …                               │
│ FUNCSTAT    ┆ G    ┆ identifies an active governmen… │
│ FUNCSTAT    ┆ I    ┆ identifies an inactive governm… │
│ FUNCSTAT    ┆ N    ┆ identifies a nonfunctioning le… │
│ PRIMGEOFLAG ┆ 1    ┆ Yes                             │
│ PRIMGEOFLAG ┆ 0    ┆ No                              │
└─────────────┴──────┴─────────────────────────────────┘
```

To retrieve metadata for specific variables, list their names in the `variables` parameter. This ensures you only receive metadata for those variables. In the example below, we retrieve metadata for two variables, `FUNCTSTAT` and `PRIMGEOFLAG`, from the U.S. Census Bureau's 2021 Population Estimates Program dataset.

```python
pep_2021_func_prime = get_census_metadata(
    name = "pep/population", 
    vintage = 2021,
    meta_type = "variables",
    variables = ["FUNCSTAT", "PRIMGEOFLAG"],
    include_labels = True
)
pep_2021_func_prime

shape: (10, 6)
┌─────────────┬──────────────────────────┬───────────────┬───────┬──────┬────────────────────────────┐
│ name        ┆ label                    ┆ predicateType ┆ group ┆ code ┆ code_label                 │
│ ---         ┆ ---                      ┆ ---           ┆ ---   ┆ ---  ┆ ---                        │
│ str         ┆ str                      ┆ str           ┆ str   ┆ str  ┆ str                        │
╞═════════════╪══════════════════════════╪═══════════════╪═══════╪══════╪════════════════════════════╡
│ FUNCSTAT    ┆ Functional Status Code   ┆ string        ┆ N/A   ┆ A    ┆ identifies an active       │
│             ┆                          ┆               ┆       ┆      ┆ governmen…                 │
│ FUNCSTAT    ┆ Functional Status Code   ┆ string        ┆ N/A   ┆ B    ┆ identifies an active       │
│             ┆                          ┆               ┆       ┆      ┆ governmen…                 │
│ FUNCSTAT    ┆ Functional Status Code   ┆ string        ┆ N/A   ┆ C    ┆ identifies an active       │
│             ┆                          ┆               ┆       ┆      ┆ governmen…                 │
│ FUNCSTAT    ┆ Functional Status Code   ┆ string        ┆ N/A   ┆ S    ┆ identifies a statistical   │
│             ┆                          ┆               ┆       ┆      ┆ entit…                     │
│ FUNCSTAT    ┆ Functional Status Code   ┆ string        ┆ N/A   ┆ F    ┆ identifies a fictitious    │
│             ┆                          ┆               ┆       ┆      ┆ entity…                    │
│ FUNCSTAT    ┆ Functional Status Code   ┆ string        ┆ N/A   ┆ G    ┆ identifies an active       │
│             ┆                          ┆               ┆       ┆      ┆ governmen…                 │
│ FUNCSTAT    ┆ Functional Status Code   ┆ string        ┆ N/A   ┆ I    ┆ identifies an inactive     │
│             ┆                          ┆               ┆       ┆      ┆ governm…                   │
│ FUNCSTAT    ┆ Functional Status Code   ┆ string        ┆ N/A   ┆ N    ┆ identifies a               │
│             ┆                          ┆               ┆       ┆      ┆ nonfunctioning le…         │
│ PRIMGEOFLAG ┆ Primitive Geography Flag ┆ int           ┆ N/A   ┆ 1    ┆ Yes                        │
│ PRIMGEOFLAG ┆ Primitive Geography Flag ┆ int           ┆ N/A   ┆ 0    ┆ No                         │
└─────────────┴──────────────────────────┴───────────────┴───────┴──────┴────────────────────────────┘
```

6. The `get_census_metadata()` function can also be used to obtain a hierarchical list of geographic areas covered in the data collection and release for a given U.S. Census Bureau dataset. For example, the code below retrieves this information for the 2021 dataset from the U.S. Census Bureau’s Population Estimates Program.

```python
pep_2021_geoLevels = get_census_metadata(
    name = "pep/population", 
    vintage = 2021,
    meta_type = "geography"
)
pep_2021_geoLevels

shape: (4, 3)
┌──────────┬─────────────────┬───────────────┐
│ name     ┆ geoLevelDisplay ┆ referenceDate │
│ ---      ┆ ---             ┆ ---           │
│ str      ┆ str             ┆ str           │
╞══════════╪═════════════════╪═══════════════╡
│ us       ┆ 010             ┆ 2021-01-01    │
│ region   ┆ 020             ┆ 2021-01-01    │
│ division ┆ 030             ┆ 2021-01-01    │
│ state    ┆ 040             ┆ 2021-01-01    │
└──────────┴─────────────────┴───────────────┘
```

7. You can also use `get_census_metadata()` to retrieve lists of available data tables, also known as groups, from the Census Bureau for a specific dataset. This enables users to explore and access variables linked to particular tables within that dataset. Below we return all groups for the 2021 dataset from the U.S. Census Bureau’s Population Estimates Program.

```python
pep_2021_groups = get_census_metadata(
    name = "pep/population", 
    vintage = 2021,
    meta_type = "groups"
)
pep_2021_groups

shape: (1, 3)
┌─────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│ name            ┆ description                     ┆ variables                       │
│ ---             ┆ ---                             ┆ ---                             │
│ str             ┆ str                             ┆ str                             │
╞═════════════════╪═════════════════════════════════╪═════════════════════════════════╡
│ NST_EST2021_POP ┆ Annual Estimates of the Reside… ┆ http://api.census.gov/data/202… │
└─────────────────┴─────────────────────────────────┴─────────────────────────────────┘
```

You can use the returned group names to obtain metadata for specific subsets of variables within a dataset. To do this, set `meta_type = "variables"` and assign the desired group name to the group parameter. The example below displays a list of variables found in the `NST_EST2021_POP` table, which provides Annual Estimates of the Resident Population for the United States, Regions, States, the District of Columbia, and Puerto Rico from April 1, 2020 to July 1, 2021.

```python
pep_2021_NST_EST2021_POP = get_census_metadata(
    name = "pep/population", 
    vintage = 2021,
    meta_type = "variables",
    group = "NST_EST2021_POP"
)
pep_2021_NST_EST2021_POP

shape: (5, 5)
┌──────────────┬──────────────────────┬─────────────────────┬───────────────┬─────────────────┐
│ name         ┆ label                ┆ concept             ┆ predicateType ┆ group           │
│ ---          ┆ ---                  ┆ ---                 ┆ ---           ┆ ---             │
│ str          ┆ str                  ┆ str                 ┆ str           ┆ str             │
╞══════════════╪══════════════════════╪═════════════════════╪═══════════════╪═════════════════╡
│ POP_2020     ┆ Population Estimate, ┆ Annual Estimates of ┆ int           ┆ NST_EST2021_POP │
│              ┆ July 1, 2…           ┆ the Reside…         ┆               ┆                 │
│ POP_2021     ┆ Population Estimate, ┆ Annual Estimates of ┆ int           ┆ NST_EST2021_POP │
│              ┆ July 1, 2…           ┆ the Reside…         ┆               ┆                 │
│ NAME         ┆ Geographic Area Name ┆ Annual Estimates of ┆ string        ┆ NST_EST2021_POP │
│              ┆                      ┆ the Reside…         ┆               ┆                 │
│ POP_BASE2020 ┆ Estimates Base       ┆ Annual Estimates of ┆ int           ┆ NST_EST2021_POP │
│              ┆ Population, Apr…     ┆ the Reside…         ┆               ┆                 │
│ GEO_ID       ┆ Geography            ┆ Annual Estimates of ┆ string        ┆ NST_EST2021_POP │
│              ┆                      ┆ the Reside…         ┆               ┆                 │
└──────────────┴──────────────────────┴─────────────────────┴───────────────┴─────────────────┘
```
