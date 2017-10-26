import re

def get_post_id(url):
    if is_fb_url(url):
        return get_post_id_from_fb_url(url)
    else:
        return None

# gets a post_id from a facebook url
# possible fb urls: https://developers.facebook.com/docs/plugins/oembed-endpoints
def get_post_id_from_fb_url(url):

    #remove any query string
    matches = re.search(r'(\/[^?]+).*', url)

    if matches:
        matches_list = matches.group(1).split('/')
        filtered_matches_list = filter(None, matches_list)
        return filtered_matches_list[-1]

    else:
        return None

def is_fb_url(url):
    matches = re.search(r'^(?:https?:\/\/)?(?:www\.)?(?:business.)?facebook.com(?=\/[a-zA-Z0-9(\.\?)?])', url)

    if matches:
        return True
    else:
        return False
