from delivery_handler import DeliveryClient
from delivery_api.pathao import PathaoAPI, OrderInput


order1 = OrderInput(
    merchant_order_id=350135,
    store_id=11028,
    recipient_name="John Doe",
    recipient_phone="01785863769",
    recipient_address="123 Main St, Dhaka",
    recipient_city=1,
    recipient_zone=2,
    delivery_type=48,
    item_type=2,
    item_quantity=1,

    item_weight=0.5,
    amount_to_collect=1000,
    special_instruction="Please call before delivery"
   

)

print("starting..")


pathao = DeliveryClient("pathao").get_client()
print(pathao.get_zones(1))