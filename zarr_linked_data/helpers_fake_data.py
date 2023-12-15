import zarr
import re
import numpy as np


def create_fake_hierarchy(
    levels, data_level, dict_ld, prefix, mother_group_name, store
):
    """Create a fake hierarchy of entities/groups and datasets in a zarr store.
    Parameters:
    levels (list): list of levels in the hierarchy
    data_level (str): level at which data is present
    dict_ld (dict): dictionary containing entities of the hierarchy defined
    prefix (str): prefix of the ontology
    mother_group_name (str): name of the mother group
    store (zarr store): store where the hierarchy is created
    """
    locals()[mother_group_name] = zarr.group(store=store, overwrite=True)
    for i, level in enumerate(levels):
        # print("--Level: " + level)
        for j, entity in enumerate(dict_ld):
            entity_type = entity["@type"][0].rsplit("/")[-1]
            if entity_type == level:
                # print("----Processing: " + entity["@id"])
                name = entity["@id"].rsplit("/")[-1]
                # print("----Processing: " + name)
                # do not go further than the last level
                if i + 1 < len(levels):
                    predicate = prefix + "has" + levels[i + 1]
                    sub_entities = entity[predicate]
                    # print("***")
                    # print(str(sub_entities))
                    # print("***")
                    for sub_entity in sub_entities:
                        sub_name = sub_entity["@id"].rsplit("/")[-1]
                        # print("------Creating: " + sub_name)
                        locals()[sub_name] = locals()[name].create_group(sub_name)
                if entity_type == data_level:
                    # then allocate data
                    locals()[name + "Dataset"] = locals()[name].create_dataset(
                        name + "Dataset",
                        data=np.random.rand(9000, 1000),
                        # shape=(9000, 1000),
                        chunks=(900,),
                        dtype="float64",
                    )
    return locals()[mother_group_name]


def find(path):
    global found
    if pattern.search(path) is not None:
        found = path
        return path


def allocate_metadata(dict_ld, mother_group):
    """Allocate metadata to the entities/groups in a zarr store.
    Parameters:
    dict_ld (dict): dictionary containing entities of the hierarchy defined
    mother_group (zarr group): mother group of the hierarchy
    """
    for j, entity in enumerate(dict_ld):
        # get name
        name = entity["@id"].rsplit("/")[-1]
        # check that the entity is in the tree
        global pattern
        pattern = re.compile(name)
        found = None
        if mother_group.visit(find):
            path = mother_group.visit(find)
            # then allocate metadata
            for key, value in entity.items():
                mother_group[path].attrs[key] = value
    return mother_group
