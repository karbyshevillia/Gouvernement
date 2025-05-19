<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;
           width: 100%;"
    src="./Gouvernement/static/logo.png" 
    alt="Cover">
</img>

___
<!-- TOC --><a name="about"></a>
# 🔎 About the Project

**Gouvernement** is a Project Management web application running on a Flask WSGI server. It allows for organised 
role-based in-project interaction, such as the creation of projects and tasks therein, with a wide range of
parameters. All enveloped in a nice Bootstrap casing)
___

<!-- toc --><a name="how-to-run"></a>
# 🚀 How to run it?

<!-- toc --><a name="dependencies"></a>
## Dependencies
- 🐍 `python >= 3.11`: the programming language
- `flask >= 3.1.0`: WSGI server framework
- `flask-login >= 0.6.3`: used for login management
- `flask-sqlalchemy >= 3.1.1` used for SQL querying of the database
- `faker >= 37.3.0` used for testing on a sample database
- `pyclean >= 3.1.0` cache clean-up

First of all, clone the project repository and switch to the corresponding directory:
```bash
$ git clone https://github.com/karbyshevillia/Gouvernement.git --depth 1
$ cd Gouvernement
```

Your further actions will depend upon the operating system and the dependency manager you are using:

<!-- TOC --><a name="poetry"></a>
## Poetry

The project employs the [Poetry](https://python-poetry.org/) dependency manager; thus, if you wish to run the code quickly, regardless of your operating system, you can download **Poetry** and execute the following:

Download the dependencies:
```bash
$ poetry install
```

Run the app:
```bash
$ poetry run python app
```

<!-- toc --><a name="windows"></a>
## Windows

### pip

Create a new virtual environment and download the dependencies:
```bash
$ python -m venv venv
$ .\venv\Scripts\activate
$ pip install -r requirements.txt
```

Run the app:
```bash
$ python app
```

<!-- TOC --><a name="linux-macos"></a>
## Linux / MacOS

### pip

If you are using **pip**, create a new virtual environment and download the dependencies:

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Run the app:
```bash
$ python app
```


<!-- TOC --><a name="developers"></a>
# 💻 Developers

<img src="https://avatars.githubusercontent.com/u/158076825?v=4" width="100">
Illia Karbyshev <br> [@karbyshevillia](https://www.github.com/karbyshevillia)
