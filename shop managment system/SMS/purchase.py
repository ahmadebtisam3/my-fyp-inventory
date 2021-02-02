from datetime import date,datetime
from custom_exceptions import shope_managment_system_exception
from inventory import inventory_records
from on_account import on_account_records
from liquid_aced import liquid_aced_records
class purchase_records:
    def __init__(self):
        self.purchases = []
    def add_record(self,item_name:str,amount:int,purchase_price:int,
    unit_price:int,date_time:str,account_name:str):
        self.purchases.append({
        'name':item_name,
        'amount':amount,
        'purchase_price':purchase_price,
        'account_name':account_name,
        'unit_price':unit_price,'date':date_time})
    def add_purchase(self,account_name:str,item_name:str,amount:int,purchase_price:int,type_of_sale:int,
    on_account:on_account_records,liquid_aced:liquid_aced_records,inventory:inventory_records):
        if len(inventory.types) > type_of_sale:
            #calculating unit price of a product that is beign purchase
            unit_price = purchase_price/amount
            # date on which this purchase is recorded
            dat = datetime.now()
            # format of date
            date_time = f"{dat.year}-{dat.month}-{dat.day} {dat.hour}:{dat.minute}:{dat.second}"
            # remove price from the liquid_aced account which is used to buy these purchases
            liquid_aced.purchase_on_account(account_name,purchase_price,on_account)
            # store record in it self
            self.add_record(item_name,amount,purchase_price,unit_price,date_time,account_name)
            # add purchases in inventory stock
            inventory.add_stock(unit_price,item_name,amount,type_of_sale)
        else:
            raise shope_managment_system_exception(" type number is invalid ")    

    def remove_purchases(self,item_name:str,date_time:str,amount:int,
    on_account:on_account_records,liquid_aced:liquid_aced_records,inventory:inventory_records):
        #search record by using item name date time as a primary key
        record = self.search_by_name_and_date_time(item_name,date_time)
        # verify if record exist or not
        if record:
            # verify the amount that is going to be returned 
            if record['amount'] >= amount:
                # calculate the total price of purchase return
                purchase_price = amount*record['unit_price']  
                # minus sign indicate that this amount is removed from the purchases          
                amount = -1*amount
                # date and time of the moment of purchase return recorded
                dat = datetime.now()
                date_time = f"{dat.year}-{dat.month}-{dat.day} {dat.hour}:{dat.minute}:{dat.second}"
                # add amount to the aced account which use to buy the purchases
                liquid_aced.purchase_return_on_account(record['account_name'],purchase_price,on_account)
                # remove stock from the inventory it also validate amount weather it can be return
                # or not
                inventory.remove_stock(item_name,record['unit_price'],-1*amount)
                # store record in purchase model or in it self
                self.add_record(item_name,amount,purchase_price,
                record['unit_price'],date_time,record['account_name'])
            else:    
                raise shope_managment_system_exception(amount+" this number of products cannot be removed  ")
        else:
            raise shope_managment_system_exception(" product with "+item_name+" and date time "+date_time+" not exist")        
    def search_by_name(self,item_name:str):
        records = []
        for record in self.purchases:
            if record['name'] == item_name:
                records.append(record)
        return records         
    def search_by_name_and_date_time(self,item_name:str,date_time:str):
        try:
            dat = datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
            dat = f"{dat.year}-{dat.month}-{dat.day} {dat.hour}:{dat.minute}:{dat.second}"
            for record in self.purchases:
                if record['date'] == dat and record['name'] == item_name:
                   return record
            return None       
        except Exception:
            raise shope_managment_system_exception(" invalid date time it should be yyyy-mm-dd hh:mm:ss ")    
    def search_all(self):
        return self.purchases     
    def get_purchase_worth(self):
        worth = 0
        for record in self.purchases:
            worth += record['purchase_price']
        return worth
    
    