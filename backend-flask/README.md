# Install python version
```
pyenv install 3.10.9
```

# Set your python version
```
pyenv global 3.10.9
```

# Create virual environment
```
python -m venv venv
```

# Activate environment
```
source venv/bin/activate
```

# Install Flask
```
pip install flask
```



"loadBalancers": [
      {
          "targetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:881652387149:targetgroup/cruddur-frontend-react-js/1f0087e794cf54c7",
          "containerName": "frontend-react-js",
          "containerPort": 3000
      }
    ],