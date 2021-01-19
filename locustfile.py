from locust import HttpUser, task
from authorizer import authorize
import config as conf

PAYLOAD = '0.234234,0.234345,0.5634,-0.23535'


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
