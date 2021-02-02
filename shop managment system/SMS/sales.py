from datetime import date,datetime
from custom_exceptions import shope_managment_system_exception
from inventory import inventory_records
from liquid_aced import liquid_aced_records
from on_account import on_account_records
class sales_records:
    def __init__(self):
        self.sales = []

    def add_record(self,inventory_id:int,date_time:str,whole_sale_price:int
    ,unit_sale_price:int,amount:int,account_name:str):
        self.sales.append({
            'id':inventory_id,
            "date":date_time,
            "whole_sale_price":whole_sale_price,
            "unit_sale_price":unit_sale_price,
            'account_name':account_name,
            "amount":amount 
        })
    def add_sales(self,account_name:str,item_name:str,unit_price:int,whole_sale_price:int,
    amount:int,inventory_data:inventory_records,on_account:on_account_records
    ,liquid_aced:liquid_aced_records):
    # use sale_stock method in inventory to remove sales from inventory if needed
    # add the whole_sale to the defined account in liquid aced model
        record = inventory_data.sale_stock(item_name,unit_price,amount)
        dat = datetime.now()
        date_time = f"{dat.year}-{dat.month}-{dat.day} {dat.hour}:{dat.minute}:{dat.second}"
        unit_sale_price = whole_sale_price/amount
        liquid_aced.sale_on_account(account_name,whole_sale_price,on_account)
        self.add_record(record['id'],date_time,whole_sale_price,unit_sale_price,amount,account_name)

    def remove_sales(self,item_name:str,date_time:str,amount:int,
    inventory_data:inventory_records,on_account:on_account_records,liquid_aced:liquid_aced_records,
    add_in_inventory=True):
    # search record by date time and its name as a primary key 
    # remove the amount from which whole sale of that product is added
    # add the product in inventory if needed by using sales return method
    # and finally add the record in it self by with new whole sale price, and -ve amount
        record = self.search_by_name_and_date_time(item_name,date_time,inventory_data)
        account_name = record['account_name']
        if record:
            if record['amount'] >= amount:
                whole_sale_price = amount*record['unit_sale_price']           
                amount = -1*amount
                dat = datetime.now()
                date_time = f"{dat.year}-{dat.month}-{dat.day} {dat.hour}:{dat.minute}:{dat.second}"
                inventory_data.add_sale_return(record['id'],-1*amount)
                liquid_aced.sale_return_on_account(account_name,whole_sale_price,on_account)
                self.add_record(record['id'],date_time,whole_sale_price,record['unit_sale_price'],amount,account_name)
            else:    
                raise shope_managment_system_exception(amount+" this number of products cannot be removed  ")
        else:
            raise shope_managment_system_exception(" product with "+item_name+" and date time "+date_time+" not exist")        


    def search_by_name_and_date_time(self,item_name:str,date_time,inventory_data:inventory_records):
        try:
            dat = datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
            dat = f"{dat.year}-{dat.month}-{dat.day} {dat.hour}:{dat.minute}:{dat.second}"
            for sales_record in self.sales:
                if sales_record['date'] == date_time and inventory_data.search_by_id(sales_record['id'])['name']==item_name:
                    return sales_record
            return None       
        except Exception:
            raise shope_managment_system_exception(" invalid date time it should be yyyy-mm-dd hh:mm:ss or inventory id ")
    def search_by_name(self,item_name:str,inventory_data:inventory_records):
        records = []
        try:
            for record in self.sales:
                if inventory_data.search_by_id(record['id'])['name'] == item_name:
                    records.append(record)
            return records        
        except Exception:
            raise shope_managment_system_exception(" data might be corrupted cannot relate sales with inventory ")
    def search_all(self,inventory_data:inventory_records):
        records = []
        temp:dict
        try:
            for record in self.sales:
                temp = record.copy()
                temp['name'] = inventory_data.search_by_id(record['id'])['name']
                records.append(temp)
            return records    
        except Exception:
            raise shope_managment_system_exception(" data might be corrupted cannot relate sales with inventory ")        
    def get_sales_worth(self):
        # add the whole sale price of a product which become the total revinew of the business
        # from sales 
        worth = 0
        for record in self.sales:
            if record['amount'] > 0:
                worth += record['whole_sale_price']
            else:
                worth -= record['whole_sale_price']        
        return worth            
    def get_sales_item_inventory_worth(self,inventory:inventory_records):
        # add the purchase price of sale product which is type one and ignore type 2 price
        # in one variable which become the investment of business on a product
        worth = 0
        inventory_r:inventory_records
        for record in self.sales:
            inventory_r = inventory.search_by_id(record['id'])
            if inventory.types[inventory_r['type']] == inventory.types[1]:
                worth += inventory_r['unit_price']*record['amount']   
        return worth            
