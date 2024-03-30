<h1 align="center"> TableTracker</h1>

<p align="center">
<img src="https://github.com/Musa-Sina-Ertugrul/DBScanner/assets/102359522/1ea4b501-898f-4b57-8a7e-90e853d50cdd">
</p>

# TODO: Write Introduction

<h3 align="center">Enviroment Creation</h3>

> To create necessary enviroment

```console
conda create -n DBScanner python=3.11 pip -y
```

> To activate enviroment

```console
conda activate DBScanner
```

> To install required modules

```console
pip install -r requirements.txt
```

<h3 align="center">Reformatting</h3>

> For reformatting use <b><i>black</i></b>. It reformat for pep8 as same as pylint but better !!!

```console
black .
```

<h3 align="center">Run App</h3>

> For running app

```console
python db_scanner
```

<h3 align="center">Linting</h3>

> For running <b><i>pylint</i></b>

```console
pylint ./db_scanner/ ./test/
```

<h3 align="center">Testing</h3>

> For running <b><i>unittest</i></b>

```console
python -m unittest discover -v
```
