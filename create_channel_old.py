from telethon.tl.functions.channels import CreateChannelRequest, CheckUsernameRequest, UpdateUsernameRequest
from telethon.tl.types import InputChannel, InputPeerChannel
createdPrivateChannel = client(CreateChannelRequest("title","about",megagroup=False))

#if you want to make it public use the rest
newChannelID = createdPrivateChannel.__dict__["chats"][0].__dict__["id"]
newChannelAccessHash = createdPrivateChannel.__dict__["chats"][0].__dict__["access_hash"]
desiredPublicUsername = "myUsernameForPublicChannel"
checkUsernameResult = client(CheckUsernameRequest(InputPeerChannel(channel_id=newChannelID, access_hash=newChannelAccessHash), desiredPublicUsername))
if(checkUsernameResult==True):
    publicChannel = client(UpdateUsernameRequest(InputPeerChannel(channel_id=newChannelID, access_hash=newChannelAccessHash), desiredPublicUsername))