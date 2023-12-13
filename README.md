# Zarr Linked Data

The project seeks to make *a dataflow composed both of the Zarr data format and linked metadata (JSON-LD)*.

The current *infrastructure prototype* implementation is kubernetes based, requiring Metaflow for code pipelines, MinIO for storage and Argo for automation. 

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

## Locally (without k8)

## With kubernetes

You will be using the manifests in the `manifest` folder.

### Set up a cluster

Install [minikube](https://minikube.sigs.k8s.io/docs/start/) (really for simple prototyping) or [K3S](https://k3s.io) (already production oriented). 
This project used minikube.

In this cluster create a namespace where you will be deploying all your other components. In our project it is called `argo`.

### Set up an S3 storage

We will need a storage for our fake data, for metaflow flow packaging, and for Argo artifacts (more below). You can use `argo-minio.yaml` [in the manifests folder](manifests/argo-minio.yaml) or set-up your own [via the MinIO documentation (for prototyping)](https://min.io/docs/minio/kubernetes/upstream/index.html)

Create a secret for allowing other services to access MinIO and its bucket storage: 
```
kubectl create secret generic argo-artifacts
--from-literal=accesskey=XXXXXXX
--from-literal=secretkey=XXXXXXXXXXXXXXX
-n argo
```

### Set up Argo for automation

Installation: 
1. [This installation was used](https://argoproj.github.io/argo-workflows/quick-start/): `kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v3.4.8/install.yaml`
2. Argo deployment is launched with: `kubectl -n argo port-forward deployment/argo-server 2746:2746` 

Artifact Repository: 
Argo needs an artifact repository (storage for flows to run). Here we will use MinIO that we previously installed. You can use the `artifact-repositories.yaml` [in the manifests folder](manifests/artifact-repositories.yaml)
(The secret for minio we created before comes in here). You can set it up with: `kubectl apply -f artifact-repositories.yaml`

Give Argo admin roles on cluster to access MinIO: : `kubectl create rolebinding argo-default-admin --clusterrole=admin --serviceaccount=argo:default --namespace=argo` (we also had to repete this rolebinding creating for argo and argo-server service accounts in the argo namespace. This rolebinding may have to be revised in a production environment where an admin role could be problematic.)


Create artifact repository using yaml : (should look like image)



### Set up an IDE (optional)




# C. Example/Usage
The system is under development
