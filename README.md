# SubsMan
SubsMan is a web application for Licence and subscription manager for Saas
application

## Purpose
The purpose of the SubsMan is to provide a way to manage a subscriptions or licences of company products.

The main target of this project was creation
of the example of the web application “Subsman”. The concept of the web application will
solve the problem of the multi-platforms and will give the possibility to use the system to
anyone with internet access.

The concept of collection the management of all companies’
products subscription in one place should solve a lot of problem. This will give a lot of
flexibility and more convenient user interaction.

## Configuration (development)

* Clone this repository:

* Go to project directory and install requirements for development
```
cd SubsMan && pipenv install --dev && pipenv shell
```

* Create .env and fill with your environment variables configuration file from example config
```
cp config/.env.example config/.env
```

* Run development server:

```
./manage.py runserver_plus
```

## System dependencies

Python: *v3.8*

PostgreSQL: *v11*
