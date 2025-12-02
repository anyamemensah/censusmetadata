import re
import polars as pl
from censusmetadata.utility import build_url
from censusmetadata.utility import enforce_int
from censusmetadata.utility import enforce_str
from censusmetadata.utility import enforce_bool
from censusmetadata.utility import enforce_list_str
from censusmetadata.utility import check_response
from censusmetadata.utility import validate_inputs
from censusmetadata.exceptions import MissingKeyError


def get_census_apis(name: str | None = None, vintage: int | None = None) -> pl.DataFrame:
    """ 
    Retrieve an overview of the available U.S. Census Bureau datasets 
    accessible via the Census Bureau API. You may also select and 
    return information about datasets that correspond to a particular 
    survey, program, or vintage year.

    Parameters
    ----------
    name
        A string representing the shorthand abbreviation used for a  
        particular Census Bureau survey or program.
    vintage
        An integer representing the reference year a dataset is 
        associated with.

    Returns
    ----------
    DataFrame, which may be empty if no records are returned.
    """
    name, vintage = validate_inputs(
        name = (enforce_str, name, True),
        vintage = (enforce_int, vintage, True)
    )

    url = build_url(name = name, vintage = vintage)

    resp = check_response(url)
    if resp is None:
        return pl.DataFrame()
    return extract_datasets(resp = resp)


def get_census_metadata(name: str,
                        vintage: int | None = None,
                        meta_type: str = "variables",
                        variables: str | list[str] | None = None,
                        group: str | None = None,
                        include_labels: bool =  False) -> pl.DataFrame:
    """ 
    Retrieve metadata for a given Census survey or program.

    Parameters
    ----------
    name
        A string representing the shorthand abbreviation used for a  
        particular Census Bureau survey or program.
    vintage
        An integer representing the reference year a dataset is 
        associated with.
    meta_type: {'variables','geography', 'groups'}
        * variables: Retrieves all variables included in the data 
        collection and release for a specific U.S. Census Bureau 
        dataset.
        * geography: Retrieves a hierarchical list of geographic areas 
        included in the data collection and release for the specified 
        U.S. Census Bureau dataset.
        * groups: Retrieves a list of all available data tables and 
        related variables for a specific dataset. Each table has an 
        identifier and an accompanying description.
    group: 
        A string that represents an identifier for a data table with 
        metadata on related variables within a specific dataset. This 
        identifier enables users to access all variables linked to the 
        group in the dataset.
    include_labels:
        If set to `True` and 'meta_type' is `variables`, variable values 
        (code) and value labels (code_label) will be returned with the 
        requested metadata. When `False` (default) and 'meta_type' is 
        `variables`, no codes or labels are returned.

    Returns
    ----------
    DataFrame, which may be empty if no records are returned.
    """
    (name, vintage, meta_type, variables, group, include_labels) = (
        validate_inputs(
            name = (enforce_str, name, False),
            vintage = (enforce_int, vintage, True),
            meta_type = (enforce_str, meta_type, False),
            variables = (enforce_list_str, variables, True),
            group = (enforce_str, group, True),
            include_labels = (enforce_bool, include_labels, False)
        )
    )

    url = build_url(
        name = name, 
        vintage = vintage, 
        meta_type = meta_type, 
        group = group
        )

    resp = check_response(url)
    if resp is None:
        return pl.DataFrame()

    if meta_type == "variables":
        return extract_variables(
            resp=resp,
            variables=variables,  # type: ignore[valid-type]
            include_labels=include_labels,
            meta_type=meta_type
        )

    meta_map = {"geography": "fips", "groups": "groups"}
    if meta_type in meta_map:
        return extract_geo_or_grp(resp=resp, meta_type=meta_map[meta_type])

    raise ValueError(f"Invalid meta_type '{meta_type}'. 'meta_type' must be one of "
                    f"'variables', 'geography', or 'groups'.")


def extract_datasets(resp: dict):
    """
    Helper function to convert a JSON object into a Polars 
    DataFrame for organizing Census Bureau API datasets

    Parameters
    ----------
    resp
        The `.text` property of the requests response, which has been 
        parsed with `json.loads()` and converted into a dict.

    Examples
    --------
    >>> import json
    >>> example = json.loads('''{
    "@type": "dcat:Catalog",
    "dataset": [
        {
        "c_vintage": 1999,
        "c_dataset": [
            "acronym"
        ],
        "c_geographyLink": "http://url.json",
        "c_variablesLink": "http://url.json",
        "c_groupsLink": "http://url.json",
        "c_documentationLink": "url/developer/",
        "c_isAggregate": true,
        "@type": "dcat:Dataset",
        "title": "Survey or Program Name",
        "accessLevel": "public",
        "description": "Description is....",
        "distribution": [
            {
            "accessURL": "http://url"
            }
        ],
        "contactPoint": {
            "hasEmail": "mailto:email@gmail.com"
        },
        "modified": "2017-02-09"
        }
    ]
    }''')

    >>> extract_datasets(resp = example).select(["dataset", "title", "description"])
    shape: (1, 3)
    ┌─────────┬────────────────────────┬────────────────────┐
    │ dataset ┆ title                  ┆ description        │
    │ ---     ┆ ---                    ┆ ---                │
    │ str     ┆ str                    ┆ str                │
    ╞═════════╪════════════════════════╪════════════════════╡
    │ acronym ┆ Survey or Program Name ┆ Description is.... │
    └─────────┴────────────────────────┴────────────────────┘
    """
    if "dataset" not in resp:
        raise MissingKeyError(value = "dataset", value_type = "key")
    
    # main df
    tmp_df = (
        pl.DataFrame(resp["dataset"])
        .select(pl.all().name.replace(r"^c_|^@", ""))
    )

    # build out expressions
    dataset_type_exprs = [
        (
            pl.when(pl.col(var)).then(True)
                .otherwise(False)
                .alias(var)
        ) if var in tmp_df.columns else (
            pl.col("dataset")
                .list.contains(re.sub("^is", "", var).lower())
                .alias(var)
        )
        for var in ["isAggregate", "isMicrodata", "isTimeseries"]
    ]

    # metadata columns
    meta_data_vars = [
        "dataset", 
        "title", 
        "description", 
        "vintage", 
        "type", 
        "variablesLink", 
        "geographyLink", 
        "api_url", 
        "contact", 
        "modified"
    ]

    # trasformations
    meta_data_df = (
        tmp_df
        .with_columns(dataset_type_exprs)
        .with_columns(
            pl.when(pl.col("isMicrodata")).then(pl.lit("Microdata"))
                .when(pl.col("isAggregate")).then(pl.lit("Aggregate"))
                .otherwise(pl.lit("Timeseries"))
                .alias("type"),
            pl.col("distribution")
                .list.explode().struct.field("accessURL").alias("api_url"),
            pl.col("contactPoint").struct.field("hasEmail").alias("contact"),
            pl.col("dataset").list.join("/").alias("dataset"),
        )
        .with_columns(pl.col("contact").str.replace(r"^mailto:", "").alias("contact"))
    )

    select_vars = [var for var in meta_data_vars if var in meta_data_df.columns]
    sort_vars = [var for var in ["vintage","dataset"] if var in meta_data_df.columns]

    return meta_data_df.select(select_vars).sort(sort_vars, descending = False)

    
def helper_extract_variables(resp_data: dict,
                             variables: list[str] | None = None,
                             include_labels: bool = False) -> pl.DataFrame:
    
    variables = list(resp_data.keys()) if variables is None else variables

    frame = []

    for var in variables:
        var_frame = pl.DataFrame({"name": var, **resp_data[var]})
        labels_frame = None

        if include_labels and "values" in var_frame.columns:
            values_frame = var_frame.select("values").unnest("values")
            if "item" in values_frame.columns:
                labels_frame = (
                    values_frame
                        .select("item")
                        .unpivot()
                        .unnest("value")
                        .unpivot()
                        .rename({"variable": "code", "value": "code_label"})
                        .filter(~pl.col("code").eq("variable"))
                        .with_columns(pl.lit(var).alias("name"))
                )

        combined = var_frame.join(labels_frame, on="name") if labels_frame is not None else var_frame
        frame.append(combined)

    vars_to_retain = [
        "name",
        "label",
        "concept",
        "required", 
        "predicateType",
        "group",
        "code", 
        "code_label" 
    ]
    full_frame = pl.concat(frame, how = "diagonal_relaxed")
    select_vars = [v for v in vars_to_retain if v in full_frame.columns]
    full_frame = full_frame.select(select_vars)
    
    return full_frame


def extract_variables(resp: dict, 
                      variables: list[str] | None = None,
                      include_labels: bool = False,
                      meta_type: str = "variables"):
    """
    Helper function to retrieve variable metadata, such as 
    names, labels, values (code), and value labels (code_label, 
    from a chosen dataset available through the Census Bureau's 
    API.
    """
    if meta_type not in resp:
        raise MissingKeyError(value = meta_type, value_type = "key")
   
    meta_data_df = helper_extract_variables(
        resp_data = resp[meta_type], 
        variables = variables, 
        include_labels = include_labels
    )
    
    return meta_data_df


def extract_geo_or_grp(resp: dict, meta_type: str):
    """
    A helper function designed to retrieve geographic or group 
    information from a chosen dataset available through the U.S.
    Census Bureau API.
    """
    if meta_type not in resp:
        raise MissingKeyError(value = "key", value_type = meta_type)
   
    tmp_df = pl.DataFrame(resp[meta_type])

    vars_to_transform = [var for var, dtype in zip(tmp_df.columns, tmp_df.dtypes) if dtype == pl.List]
    if vars_to_transform:
        vars_exprs = [pl.col(var).list.join(", ").alias(var) for var in vars_to_transform]
        tmp_df = tmp_df.with_columns(vars_exprs)

    meta_data_df = tmp_df

    return meta_data_df
