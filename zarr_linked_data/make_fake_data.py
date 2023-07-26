import zarr
import json
from zarr_linked_data.helpers_fake_data import create_fake_hierarchy, allocate_metadata


def make_fake_data(path_for_store, jsonld_file, prefix, levels, data_level):

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

    myCampaign = create_fake_hierarchy(
        levels, data_level, dict_ld, prefix, "myCampaign", store
    )
    # Tree:
    # print(myCampaign.tree())

    # ----------------------------------------------
    ###### Step 2: Allocate Metadata
    myCampaign = allocate_metadata(dict_ld, myCampaign)

    # ----------------------------------------------
    ######  Close store
    store.close()
