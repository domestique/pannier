[![Build Status](https://travis-ci.org/domestique/pannier.svg?branch=master)](https://travis-ci.org/domestique/pannier)
[![codecov](https://codecov.io/gh/domestique/pannier/branch/master/graph/badge.svg)](https://codecov.io/gh/domestique/pannier)

Pannier - built by Danny Peck and Mark Rogers of Domestique Studios

This is a simple management portal application

Requirements
=====================================

Tools Required:

* Git (of course)
* Docker
* Python 3
* Postgres
* Virtualenv

Getting Started
=====================================

Initial Steps:

* Setup a new virtualenv `virtualenv pannier`
* Clone this repo `git clone <url> pannier/src`
* Activate the new virtualenv `cd pannier && . bin/activate`
* Install the requirements `cd src && pip install -r requirements.txt`
* Set up testing requirements `pip install -r testing_requirements.txt`
* Set up for development `python pannier/setup.py develop`
* Create an /etc/hosts entry that looks like so: "127.0.0.1 pannier_db"

Local Python Setup - Running tests, debugging, etc:

* Create the db `python dt/manage.py migrate`
* Set up an administrator `python dt/manage.py createsuperuser`
* Startup the server `python dt/manage.py runserver`
* Optionally: `python manage.py runserver 8008` to run on a different port
* Login via the admin at http://localhost:8000/

Docker Setup:

* If using Docker on Mac with Virtualbox, be sure to map port 8034
* `cd src`
* Create a Docker data volumes: 
    - `docker volume create --name pannier_pg_data`
* Startup with docker-compose: `invoke control_docker_dev`
* To stop the containers: `invoke control_docker_dev --cmd=down`
* Login via http://localhost:8034/
