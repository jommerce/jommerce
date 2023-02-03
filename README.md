![djplus version](https://img.shields.io/pypi/v/djplus?style=flat-square)
![django version](https://img.shields.io/pypi/djversions/djplus?style=flat-square)
![python version](https://img.shields.io/pypi/pyversions/djplus?style=flat-square)
![license](https://img.shields.io/pypi/l/djplus?color=blue&style=flat-square)

# Why does this package exist?
Because as a freelancer, when I look at all customer orders, 
I see that 80% of those projects have common apps such as 
authentication, blog, store, admin, academy, community, etc. 
So we made this package to code all these apps **only once** and 
use them in **several projects** (Don't Repeat Yourself) and 
these apps can be **customized** by the **settings of each project**.

# Installing
You can use pip to install `djplus` for usage:
```shell
pip install djplus
```

# Usage
## Create Project
Simple command line for jumpstarting production-ready Django projects:
```shell
dj
```
or
```shell
python -m dj
```

## Auth

```python
#settings.py

INSTALLED_APPS = [
    # ...
    "dj.auth", 
    # ...
]

MIDDLEWARE = [
    # ...
    'dj.auth.middleware.AuthenticationMiddleware',
    # ...
]
```
```python
# urls.py

urlpatterns = [
    # ...
    path("auth/", include("dj.auth.urls", namespace="auth")),
    # ...
]
```
## Blog
```python
#settings.py

INSTALLED_APPS = [
    # ...
    "dj.blog", 
    # ...
]
```
```python
# urls.py 

urlpatterns = [
    # ...
    path("blog/", include("dj.blog.urls", namespace="blog")),
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
