import s3fs
import zarr
import os 

def store_downloader(): 
    # use fsspec instead? 

    s3 = s3fs.S3FileSystem(
        endpoint_url=os.environ["AWS_S3_ENDPOINT"],
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"])
    #check what is being created as a filesystem
    # bucket = "s3://argo-bucket"
    # files = s3.ls(bucket)
    # print(files)

    # test getting access to the store and check the hierarchy
    store = s3fs.S3Map(root='argobucket/zarr_linked_data/data/test_store.zarr', s3=s3, check=False)
    data = zarr.group(store=store)
    print(data.tree())
    print(data.info)

    # test accessing the metadata only 
    metadata = zarr.open_consolidated(store, metadata_key=".all_metadata") 
    print(metadata.tree())
    print(metadata.info)

if __name__ == "__main__":
    store_downloader()