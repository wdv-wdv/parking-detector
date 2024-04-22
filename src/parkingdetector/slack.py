import os
import cv2
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import Config

class Slack(object):
    _client = None
    _slackConfig = Config().GetSlack()

    def __init__(cls):
        cls._client = WebClient(token=cls._slackConfig["token"])

    def sendMsg(self, msg, img):
        print("Send message")
        channel_id = self._getChannelID()
        print(channel_id)

        if(channel_id == None):
            print("channel not found")
            return 
        
        if(img is None):
            print("Send text msg")
            try:
                response = self._client.chat_postMessage(
                    channel=channel_id,
                    text=msg
                )

                assert response["ok"] is True
            except SlackApiError as e:
                print(f"Error: {e}")

        else:
            print("Send img")
            try:
                image_bytes = cv2.imencode('.jpg', img)[1].tobytes()

                response = self._client.files_upload_v2(
                    channel=channel_id,
                    file=image_bytes,
                    filename="parking-report.jpg",
                    #filetype="jpg",
                    initial_comment=msg
                )

                assert response["file"]  # the uploaded file
            except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                assert e.response["ok"] is False
                assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
                print(f"Got an error: {e.response['error']}")


    def _getChannelID(self):
        channel_name = self._slackConfig["channel_name"]
        conversation_id = None
        try:
            # Call the conversations.list method using the WebClient
            for result in self._client.conversations_list(types="public_channel, private_channel, mpim, im"):
                if conversation_id is not None:
                    break
                for channel in result["channels"]:
                    if channel["name"] == channel_name:
                        conversation_id = channel["id"]
                        break

        except SlackApiError as e:
            print(f"Error: {e}")

        return conversation_id