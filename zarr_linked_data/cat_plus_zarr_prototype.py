import zarr
import json

# import rdflib
# from rdflib.term import URIRef
from helpers import create_synthetic_hierarchy, allocate_metadata
from uri_matching import match_uri, open_metadata_store, extract_dataset

# ----------------------------------------------
###### Load in Data

jsonld_file = "data/CatPlusSampleData.jsonld"

with open(jsonld_file) as jsonld:
    dict_ld = json.load(jsonld)

# ----------------------------------------------
###### Parameters for fu
levels = [
    "Campaign",
    "Batch",
    "SamplePreparation",
    "Sample",
    "SampleChemical",
    "Chemical",
]
prefix = "http://www.catplus.ch/ontology/concepts/"
data_level = "Sample"

# ----------------------------------------------
###### Step 0: Storage

# Option 1: DirectoryStore
store = zarr.DirectoryStore("data/test_store.zarr")

# Option 2: SQLiteStore
# store = zarr.SQLiteStore('data/test_store_SQLite.sqldb')

# ----------------------------------------------
###### Step 1 : Build the hierarchy

myCampaign = create_synthetic_hierarchy(
    levels, data_level, dict_ld, prefix, "myCampaign", store
)
# Tree:
print(myCampaign.tree())

# ----------------------------------------------
###### Step 2: Allocate Metadata
myCampaign = allocate_metadata(dict_ld, myCampaign)

# ----------------------------------------------
######  Close store
store.close()

# ----------------------------------------------
###### Create Metadata Store
metadata_store = zarr.convenience.consolidate_metadata(
    store, metadata_key=".all_metadata"
)


# ----------------------------------------------
###### Use metadata store to find URI
uri = "http://www.catplus.ch/ontology/concepts/sample1"

dict_metadata = open_metadata_store("data/test_store.zarr/.all_metadata")
key_uri = match_uri(uri, dict_metadata)
dataset = extract_dataset(key_uri, store)
print("Data Retrieval: ")
print(dataset[1:10])
print("***")


# LOADS ENTIRE STORE THAT IS CONSOLIDATED
# loaded = zarr.convenience.open_consolidated(store,
#                                    metadata_key=".all_metadata",
#                                    mode='r+')
# print("----loaded----")
# print(loaded.tree())

# *** Notes:
# 1. get keys of level below
# print(sorted(myCampaign.group_keys()))


# Sanity Check
# print("----CAMPAIGN----")
# print(myCampaign.info)
# see all attributes
# print(sorted(myCampaign.attrs))

# print("----chemical2----")
# print(sampleChemical1.info)
# access just one attribute
# print(chemical2.attrs["@id"])
# print(sorted(chemical2.attrs))

# print(sampleChemical1.attrs["http://www.catplus.ch/ontology/concepts/predictedQuantity"])

# ----------------------------------------------
# OTHER OPTION

# g = rdflib.Graph().parse(jsonld_file)
# #print(list(g.subject_objects(URIRef("http://www.catplus.ch/ontology/concepts/hasChemical"))))
# print(list(g.subject_objects("@type")))

# searched_uri = "http://www.catplus.ch/ontology/concepts/chemical2"
