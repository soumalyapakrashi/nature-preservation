# Nature Preservation

## Contents

* Setup
    * Node Installation
    * image-fetcher


## Setup

This section outlines the process of setting up the various services in the project.

### Node Installation

Install [Node JS](https://nodejs.org/en/) version `16.14.0 LTS`. The following are the versions used for development:

```shell
node --version
>> v16.14.0

npm --version
>> 8.3.1
```

### image-fetcher

Initially, move to the ```image-fetcher``` directory and setup the virtual environment:

```shell
cd services/image-fetcher
virtualenv venv
```

Then initialize the virtual environment:

```shell
venv/Scripts/activate
```

Then install Earth Engine into the virtual environment:

```shell
pip install earthengine-api
```

After installing for the first time, authentication of the API needs to be done. For this, run the following command:

```powershell
earthengine authenticate
```

This will open up a browser which will first ask to choose a Google Account. Choose a Google Account with which you have previously registered for Earth Engine. Then it will display a token. Copy this token to the terminal and authentication will be finished.
