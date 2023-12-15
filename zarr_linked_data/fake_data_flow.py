from zarr_linked_data.make_fake_data import make_fake_data

if __name__ == "__main__":
    # ----------------------------------------------
    ###### MAKE FAKE DATA
    # ----------------------------------------------
    ###### Parameters for fake data

    jsonld_file = "zarr_linked_data/data/original_data.jsonld"
    path_for_store = "zarr_linked_data/data/test_store.zarr"

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
    mother_group_name = "myCampaign"
    # ----------------------------------------------
    # Q: is there 1 big store or multiple stores??
    # and then the URI needs to be searched for in a specific store or accross multiple stores?
    store = make_fake_data(path_for_store, jsonld_file, prefix, levels, data_level, mother_group_name)
