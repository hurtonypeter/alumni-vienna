# ZQFA

## Installation locally
(see http://flask.pocoo.org/docs/0.10/installation)

Clone the project from GitHub:

    $ git clone zqfa-platform

Install virtualenv in order to be able to install the needed packages in an isolated environment to not infer with existing packages:

    $ sudo pip install virtualenv
    
Setup the virtualenv in the project directory:

    $ virtualenv venv
    New python executable in venv/bin/python
    Installing distribute............done.

And activate it and download the required packages:

    $ . venv/bin/activate
    $ pip install -r requirements.txt


## Installation with Heroku in mind
(Preliminary: Install the Heroku Toolbelt)

The best way to install ZQFA on your local computer is as virtual environment.

Install virtualenv:

    $ sudo easy_install virtualenv
    
Create the virtual environment in the zqfa directory and activate it:

    $ virtualenv .venv
    $ source .venv/bin/activate

Install requirements in the virtualenv:

    $ pip install -r requirements.txt

Setup the needed config vars by copying them from production:

    $ heroku plugins:install git://github.com/ddollar/heroku-config.git
    $ heroku config:pull --overwrite --interactive

Change the config vars in `.env` to your local setup (you probably want to use a differnt database).
    
Start the app:

    $ foreman start
   
   
## Using `alembic` for migrating database changes across environments
`alembic` is used to manage changes to database files and the DB.

First do the changes to the model files. 

Creating the migration script with `alembic`:

    $ alembic revision -m "create unique index on industry.name" 
    
And finally deploy the changes to the database
    
    $ alembic upgrade head
    
    
## Flask-Mail

## Flask-Bootstrap

## Mandrill


## Heroku Deployment
We use a free Heroku instance which is linked to the official domain (www.zqfa.ch).
