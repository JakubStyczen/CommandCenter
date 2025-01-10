# Command Center Django App

Project provide several simple web applications:
- pigeonDeterrent - displays pigeon interrupts from mongoDB (poritng from documents to model objects by **djongo**)
- weatherApp - displays weather conditions like temperature (default database sqlite3)
This repo was also created to move backend (Flask) and frontend form [pigeonDeterrent](https://github.com/JakubStyczen/PigeonDeterrent) repo to Django.

Structure of project is basic and most common for Django projects (views, models and forms).
However there is some additional functionalities:
- CommandCenter.config - env varialbes reading and log setup
- ExternalModules - containing 2 inch LCD display handler provided by Waveshare
- mainApp - contains basic layout for all apps
- weatherApp.logic - hardware logic of handling displays and temperature sensors but also controller
- weatherApp.management - custom commands for app
- weatherApp.cron - custom cron job for cleaning db if amount of record is above limit
- routers - assure proper databases assigment for apps


## Instalation
Basic requirements:
    - python 3.11
    - poetry
    - proper hardware (Rapsberry Pi, sensors, displays)

1. Move into CommandCenter directory and run `poetry install`
2. Set proper env variables in **.env** file

## Basic usage
All django commands have to run in venv:

    `poetry shell`

To start django server run:

    `python3 manage.py runserver IP_ADDR:PORT`

To start temperature measurement hardware logic run:

    `python3 manage.py temperature_measurements`

By default this command run with no arguments displays measurements by webpage. You can provide additional displays by e.g.:
    
    `python3 manage.py temperature_measurements --displays cmd lcd`

For more info use `--help`.


## Tests
To run all tests locally type:

    `python3 manage.py test --settings=CommandCenter.test_settings`

## Additional funtionalities

Here is list of the functionalities available in this repo:
- github actions CI pipeline -> install dependencies, run tests, format code and generate coverage report
- pre-commit -> code formatting with Black locally
- generating coverage tests report with *coverage*
- managing dependencies with *poetry*