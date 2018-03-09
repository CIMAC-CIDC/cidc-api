![circleci](https://circleci.com/gh/dfci/cidc-ingestion-api.svg?style=shield&circle-token=f1cc21bf7abc3bddd43d1ed02bc2d24849d18f0f|alt=circleci)
## Ingestion API

Python-EVE powered API for CIDC bioinformatics pipeline. This API is designed to be used with a CLI tool dsitributed to bioinformaticians. 

### Installation

At the root of the directory there is a bash script called "dockerbuild.sh", simply run the command

```bash dockerbuild.sh```

to build the image. 

### File Tree

```
├── dockerbuild.sh
├── Dockerfile
├── docs
│   ├── _build
│   ├── conf.py
│   ├── index.rst
│   ├── Makefile
│   ├── _static
│   └── _templates
├── ingestion_api.py
├── Pipfile
├── Pipfile.lock
├── rabbit_handler.py
├── README.md
├── settings.py
└── tests
    ├── __pycache__
    ├── test_ingestion_api.py
```


