# API Reference

This API is modeled after Slack, which is a communication platform for organizations. This application implements Workspapces, Users, Channels, Threads, and Direct Messaging.

- **Workspaces**: A workspace is where on organization and its members be organized on and is made up of channels.
- **Channels**: Channels are where team members can communicate collective and work together. Team members can communicate on a channel by posting a message and having a discussion via a Thread.
- **Direct Messaging**: DMs are a way to have a conversation outside of a channel in a workspace in a 1-on-1 scenario or as a group.

# Users

## Create a User
**POST** `/users/`
##### Request
``` yaml
{
    "name": "Jack Wang",
    "email": "jw123@gmail.com",
    "username": "jack.wang"
}
```
##### Response
``` yaml
{
    "success": true,
    "data": {
        "id": 1,
        "name": "Jack Wang",
        "email": "jw123@gmail.com",
        "username": "jack.wang",
        "workspaces": [SERIALIZED WORKSPACES OF USER, ...]
    }
} 
```

## Get a specific User
**GET** `/users/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED USER OBJECT>
} 
```

## Delete User
**DELETE** `/users/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED USER OBJECT>
} 
```

## Get User's Workspaces
**GET** `/users/{id}/workspaces/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED WORKSPACE OBJECT>
} 
```

## Get User's followed Threads
* Will get the Messages the user either sent or replied in a thread
**GET** `/users/{id}/threads/`
##### Response
``` yaml
{
    "success": true,
    "data": [
        {
            "id": 1,
            "sender_id": 1,
            "content": "Hello World",
            "timestamp": "2020-12-30 21:43:40.149970",
            "updated": true
        },
        {
            "id": 2,
            "sender_id": 1,
            "content": "Feel your soul :)",
            "timestamp": "2020-12-30 22:26:20.237300",
            "updated": true
        },
        ... 
    ]
}
```


# Workspace
## Create a Workspace
**POST** `/workspaces/`
##### Request
``` yaml
{
    "name": "Computer Science Mentors",
    "url": "/csm"
}
```

##### Response
``` yaml

    "success": true,
    "data": {
        "id": 1,
        "name": "Computer Science Mentors",
        "url": "/csm",
        "users": [],
        "channels": []
    }
}
```
* *users* and *channels* are empty when initially creating a workspace

## Get a Workspace
**GET** `"/workspaces/{id}/"`
##### Response
``` yaml
    "success": true,
    "data": {
        "id": 1,
        "name": "Computer Science Mentors",
        "url": "/csm",
        "users": [
            {
                "id": 1,
                "name": "Jack Wang",
                "username": "jack.wang"
            },
            ...
        ],
        "channels": [
            {
                "id": 1,
                "name": "announcements",
            },
            {
                "id": 2,
                "name": "general",
            }
            ...
        ]
    }
}
```
* Data: serialized workspace object

## Add a User to a Workspace
**POST** `/workspaces/{id}/add-user/`
##### Request
``` yaml
{
    "user_id": 1
}
```
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED WORKSPACE OBJECT>
}
```

## Delete a Workspace
**DELETE** `/workspaces/{id}/`
##### Response
``` yaml
    "success": true,
    "data": <SERIALIZED WORKSPACE OBJECT>
}
```
* this will also delete all the channels in the workspace

## Get Channels of a Workspace
**GET** `/workspaces/{id}/channels/`
```yaml
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "announcements",
            "description": "important stuff",
            "workspace": {
                "id": 1,
                "name": "HKN",
                "url": "/hkn"
            },
            "users": [
                {
                    "id": 1,
                    "name": "Jack Wang",
                    "username": "jackwang"
                },
                ...
            ],
            "messages": [
                {
                    "id": 1,
                    "sender_id": 1,
                    "content": "First Message",
                    "timestamp": "2020-12-31 11:12:56.927812",
                    "updated": false
                },
                ...
            ]
        },
        {
            "id": 5,
            "name": "general",
            "description": "chats",
            "workspace": {
                "id": 1,
                "name": "HKN",
                "url": "/hkn"
            },
            "users": [
                {
                    "id": 1,
                    "name": "Jack Wang",
                    "username": "jackwang"
                },
                ...
            ],
            "messages": []
        },
        ...
    ]
}
```

# Channel
## Create a Channel
**POST** `/workspaces/{id}/channels/`
##### Request
```yaml
{
    "name": "announcements",
    "description": "important messages",
    "public": true or false
}
```
* setting **public** to `true` will add automatically add all members to the channel

##### Response
```yaml
{
    "success": true,
    "data": {
        "id": 1,
        "name": "announcements",
        "description": "important messages",
        "workspace": {
            "id": 1,
            "name": "Computer Science Mentors",
            "url": "/csm"
        },
        "users": [
            {
                "id": 1,
                "name": "Jack Wang",
                "username": "jack.wang"
            },
            ...
        ],
        "messages": []
    }
}
```
* **messages** will be empty when initializing a channel

## Get a Channel
**GET** `/channels/{id}/`
##### Response
```yaml
{
    "success": true,
    "data": <SERIALIZED CHANNEL OBJECT>
}
```

## Delete a Channel
**DELETE** `/channels/{id}/`
##### Response
``` yaml
    "success": true,
    "data": <SERIALIZED CHANNEL OBJECT>
}
```
* this will also delete all the messages in the channel

## Add a User to a Channel
**POST** `/channels/{id}/users/`
##### Request
```yaml
{
    "user_id": 1
}
```

##### Response
```yaml
{
    "success": true,
    "data": <SERIALIZED CHANNEL OBJECT>
}
```

## Remove a User from a Channel
**DELETE** `/channels/{id}/users/{id}/`
##### Response
```yaml
{
    "success": true,
    "data": <SERIALIZED CHANNEL OBJECT>
}
```

## Get Messages of a Channel
**GET** `/channels/{id}/messages/`
##### Response
```yaml
{
    "success": true,
    "data": [
        {
            "id": 1,
            "sender_id": 1,
            "content": "Hello World",
            "timestamp": "2020-12-31 11:12:56.927812",
            "updated": false
        },
        {
            "id": 3,
            "sender_id": 2,
            "content": "Stay Brilliant",
            "timestamp": "2020-12-31 11:12:56.927812",
            "updated": true
        },
        ...
    ]
}
```

# Threads
## Create a Message in a Channel
**POST** `/channels/{id}/messages/`
##### Request
```yaml
{
    "user_id": 1,
    "content": "Hello World"
}
```
##### Response
```yaml
{
    "success": true,
    "data": {
        "id": 2,
        "sender_id": 1,
        "content": "Hello World",
        "timestamp": "2020-12-31 12:53:04.062271",
        "channel": {
            "id": 1,
            "name": "announcements",
            "description": "important messages"
        },
        "threads": [],
        "users_following": [
            {
                "id": 1,
                "name": "Jack Wang",
                "username": "jackwang"
            }
        ],
        "updated": false
    }
}
```
* **users_following** will be users who either created the message or replied in a thread
* **threads** will be empty when intially creating a message

## Get A Message
**GET** `/messages/{id}/`
##### Response
```yaml
{
    "success": true,
    "data": <SERIALIZED MESSAGE OBJECT>
} 
```

## Update A Message
**POST** `/messages/{id}/`
##### Request
```yaml
{
    "user_id": 1,
    "content": "Hello World"
}
```
##### Response
```yaml
{
    "success": true,
    "data": <SERIALIZED MESSAGE OBJECT>
} 
```

## Delete a Message
**DELETE** `/messages/{id}/`
##### Response
``` yaml
    "success": true,
    "data": <SERIALIZED MESSAGE OBJECT>
}
```
* this will also delete the messages threads

## Get Users following a Message (and it's thread)
**GET** `/messages/{id}/users/`
##### Response
``` yaml
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Jack Wang",
            "username": "jack.wang"
        },
        {
            "id": 8,
            "name": "Cesar",
            "username": "cesar.pz"
        },
        ...
    ]
} 
```

## Get the threads (replies) of a Message
**GET** `/messages/{id}/threads/`
##### Request
```yaml
{
    "success": true,
    "data": [
        {
            "id": 1,
            "sender_id": 3,
            "content": "i like them :)",
            "timestamp": "2020-12-31 11:13:21.463828",
            "updated": false
        },
        {
            "id": 3,
            "sender_id": 8,
            "content": "i like threads too!",
            "timestamp": "2020-12-31 11:15:51.463828",
            "updated": false
        },
        ...
    ]
}
```

## Create a Thread
**POST** `/messages/<int:msg_id>/threads/`
##### Request
```yaml
{
    "user_id": 2,
    "content": "test thread"
}
```
##### Response
```yaml
{
    "success": true,
    "data": {
        "id": 3,
        "sender_id": 2,
        "content": "hiiiii",
        "timestamp": "2020-12-31 12:53:37.331404",
        "message": {
            "id": 1,
            "sender_id": 1,
            "content": "Hello World",
            "timestamp": "2020-12-31 12:53:04.062271",
            "updated": false
        },
        "updated": false
    }
}
```

## Get a Thread Response
**GET** `/threads/{id}/`
``` yaml
{
    "success": true,
    "data": <SERIALIZED THREAD OBJECT>
}
```

## Update a Thread Response
**UPDATE** `/threads/{id}/`
``` yaml
{
    "success": true,
    "data": <SERIALIZED THREAD OBJECT>
}
```

## Delete a Thread Response
**DELETE** `/threads/{id}/`
``` yaml
{
    "success": true,
    "data": <SERIALIZED THREAD OBJECT>
}
```