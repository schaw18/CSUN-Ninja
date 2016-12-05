# FOR USE with LAMBDA
# not directly relevant for this project
# I don't really know why I keep it here

import urllib

import time

import boto3


def schedule_download_and_archive(FILE_SAVE_PATH):
    """downloads a pdf of schedule and saves it locally,
    if a local file already exists - deletes it,
    then timesmaps it with UNIX time and
    stores in in S3"""

    URL_OF_SCHEDULE_PDF = 'http://www.csun.edu/OpenClasses'


    our_file = urllib.request.urlretrieve(URL_OF_SCHEDULE_PDF, FILE_SAVE_PATH)

    timestamp = int(time.time())


    timestamped_filename = "{}_openclasses.pdf".format(str(timestamp))
    s3 = boto3.resource('s3')
    s3.Object('csunninja', timestamped_filename).put(Body=our_file)
    return