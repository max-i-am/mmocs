<!-- omit in toc -->
# Multi Modal Open Communication System
This repository contains the code for a role-based multi-chat system for space mission control as presented by Schiffner and Burr in:

**Role-based Multi-Chat System for Space Mission Control** <!-- [PDF](tbd) -->

As presented at SpaceOps 2023

The chat system is a Python web application. The chat system is developed for Python 3.10.

<!-- omit in toc -->
## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Dataset](#dataset)
- [References](#references)
- [Citation](#citation)

## Requirements
The chat system is built and tested as a web application for Python 3.10. 
For an optimal experience please use a Python virtual environment through venv.

&rarr; For further instructions regarding Python see: [https://www.python.org](https://www.python.org)

All other requirements are listed in the [requirements.txt](requirements.txt). In the [Installation](#installation) section the installation process for the requirements is shown.

Since it is a web application, a recent web browser is necessary to interact with the chat system. The chat system is tested with the following web browsers:

- Google Chrome (version 105)
- Mozilla Firefox (version 104, 105)
- Chromium (version 105)
- Chromium (version 92)

## Installation
After making sure that all requirements are installed as presented in the [Requirements](#requirements) section, the installation of the chat system begins.

Download the code and navigate to the main folder (chatloopsystem). 

Create a python virtual environment using the following command:
```````bash
python3 -m venv ./venv
```````

Activate the python virtual environment using the following command:
```````bash
source ./venv/bin/activate
```````

Install all necessary requirements using the following command:
```````bash
pip install -r requirements.txt
```````

The system does not contain any pre-loaded data and thus, pre-loaded data must be created by executing the following command:
```````bash
PYTHONPATH=$PWD/ python3 aux/create_dummy_data.py
```````

Finally, execute the server by using the following command:
```````bash
python3 chatLoopSystem.py
```````

The chat loop system is now available at [https://localhost:5000](https://localhost:5000) and can be accessed through the web browser.

When accessing the chat system in a local area network through a different client than the server, the "localhost" must be replaced by the IP address of the server running the chat system.

Since the system uses HTTPS and the certificate is created for demonstration purposes only and not certified by a CA authority, most browsers will prohibit access to the application. Therefore, an exception must be created. Have a look at your browser's documentation for further information on how to create an exception.

For a demonstration of proper communication between two participants, the chat system should be opened in two different browsers. For example, it is possible to use Firefox for one client and Chrome for the other client. Then it is possible to send a message from one client to the other and vice versa. If only one browser is used, only one user is logged in which does not offer the ability to receive the messages on the other end.

For login data and further information on the dataset provided with this code, check the [Dataset](#dataset) section, which contains the credentials to the different user accounts. 

## Dataset
The chat system does not properly work without a dataset containing example users and their rights.

The script [create_dummy_data.py](aux/create_dummy_data.py) creates the example data in the database. Afterward, the chat system can be used with the provided accounts.

As described in the [Installation](#installation) section, the following command executes the script and creates some example data:
```````bash
PYTHONPATH=$PWD/ python3 aux/create_dummy_data.py
```````

The dataset contains six different users with different positions. Therefore, the users have, as explained in more detail in the paper, different rights and loops to communicate. The following table shows the users with their respective usernames and password for authentication:

| Username  | Password |
|-----------|----------|
| developer | 2simple  |
| maxi      | 2simple  |
| insa      | 2simple  |
| anna      | 2simple  |
| thomas    | 2simple  |
| maika     | 2simple  |

The "developer" has all possible loops and can select every possible position. Therefore, in this dataset, the "developer" is the most powerful account. 

## References
This project uses code and packages from other sources in order to function properly.
For an elaborate overview of what is used and what license it has, have a look at the separate [references](references.md) markdown file.

## Citation
<!-- [PDF](tbd) -->

```
@inproceedings{schiffner_role-based_2023,
	address = {Dubai, UAE},
	title = {Role-based {Multi}-{Chat} {System} for {Space} {Mission} {Control}},
	booktitle = {{SpaceOps} 2023 {Conference}},
	author = {Schiffner, Falk and Burr, Maximilian},
	month = mar,
	year = {2023},
	keywords = {Chat System, Role-based Chat Communication, Space Mission Operation, Voice Communication System},
}
```