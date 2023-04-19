# UKS-Tim5

This is a web based VCS, project management and collaboration tool. GitHub's twin brother.

## Setup:

### Clone repo:

```
git clone https://github.com/JSTheGreat/UKS-Tim5.git
cd UKS-Tim5
```

### Create venv:

```python
# Create virtual environment
python -m venv venv

# Start virtual environment
.\venv\Scripts\activate
```

### Run with docker:

You will need docker installed on your machine and set to run on Linux containers.

```python
# To setup the environment and run the Django app, execute the following command:
docker-compose up

# It is possible to order the docker-compose to build uks_tim5_web the container:
docker-compose up --build

# If all containers should be recreated, then execute:
docker-compose up --build --force-recreate
```

App will be running on [http://localhost:8083/](http://localhost:8083/), but only after you try to enter [http://localhost:8001/](http://localhost:8001/) or else NgInx will throw 502 Bad Gateway error.
