# Web Scraping Tool And API #

This project consists of a tool that scrapes the website 'www.techcrunch.com' and stores data about the articles, authors and subjects, providing API endpoints that serve
these data.

***
## Technologies Stack ##

* Python
* Django
* Django REST Framework
* PostgreSQL
* Heroku

***
## Usage ##
### Articles Endpoint ###
Endpoint: https://web-scraping-api.herokuapp.com/api/v1/articles/

Methods: only GET.

Versioning: It's versioned and has only one version (v1).

Ordering: Ordered by most recent published articles.

Filtering: It accepts subject as filter parameter. For example, to fetch all the articles whose subject is Startups: https://web-scraping-api.herokuapp.com/api/v1/articles/?subject__name=Startups

It provides the following fields:

* slug
* title
* hero image
* author name
* subject
* publish date
* text