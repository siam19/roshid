import os
from fastapi import Request
from abc import ABC, abstractmethod
from plugin_manager import PluginManager
import plugins
import logging

from classes import DeliveryInfo


class DeliveryAPI(ABC):
    @abstractmethod
    def create_order(self, delivery_info):
        pass

    @abstractmethod
    def create_bulk_order(self, delivery_infos):
        pass

    @abstractmethod
    def get_delivery_status(self, order_id):
        pass




class DeliveryInterface:
    # request is handled by fastapi router
    def __init__(self) -> None:

        # Load plugins
        try:
            plugin_manager = PluginManager()
            plugin_manager.load_plugins(plugins)
            self.plugins = plugin_manager.plugins
        except Exception as e:
            logging.error(f"Error loading plugins: {e}")
            self.plugins = PluginManager()  # Initialize with an empty manager

    #TODO This isnt production ready

    def authenticate(self, users_dalx   =None):
        # enabled_plugins = user.get_enabled_delivery_services()
        
        service = self.plugins.get('steadfast')
        service.api_key = os.environ.get("STEADFAST_API_KEY")
        service.secret_key = os.environ.get("STEADFAST_SECRET_KEY")
        print("Updated keys!")
        logging.info("Delivery API keys Added!")
    
    def create_pickup_request(self, delivery_info: DeliveryInfo, service_name:str):
        client = self.plugins.get(service_name)
        return client.create_order(delivery_info)

    def get_api_key(self):
        return self.plugins.get("steadfast").api_key
