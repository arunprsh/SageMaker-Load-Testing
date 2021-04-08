from construct_payload import PAYLOAD
from locust import HttpUser, task
from authorizer import authorize
from random import choice
import config as config

# For content type=text/csv use below line
# PAYLOAD = '0.234234,0.234345,0.5634,-0.23535'

# For content type=text/csv (with header) use below style
# PAYLOAD = 'id,text,filename__v,format__v,size__v,charsize,pages__v\n31011,foo,foo,foo,16290,768,1'

# For content type=application/json use similar to below 2 lines
"""
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
PAYLOAD = json.dumps(PAYLOAD)
"""

target_models = [f'customer{i}.tar.gz' for i in range(1, 1001)]


class WebsiteUser(HttpUser):
    min_wait = 1
    max_wait = 5  # time in ms

    """
    @task(20)  # Model-1 gets called 20x times more than Model-2
    def test_post_model_1(self):
        # Load Test SageMaker Endpoint (POST request)
        headers = authorize(PAYLOAD, 'customer1.tar.gz')
        self.client.post(conf.SAGEMAKER_ENDPOINT_URL, data=PAYLOAD, headers=headers, name='Post Request')
        # time.sleep(5)

    @task(1)
    def test_post_model_2(self):
        # Load Test SageMaker Endpoint (POST request)
        headers = authorize(PAYLOAD, 'customer2.tar.gz')
        self.client.post(conf.SAGEMAKER_ENDPOINT_URL, data=PAYLOAD, headers=headers, name='Post Request')
        # time.sleep(15)
    """
    @task
    def test_post(self):
        headers = authorize(PAYLOAD, choice(target_models))
        self.client.post(config.SAGEMAKER_ENDPOINT_URL, data=PAYLOAD, headers=headers, name='Post Request')
