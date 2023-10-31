from metaflow import FlowSpec, step, current, Parameter

class MetadataConsolidateFlow(FlowSpec):

    path_for_store = Parameter(
        "path_for_store",
        help="The path to the Zarr Store who's metadata we want to consolidate into a Zarr MetadataStore.",
    )

    @step
    def start(self):
        """Start the consolidation flow."""
        # for an s3 storage of the zarr store: 
        import zarr
        from store_downloader import downloader
        store = downloader() #future enhancement, have the path store in the s3 system a parameter
        zarr.convenience.consolidate_metadata(
            store=store,
            metadata_key=".all_metadata"
        )

        #for local filesystem: 
        #import zarr
        #path_for_store = "zarr_linked_data/data/test_store.zarr"
        # zarr.convenience.consolidate_metadata(
        #     #store=path_for_store, 
        #     store=self.path_for_store,
        #     metadata_key=".all_metadata"
        # )
        self.next(self.end)

    @step
    def end(self):
        """End the consolidation flow."""
        pass


if __name__ == "__main__":
# ----------------------------------------------
    ###### CONSOLIDATE METADATA FLOW
    # ----------------------------------------------
    # call with:
    # python zarr_linked_data/consolidate_metadata_flow.py run --path_for_store="zarr_linked_data/data/test_store.zarr"
    MetadataConsolidateFlow()