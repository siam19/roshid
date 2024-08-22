from delivery_api.base import DeliveryAPI
from delivery_api.pathao import PathaoAPI


class DeliveryClient:
    def __init__(self, vendor_name:str) -> DeliveryAPI:
        if vendor_name == 'pathao':
            pathao = PathaoAPI("7N1aMJQbWm", "wRcaibZkUdSNz2EI9ZyuXLlNrnAv0TdPUPXMnD39", base_url="https://courier-api-sandbox.pathao.com/",)
            #pathao.authenticate("test@pathao.com", "lovePathao")
            pathao.access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyNjciLCJqdGkiOiJlNDY1ZTgyMmZjNGZhY2E3NjYwZDI2NWVhZmM3MjQyNDZjYmM1NWM0NDVmNDc1NmZmNTNhMmMwNjE4ZTQ0MDExMDFiYTAzZjFiOGVkODIwZSIsImlhdCI6MTcyMjg4NTE3Ny45NzI4OTQsIm5iZiI6MTcyMjg4NTE3Ny45NzI4OTcsImV4cCI6MTcyMzMxNzE3Ny45MzExMzMsInN1YiI6IjM1MiIsInNjb3BlcyI6W119.DeDEaLfVrU_UwDNEK57SBz6dwHW6uM1AKKjrrnSm2fPv4kNAaeJcH8nMKzZlrQ0qgzzKdf3bB0eX5qbUG-pKkPTsmE9UnIBJ8aDwKArOc6TY53CSO-b4ypKkabkdkn-6qe5COJV1MtQWivi-4sKguZ2kSvYoCaHhNvG_fWNlArvrBjTBXgXUoAP3fc_8PiiWHV8iSqapIcEdekhkgMUNokrgWQrVD7JGjk30yKAJI3Rf48CFvIo1eaEVmQViwH2Ygz1uWtTmxxU9thULefMzsR7HVtc0bAggvldfZQBX1gmHOTBOiiZWAH6BvSNNIf-trmE4ILAxvWX_OaEKpeRhSDZesuQVrCO_O3X4Q0U3CcTQsLXKOH3GV8K3LrHgE3z5YTom_bTlTDlqGX7zQnK2uJs5BAB9GuuT4eAcNs21bdK2Gy8zBKTYldm_2a0iVGPsUmcOMdaM70KWZAPGAD8lcshYvBhcI8ZBW0z2BAQhzh_P-RSpxlOS5ebnnV52y82Aot3ko2CV9wApBlqEGSj-ZFCDklZdG3mY9qawIgQiEHm-e_R0p8wiaqzOjW8czcKfnVMkJc1GhvmOh-OfGwlWF6gJxHn6iU5ytjWH2fxjSJMmIg0xeGUTlwjjEOPvQ256cSdUxkpSrokeDQvBlXb_m12XMDV-yqEuyUocvbffSs0"
            self.vendor = pathao

        elif vendor_name == 'noti':
            return "notir pola emon kisu nai"
        else: 
            raise ValueError("no such vendor. only 'pathao' and 'steadfast' is supported")
        
    def get_client(self):
       return self.vendor
    
