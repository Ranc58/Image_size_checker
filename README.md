Image size checker
=====================

[![Build Status](https://travis-ci.org/Ranc58/Image_size_checker.svg?branch=master)](https://travis-ci.org/Ranc58/Image_size_checker)


REST API based on aiohttp and MongoDB for check images sizes. 


# How to install
#### With docker:
If it need (By default conf file have settings for docker) - setup MongoDB and max urls count per request in `config/conf.yaml`.\
Then run `docker-compose build`

#### Without docker
1) with `pipenv`: \
   `pipenv shell` \
   `pipenv install`
2) with `virtualenv`: \
   `python3 -m venv myenv`\
   `source myenv/bin/activate`\
   `pip3 install -r requirements.txt`\
Create dir for images! `mkdir src/images`

# Tests
If you use `pipenv`: `pipenv install --dev`

Run `./run_tests`

# How to run
#### With Docker:
`docker-compose up`

#### Without Docker:
If it need - setup MongoDB and max urls count per request in `config/conf.yaml`.\
Run MongoDB (locally for example setup `host` in `conf.yaml` and run mongo from docker file: `docker-compose up mongo`)\
Run server `python3 src/main.py`


# Work example
For get images info : POST request to http://localhost:8080/api/v1/images. \
Data should be an array and have by default maximum 5 urls. Like this:
  ```python
  [
    {"url": "https://example.com/1.jpg"},
    {"url": "https://example.com/2.jpg"},
    {"url": "https://example.com/3.jpg"},
  ]
  ```
 By default, if request contains >5 elements or have recurring urls - the array will be truncated to 5 elems. 
 You can change it in `config/conf.yaml`.

Response example:
```python
{"id": "5b8ce03685022d486fd0b316", "result": [
{"url": "https://example.com/1.jpg", "width": 2560, "height": 1707, "created": "2018.09.03 10:18"},
{"url": "https://example.com/2.jpg", "width": 2560, "height": 1707, "created": "2018.09.03 10:18"},
{"url": "https://example.com/3.jpg", "width": 2560, "height": 1707, "created": "2018.09.03 10:18"},
]}
```

In future you can `GET` info by `id`: `http://localhost:8080/api/v1/images/5b8ce03685022d486fd0b316`
