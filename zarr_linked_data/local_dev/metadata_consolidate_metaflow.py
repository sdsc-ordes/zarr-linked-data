from metaflow import FlowSpec, step, Parameter

class MetadataConsolidateFlow(FlowSpec):

    path_for_store = Parameter(
        "path_for_store",
        help="The path to the Zarr Store who's metadata we want to consolidate into a Zarr MetadataStore.",
    )

    @step
    def start(self):
        """Start the consolidation flow."""  
        self.next(self.consolidate)

    @step
    def consolidate(self):
        """Consolidate metadata."""
        import zarr
        zarr.convenience.consolidate_metadata( 
            store=self.path_for_store,
            metadata_key=".all_metadata"
        )
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
    # python zarr_linked_data/local_dev/metadata_consolidate_metaflow.py run --path_for_store="zarr_linked_data/data/test_store.zarr"

    MetadataConsolidateFlow()