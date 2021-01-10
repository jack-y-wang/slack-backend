from . import *

def create_image(**kwargs):
    image_data = kwargs.get("image_data")
    source = kwargs.get("source")
    source_id = kwargs.get("source_id")
    channel_id = kwargs.get("channel_id")
    workspace_id = kwargs.get("workspace_id")
    sender_id = kwargs.get("sender_id")

    if image_data is None:
        return None, "No base64 URL is found"
    
    image = MessageImage(
        image_data=image_data, 
        sender_id=sender_id, 
        source=source, 
        source_id=source_id,
        channel_id=channel_id,
        workspace_id=workspace_id
    )
    db.session.add(image)
    return image

def get_image_by_id(image_id):
    image = Asset.query.filter_by(id=image_id).first()
    if not image:
        raise Exception("Image not found")
    return image

def delete_image_by_id(image_id):
    optional_image = get_image_by_id(image_id)

    try:
        optional_image.delete()
    except Exception as e:
        raise Exception(f"Unable to delete image due to {e}")

    db.session.delete(optional_image)

    # if image is from a message/thread remove from them
    try:
        if optional_image.source == "message":
            message = Message.query.filter_by(id=optional_image.source_id).first()
            message.image_id = None
        else:
            thread = Thread.query.filter_by(id=optional_image.source_id).first()
            thread.image_id = None
    except Exception as e:
        pass
    
    db.session.commit()
    return optional_image
