# API Reference

This API is modeled after Slack, which is a communication platform for organizations. This application implements Workspapces, Users, Channels, Threads, Direct Messaging, and Images.

- **Workspaces**: A workspace is where on organization and its members be organized on and is made up of channels.
- **Channels**: Channels are where team members can communicate collective and work together. Team members can communicate on a channel by posting a message and having a discussion via a Thread. Messages in a channel can also have an image attatched to it which is uploaded to an AWS S3 bucket.
- **Direct Messaging**: DMs are a way to have a conversation outside of a channel in a workspace in a 1-on-1 scenario or as a group.

- Users
    - [Register](#register)
    - [Login](#login)
    - [Get information of current user](#get-information-of-current-user)
    -[Update current user](#update-current-user)
    - [Delete current user](#delete-current-user)
    - [Get workspaces of current user](#get-workspaces-of-current-user)
    - [Get channels in a workspace of current user](#get-channels-in-a-workspace-of-current-user)
    - [Get DMS in a workspace of current user](#get-dms-in-a-workspace-of-current-user)
    - [Get following threads of current user](#get-following-threads-of-current-user)
    - [Get posted images of current user](#get-posted-images-of-current-user)]
- Workspace
    - [Create a Workspace](#create-a-workspace)
    - [Get a Workspace](#get-a-workspace)
    - [Join a Workspace](#join-a-workspace)
    - [Delete a Workspace](#delete-a-workspace)
    - [Get Channels of a Workspace](#get-channels-of-a-workspace)
    - [Get Images of a Workspace](#get-images-of-a-workspace)
- Channel
    - [Create a Channel](#create-a-channel)
    - [Get a Channel](#get-a-channel)
    - [Delete a Channel](#delete-a-channel)
    - [current user adds a user to a channel](#add-a-user-to-a-channel)
    - [Current user joins a channel](#current-user-joins-a-channel)
    - [Current user leaves a channel](#current-user-leaves-a-channel)
    - [Get Messages of a Channel](#get-messages-of-a-channel)
    - [Get Images of a Channel](#get-images-of-a-channel)
- Messages / Threads
    - [Create a Message in a Channe](#create-a-message-in-a-channel)
    - [Get a Message](#get-a-message)
    - [Update a Message](#update-a-message)
    - [Delete a Message](#delete-a-message)
    - [Get Users following a Message](#get-Users-following-a-message-(and-it's-thread))
    - [Create a Thread](#create-a-thread)
    - [Get a Thread Response](#get-a-thread-response)
    - [Update a Thread Response](#update-a-thread-response)
    - [Delete a Thread Response](#delete-a-thread-response)
- Direct Messages
    - [Create a DM group](#create-a-dm-group)
    - [Get a DM group](#get-a-dm-group)
    - [Delete a DM group](#delete-a-dm-group)
    - [Get users of a DM group](#get-users-of-a-dm-group)
    - [Get messages of a DM group](#get-messages-of-a-dm-group)
    - [Create a DM message](#create-a-dm-message)
    - [Get a DM message](#get-a-dm-message)
    - [Update a DM message](#update-a-dm-message)
    - [Delete a DM message](#delete-a-dm-message)
- Images
    - [Get Image](#get-image-by-id)
    - [Delete Image](#delete-image-by-id)

# Users
- Endpoints: [Register](#register) | [Login](#login) | [Get information of current user](#get-information-of-current-user) | [Update current user](#update-current-user) | [Delete current user](#delete-current-user) | [Get workspaces of current user](#get-workspaces-of-current-user) | [Get channels in a workspace of current user](#get-channels-in-a-workspace-of-current-user) | [Get DMS in a workspace of current user](#get-dms-in-a-workspace-of-current-user) | [Get following threads of current user](#get-following-threads-of-current-user) | [Get posted images of current user](#get-posted-images-of-current-user)]
- Other categories: [Workspace](#workspace) | [Channel](#channel) | [Threads](#threads) | [DMs](#dms) | [Images](#images)

## Register
**POST** ``/api/register/`
##### Request
``` yaml
{
    "name": "Jack Wang",
    "email": "jw123@gmail.com",
    "username": "jack.wang",
    "password": "123456789"
    "image: <OPTIONAL BASE64 IMAGE>
}
```
##### Response
``` yaml
{
    "data": {
        "session_expiration": 1610326829,
        "session_token": "t31830f87f1b6469d13b3a918646aafd68795b19",
        "update_token": "l1454c11f7a9271afd0461104aaf42545be6fa3d"
    },
    "success": true,
    "timestamp": 1610310429
}
```


## Login
**POST** ``/api/login/`
##### Request
``` yaml
{
    "email": "jw123@gmail.com",
    "password": "123456789"
}
```
##### Response
``` yaml
{
    "data": {
        "session_expiration": 1610326829,
        "session_token": "t31830f87f1b6469d13b3a918646aafd68795b19",
        "update_token": "l1454c11f7a9271afd0461104aaf42545be6fa3d"
    },
    "success": true,
    "timestamp": 1610310429
}
```


## Get information of current user
**GET** `/api/user/`
##### Response
```yaml
{
    "success": true,
    "data": {
        "id": 1,
        "name": "Jack Wang",
        "email": "jw123@gmail.com",
        "username": "jack.wang",
        "profile_img": null or {
            "id": 5,
            "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
            "created_at": "2021-01-04 22:03:56.388387",
            "width": 88,
            "height": 62
        }
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
    },
    "timestamp": 1610310429
}
```
* **data: serialized user object**


## Update current user
**POST** ``/api/login/`
##### Request
``` yaml
{
    "image": <OPTIONAL BASE64 IMAGE>
}
```
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED USER OBJECT>,
    "timestamp": 1610310429
} 
```

## Delete current user
**DELETE** `/api/user/update-profile/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED USER OBJECT>,
    "timestamp": 1610310429
} 
```

## Get workspaces of current user
**GET** `/api/user/workspaces/`
##### Response
``` yaml
{
    "success": true,
    "data": [<SERIALIZED WORKSPACE OBJECT>, ...],
    "timestamp": 1610310429
} 
```

## Get channels in a workspace of current user
**GET** `/api/user/workspaces/{id}/channels/`
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
    ],
    "timestamp": 1610310429
}
```

## Get DMs in a workspace of current user
**GET** `/api/user/workspaces/{id}/dms/`
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
                    "username": "jack.wang",
                    "profile_img": {
                        "id": 5,
                        "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
                        "created_at": "2021-01-04 22:03:56.388387",
                        "width": 88,
                        "height": 62
                    }
                },
                {
                    "id": 3,
                    "name": "Anthony P",
                    "username": "a.p",
                    "profile_imag": null
                },
                ...
            ],
            "messages": [
                {
                    "id": 1,
                    "sender": {
                        "id": 1,
                        "name": "Jack Wang",
                        "username": "jack.wang",
                        "profile_img": {
                            "id": 5,
                            "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
                            "created_at": "2021-01-04 22:03:56.388387",
                            "width": 88,
                            "height": 62
                        }
                    },
                    "content": "anime is p cool",
                    "image": {
                        "id": 5,
                        "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/WES9CVS7EDYZVTWO.png",
                        "sender_id": 1,
                        "created_at": "2021-01-02 15:00:10.860038",
                        "width": 88,
                        "height": 62
                    },
                    "timestamep": "2021-01-01 20:18:49.061647"
                },
                {
                    "id": 2,
                    "sender": {
                        "id": 3,
                        "name": "Anthony P",
                        "username": "a.p",
                        "profile_imag": null
                    },
                    "content": "yaaaa anime is p cool",
                    "timestamep": "2021-01-01 20:39:27.176679"
                }
            ]
        },
        ...
    ],
    "timestamp": 1610310429
}
```

## Get following threads of current user
* Will get the Messages the user either sent or replied in a thread
**GET** `/api/user/threads/`
##### Response
``` yaml
{
    "success": true,
    "data": [
        {
            "id": 1,
            "sender_id": 1,
            "content": "Hello World",
            "image": {
                "id": 5,
                "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/WES9CVS7EDYZVTWO.png",
                "sender_id": 1,
                "created_at": "2020-12-30 22:26:20.237300",
                "width": 88,
                "height": 62
            },
            "timestamp": "2020-12-30 21:43:40.149970",
            "updated": true
        },
        {
            "id": 2,
            "sender_id": 1,
            "content": "Feel your soul :)",
            "image": {
                "id": 5,
                "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/WES9CVS7EDYZVTWO.png",
                "sender_id": 1,
                "created_at": "2020-12-30 22:26:20.237300",
                "width": 88,
                "height": 62
            },
            "timestamp": "2020-12-30 22:26:20.237300",
            "updated": true
        },
        ... 
    ],
    "timestamp": 1610310429
}
```

## Get posted images of current user
**GET** `/api/user/images/`
##### Response
``` yaml
{
    "success": true,
    "data": [
        {
            "id": 2,
            "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/NQWTOFOVZZXULCF1.png",
            "sender_id": 1,
            "created_at": "2021-01-02 14:42:15.250883",
            "width": 88,
            "height": 62,
            "source": "message",
            "source_id": "2"
        },
        {
            "id": 3,
            "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/BLIBSBSIGPYT3IU0.png",
            "sender_id": 1,
            "created_at": "2021-01-02 14:43:41.689285",
            "width": 88,
            "height": 62,
            "source": "message",
            "source_id": "3"
        },
        ...
    ],
    "timestamp": 1610310429
}
```

# Workspace
- Endpoints: [Create a Workspace](#create-a-workspace) | [Get a Workspace](#get-a-workspace) | [Join a Workspace](#join-a-workspace) | [Delete a Workspace](#delete-a-workspace) | [Get Channels of a Workspace](#get-channels-of-a-workspace) | [Get Images of a Workspace](#get-images-of-a-workspace)
- Other Categories: [User](#user) | [Channel](#channel) | [Threads](#threads) | [DMs](#dms) | [Images](#images)

## Create a Workspace
**POST** `/api/workspaces/`
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
    },
    "timestamp": 1610310429
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
                "username": "jack.wang",
                "profile_img": {
                    "id": 5,
                    "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
                    "created_at": "2021-01-04 22:03:56.388387",
                    "width": 88,
                    "height": 62
                }
            },
            {
                "id": 3,
                "name": "Jerry Song",
                "username": "jerry.s",
                "profile_img": null
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
    },
    "timestamp": 1610310429
}
```
* **data: serialized workspace object**

## Join a workspace
current user joins workspace

**POST** `/api/workspaces/{id}/join/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED WORKSPACE OBJECT>,
    "timestamp": 1610310429
}
```
* **User** is automatically added to all public channels in the Workspace

## Delete a Workspace
**DELETE** `/api/workspaces/{id}/`
##### Response
``` yaml
    "success": true,
    "data": <SERIALIZED WORKSPACE OBJECT>,
    "timestamp": 1610310429
}
```
* this will also delete all the channels in the workspace

## Get Channels of a Workspace
**GET** `/api/workspaces/{id}/channels/`
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
                    "username": "jackwang",
                    "profile_img": {
                        "id": 5,
                        "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
                        "created_at": "2021-01-04 22:03:56.388387",
                        "width": 88,
                        "height": 62
                    }
                },
                ...
            ],
            "messages": [
                {
                    "id": 1,
                    "sender_id": 1,
                    "content": "First Message",
                    "image": {
                        "id": 5,
                        "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/WES9CVS7EDYZVTWO.png",
                        "sender_id": 1,
                        "created_at": "2020-12-30 22:26:20.237300",
                        "width": 88,
                        "height": 62
                    },
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
                    "username": "jackwang",
                    "profile_img": {
                        "id": 5,
                        "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
                        "created_at": "2021-01-04 22:03:56.388387",
                        "width": 88,
                        "height": 62
                    }
                },
                ...
            ],
            "messages": []
        },
        ...
    ],
    "timestamp": 1610310429
}
```

## Get Images of a Workspace
**GET** `/api/workspaces/{id}/images/`
``` yaml
{
    "success": true,
    "data": [
        {
            "id": 2,
            "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/NQWTOFOVZZXULCF1.png",
            "sender_id": 1,
            "created_at": "2021-01-02 14:42:15.250883",
            "width": 88,
            "height": 62,
            "source": "message",
            "source_id": "2"
        },
        {
            "id": 3,
            "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/BLIBSBSIGPYT3IU0.png",
            "sender_id": 1,
            "created_at": "2021-01-02 14:43:41.689285",
            "width": 88,
            "height": 62,
            "source": "message",
            "source_id": "3"
        },
        ...
    ],
    "timestamp": 1610310429
}
```

# Channel
- Endpoints: [Create a Channel](#create-a-channel) | [Get a Channel](#get-a-channel) | [Delete a Channel](#delete-a-channel)
 | [current user adds a user to a channel](#add-a-user-to-a-channel) | [Current user joins a channel](#current-user-joins-a-channel) | [Current user leaves a channel](#current-user-leaves-a-channel) | [Get Messages of a Channel](#get-messages-of-a-channel) | [Get Images of a Channel](#get-images-of-a-channel)
 - Other Categories: [User](#user) | [Workspace](#workspace) | [Threads](#threads) | [DMs](#dms) | [Images](#images)

## Create a Channel
**POST** `/api/workspaces/{id}/channels/`
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
                "username": "jack.wang",
                "profile_img": {
                    "id": 5,
                    "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
                    "created_at": "2021-01-04 22:03:56.388387",
                    "width": 88,
                    "height": 62
                }
            },
            ...
        ],
        "messages": []
    },
    "timestamp": 1610310429
}
```
* data: serialized channel object
* **messages** will be empty when initializing a channel

## Get a Channel
**GET** `/api/channels/{id}/`
##### Response
```yaml
{
    "success": true,
    "data": <SERIALIZED CHANNEL OBJECT>,
    "timestamp": 1610310429
}
```

## Delete a Channel
**DELETE** `/api/channels/{id}/`
##### Response
``` yaml
    "success": true,
    "data": <SERIALIZED CHANNEL OBJECT>,
    "timestamp": 1610310429
}
```
* this will also delete all the messages in the channel

## Current user adds a user to a channel
current user must already be in the channel to add another user

**POST** `/api/channels/{id}/users/`
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
    "data": <SERIALIZED CHANNEL OBJECT>,
    "timestamp": 1610310429
}
```

## Current user joins a channel
channel must be public for current user to join

**POST** `/api/channels/{id}/join/`

##### Response
```yaml
{
    "success": true,
    "data": <SERIALIZED CHANNEL OBJECT>,
    "timestamp": 1610310429
}
```

## Current user leaves a channel
**POST** `/api/channels/{id}/leave/`
##### Response
```yaml
{
    "success": true,
    "data": <SERIALIZED CHANNEL OBJECT>,
    "timestamp": 1610310429
}
```

## Get Messages of a Channel
**GET** `/api/channels/{id}/messages/`
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
    ],
    "timestamp": 1610310429
}
```

## Get Images of a Channel
**GET** `/api/channels/{id}/images/`
``` yaml
{
    "success": true,
    "data": [
        {
            "id": 2,
            "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/NQWTOFOVZZXULCF1.png",
            "sender_id": 1,
            "created_at": "2021-01-02 14:42:15.250883",
            "width": 88,
            "height": 62,
            "source": "message",
            "source_id": "2"
        },
        {
            "id": 3,
            "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/BLIBSBSIGPYT3IU0.png",
            "sender_id": 1,
            "created_at": "2021-01-02 14:43:41.689285",
            "width": 88,
            "height": 62,
            "source": "thread",
            "source_id": "3"
        },
        ...
    ],
    "timestamp": 1610310429
}
```

# Threads
- Endpoints [Create a Message in a Channe](#create-a-message-in-a-channel) | [Get a Message](#get-a-message) | [Update a Message](#update-a-message) | [Delete a Message](#delete-a-message) | [Get Users following a Message](#get-Users-following-a-message-(and-it's-thread)) | [Create a Thread](#create-a-thread) | [Get a Thread Response](#get-a-thread-response) | [Update a Thread Response](#update-a-thread-response) | [Delete a Thread Response](#delete-a-thread-response)
Other Categories: [User](#user) | [Workspace](#workspace) | [Channel](#channel) | [DMs](#dms) | [Images](#images)

## Create a Message in a Channel
current user creates a message

**POST** `/api/channels/{id}/messages/`
##### Request
```yaml
{
    "content": "Hello World",
    "image": <BASE64 OF IMAGE> - optional
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
        "image": null or {
            "id": 5,
            "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/WES9CVS7EDYZVTWO.png",
            "sender_id": 1,
            "created_at": "2020-12-30 22:26:20.237300",
            "width": 88,
            "height": 62
        },
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
                "username": "jackwang",
                "profile_img": {
                    "id": 5,
                    "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
                    "created_at": "2021-01-04 22:03:56.388387",
                    "width": 88,
                    "height": 62
                }
            },
            ...
        ],
        "updated": false,
    },
    "timestamp": 1610310429
}
```
* **data: serialized message object**
* **users_following** will be users who either created the message or replied in a thread
* **threads** will be empty when intially creating a message

## Get A Message
**GET** `/api/messages/{id}/`
##### Response
```yaml
{
    "success": true,
    "data": <SERIALIZED MESSAGE OBJECT>,
    * Can't update the image of a message after uploading. But the message or the image can be deleted
} 
```

## Update A Message
current user updates a previous message made by them
* Can't update the image of a message after uploading. But the message or the image can be deleted

**POST** `/api/messages/{id}/`
##### Request
```yaml
{
    "content": "Hello World"
}
```

##### Response
```yaml
{
    "success": true,
    "data": <SERIALIZED MESSAGE OBJECT>,
    "timestamp": 1610310429
} 
```

## Delete a Message
current user deletes their message

**DELETE** `/api/messages/{id}/`
##### Response
``` yaml
    "success": true,
    "data": <SERIALIZED MESSAGE OBJECT>,
    "timestamp": 1610310429
}
```
* this will also delete the messages threads

## Get Users following a Message (and it's thread)
**GET** `/api/messages/{id}/users/`
##### Response
``` yaml
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Jack Wang",
            "username": "jack.wang",
            "profile_img": {
                "id": 5,
                "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
                "created_at": "2021-01-04 22:03:56.388387",
                "width": 88,
                "height": 62
            }
        },
        {
            "id": 8,
            "name": "Cesar",
            "username": "cesar.pz",
            "profile_img": null
        },
        ...
    ]
} 
```

## Get the threads (replies) of a Message
**GET** `/api/messages/{id}/threads/`
##### Response
```yaml
{
    "success": true,
    "data": [
        {
            "id": 1,
            "sender_id": 3,
            "content": "i like them :)",
            "image": {
                "id": 5,
                "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/WES9CVS7EDYZVTWO.png",
                "sender_id": 1,
                "created_at": "2020-12-30 22:26:20.237300",
                "width": 88,
                "height": 62
            },
            "timestamp": "2020-12-31 11:13:21.463828",
            "updated": false
        },
        {
            "id": 3,
            "sender_id": 8,
            "content": "i like threads too!",
            "image": null,
            "timestamp": "2020-12-31 11:15:51.463828",
            "updated": false
        },
        ...
    ],
    "timestamp": 1610310429
}
```

## Create a Thread
current user creates a thread reply to a message

**POST** `/api/messages/<int:msg_id>/threads/`
##### Request
```yaml
{
    "content": "hiiiii",
    "image": <BASE64 OF IMAGE> - optional
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
            "image": null or {
                "id": 5,
                "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/WES9CVS7EDYZVTWO.png",
                "sender_id": 1,
                "created_at": "2020-12-30 22:26:20.237300",
                "width": 88,
                "height": 62
            },
            "timestamp": "2020-12-31 12:53:04.062271",
            "updated": false
        },
        "updated": false
    },
    "timestamp": 1610310429
}
```
* **data: serialized thread object**

## Get a Thread Response
**GET** `/api/threads/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED THREAD OBJECT>,
    "timestamp": 1610310429
}
```

## Update a Thread Response
current user updates their thread message
* Can't update the image of a thread after uploading. But the thread or the image can be deleted

**POST** `/api/threads/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED THREAD OBJECT>,
    "timestamp": 1610310429
}
```

## Delete a Thread Response
current user deletes their thread message
**DELETE** `/api/threads/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED THREAD OBJECT>,
    "timestamp": 1610310429
}
```

# DMs
- Endpoints: [Create a DM group](#create-a-dm-group) | [Get a DM group](#get-a-dm-group) | [Delete a DM group](#delete-a-dm-group) | [Get users of a DM group](#get-users-of-a-dm-group) | [Get messages of a DM group](#get-messages-of-a-dm-group) | [Create a DM message](#create-a-dm-message) | [Get a DM message](#get-a-dm-message) | [Update a DM message](#update-a-dm-message) | [Delete a DM message](#delete-a-dm-message)
- Other categories: [User](#user) | [Workspace](#workspace) | [Channel](#channel) | [Threads](#threads) | [Images](#images)

## Create a DM group
current user will automatically be added to dm group

**POST** `/api/workspaces/{id}/dms/' 
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
                "username": "jack.wang",
                "profile_img": {
                    "id": 5,
                    "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
                    "created_at": "2021-01-04 22:03:56.388387",
                    "width": 88,
                    "height": 62
                }
            },
            {
                "id": 8,
                "name": "Cesar",
                "username": "cesar.pz",
                "profile_img": null
            },
            ...
        ],
        "messages": []
    },
    "timestamp": 1610310429
}
```
* **messages** is empty when creating a DM group

## Get a DM group
**GET** `/api/dms/{id]/`
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
                "username": "jack.wang",
                "profile_img": {
                    "id": 5,
                    "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
                    "created_at": "2021-01-04 22:03:56.388387",
                    "width": 88,
                    "height": 62
                }
            },
            {
                "id": 8,
                "name": "Cesar",
                "username": "cesar.pz",
                "profile_img": null
            },
            ...
        ],
        "messages": [
            {
                "id": 1,
                "sender_id": 3,
                "content": "Whats up all",
                "image": {
                    "id": 1,
                    "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/WES9CVS7EDYZVTWO.png",
                    "sender_id": 1,
                    "created_at": "2020-12-30 22:26:20.237300",
                    "width": 88,
                    "height": 62
                },
                "timestamp": "2020-12-31 11:13:21.463828",
                "updated": false
            },
            {
                "id": 3,
                "sender_id": 8,
                "content": "hey :wave:",
                "image": null,
                "timestamp": "2020-12-31 11:15:51.463828",
                "updated": false
            },
            ...
        ]
    },
    "timestamp": 1610310429
}
```
* **data: serialized DM group object**

## Delete a DM group
**DELETE** `/api/dms/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED DM GROUP OBJECT>,
    "timestamp": 1610310429
}
```

## Get users of a DM group
**GET** `/api/dms/{id}/users/`
##### Response
``` yaml
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Jack Wang",
            "username": "jack.wang",
            "profile_img": {
                "id": 5,
                "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
                "created_at": "2021-01-04 22:03:56.388387",
                "width": 88,
                "height": 62
            }
        },
        {
            "id": 8,
            "name": "Cesar",
            "username": "cesar.pz",
            "profile_img": null
        },
        ...
    ],
    "timestamp": 1610310429
} 
```

## Get messages of a DM group
**GET** `/api/dms/{id}/messages/`
##### Response
```yaml
{
    "success": true,
    "data": [
        {
            "id": 1,
            "sender_id": 3,
            "content": "Whats up all",
            "image": {
                "id": 1,
                "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/WES9CVS7EDYZVTWO.png",
                "sender_id": 1,
                "created_at": "2020-12-30 22:26:20.237300",
                "width": 88,
                "height": 62
            },
            "timestamp": "2020-12-31 11:13:21.463828",
            "updated": false
        },
        {
            "id": 3,
            "sender_id": 8,
            "content": "hey :wave:",
            "image": null,
            "timestamp": "2020-12-31 11:15:51.463828",
            "updated": false
        },
        ...
    ],
    "timestamp": 1610310429
}
```

## Create a DM message
current user creates a dm message

**POST** `/api/dms/{id}/messages/`
##### Request
```yaml
{
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
            "username": "jack.wang",
            "profile_img": {
                "id": 5,
                "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/0IOUZDUR6QUWHSNO.png",
                "created_at": "2021-01-04 22:03:56.388387",
                "width": 88,
                "height": 62
            }
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
    },
    "timestamp": 1610310429
}
```
* **data: serialized DM message**

## Get a DM message
**GET** '/dm-messages/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED DM MESSAGE OBJECT>,
    "timestamp": 1610310429
}
```

## Update a DM message
**POST** '/dm-messages/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED DM MESSAGE OBJECT>,
    "timestamp": 1610310429
}
```

## Delete a DM message
**DELETE** '/dm-messages/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": <SERIALIZED DM MESSAGE OBJECT>,
    "timestamp": 1610310429
}
```

# Images
Images are created with a message or a thread reply - An image cannot be made alone
- Other categories: [User](#user) | [Workspace](#workspace) | [Channel](#channel) | [Threads](#threads) | [DMs](#dms)

## Get Image by ID
**GET** `/api/images/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": {
        "id": 5,
        "url": "https://slack-backend-images.s3-us-west-1.amazonaws.com/WES9CVS7EDYZVTWO.png",
        "sender_id": 1,
        "created_at": "2021-01-02 15:00:10.860038",
        "width": 88,
        "height": 62,
        "source": "message",
        "source_id": 5
    }
}
```
* data: serialialized image object
* source: message or thread

## Delete Image by ID
**DELETE** `/api/images/{id}/`
##### Response
``` yaml
{
    "success": true,
    "data": {<SERIALIZED IMAGE OBJECT>}
}
```
