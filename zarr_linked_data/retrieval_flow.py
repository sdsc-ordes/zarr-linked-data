import json
import zarr
from metaflow import FlowSpec, step, Parameter, current, kubernetes, trigger

# IMPORTANT NOTE: it has been determined that this flow is better designed as a FastAPI than an Argo flow

# The Flow triggers when MetadataConsolidateFlow ends and if there is a data retrieval event
# @trigger(events=['metaflow.MetadataConsolidateFlow.end', 'data_retrieval'])
class RetrievalFlow(FlowSpec):
    """Given an input URI look for the corresponding instance in the metadata store and extract the associated data.
    Parameters:
    uri (str): URI to be matched
    """

    uri = Parameter(
        "uri",
        help="The URI referencing the dataset object which should be retrieved.",
    )

    @kubernetes(secrets="argo-artifacts", service_account='argo')
    @step 
    def start(self):
        """Start the retrieval flow."""
        import os
        import s3fs
        #future enhancement, have the path store in the s3 system a parameter
        s3 = s3fs.S3FileSystem(
                endpoint_url=os.environ["AWS_S3_ENDPOINT"],
                key=os.environ["AWS_ACCESS_KEY_ID"],
                secret=os.environ["AWS_SECRET_ACCESS_KEY"])
        self.metadata_store = s3fs.S3Map(root='argobucket/zarr_linked_data/data/test_store.zarr/.all_metadata', s3=s3, check=False)
        self.next(self.open_metadata_store)

    @kubernetes(secrets="argo-artifacts", service_account='argo')
    @step
    def open_metadata_store(self):
        """Open a zarr metadata store and returns it in a dictionary format."""
        try:
            with open(self.metadata_store) as all_metadata:
                store_metadata = json.load(all_metadata)
                self.dict_metadata = store_metadata["metadata"]
        except ImportError:
            print("Could not open metadata store.")
        self.next(self.match_uri)

    @kubernetes(secrets="argo-artifacts", service_account='argo')
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

    @kubernetes(secrets="argo-artifacts", service_account='argo')
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

    @kubernetes(secrets="argo-artifacts", service_account='argo')
    @step
    def end(self):
        """End the flow and return associted data."""
        return self.data

if __name__ == "__main__":
    # ----------------------------------------------
    ###### RETRIEVAL FLOW
    # ----------------------------------------------
    # test_uri = "http://www.catplus.ch/ontology/concepts/sample1"
    # Commands: 
    # running the flow : 
    # python zarr_linked_data/retrieval_flow.py run --uri "http://www.catplus.ch/ontology/concepts/sample1" 
    # creating an Argo DAG for the flow: 
    # python zarr_linked_data/retrieval_flow.py --with retry argo-workflows

    data = RetrievalFlow()