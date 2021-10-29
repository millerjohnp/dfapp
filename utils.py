"""Utilities for data visualization."""
from collections import defaultdict, Counter
import json

import pandas as pd

def parse_courtname(pubname):
    """Extract courtname from Google scholar publication name."""
    pubname = pubname.replace("- Google Scholar", "")
    arr = pubname.split(",")
    return ",".join(arr[:-1])

def parse_year(pubname):
    """Extract year from Google scholar publication name."""
    pubname = pubname.replace("- Google Scholar", "")
    arr = pubname.split(",")
    return int(arr[-1])

def load_metadata_df(path):
    """Load metadata for scraped cases as a DataFrame."""
    with open(path) as handle:
        metadata = json.load(handle)
    
    all_cases = []
    for tool, cases in metadata.items():
        for case in cases:
            case["tool"] = tool
            all_cases.append(case)

    df = pd.DataFrame(all_cases)

    # Drop cases with no casename
    df = df[~df.casename.isna()]

    df["court"] = df.publication.apply(parse_courtname)
    df["year"] = df.publication.apply(parse_year)
    
    # Only consider results after 2006
    df = df[df.year >= 2006]

    return df

def get_entity_recognition_counts(path):
    """Get lists of recognized named entities by tool"""
    with open(path) as handle:
        all_ents = json.load(handle)
    
    people = defaultdict(list)
    orgs = defaultdict(list)
    for case in all_ents.values():
        tool = case["tool"]
        if "ORG" in case["entities"]:
            orgs[tool].extend(case["entities"]["ORG"])
        if "PERSON" in case["entities"]:
            people[tool].extend(case["entities"]["PERSON"])

    for tool, entities in people.items():
        people[tool] = Counter(entities)
    for tool, entities in orgs.items():
        orgs[tool] = Counter(entities)

    return people, orgs
