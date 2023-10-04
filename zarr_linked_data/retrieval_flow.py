import json
import zarr
from metaflow import FlowSpec, step, Parameter, current, kubernetes
from dotenv import load_dotenv
load_dotenv()

class RetrievalFlow(FlowSpec):
    """Given an input URI look for the corresponding instance in the metadata store and extract the associated data.
    Parameters:
    path_metadata_store (str): path to the metadata store
    uri (str): URI to be matched
    store (zarr store): store where to search for the dataset
    """

    uri = Parameter(
        "uri",
        # type="str",
        help="The URI referencing the dataset object which should be retrieved.",
    )
    # path_store = Parameter(
    #     "path_store", type="str",
    #     help="The path to the Zarr Store where the dataset is stored."
    # )

    @kubernetes(secrets=["argo-artifacts"])
    @step 
    def start(self):
        """Start the retrieval flow."""
        # print(
        #     "Looking for the following URI [%s] in the metadata of the following store: %s"
        #     % (self.uri, self.path_store)
        # )
        # zarr.convenience.consolidate_metadata(
        #         store="../data/test_store.zarr"
        #         #store=str(path_store),
        #         #metadata_key=".all_metadata"
        #     )
        self.path_store = "../data/test_store.zarr"
        self.path_metadata_store = self.path_store + "/.all_metadata"
        self.next(self.open_metadata_store)

    @kubernetes(secrets=["argo-artifacts"])
    @step
    def open_metadata_store(self):
        """Open a zarr metadata store and returns it in a dictionary format."""
        try:
            with open(self.path_metadata_store) as all_metadata:
                store_metadata = json.load(all_metadata)
                self.dict_metadata = store_metadata["metadata"]
        except ImportError:
            print(
                "Could not open metadata store. Check that `path_metadata_store` is correct."
            )
        self.next(self.match_uri)

    @kubernetes(secrets=["argo-artifacts"])
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

    @kubernetes(secrets=["argo-artifacts"])
    @step
    def extract_dataset(self):
        """Extract the dataset attached to the metadata path/key."""
        # the path coming in will be in the format "path/.zattrs" so we strip this last part
        path = self.key_uri.split("/.zattrs")[0]
        # all Datasets will be stored as a subentity of their group with the prefix "Dataset"
        uri_data = path + "/" + path.split("/")[-1] + "Dataset"
        try:
            # two options: path or store
            # option 1
            # self.data = zarr.open(self.path_store + "/" + uri_data,
            #                 mode='r',
            #                 #shape=(9000, 10000),
            #                 #chunks=(900, 1000),
            #                 dtype='float64')
            # option 2
            self.data = zarr.open(
                self.path_store,
                mode="r",
                # ho to handle chunking ?
                # shape=(9000, 10000),
                # chunks=(900, 1000),
                dtype="float64",
                path=uri_data,
            )
        except ImportError:
            print(
                "Could not open the dataset. Check that `path_store` is correct. OR There may not be any data associated with the instance you are looking for."
            )
        self.next(self.end)

    @kubernetes(secrets=["argo-artifacts"])
    @step
    def end(self):
        """End the flow and return associted data."""
        return self.data

if __name__ == "__main__":
    # ----------------------------------------------
    ###### RETRIEVAL FLOW
    # ----------------------------------------------
    # test_uri = "http://www.catplus.ch/ontology/concepts/sample1"
    # test call terminal:
    # step 1: python zarr_linked_data/retrieval_flow.py run --uri "http://www.catplus.ch/ontology/concepts/sample1" 
    # step 2: python zarr_linked_data/retrieval_flow.py run --uri "http://www.catplus.ch/ontology/concepts/sample1" --path_store "../data/test_store.zarr"

    #python zarr_linked_data/retrieval_flow.py --with retry argo-workflows create --datastore=s3

    data = RetrievalFlow()