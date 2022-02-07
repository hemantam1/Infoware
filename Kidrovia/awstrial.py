from re import S
from typing import Pattern
import boto3
import pandas as pd
from cloudpathlib import CloudPath
import os
import gzip
import shutil
import re
import datetime
"""
# Let's use Amazon S3
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('infowarekidrovia')
input_path = 'rawfiles/linkshare/28012022'

# Print out bucket names
for bucket in my_bucket.objects.filter(Prefix = input_path):
    print(bucket)

"""
# Downloading bucket files
cp = CloudPath('s3://infowarekidrovia/rawfiles/linkshare/24012022')
cp.download_to('Downloaded_files')

# Opening and extracting the zip files
start = datetime.datetime.now()
source_path = 'Downloaded_files'
destination_path = 'Extracted_files'
for file in os.listdir(source_path):
    if file.endswith('.xml.gz'):
        filename = re.split(pattern='.gz', string = file)[0]
        with gzip.open('{}/{}'.format(source_path, file), 'rb') as inp:
            with open('{}/{}'.format(destination_path, filename), 'wb') as out:
                shutil.copyfileobj(inp, out)
        print('{} extracted!'.format(file))
end = datetime.datetime.now()
print(end - start)
