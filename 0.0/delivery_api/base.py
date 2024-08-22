from abc import ABC, abstractmethod

class DeliveryAPI(ABC):
    @abstractmethod
    def create_order(self):
        pass
    
    @abstractmethod
    def create_bulk_order(self):
        pass
    
    @abstractmethod
    def get_delivery_status(self):
        pass