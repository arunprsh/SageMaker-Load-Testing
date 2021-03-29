from locust import HttpUser, task
from authorizer import authorize
import config as conf
import json

# For content type=text/csv use below line
# PAYLOAD = '0.234234,0.234345,0.5634,-0.23535'

# For content type=application/json use similar to below 2 lines
PAYLOAD = {'instances': [[-1.1617474484872234,-0.7582725561441886,0.3944614964772361,0.4812270430077439]]}
PAYLOAD = json.dumps(PAYLOAD)


class WebsiteUser(HttpUser):
    min_wait = 1
    max_wait = 5  # time in ms

    @task
    def test_post(self):
        """
        Load Test SageMaker Endpoint (POST request)
        """
        headers = authorize(PAYLOAD)
        self.client.post(conf.SAGEMAKER_ENDPOINT_URL, data=PAYLOAD, headers=headers, name='Post Request')
