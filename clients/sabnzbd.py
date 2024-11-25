import requests
from typing import Union
from os import path
import json
from helpers.config import SpeedrrConfig, ClientConfig
from helpers.log_loader import logger
from helpers.bit_convert import bit_conv

class SABnzbdClient:
    _logname: str = "sabnzbd"
    
    def __init__(self, config: SpeedrrConfig, config_client: ClientConfig) -> None:
        self._host = config_client.url
        self._apikey = config_client.apikey
        

        logger.debug(self.log_string(f"Testing connection with SABnzbd at {config_client.url}"))
        
        try:
            self.get()
            logger.debug(self.log_string("Connected to SABnzbd"))
        except:
            raise Exception(self.log_string("Failed to authenticate with SABnzbd, check your credentials"))

    def log_string(self, message):
        return f"<{self._logname}|{self._host}> {message}"

    def get(self, **kwargs) -> bool:
        args = "&".join([f"{key}={value}" for key, value in kwargs.items()])
        query_string = f"api?output=json&apikey={self._apikey}&{args}"
        request_url = path.join(self._host, query_string)

        response = requests.get(request_url)

        if response.text == "API Key Incorrect":
            raise Exception(self.log_string("Failed to authenticate with SABnzbd, check your credentials"))
        else:
            response_dict = json.loads(response)
        
        return response_dict['count']
        

    def get_active_torrent_count(self) -> int:
        "Get the number of downloads that are currently queued."
        logger.debug(f"<sabnzbd|{self._client_config.url}> Getting number of queued downloads")

        response = self.get(mode="queue")

        return 1
    

    def set_upload_speed(self, speed: Union[int, float]) -> None:
        "Set the upload speed limit for the client, in client units."
        
        logger.debug(f"<qbit|{self._client_config.url}> Setting upload speed to {speed}{self._config.units}")
        self._client.transfer_set_upload_limit(
            max(1, int(bit_conv(speed, self._config.units, 'b')))
        )

