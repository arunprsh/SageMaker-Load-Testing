# SageMaker-Load-Testing
SageMaker Endpoint Load Testing using Locust

#### Setup Instructions:

1. Create a Python virtual or conda environment or use native Python on your desktop  
2. Using your terminal   
    `$ pip install locust` or `$ pip install -r requirements.txt`
3. Set your parameters in `config.py`  
4. Start the locust server:  
    `$ locust --host=http://localhost:8080 --locustfile=locustfile.py`
5. Access Locust UI running at this location: http://localhost:8089/
