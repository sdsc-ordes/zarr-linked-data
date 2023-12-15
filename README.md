# Zarr Linked Data

The project seeks to make **a dataflow composed both of the Zarr data format and linked metadata (JSON-LD)**.

The current **infrastructure prototype** implementation is kubernetes based, requiring Metaflow for code pipelines, MinIO for storage and Argo for automation. 

The project is a prototype infrastructure **under construction** and is still incomplete. Its components need to be assessed and adapted to a new use-case before being used.  

<img width="919" alt="Screenshot 2023-12-13 at 15 04 29" src="https://github.com/SDSC-ORD/zarr-linked-data/assets/22447169/ed7153f0-e22b-46a9-bf1f-fffb3a7f5445">

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

Set-up you [poetry project](https://python-poetry.org/docs/#installation) using `poetry install` in the same folder as the pyproject.toml

OR 

Install the requirements with `pip install -r requirements.txt` (these are the requirements for the kubernetes set-up so you will have some useless packages for local dev)

## With kubernetes

You will be using the manifests in the `manifest` folder.

### Set up a cluster

Install [minikube](https://minikube.sigs.k8s.io/docs/start/) (really for simple prototyping) or [K3S](https://k3s.io) (already production oriented). 
This project used minikube.

In this cluster create a namespace where you will be deploying all your other components. In our project it is called `argo`.

### Set up an S3 storage

We will need a storage for our fake data, for metaflow flow code packages, and for Argo artifacts (more below). You can use `argo-minio.yaml` [in the manifests folder](manifests/argo-minio.yaml) or set-up your own [via the MinIO documentation (for prototyping)](https://min.io/docs/minio/kubernetes/upstream/index.html)

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

Give Argo admin roles on cluster to access MinIO: : `kubectl create rolebinding argo-default-admin --clusterrole=admin --serviceaccount=argo:default --namespace=argo` (we also had to repete this rolebinding creating for argo and argo-server service accounts in the argo namespace. This rolebinding may have to be revised in a production environment where an admin role could be problematic.

### Set up an IDE (optional)

If you want an IDE deployed (e.g. working on a server). Install [a vscode service](https://artifacthub.io/packages/helm/inseefrlab/vscode) via Helm, then access by port-forwarding `kubectl -n argo port-forward deployment/my-vscode 35547:8080`. You will probably have to give admin rights to this VSCode (service account: `my-vscode` over MinIO (as done for Argo)). Finally, you will also have to add Metaflow configuration variables to the ConfigMap of VSCode, for putting metaflow code packages in MinIO. 

![configmap-my-vscode-configmaps3metaflow](https://github.com/SDSC-ORD/zarr-linked-data/assets/22447169/498a1306-5289-4527-9cfa-22e947d555e3)

Then you just install the requirements with `pip install -r requirements.txt` and you're set to go! 

# C. Example/Usage

## Fake Zarr Data
You may not have data under the zarr format yet. You can define some metadata instance objects (such as in `zarr_linked_data/data/original_data.jsonld`), then define your hierarchy levels, data level and other parameters for the creation of a random Zarr test store using `zarr_linked_data/fake_data_flow.py`.
You can find all our example data in the `data` folder, from the original jsonld metadata instance data, to the `test_store.zarr` containing random arrays as well as the jsonld metadata.

## Local scripts

- Explore Zarr group and attributes functionalities with `python zarr_linked_data/local_dev/zarr_explore.py`
- Fake data creation pipeline with: `python zarr_linked_data/fake_data_flow.py`
- Metadata consolidation Metaflow pipeline with: `python zarr_linked_data/local_dev/consolidate_metadata_flow.py run`
- Retrieve URI Metaflow pipeline with: `python zarr_linked_data/local_dev/retrieval_flow.py run`

## Scripts on kubernetes

- Fake data creation pipeline with: `python zarr_linked_data/fake_data_flow.py` (same as for locally)
- Metadata consolidation Metaflow pipeline with: `python zarr_linked_data/consolidate_metadata_flow.py run`
- Retrieve URI Metaflow pipeline with: `python zarr_linked_data/retrieval_flow.py run`

You can check the correct run of the metaflow flows with the command specified in the script. Then you will need to send them to Argo workflows. [Using Metaflow to create Argo DAGs](https://docs.metaflow.org/production/scheduling-metaflow-flows/scheduling-with-argo-workflows): `python zarr_linked_data/retrieval_flow.py --with retry argo-workflows create` (same for `consolidate_metadata_flow`)

# Roadmap

- Retrieval flow will be converted to a FastAPI instead
- A flow `metadata update` will be added: it will transform the consolidated metadata and add it to a graph database (such as GraphDB or ApacheJenaFuseki): local development of [this flow is on an annex branch here](https://github.com/SDSC-ORD/zarr-linked-data/blob/metadata_extractor/zarr_linked_data/extract_all_metadata.py)
- Monitoring / tests of the different automated steps


