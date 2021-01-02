# Slack Backend API

A backend application modeled after Slack, a communication platform for organizations. This application implements Workspapces, Users, Channels, Threads, Direct Messaging, and Images.

- **Workspaces**: A workspace is where on organization and its members be organized on and is made up of channels.
- **Channels**: Channels are where team members can communicate collective and work together. Team members can communicate on a channel by posting a message and having a discussion via a Thread. Messages in a channel can also have an image attatched to it which is uploaded to an AWS S3 bucket.
- **Direct Messaging**: DMs are a way to have a conversation outside of a channel in a workspace in a 1-on-1 scenario or as a group.

Made with: Flask, SQLAlchemy, & AWS
