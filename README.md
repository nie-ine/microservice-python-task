# microservice-json-task

This microservice renders a view to let a user work with JSON data in Python 3 and is part of the microservice pipline in [inseri](https://github.com/nie-ine/inseri). The service provides the possibility to transform a JSON data response received by an API call into the needed data structure in order to pass it to an according inseri app. With a very pragmatic approach, it currently temporarily saves your data and code input as files and runs your script against your data file.

## Run and Develop Locally

### Install and Run
1. Create a virtual environment
1. Activate your created virtual environment
1. ``pip3 install -r requirements.txt``
1. Run with ``python3 json-task.py``
1. Go to http://localhost:50000

## Run with Docker

1. Build the image: ``[sudo] docker build -t nieine/microservice-json-task .``
1. Run the container: ``[sudo] docker run -p 50000:50000 nieine/microservice-json-task``
1. Go to http://localhost:50000

## Call the Service in a RESTful Way

If the service is running, you can POST a body with JSON data from any application. 

Body:
```
{
  "datafile": "...", 
  "data": "...", 
  "codefile": "...", 
  "code": "..."
}
```
Response:
```
{
  "output": "...", 
}
```

E.g: 
```
{
  "datafile":"yourData.json",
  "data":"{\n    \"message\": \"Hel777888lo World!\"\n}\n",
  "codefile":"yourCode.py",
  "code":"# Your python 3 code goes here\nimport json\n\ndef show_message(json_file):\n    with open(json_file, 'r') as f:\n        content = json.load(f)\n\n    return content['message']\n\nif __name__ == \"__main__\":\n    print(show_message(\"yourData.json\"))\n"
}

```

```
{
  "output": "Hello World!"
}
```

## Publish on Dockerhub

1. Build the image: ``[sudo] docker build -t nieine/microservice-json-task:YYYY-MM-DD .``
1. Push the image: ``[sudo] docker push nieine/microservice-json-task:YYYY-MM-DD``
