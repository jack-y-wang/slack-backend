# Slack Backend API

A backend application modeled after Slack, a communication platform for organizations. This application implements Workspapces, Users, Channels, Threads, Direct Messaging, and Images.

- **Workspaces**: A workspace is where on organization and its members be organized on and is made up of channels.
- **Channels**: Channels are where team members can communicate collective and work together. Team members can communicate on a channel by posting a message and having a discussion via a Thread. Messages in a channel can also have an image attatched to it which is uploaded to an AWS S3 bucket.
- **Direct Messaging**: DMs are a way to have a conversation outside of a channel in a workspace in a 1-on-1 scenario or as a group.

Made with: Flask, SQLAlchemy, & AWS S3

API Spec can be found [here](https://github.com/jack-y-wang/slack-backend/blob/master/api.md)

## Setup
### Setup virtual env
```python
virtualenv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

### Setup AWS env
[Guide](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)

Create the `credentials` and `config` files. By default, their locations are at `~/.aws/credentials` and `~/.aws/cofig`

credentials:
```python
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```
config:
```python
[default]
region=us-east-1
```

## Run
```
python3 src/run.py
```
