# MIT License
#
# Copyright (c) 2017 Max Woolf
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom
# the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# https://github.com/minimaxir/facebook-page-post-scraper
#
import json
import datetime
import csv
import time

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request

# Modififed to only attempt once - Logan Sims
def request_once(url):
    req = Request(url)
    try:
        response = urlopen(req)
        if response.getcode() == 200:
            success = True
    except Exception as e:
        print(e)
        print("Error for URL {}: {}".format(url, datetime.datetime.now()))
        return None

    return response.read()

# Needed to write tricky unicode correctly to csv
def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')

def getFacebookCommentFeedUrl(base_url):

    # Construct the URL string
    fields = "&fields=id,message,reactions.limit(0).summary(true)" + \
        ",created_time,comments,from,attachment"
    url = base_url + fields

    return url

def processFacebookComment(comment, status_id, parent_id=''):

    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.

    # Additionally, some items may not always exist,
    # so must check for existence first

    comment_id = comment['id']
    comment_message = '' if 'message' not in comment or comment['message'] \
        is '' else unicode_decode(comment['message'])

    comment_author = unicode_decode(comment['from']['name'] if 'from' in comment else "user")

    if 'attachment' in comment:
        attachment_type = comment['attachment']['type']
        attachment_type = 'gif' if attachment_type == 'animated_image_share' \
            else attachment_type
        attach_tag = "[[{}]]".format(attachment_type.upper())
        comment_message = attach_tag if comment_message is '' else \
            comment_message + " " + attach_tag

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    comment_published = datetime.datetime.strptime(
        comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
    comment_published = comment_published + datetime.timedelta(hours=-5)  # EST
    comment_published = comment_published.strftime(
        '%Y-%m-%d %H:%M:%S')  # best time format for spreadsheet programs

    # Return a tuple of all processed data

    return (comment_id, status_id, parent_id, comment_message, comment_author,
            comment_published)

# Modififed to yield contents of CSV - Logan Sims
def scrapeFacebookPageFeedComments(stringIO, writer, page_id, access_token, status_id):
    writer.writerow(["comment_id", "status_id", "parent_id", "comment_message",
                "comment_author", "comment_published"])

    num_processed = 0
    scrape_starttime = datetime.datetime.now()
    after = ''
    base = "https://graph.facebook.com/v2.9"
    parameters = "/?limit={}&access_token={}".format(
        100, access_token)

    print("Scraping {} Comments From Posts: {}\n".format(page_id, scrape_starttime))

    reader = [dict(status_id=status_id)]

    for status in reader:
        has_next_page = True

        while has_next_page:

            node = "/{}/comments".format(status['status_id'])
            after = '' if after is '' else "&after={}".format(after)
            base_url = base + node + parameters + after

            url = getFacebookCommentFeedUrl(base_url)

            data = request_once(url)

            if data is None:
                writer.writerow(['url error'])
                yield stringIO.getvalue()
                stringIO.seek(0)
                stringIO.truncate(0)
                raise StopIteration
                
            # python 3.6+ decodes automatically 
            try:
                comments = json.loads(data)
            except TypeError:
                comments = json.loads(data.decode('utf-8'))

            for comment in comments['data']:
                comment_data = processFacebookComment(
                    comment, status['status_id'])

                writer.writerow(comment_data)
                yield stringIO.getvalue()
                stringIO.seek(0)
                stringIO.truncate(0)

                if 'comments' in comment:
                    has_next_subpage = True
                    sub_after = ''

                    while has_next_subpage:
                        sub_node = "/{}/comments".format(comment['id'])
                        sub_after = '' if sub_after is '' else "&after={}".format(
                            sub_after)
                        sub_base_url = base + sub_node + parameters + sub_after

                        sub_url = getFacebookCommentFeedUrl(
                            sub_base_url)
                        sub_comments = json.loads(
                            request_once(sub_url))

                        for sub_comment in sub_comments['data']:
                            sub_comment_data = processFacebookComment(
                                sub_comment, status['status_id'], comment['id'])

                            writer.writerow(sub_comment_data)
                            yield stringIO.getvalue()
                            stringIO.seek(0)
                            stringIO.truncate(0)

                            num_processed += 1
                            if num_processed % 100 == 0:
                                print("{} Comments Processed: {}".format(num_processed,datetime.datetime.now()))

                        if 'paging' in sub_comments:
                            if 'next' in sub_comments['paging']:
                                sub_after = sub_comments[
                                    'paging']['cursors']['after']
                            else:
                                has_next_subpage = False
                        else:
                            has_next_subpage = False

                # output progress occasionally to make sure code is not
                # stalling
                num_processed += 1
                if num_processed % 100 == 0:
                    print("{} Comments Processed: {}".format(num_processed, datetime.datetime.now()))

            if 'paging' in comments:
                if 'next' in comments['paging']:
                    after = comments['paging']['cursors']['after']
                else:
                    has_next_page = False
            else:
                has_next_page = False

        print("\nDone!\n{} Comments Processed in {}".format(num_processed, datetime.datetime.now() - scrape_starttime))
