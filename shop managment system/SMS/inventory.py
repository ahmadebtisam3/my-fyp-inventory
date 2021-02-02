from datetime import date,datetime
from custom_exceptions import shope_managment_system_exception
class inventory_records:
    types = ["renewable","nonrenewable"]
    def __init__(self):
        self.inventory = []
    def add_record(self,id:int,unit_price:int,item_name:str,amount:int,type_of_sale:int):
        record = {
            'id':id,
            'name':item_name,
            "unit_price":unit_price,
            "amount":amount,
            "type":type_of_sale
        }
        self.inventory.append(record)

    def add_stock(self,unit_price:int,item_name:str,amount:int,type_of_sale:int):
        # add stock in inventory used by purchase model only
        # if inventory is empty than add the record in it self
        if self.inventory == []:
            self.add_record(0,unit_price,item_name,amount,type_of_sale)
            # else if find the item with same name and unit_price than add the amount in
            # that same record in inventory 
        else:
            for record in self.inventory:
                if record['name'] == item_name and record['unit_price'] == unit_price:
                    record['amount'] += amount
                    return
            # make a new record if not find the same name and unit price        
            ide = self.inventory[len(self.inventory)-1]['id'] + 1
            self.add_record(ide,unit_price,item_name,amount,type_of_sale)
    
    def remove_stock(self,item_name:str,unit_price:int,amount:int):
        # remove stock for purchase model only
        # find the item name and unit price if amount is greater than substract the amount
        # from the inventory
        # else raise error
        for record in self.inventory:
            if record['name'] == item_name and record['unit_price'] == unit_price:
                if record['amount'] >= amount:
                    record['amount'] -= amount 
                else:
                    raise shope_managment_system_exception(" product with "+item_name+" and price "+unit_price+" not exist")
                return True    
        raise shope_managment_system_exception(" item_name or unit_price not match ")        
    def sale_stock(self,item_name:str,unit_price:str,amount:int):
        # deals with sales in inventory used by sale model only
        # search the inventory with item name and unit price 
        # if record exist than check its type if type is nonrenewable which is 1
        # than remove the amount from the inventory by ensuring that the result >= 0
        # else raise respactive error
        record = self.search_by_name_and_unit_price(item_name,unit_price)
        if record != {}:
            if inventory_records.types[record['type']] == inventory_records.types[1] and record['amount'] >= amount:
                record['amount'] -= amount 
                return record
            elif inventory_records.types[record['type']] == inventory_records.types[0]:
                return record
            else:    
                raise shope_managment_system_exception(" not enough product for sale for item "+record['name'])    
        else:
            raise shope_managment_system_exception(" product  "+record['name']+" does not exist ")
    def add_sale_return(self,id:int,amount:int):
        # search inventory item by id used by sales in sales return only
        # after taking the record from inventory by using it id it first check the type of product
        # if type is nonrenewable than add the product in that same record
        record = self.search_by_id(id)
        if record != {} and inventory_records.types[record['type']] == inventory_records.types[1]:
            record['amount'] += amount
        return record    

                
    def search_by_name(self,item_name:str):
        records = []
        for record in self.inventory:
            if record['name'] == item_name:
                records.append(record)
        return records           
    def search_by_id(self,id:int):
        for record in self.inventory:
            if record['id'] == id:
                return record
        return {}
    def search_by_name_and_unit_price(self,item_name:str,unit_price:int):
        for record in self.inventory:
            if record['name'] == item_name and record['unit_price'] == unit_price:
                return record
        return {}                       
    def search_all(self):
        return self.inventory
    def get_inventory_worth(self):
        worth = 0
        for record in self.inventory:
            worth += record['unit_price']*record['amount']
        return worth    