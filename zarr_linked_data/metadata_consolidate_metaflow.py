import zarr
from metaflow import FlowSpec, step, Parameter

# ISSUE: At the moment this flow does not generate the consolidate metadata store.
# UNKNOWN Resolution: There is no error message and no clear explanation.


class MetadataConsolidateFlow(FlowSpec):

    path_store = Parameter(
        "path_store",
        help="The path to the Zarr Store who's metadata we want to consolidate into a Zarr MetadataStore.",
    )

    @step
    def start(self):
        """Start the consolidation flow."""
        print(
            "Consolidating the metadata of the following store: %s" % (self.path_store)
        )
        self.next(self.consolidate_metadata_store)

    @step
    def consolidate_metadata_store(self):
        """Consolidate the metadata of a zarr store."""
        try:
            metadata_store = zarr.convenience.consolidate_metadata(
                self.path_store, metadata_key=".all_metadata"
            )
        except ImportError:
            print("Could not open metadata store. Check that `path_store` is correct.")
        self.next(self.end)

    @step
    def end(self):
        """End the consolidation flow."""
        print("Consolidation complete.")


if __name__ == "__main__":
    MetadataConsolidateFlow()
