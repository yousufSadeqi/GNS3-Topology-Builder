# GNS3 Topology Builder

A simple Python script that automatically creates a network topology in GNS3 using the GNS3 REST API.

## Features

* Creates a GNS3 project (or reuses an existing one)
* Adds three Cisco C7200 routers
* Adds three Ethernet switches
* Adds six VPCS hosts
* Automatically connects all devices
* Opens the project after creation

## Requirements

* Python 3.8 or later
* GNS3 installed and running
* GNS3 server API enabled
* The following templates must already exist in GNS3:

  * Cisco C7200
  * Ethernet Switch
  * VPCS

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

Create a virtual environment (recommended):

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required dependency:

```bash
pip install requests
```

Or create a `requirements.txt` file containing:

```text
requests
```

Then install it with:

```bash
pip install -r requirements.txt
```

## Configuration

Before running the script, update the following variables if needed:

```python
SERVER = "http://127.0.0.1:3080"
AUTH = ("username", "password")
PROJECT_NAME = "tests"
```

* `SERVER` should point to your GNS3 server.
* `AUTH` should contain your GNS3 API username and password.
* `PROJECT_NAME` is the name of the project that will be created or reused.

## Running the Script

Run the script with:

```bash
python main.py
```

If successful, the output will end with:

```text
Topology built.
```

## Topology

The script creates:

* 3 Cisco C7200 routers

  * R1
  * R2
  * R3
* 3 Ethernet switches

  * SW1
  * SW2
  * SW3
* 6 VPCS hosts

  * PC1
  * PC2
  * PC3
  * PC4
  * PC5
  * PC6

Connections:

* Each router is connected to its local switch.
* Routers are connected in a chain:

  * R1 ↔ R2
  * R2 ↔ R3
* Each switch connects to two PCs.

## Notes

* Ensure the required templates are available before running the script.
* The script assumes the Cisco C7200 image is already installed in GNS3.
* If a project with the specified name already exists, it will be reused instead of creating a new one.
