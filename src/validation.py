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
        filtered_matches_list = [_f for _f in matches_list if _f]
        return filtered_matches_list[-1]

    else:
        return None

def get_page_name(url):
    if is_fb_url(url):
        return get_page_name_from_fb_url(url)
    else:
        return None

def get_page_name_from_fb_url(url):

    # Matches the page name from a facebook url.
    # https://gist.github.com/marcgg/733592/ae0ca10a7a344140abf8e9bb890868e872c39756
    matches = re.search(r'^(?:https?:\/\/)?(?:www\.|m\.|touch\.|business\.)?(?:facebook\.com|fb(?:\.me|\.com))\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*?(\/)?([^/?\s]*)(?:/|&|\?)?.*$', url)

    if matches is None:
        return matches
    else:
        return matches.group(2)


def is_fb_url(url):
    matches = re.search(r'^(?:https?:\/\/)?(?:www\.)?(?:business.)?facebook.com(?=\/[a-zA-Z0-9(\.\?)?])', url)

    if matches:
        return True
    else:
        return False
