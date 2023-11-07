# Yelp crawler

> Script for scrape business data from yelp.com.

![python](https://img.shields.io/badge/python-3.11-BLUE)

## Content
- [Installation](#installation)
- [Setup](#setup)
- [Description](#description)

## Installation
- Ubuntu
- Python3.11

#### Virtualenv
```shell script
$ sudo apt install virtualenv
```
## Clone
`https://github.com/Sava777cool/yelp_crawler.git`

## Setup
Install virtualenv in project folder.
```shell script
[project_folder]$ virtualenv -p $(which python3.11) venv
```
**Don't change the name "venv", the path to the virtual environment is used when creating services.** 

**If you want to change the name, make the appropriate changes to the file `[project_folder]/services/install.sh`**
```shell script
...
touch "$ENV_PRJ_SRC"
echo "VENV_PATH=${PWD}/venv" >> "${ENV_PRJ_SRC}"
...
```
Activate virtualenv
```shell script
[project_folder]$ source venv/bin/activate
```
Install python packages from requirements.txt
```shell script
(venv)[project_folder]$ pip install -r requirements.txt
```
Create the .env in the following folder `[project_folder]/config/`
and enter the appropriate data for each service, example data in file .env_example:

## Description
The program consists of the following packages:

- src
- main.py

The main scripts are specified in the `main.py` file.

#### src
Consists of:
  - `api` - this package contains files for work with api;
  - `schemas` - package contains pydantic schemas for validation json data
  - `scraper` - this package describe main scrape logic

#### Run script from console

`python main.py --category="contractors" --location="San Francisco, CA --amount_of_businesses=100"
` - main file for start main scrape.
- `--category="category"`: set category of business for parse (NECESSARY TO ENTER)
- `--location="San Francisco, CA`: location of business (NECESSARY TO ENTER)
- `--amount_of_businesses=100`: limit of parse businesses, default 100 (NOT NECESSARY TO ENTER)

As a result of the work, a file will be generated in the main directory. File will have name {category name}_data.json.
