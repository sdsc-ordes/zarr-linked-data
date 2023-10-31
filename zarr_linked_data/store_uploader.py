# a small script to add data to the s3 bucket of the project

from minio import Minio
from minio.error import S3Error
import os



def store_uploader(bucket_name, store_path):

    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        #os.environ["AWS_S3_ENDPOINT"],
        "minio-service:9000",
        access_key=os.environ["AWS_ACCESS_KEY_ID"],
        secret_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        secure=False,
    )

    # Make 'argo-bucket' bucket if not exist.
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print(f"Bucket does not exist: creating {bucket_name}!")
    else:
        print(f"Bucket {bucket_name} already exists")

    for subdir, dirs, files in os.walk(store_path):
        for file_name in files:
            object_path = os.path.join(subdir, file_name)
            object_name_in_s3 = object_path
            # Upload 'store_path' as object name 'object_name' to bucket 'bucket_name'.
            client.fput_object(bucket_name, object_name_in_s3, object_path)
            print(f"{object_path} is successfully uploaded as object {object_name_in_s3} to bucket {bucket_name}.")


if __name__ == "__main__":
    # call with argo-bucket, "test_store.zarr", "data/test_store.zarr"
    bucket_name = "argobucket"
    store_path = "zarr_linked_data/data/test_store.zarr"
    
    try:
        store_uploader(bucket_name, store_path)
    except S3Error as exc:
        print("error occurred.", exc)