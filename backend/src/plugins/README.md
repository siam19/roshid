Each plugin module should implement the DeliveryAPI interface and expose a DeliveryServicePlugin.

```python
# plugins/steadfast.py

from delivery_api import DeliveryAPI

class SteadfastAPI(DeliveryAPI):
    def create_order(self, delivery_info):
        # Implement Steadfast-specific order creation logic
        pass

    def create_bulk_order(self, delivery_infos):
        # Implement bulk order logic
        pass

    def get_delivery_status(self, order_id):
        # Implement status retrieval logic
        pass

# Expose the plugin class with a standard name
DeliveryServicePlugin = SteadfastAPI
```

