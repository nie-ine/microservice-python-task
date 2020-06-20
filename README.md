# microservice-json-task

This microservice renders a view to let a user work with JSON data in Python 3 and is part of the microservice pipline in [inseri](https://github.com/nie-ine/inseri). The service provides the possibility to transform a JSON data response received by an API call into the needed data structure in order to pass it to an according inseri app. With a very pragmatic approach, it currently temporarily saves your data and code input as files and runs your script against your data file.

The service has two routes: 

## /json-task
The route /json-task is meant for pipelining requests and returns json to be consumed by the next inseri app.

## /json-gui
The route /json-gui returns the output of the Python code inside the HTML view. 

## Run and Develop Locally

### Dependencies
1. python3
2. packages: see requirements.txt

### Install and Run
1. ``pip3 install -r requirements.txt``
1. Run with ``python3 json-task.py``
1. Go to http://localhost:8080/json-task

## Run with Docker

1. Build the image: ``[sudo] docker build -t nieine/json-task .``
1. Run the container: ``[sudo] docker run -p 8080:8080 nieine/json-task``
1. Go to http://localhost:8080/json-task or http://localhost:8080/json-gui

## Call the service in a RESTful Way

If the service is running, you can POST a body with form data to one of the routes from any application. 

Body:
| Key | Value |
| --- | ----  |
| d_name | The name of your JSON file |
| c_name | The name of your Python file |
| data | Your JSON data |
| code | Your (correctly indented) Python code |

E.g.:
```
d_name:yourData.json
c_name:yourCode.py
data:{↵    "message": "Hello World!"↵}
code:import json↵↵def show_message(json_file):↵    with open(json_file, 'r') as f:↵        content = json.load(f)↵↵    return content['message']↵↵if __name__ == "__main__":↵    print(show_message("yourData.json"))
```
## Publish on Dockerhub
See [microservice-template](https://github.com/nie-ine/microservice-template)
