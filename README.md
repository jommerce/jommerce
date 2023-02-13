![jommerce version](https://img.shields.io/pypi/v/jommerce?style=flat-square)
![django version](https://img.shields.io/pypi/djversions/jommerce?style=flat-square)
![python version](https://img.shields.io/pypi/pyversions/jommerce?style=flat-square)
![license](https://img.shields.io/pypi/l/jommerce?color=blue&style=flat-square)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Why does this package exist?
Because 80% of customer projects have common apps 
such as authentication, store, admin, blog, forum, academy, etc. 
Therefore, as freelancers, we decided to code all these apps only once in one place 
and use them in different projects as often as desired, 
and all these apps can be customized by the settings of each project.
This helps to save our time and increase our income in exchange for doing projects.

# Installing
You can use pip to install `jommerce` for usage:
```shell
pip install jommerce
```

# Usage
## Create Project
Simple command line for jumpstarting production-ready Django projects:
```shell
jommerce
```
or
```shell
python -m jommerce
```

## Auth

```python
#settings.py

INSTALLED_APPS = [
    # ...
    "jommerce.auth", 
    # ...
]

MIDDLEWARE = [
    # ...
    'jommerce.auth.middleware.AuthenticationMiddleware',
    # ...
]
```
```python
# urls.py
from django.urls import path, include

urlpatterns = [
    # ...
    path("auth/", include("jommerce.auth.urls", namespace="auth")),
    # ...
]
```
## Blog

```python
#settings.py

INSTALLED_APPS = [
    # ...
    "jommerce.blog", 
    # ...
]
```
```python
# urls.py 
from django.urls import path, include

urlpatterns = [
    # ...
    path("blog/", include("jommerce.blog.urls", namespace="blog")),
    # ...
]
```
# Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
