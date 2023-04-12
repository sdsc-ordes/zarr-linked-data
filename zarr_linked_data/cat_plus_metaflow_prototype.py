import zarr
from make_synthetic_data import make_synthetic_data
from metadata_consolidate_metaflow import MetadataConsolidateFlow
from uri_matching_metaflow import RetrievalFlow

if __name__ == "__main__":
    # ----------------------------------------------
    ###### MAKE SYNTHETIC DATA
    # ----------------------------------------------
    ###### Parameters for synthetic data

    jsonld_file = "../data/CatPlusSampleData.jsonld"
    path_for_store = "../data/test_store.zarr"

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
    store = make_synthetic_data(path_for_store, jsonld_file, prefix, levels, data_level)

    # ----------------------------------------------
    ###### CONSOLIDATE METADATA FLOW
    # ----------------------------------------------
    # BIG ISSUE: how to automate this if not compatible with metaflow ?
    metadata_store = zarr.convenience.consolidate_metadata(
        path_for_store, metadata_key=".all_metadata"
    )

    # The consolidation flow is not functional:
    # it renders no errors but no metadata store is created.
    # MetadataConsolidateFlow()

    # ----------------------------------------------
    ###### RETRIEVAL FLOW
    # ----------------------------------------------
    # test_uri = "http://www.catplus.ch/ontology/concepts/sample1"
    # test call terminal:
    # python cat_plus_metaflow_prototype.py run --uri "http://www.catplus.ch/ontology/concepts/sample1" --path_store "../data/test_store.zarr"

    data = RetrievalFlow()
