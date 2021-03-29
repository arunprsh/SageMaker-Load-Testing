HOST = 'runtime.sagemaker.us-east-1.amazonaws.com'
REGION = 'us-east-1'
# replace the url below with the sagemaker endpoint you are load testing
SAGEMAKER_ENDPOINT_URL = 'https://runtime.sagemaker.us-east-1.amazonaws.com/endpoints/emr-byoc-sklearn-2021-03-28-21-08-24/invocations'
# ACCESS_KEY = '<USE YOUR AWS ACCESS KEY HERE>'
# SECRET_KEY = '<USE YOUR AWS SECRET KEY HERE>'
# replace the context type below as per your requirements
# CONTENT_TYPE = 'text/csv'
CONTENT_TYPE = 'application/json'
METHOD = 'POST'
SERVICE = 'sagemaker'
SIGNED_HEADERS = 'content-type;host;x-amz-date'
CANONICAL_QUERY_STRING = ''
ALGORITHM = 'AWS4-HMAC-SHA256'
