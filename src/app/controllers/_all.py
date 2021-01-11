from app.controllers.hello_world_controller import HelloWorldController

# USER CONTROLLERS
from app.controllers.user_controllers.register_user_controller import *
from app.controllers.user_controllers.login_user_controller import *
from app.controllers.user_controllers.update_profile_image_controller import *
from app.controllers.user_controllers.get_current_user_controller import *
from app.controllers.user_controllers.get_followed_threads_of_user import *
from app.controllers.user_controllers.get_user_controller import *
from app.controllers.user_controllers.get_users_images import *
from app.controllers.user_controllers.delete_user_controller import *
from app.controllers.user_controllers.get_workspace_channels_of_user_controller import *
from app.controllers.user_controllers.get_workspace_dms_of_user import *
from app.controllers.user_controllers.get_workspaces_of_user_controller import *

# WORKPSACE CONTROLLERS
from app.controllers.workspace_controllers.create_workspace_controller import *
from app.controllers.workspace_controllers.join_workspace_controller import *
from app.controllers.workspace_controllers.leave_workspace_controller import *
from app.controllers.workspace_controllers.get_all_workspaces_controller import *
from app.controllers.workspace_controllers.get_workspace_controller import *
from app.controllers.workspace_controllers.get_channels_of_workspace_controller import *
from app.controllers.workspace_controllers.get_images_of_workspace_controller import *
from app.controllers.workspace_controllers.delete_workspace_controller import *

# CHANNEL CONTROLLERS
from app.controllers.channel_controllers.get_channel_controller import *
from app.controllers.channel_controllers.create_channel_controller import *
from app.controllers.channel_controllers.join_channel_controller import *
from app.controllers.channel_controllers.add_user_to_channel_controller import *
from app.controllers.channel_controllers.leave_channel_controller import *
from app.controllers.channel_controllers.get_messages_of_channel_controller import *
from app.controllers.channel_controllers.get_images_of_channel_controller import *
from app.controllers.channel_controllers.remove_channel_controller import *

# MESSAGE CONTROLLERS
from app.controllers.message_controllers.create_message_controller import *
from app.controllers.message_controllers.get_message_controller import *
from app.controllers.message_controllers.update_message_controller import *
from app.controllers.message_controllers.get_users_following_message_controller import *
from app.controllers.message_controllers.delete_message_controller import *
from app.controllers.message_controllers.get_threads_of_message_controller import *

# THREAD CONTROLLERS
from app.controllers.message_controllers.create_thread_controller import *
from app.controllers.message_controllers.get_thread_controller import *
from app.controllers.message_controllers.update_thread_controller import *
from app.controllers.message_controllers.remove_thread_controller import *

# DM CONTROLLERS
from app.controllers.dm_controllers.create_dm_group_controller import *
from app.controllers.dm_controllers.get_dm_group_controller import *
from app.controllers.dm_controllers.get_messages_of_dm_group_controller import *
from app.controllers.dm_controllers.get_users_of_dm_group_controller import *
from app.controllers.dm_controllers.delete_dm_group_controller import *
from app.controllers.dm_controllers.create_dm_message_controller import *
from app.controllers.dm_controllers.get_dm_message_controller import *
from app.controllers.dm_controllers.update_dm_message_controller import *
from app.controllers.dm_controllers.delete_dm_message_controller import *

# IMAGE CONTROLLERS
from app.controllers.image_controllers.get_image_controller import *
from app.controllers.image_controllers.delete_image_controller import *

controllers = [
    HelloWorldController(),

    RegisterUserController(),
    LoginUserController(),
    GetUserController(),
    GetCurrentUserController(),
    UpdateProfilePicController(),
    GetUsersFollowedThreadsController(),
    GetWorkspacesOfUserController(),
    GetUserImagesController(),
    GetUserChannelsController(),
    GetUserDMsController(),
    DeleteUserController(),

    CreateWorkspaceController(),
    JoinWorkspaceController(),
    LeaveWorkspaceController(),
    GetAllWorkspaceController(),
    GetWorkspaceController(),
    GetChannelsOfWorkspaceController(),
    GetImagesOfWorkspaceController(),
    DeleteWorkspaceController(),

    GetChannelController(),
    CreateChannelController(),
    JoinChannelController(),
    AddUserToChannelController(),
    LeaveChannelController(),
    GetMessagesOfChannelController(),
    GetImagesOfChannelController(),
    RemoveChannelController(),

    CreateMessageController(),
    GetMessageController(),
    UpdateMessageController(),
    GetUsersFollowingMessageController(),
    DeleteMessageController(),
    GetThreadsOfMessageController(),

    CreateThreadController(),
    GetThreadController(),
    UpdateThreadController(),
    RemoveThreadController(),

    CreateDMGroupController(),
    GetDMGroupController(),
    GetMessagesOfDMGroupController(),
    GetUsersOfDMGroup(),
    DeleteDmGroupController(),
    CreateDmMessageController(),
    GetDmMessageController(),
    UpdateDmMessageController(),
    DeleteDmMessageController(),

    GetImageController(),
    DeleteImageController()
]
