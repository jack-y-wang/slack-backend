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
        "workspaces": []
    }
} 
```

## Get a specific User
**GET** `/users/{id}/`
##### Response
```yaml
{
    "success": true,
    "data": {
        "id": 1,
        "name": "Jack Wang",
        "email": "jw123@gmail.com",
        "username": "jack.wang",
        "workspaces": [
            {
                "id": 1,
                "name": "HKN",
                "url": "/hkn"
            },
            {
                "id": 1,
                "name": "Computer Science Mentors",
                "url": "/csm"
            },
            ...
        ]
    }
}
```
* data: serialized user object

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
    "data": [<SERIALIZED WORKSPACE OBJECT>, ...]
} 
```

## Get User's Channels of a Workspace
**GET** `/users/{id}/workspaces/{id}/channels/`
```yaml
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "announcements",
            "description": "important messages"
        },
        {
            "id": 3,
            "name": "general",
            "description": "for chats"
        },
        ...
    ]
}
```

## Get User's DMs of a Workspace
**GET** `/users/{id}/workspaces/{id}/dms/`
```yaml

    "success": true,
    "data": [
        {
            "id": 1,
            "worskpace": {
                "id": 1,
                "name": "HKN",
                "url": "/hkn"
            },
            "users": [
                {
                    "id": 1,
                    "name": "Jack Wang",
                    "username": "jack.wang"
                },
                {
                    "id": 3,
                    "name": "Anthony P",
                    "username": "a.p"
                }
            ],
            "messages": [
                {
                    "id": 1,
                    "sender": {
                        "id": 1,
                        "name": "Jack Wang",
                        "username": "jack.wang"
                    },
                    "content": "anime is p cool",
                    "timestamep": "2021-01-01 20:18:49.061647"
                },
                {
                    "id": 2,
                    "sender": {
                        "id": 3,
                        "name": "Anthony P",
                        "username": "a.p"
                    },
                    "content": "yaaaa anime is p cool",
                    "timestamep": "2021-01-01 20:39:27.176679"
                }
            ]
        },
        ...
    ]
}
``

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
            {
                "id": 3,
                "name": "Jerry Song",
                "username": "jerry.s"
            },
            ...
        ],
        "channels": [
            {
                "id": 1,
                "name": "announcements",
                "description": "important messages"
            },
            {
                "id": 2,
                "name": "general",
                "description": "chatting"
            }
            ...
        ]
    }
}
```
* data: serialized workspace object

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
* **User** is automatically added to all public channels in the Workspace

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
* data: serialized channel object
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
* data: serialized message object
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
##### Response
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
    "content": "hiiiii"
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
* data: serialized thread object

## Get a Thread Response
**GET** `/threads/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED THREAD OBJECT>
}
```

## Update a Thread Response
**POST** `/threads/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED THREAD OBJECT>
}
```

## Delete a Thread Response
**DELETE** `/threads/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED THREAD OBJECT>
}
```

# DMs

## Create a DM group
**POST** `/workspaces/{id}/dms/' 
##### Request
``` yaml
{
    "users": [
        {
            "user_id": <USER ID>
        },
        ...
    ]
}
```
##### Responase
```yaml
{
    "success": true,
    "data": {
        "id": 3,
        "worskpace": {
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
            {
                "id": 8,
                "name": "Cesar",
                "username": "cesar.pz"
            },
            ...
        ],
        "messages": []
    }
}
```
* **messages** is empty when creating a DM group

## Get a DM group
**GET** `/dms/{id]/`
##### Response
```yaml
{
    "success": true,
    "data": {
        "id": 3,
        "worskpace": {
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
            {
                "id": 8,
                "name": "Cesar",
                "username": "cesar.pz"
            },
            ...
        ],
        "messages": [
            {
                "id": 1,
                "sender_id": 3,
                "content": "Whats up all",
                "timestamp": "2020-12-31 11:13:21.463828",
                "updated": false
            },
            {
                "id": 3,
                "sender_id": 8,
                "content": "hey :wave:",
                "timestamp": "2020-12-31 11:15:51.463828",
                "updated": false
            },
            ...
        ]
    }
}
```
* data: serialized DM group object

## Delete a DM group
**DELETE** `/dms/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED DM GROUP OBJECT>
}
```

## Get users of a DM group
**GET** `/dms/{id}/users/`
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

## Get messages of a DM group
**GET** `/dms/{id}/messages/`
##### Response
```yaml
{
    "success": true,
    "data": [
        {
            "id": 1,
            "sender_id": 3,
            "content": "Whats up all",
            "timestamp": "2020-12-31 11:13:21.463828",
            "updated": false
        },
        {
            "id": 3,
            "sender_id": 8,
            "content": "hey :wave:",
            "timestamp": "2020-12-31 11:15:51.463828",
            "updated": false
        },
        ...
    ]
}
```

## Create a DM message
**POST** `/dms/{id}/messages/`
##### Request
```yaml
{
    "user_id": 1,
    "content": "anime is p cool"
}
```
##### Response
```yaml
{
    "success": true,
    "data": {
        "id": 8,
        "sender": {
            "id": 1,
            "name": "Jack Wang",
            "username": "jack.wang"
        },
        "content": "anime is p cool",
        "timestamp": "2021-01-01 15:42:21.658703",
        "updated": false,
        "dm_group": {
            "id": 3,
            "worskpace": {
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
                {
                    "id": 8,
                    "name": "Cesar",
                    "username": "cesar.pz"
                },
                ...
            ]
        } 
    }
}
```
* data: serialized DM message

## Get a DM message
**GET** '/dm-messages/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED DM MESSAGE OBJECT>
}
```

## Update a DM message
**POST** '/dm-messages/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED DM MESSAGE OBJECT>
}
```

## Delete a DM message
**DELETE** '/dm-messages/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED DM MESSAGE OBJECT>
}
```