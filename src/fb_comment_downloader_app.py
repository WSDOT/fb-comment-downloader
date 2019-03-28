import io
import csv
import re

from flask import Flask
from flask import render_template
from flask import stream_with_context
from flask import Response
from flask import request
from flask import jsonify

from werkzeug.datastructures import Headers

from validation import get_post_id
from validation import get_page_name

from get_fb_comments_from_fb import scrapeFacebookPageFeedComments
from get_fb_comments_from_fb import request_once

import config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page_name=config.page_name)

@app.route('/', methods=['POST'])
def index_post():

    error = None
    url = request.form['text']

    if request_once(url) == None:
        message="Please make sure you entered a vaild url"
        return jsonify({"error": message})

    if get_page_name(url) != config.page_name:
        message="Please enter a post url for the {0} page".format(config.page_name)
        return jsonify({"error": message})


    post_id = get_post_id(url)

    status_id = "{0}_{1}".format(config.page_id, post_id)

    if status_id == None:
        message="Please make sure you entered a vaild Facebook url"
        return jsonify({"error": message})

    si = io.StringIO()
    cw = csv.writer(si)

    # add a filename
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='fb_comments.csv')

    # stream the response as the data is generated
    return Response(
        stream_with_context(scrapeFacebookPageFeedComments(
            si,
            cw,
            config.page_id,
            config.access_token,
            status_id)),
        mimetype='application/download', headers=headers
    )

if __name__ == "__main__":
        app.run()
