# Facebook Comment Scraper #

A small web app for downloading comments from a public facebook page post.
Comment scraping from https://github.com/minimaxir/facebook-page-post-scraper

Setup
-----

We use pip for dependencies.

```
pip install -r requirements.txt
```

You will need to [register and configure a Facebook app](https://developers.facebook.com/docs/apps/register/). Once you've done this fill out `config.py` with your information.

This project is built with [Flask](http://flask.pocoo.org/).
Hosting is up to you, the Flask webpage explains [some options](http://flask.pocoo.org/docs/0.12/deploying/).

Development Setup
----------------

```
pip install -r requirements-dev.txt
```

##### Start Flask dev server 

`FLASK_APP=fb_comment_downloader_app.py flask run`

##### Run tests

`python test_validation.py`. 
Currently, we only have a few tests for checking the facebook urls.

Contributing
------------

Find a bug? Got an idea? Send us a pull request or open an issue and we'll take a look. You can also check the issue tracker.

License
-------

MIT
