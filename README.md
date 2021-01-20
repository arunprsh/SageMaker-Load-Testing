# SageMaker Endpoint Load Testing
SageMaker Endpoint Load Testing using Locust

#### Setup Instructions:

1. Create a Python virtual or conda environment or use native Python on your desktop  
2. Using your terminal   
    `$ pip install locust` or `$ pip install -r requirements.txt`
3. Set your parameters in `config.py`  
4. Start the locust server:  
    `$ locust --host=http://localhost:8080 --locustfile=locustfile.py`
5. Access Locust UI running at this location: http://localhost:8089/


> This document encompasses all the instructions to calibrate a SageMaker model endpoint using Locust. Also, it includes pointers to help pick the optimal strategy for auto scaling.

### **Locust Resources:**

* [Locust Quick Start](https://docs.locust.io/en/stable/quickstart.html)
* [Writing a Locust file](https://docs.locust.io/en/stable/writing-a-locustfile.html)


In the Locust UI, we need to set 2 main parameters:

* *The number of users =* the number of users testing your application. Each user opens a TCP connection to your application and tests it.
* *Hatch or spawn rate*: For each second, how many users will be added to the current pool of users until the total amount of users is reached. At each hatch, Locust calls the `on_start` function if you have one defined in the `locustfile.py`.

*Example:*

* Number of users: 1000
* Hatch rate: 10
* For every second, 10 users will be added to current pool of users starting from 0. So in 100 seconds, you will have 1000 users. Locust tries to distribute the load equally for each user.

Basically, requests per second (RPS) or throughput indicates the number of transactions per second your application can handle. And response time or latency is the amount of time from the moment that a user sends a request until the time that your application indicates that the request has completed. 

The overall throughput tends to decrease as you increase the response time for an average transaction. The reason is, after sending the 1st request, locust needs to wait (blocking) until the request is completed or processed before sending the 2nd request.

In the Locust UI, we can track the following parameters:

*  Request — Total number of requests made so far
*  Fails — Number of requests that have failed
*  Median — Response speed for 50 percentile in ms
*  90%ile — Response speed for 90 percentile in ms
*  Average — Average response speed in ms
*  Min — Minimum response speed in ms
*  Max — Maximum response speed in ms
*  Average bytes — Average response size in bytes
*  Current RPS — Current requests per second
*  Current Failure/s — Total number of failures per second


In Locust, each simulated user does the following:

1. Pick one of the tasks from your locust file
2. Run the task (execute that task function)
3. Pick a random wait time between `min_wait` and `max_wait` (specified in your `locustfile.py`)
4. Wait that amount of time
5. Repeat from 1




