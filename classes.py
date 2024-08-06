class Product:
    def __init__(self, name: str, price: float, details: dict=None): 
        self.name = name 
        self.price = price 
        self.details = {} if details == None else details

    def add_detail(self, key, value):
        '''
        Details should be in the form {"attribute": "datatype"}
        note that this class should be used to template orders
        '''
        self.details[key] = value

    def get_attributes(self) -> list[str]:
        #This returns all the attributes listed on the product. eg. ['name', 'price', 'color','size']
        attb = ['name', 'price'] #name and price are required fields
        for key in self.details.keys():
            attb.append(key)
        return attb
    
    
    def __repr__(self):
        return f"Product({self.name}, Price=)" 
    

    
    


