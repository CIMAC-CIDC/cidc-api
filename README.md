![codecov](https://codecov.io/gh/dfci/cidc-ingestion-api/branch/master/graph/badge.svg)
## Ingestion API
Python-EVE powered API for CIDC bioinformatics pipeline. This API is designed to be used with a CLI tool dsitributed to bioinformaticians. 

### Build
At the root of the directory there is a bash script called "dockerbuild.sh", simply run the command `bash dockerbuild.sh`
to build the image. 

## Installation
This application is not meant to be run outside of the context of a container such as Docker, Docker-Compose, or Kubernetes. The easiest way to install this application without building it yourself is to copy the Helm chart from our [helm repo](https://github.com/dfci/cidc-devops/tree/master/kubernetes/helm/ingestion-api). And then use `helm install` to install the service on your kubernetes cluster.