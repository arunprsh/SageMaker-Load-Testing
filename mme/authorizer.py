import config as conf
import datetime
import hashlib
import logging
import hmac
import json

logging.basicConfig(level=logging.INFO)

"""
Please refer to the documentation below for more details on SageMaker endpoint access using 
authorization headers.
https://docs.amazonaws.cn/en_us/general/latest/gr/sigv4-signed-request-examples.html
"""


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def get_canonical_url(endpoint_url):
    canonical_uri = '/' + '/'.join(endpoint_url.split('/')[-3:])
    return canonical_uri


def get_date_time():
    date_time = datetime.datetime.utcnow()
    date = date_time.strftime('%Y%m%d')
    time = date_time.strftime('%Y%m%dT%H%M%SZ')
    return date, time


def construct_signature_key(key, date_stamp, region_name, service_name):
    signature_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    signature_region = sign(signature_date, region_name)
    signature_service = sign(signature_region, service_name)
    signature_key = sign(signature_service, 'aws4_request')
    return signature_key


def construct_canonical_headers(time):
    canonical_headers = f'content-type:{conf.CONTENT_TYPE}\nhost:{conf.HOST}\nx-amz-date:{time}\n'
    return canonical_headers


def get_payload_hash(payload):
    payload = payload.encode('utf-8')
    payload_hash = hashlib.sha256(payload).hexdigest()
    return payload_hash


def construct_canonical_request(canonical_uri, canonical_headers, payload_hash):
    canonical_request = f'{conf.METHOD}\n{canonical_uri}\n{conf.CANONICAL_QUERY_STRING}\n{canonical_headers}\n{conf.SIGNED_HEADERS}\n{payload_hash}'
    return canonical_request


def get_credential_scope(date):
    credential_scope = f'{date}/{conf.REGION}/{conf.SERVICE}/aws4_request'
    return credential_scope


def get_string_to_sign(time, credential_scope, canonical_request):
    digest = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    string_to_sign = f'{conf.ALGORITHM}\n{time}\n{credential_scope}\n{digest}'
    return string_to_sign


def get_signing_key(date):
    key = construct_signature_key(conf.SECRET_KEY, date, conf.REGION, conf.SERVICE)
    return key


def get_signature(key, string_to_sign):
    signature = hmac.new(key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature


def construct_authorization_headers(credential_scope, signature):
    authorization_headers = f'{conf.ALGORITHM} Credential={conf.ACCESS_KEY}/{credential_scope}, SignedHeaders={conf.SIGNED_HEADERS}, Signature={signature}'
    return authorization_headers


def get_headers(time, authorization_headers, target):
    headers = {'Content-Type': conf.CONTENT_TYPE,
               'X-Amz-Date': time,
               'X-Amzn-SageMaker-Target-Model': target,
               'Authorization': authorization_headers}
    return headers


def authorize(payload, target):
    # Comment out logging when running load test
    date, time = get_date_time()
    canonical_headers = construct_canonical_headers(time)
    # logging.info(f'[CANONICAL HEADERS: {canonical_headers}]')

    canonical_uri = get_canonical_url(conf.SAGEMAKER_ENDPOINT_URL)
    payload_hash = get_payload_hash(payload)
    canonical_request = construct_canonical_request(canonical_uri, canonical_headers, payload_hash)
    # logging.info(f'[CANONICAL REQ: {canonical_request}]')

    credential_scope = get_credential_scope(date)
    string_to_sign = get_string_to_sign(time, credential_scope, canonical_request)
    signing_key = get_signing_key(date)
    signature = get_signature(signing_key, string_to_sign)
    # logging.info(f'[SIGNATURE: {signature}]')

    authorization_headers = construct_authorization_headers(credential_scope, signature)
    # logging.info(f'[AUTHORIZATION HEADER: {authorization_headers}]')

    headers = get_headers(time, authorization_headers, target)
    # logging.info(f'[HEADERS: {headers}]')
    return headers


if __name__ == '__main__':
    # Execute this script alone for testing authorize function

    # Use below format for content type=text/csv
    # payload = '0.234234,0.234345,0.5634,-0.23535'
    # Use below format for content type=application/json
    PAYLOAD = {'instances': [[2.804030096111861,
                              -0.5078493396918523,
                              0.9696087678038148,
                              -0.3296902366978934,
                              1.2317458148495393,
                              0.11934137168357777,
                              1.1473978828301732,
                              -0.9193527632708587,
                              1.6060928595608375,
                              1.4077822707538348,
                              0.9051304120610045,
                              -4.278295167692499,
                              2.513247725276389]]}
    payload = json.dumps(PAYLOAD)
    authorize(payload, 'model2.tar.gz')
