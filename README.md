# Python REST API With Flask, Connexion, and SQLAlchemy

You should first create a virtual environment:

```console
$ python -m venv venv
$ source venv/bin/activate
```

Install the pinned dependencies from `requirements.txt`:

```console
(venv) $ python -m pip install -r requirements.txt
```

Then, navigate into the `flask_api/` folder:

```console
(venv) $ cd flask_api
(venv) $ python app.py
```

To see your home page, visit `http://127.0.0.1:8000`. You can find the Swagger UI API documentation on `http://127.0.0.1:8000/api/ui`.

### Optional: Build the Database

You can build a SQLite database with content by following the commands below.

Navigate into the `flask_api/` folder:

```console
(venv) $ python build_database.py
```

This will delete any existing database and create a new database named `menu.db` that you can use with your project.

## License

Distributed under the MIT license. See [`LICENSE`](../LICENSE) for more information.
