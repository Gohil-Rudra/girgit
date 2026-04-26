# Girgit

It is a CLI replica of Git and its main aim is to study
**git-internals** !

- [Project Structure](#project-structure-)
- [Base Files](#base-files--__init__py--mainpy)
- [Setup](#setup--creation-of-cli-package)

### Project Structure :

Our Project structure looks like :
``` text
girgit/
├── venv/
├── girgit/
│   ├── __init__.py
│   └── main.py
├── README.md
├── requirements.txt
└── setup.py
```
> Our project name and package both are **girgit**.

--- 

### Base Files : `__init__.py` & `main.py`
#### `init.py` :
> we can think of `__init__.py` as a mapping file in the sense that
> we specify the functions we want to expose in our final cli tool here. 

e.g. `from .main import main` where **.main** is `main.py` in girgit's *root* directory
and **main** is the function name defined in main.py ;)

#### `main.py` :

>This is the heart of our program where
>actual work is done.

e.g. 
```bash
def main():
    print("Hello Girgit")
```

---

### Setup : Creation of CLI Package

> Create the `setup.py` file and run it in `develop --user` mode (if in
> `venv` like *pycharm IDE* no need to write
> `--user`) `develop` mode helps to automatically reload the changes
> we make in source-code all we need to do is make some
> change and reopen the terminal and *voila* !

In `setup.py` we have used `packages=find_packages()` which will
auto find and link the packages that have `__init__.py` file in them,to
exclude tests directory if present we could write `packages=find_packages(exclude="tests*")`

``` bash
python setup.py develop
```

You can test it by :
```bash
from girgit import main
main
```

---

