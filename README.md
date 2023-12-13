# Zarr Linked Data
The project seeks to make a dataflow composed both of the Zarr data format and linked metadata (JSON-LD).

The current implementation is kubernetes based, requiring Metaflow for pipeline, MinIO for storage and Argo for automation. 

The project is a prototype infrastructure *under construction* and is still incomplete. Its components needs to be assessed and adapted to a new use-case before being used.  

The following section describe the project further: 
- A. Project Description 
- B. Getting Started 
- C. Example / Usage 

# A. Project Description

The project's main interesting features are pipelines to manipulate [Zarr data formats](https://zarr.dev). Zarr files can store both data and [metadata](https://zarr.readthedocs.io/en/stable/tutorial.html#user-attributes), in a [hierarchical manner](https://zarr.readthedocs.io/en/stable/tutorial.html#groups). Zarr is best for storing any array-like data, as it allows compression and chunking. The metadata present with the data makes the Zarr file format of high interest for interoperability and findability goals of FAIR requirements. 

This project came into being tied to the [Cat+ initiative from EPF domain in Switzerland](https://swisscatplus.ch). From a fully automated chemistry lab, numerous samples will be processed under different parameters by a variety of machines. The idea is to have the output data of this lab, and even more so the associated metadata, to be queryable and retrievable. On the long run, the idea is also to allow external sources to contribute their data to the system as well, following metadata standards. 

The *main functionalities* that were implemented in this project were: 
- Retrieve (["consolidate"](https://zarr.readthedocs.io/en/stable/tutorial.html#consolidating-metadata) in zarr jargon) all the metadata from the numerous arrays of data
- From a metadata Universal Resource Identifier [URI](https://www.w3.org/wiki/URI), retrieve the associated dataset in the [Zarr store](https://zarr.readthedocs.io/en/stable/api/storage.html)

# B. Getting Started

# C. Example/Usage
The system is under development
