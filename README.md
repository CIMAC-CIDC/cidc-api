![Build Status](http://35.229.46.114/jenk/buildStatus/icon?job=API%20Repo/master)

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


