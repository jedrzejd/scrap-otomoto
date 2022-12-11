# scrap-otomoto

This program gets more than 95% advertisements from [otomoto.pl](https://otomoto.pl) with 227 features - [show features](feats.txt)

---

## Table of content
* [General info](#General-info)
* [Installation](#Installation)
* [Usage](#Usage)
* [Technologies](#technologies)

## General info

Program saves datasets to ```data/``` directory.

Each the car brand has a separate file ```car_name.xlsx``` with data and have ```car.xlsx``` with all cars.

Results should be 12 hours later.



## Installation on Linux/Macos

* Download and install `Python 3.7.9`

    ```
    https://www.python.org/downloads/release/python-379/
    ```
* Download this repository and unzip


* Create python virtual environment

```bash
cd scrap-otomoto-master
python3 -m venv venv
```

* Active python virtual environment

```bash
. venv/bin/activate
```

* Install require packages

```bash
pip install -r Requirements.txt
```

### Usage

```bash
python3 scrap_cars.py
```

## Installation on Windows

* Download and install `Python 3.7.9`

    ```
    https://www.python.org/downloads/release/python-379/
    ```
* Download this repository and unzip


* Create python virtual environment

```bash
cd scrap-otomoto-master
py -m venv venv
```

* Active python virtual environment

```bash
venv\Scripts\activate
```

* Install require packages

```bash
pip install -r Requirements.txt
```

### Usage

```bash
py scrap_cars.py
```

## Technologies
- Python 3.7
- beautifulsoup4
- requests
