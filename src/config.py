import os

app_id = os.environ['APP_ID'] or "-1" # Facebook app ID. see https://developers.facebook.com/docs/apps/register/
app_secret = os.environ['APP_SECRET'] or "-1" # DO NOT SHARE WITH ANYONE!

access_token = app_id + "|" + app_secret

page_id = os.environ['PAGE_ID'] or "-1" # ID of the public Facebook page where comments will be downloaded from.
page_name = os.environ['PAGE_NAME'] or "PAGE NAME" # Name of page, must be exactly as shown in page url.
