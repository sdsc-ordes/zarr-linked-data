import zarr

# import rdflib
# from rdflib.term import URIRef
from make_synthetic_data import make_synthetic_data
from uri_matching import match_uri, open_metadata_store, extract_dataset

# ----------------------------------------------
###### MAKE SYNTHETIC DATA
# ----------------------------------------------
###### Parameters for synthetic data

jsonld_file = "data/CatPlusSampleData.jsonld"
path_for_store = "data/test_store.zarr"

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
# Q: is there 1 big store or multiple stores
# and then the URI needs to be searched for in a specific store or accross multiple stores?
make_synthetic_data(path_for_store, jsonld_file, prefix, levels, data_level)

# ----------------------------------------------
###### Create Metadata Store
metadata_store = zarr.convenience.consolidate_metadata(
    path_for_store, metadata_key=".all_metadata"
)


# ----------------------------------------------
###### Use metadata store to find URI
uri = "http://www.catplus.ch/ontology/concepts/sample1"

dict_metadata = open_metadata_store("data/test_store.zarr/.all_metadata")
key_uri = match_uri(uri, dict_metadata)
dataset = extract_dataset(key_uri, path_for_store)
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
