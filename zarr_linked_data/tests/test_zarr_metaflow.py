from metaflow import FlowSpec, step, current

# ----------------------------------------------
###### ARCHIVE COMMENT
# ----------------------------------------------
# Code to ensure compatibility between zarr and metaflow
# ----------------------------------------------


class ZarrFlow(FlowSpec):

    # path_store = Parameter(
    #     "path_store", help="The path to the Zarr Store where the dataset is stored."
    # )

    @step
    def start(self):
        # zarr.convenience.consolidate_metadata(self.path_store)
        zarr.convenience.consolidate_metadata("test_case/test_metaflow")
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    import zarr
    import numpy as np

    st = zarr.DirectoryStore("test_case/test_metaflow")
    root = zarr.group(st, overwrite=True)
    ds = root.create_dataset("ds", shape=100, chunks=50, dtype="i8")
    ds[:] = np.arange(100)
    ZarrFlow()
