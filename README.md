# To-do list application in Django

http://www.improvedpancake.tk
https://improvedpancake.herokuapp.com/

Everyone seems to be making one, so why not?

### Setting up

* Clone the repository

* Navigate to local repository folder

* Create a `virtualenv` (Python 3.6)

  `python -m venv virtualenv`


> If you have multiple versions of Python installed:
> `python3 -m venv virtualenv`


* Activate the virtual environment

  `source virtualenv/bin/activate`

  * *For Windows:* `.\env\Scripts\active`



* You should see a prompt with `virtualenv` in your terminal

* Install requirements

  `pip install -r requirements.txt`

* You're good to go!

---


> * For running the server:
>  `python manage.py runserver --settings=superlists.local_settings`
> * For running tests:
>  `python manage.py test --settings=superlists.local_settings`

Make sure you're running this **inside** the `virtualenv`

---

Based on: https://www.obeythetestinggoat.com/
