# Facebook Comment Downloader #

A small web app for downloading comments from a public facebook page post.
Comment downloading from https://github.com/minimaxir/facebook-page-post-scraper

![web app screenshot](https://user-images.githubusercontent.com/6343384/32192303-0a58cc90-bd71-11e7-8c79-bf12a3203040.png)

Setup
-----

```
pip install -r requirements.txt
```

*Note: this will install [Gunicorn](http://gunicorn.org/) and [Gevent](http://www.gevent.org/). These packages are not required if you choose a different server.*

This application is set up to only download comments on posts from a specified public facebook page. You will need to [register and configure a Facebook app](https://developers.facebook.com/docs/apps/register/). Once you've done this, fill out `config.py` with your information.

To get comment author and reactions info you will need to use a [Page Access token](https://developers.facebook.com/docs/facebook-login/access-tokens/#pagetokens) from a user who has admin rights to the page. You can get a token by setting up a [system user](https://developers.facebook.com/docs/audience-network/reporting-api/systemuser/).

Be aware of the following restriction: 
> Devmode Apps — Apps in Devmode are now rate-limited to 200 calls per hour, per page-app pair, and can only access Users who have a role on the app (admin, developer, or tester).

https://developers.facebook.com/docs/graph-api/changelog/breaking-changes

Deployment
----------
This project is built with [Flask](http://flask.pocoo.org/).
Hosting is up to you, the Flask webpage lists [some options](http://flask.pocoo.org/docs/0.12/deploying/).

Click below to deploy the app with [Gunicorn](http://gunicorn.org/) on Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

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
