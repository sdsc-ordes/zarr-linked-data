from metaflow import FlowSpec, step, Parameter


class UriMatchingFlow(FlowSpec):
    """Given an input URI look for the corresponding instance in the metadata store and extract the associated data.
    Parameters:
    uri (str): URI to be matched
    path_for_store (str): path to the Zarr Store where the dataset is stored
    path_save (str): path where the dataset should be saved
    """

    uri = Parameter(
        "uri",
        help="The URI referencing the dataset object which should be retrieved.",
    )
    path_for_store = Parameter(
        "path_for_store",
        help="The path to the Zarr Store where the dataset is stored."
    )

    path_save = Parameter(
        "path_save",
        help="The path where the dataset should be saved."
    )

    @step
    def start(self):
        """Start the retrieval flow."""
        print(
            "Looking for the following URI [%s] in the metadata of the following store: %s"
            % (self.uri, self.path_for_store)
        )
        self.path_metadata_store = self.path_for_store + "/.all_metadata"
        self.next(self.open_metadata_store)

    @step
    def open_metadata_store(self):
        """Open a zarr metadata store and returns it in a dictionary format."""
        import json
        try:
            with open(self.path_metadata_store) as all_metadata:
                store_metadata = json.load(all_metadata)
                self.dict_metadata = store_metadata["metadata"]
        except ImportError:
            print(
                "Could not open metadata store. Check that `path_metadata_store` is correct."
            )
        self.next(self.match_uri)

    @step
    def match_uri(self):
        """Match a URI to an @id in a dictionary and extract the associated key i.e. store path.
        Parameters:
        key_uri (str): key (path in metastore) associated to the @id matching the URI
        """
        try:
            for key, value in self.dict_metadata.items():
                if "@id" in value.keys():
                    if self.uri == value["@id"]:
                        self.key_uri = key
        except LookupError:
            print("Could not find URI in the metadata. Check that `uri` is correct.")
        self.next(self.extract_dataset)

    @step
    def extract_dataset(self):
        """Extract the dataset attached to the metadata path/key."""
        import zarr

        # the path coming in will be in the format "path/.zattrs" so we strip this last part
        path = self.key_uri.split("/.zattrs")[0]
        # all Datasets will be stored as a subentity of their group with the prefix "Dataset"
        uri_data = path + "/" + path.split("/")[-1] + "Dataset"
        try:
            # two options: path or store
            # option 1
            # self.data = zarr.open(self.path_for_store + "/" + uri_data,
            #                 mode='r',
            #                 #shape=(9000, 10000),
            #                 #chunks=(900, 1000),
            #                 dtype='float64')
            # option 2
            self.data = zarr.open(
                self.path_for_store,
                mode="r",
                # ho to handle chunking ?
                # shape=(9000, 10000),
                # chunks=(900, 1000),
                dtype="float64",
                path=uri_data,
            )
        except ImportError:
            print(
                "Could not open the dataset. Check that `path_for_store` is correct. OR There may not be any data associated with the instance you are looking for."
            )
        self.next(self.end)

    @step
    def end(self):
        """End the flow and return associated data."""
        import numpy as np
        np.save(self.path_save, self.data)
        print("Data saved at: %s" % self.path_save)


if __name__ == "__main__":
    # ----------------------------------------------
    ###### URIMatching FLOW
    # ----------------------------------------------
    # call with:
    # python zarr_linked_data/local_dev/uri_matching_metaflow.py run --path_for_store="zarr_linked_data/data/test_store.zarr" --uri "http://www.catplus.ch/ontology/concepts/sample1" --path_save="zarr_linked_data/data/results/dataset.npy"
    
    UriMatchingFlow()

    