import zarr
from metaflow import FlowSpec, step

# from metaflow import Parameter


class MetadataConsolidateFlow(FlowSpec):

    # path_store = Parameter(
    #     "path_store",
    #     help="The path to the Zarr Store who's metadata we want to consolidate into a Zarr MetadataStore.",
    # )

    @step
    def start(self):
        """Start the consolidation flow."""
        import zarr

        zarr.convenience.consolidate_metadata(
            store="../data/test_store.zarr", metadata_key=".all_metadata"
        )
        self.next(self.end)

    @step
    def end(self):
        """End the consolidation flow."""
        pass
