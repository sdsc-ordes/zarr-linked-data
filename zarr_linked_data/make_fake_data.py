import zarr
import json
from zarr_linked_data.helpers_fake_data import create_fake_hierarchy, allocate_metadata


def make_fake_data(path_for_store, jsonld_file, prefix, levels, data_level, mother_group_name):
    """ Make fake data in Zarr file format. Creates a Zarr store in the data folder.
    Parameters:
    path_for_store (str): path where to store the Zarr store
    jsonld_file (str): path to the JSON-LD file containing the instance data that will be converted into the Zarr store metadata
    prefix (str): prefix of the ontology which will be used for each field of the metadata
    levels (list): list of the different levels of the hierarchy for the Zarr store
    data_level (str): level at which there is data i.e. an array
    mother_group_name (str): name of the first group in the hierarchy
    """
    with open(jsonld_file) as jsonld:
        dict_ld = json.load(jsonld)

    # ----------------------------------------------
    ###### Step 0: Storage

    # Option 1: DirectoryStore
    store = zarr.DirectoryStore(path_for_store)

    # Option 2: SQLiteStore
    # store = zarr.SQLiteStore('data/test_store_SQLite.sqldb')

    # ----------------------------------------------
    ###### Step 1 : Build the hierarchy

    myFakeData = create_fake_hierarchy(
        levels, data_level, dict_ld, prefix, mother_group_name, store
    )
    # Tree:
    print("This is what the fake data looks like: ")
    print(myFakeData.tree())

    # ----------------------------------------------
    ###### Step 2: Allocate Metadata
    myFakeData = allocate_metadata(dict_ld, myFakeData)

    # ----------------------------------------------
    ######  Close store
    store.close()
