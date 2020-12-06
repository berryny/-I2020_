# Class Project

## Install

**Tip:** There are `.env` or `.flaskenv` files present. Do "pip install python-dotenv" to use them.

- Run the below command lines

```
pip install python-dotenv
flask run
```

## Files

- Create a `config.py` to set Flask config variables with a `class Config:`
- Create a `.env` file containing
    - Database `SQLALCHEMY_DATABASE_URI = 'sqlite:///sitepreview.db'`
```
SECRET_KEY =
SQLALCHEMY_DATABASE_URI =
```
- `import_script.py` a separates py file to Create and Inserts json data into SQLAlchemy
- `app.py` executes the web application and creates the api class to render to the page

## Execute

View the [site](https://python-web-scrapping.herokuapp.com/) in action.