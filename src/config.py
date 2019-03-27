import os

access_token = os.environ['PAGE_ACCESS_TOKEN'] or "x"

page_id = os.environ['PAGE_ID'] or "-1" # ID of the public Facebook page where comments will be downloaded from.
page_name = os.environ['PAGE_NAME'] or "PAGE NAME" # Name of page, must be exactly as shown in page url.
