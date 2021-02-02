from datetime import date,datetime
from custom_exceptions import shope_managment_system_exception
from liquid_aced import liquid_aced_records
from inventory import inventory_records
class expances_records:
    def __init__(self):
        self.expances = []

    def add_record(self,expance_name:str,price:int,date_time:str,account_name:str):
        date = datetime.now()
        date = str(date)
        self.expances.append(
            {
            "date":date_time,    
            'name':expance_name,
            'amount':price,
            'account_name':account_name
            }
        )
    def add_expance(self,account_name,expance_name:str,amount:int,liquid_aced:liquid_aced_records):
        # this method substact amount from the liquid aced model account which is supporting 
        # the expance and than record it
        dat = datetime.now()
        date_time = f"{dat.year}-{dat.month}-{dat.day} {dat.hour}:{dat.minute}:{dat.second}"
        liquid_aced.remove_liquid_aced(account_name,amount)
        self.add_record(expance_name,amount,date_time,account_name)
    
    def remove_expance(self,expance_name:str,date_time:str,amount:int,liquid_aced:liquid_aced_records):
        # find the expance with name ,
        # add the amount to the liquid aced amount which is responsible for this expance
        #  and record the amount with negative value in it 
        record = self.search_by_name_and_date_time(expance_name,date_time)
        if record:
            if record['amount'] >= amount:
                amount = -1*amount
                dat = datetime.now()
                date_time = f"{dat.year}-{dat.month}-{dat.day} {dat.hour}:{dat.minute}:{dat.second}"
                liquid_aced.add_liquid_aced(record['account_name'],-1*amount)
                self.add_record(expance_name,amount,date_time,record['account_name'])
            else:    
                raise shope_managment_system_exception(amount+" this number of products cannot be removed  ")
        else:
            raise shope_managment_system_exception(" product with "+expance_name+" and date time "+date_time+" not exist")        
    def discard_product_in_inventory(self,item_name:str,unit_price:str,amount:int,
    inventory_data:inventory_records,ignore_name:str):
        # this method is use for discarding inventory product this method create an expance
        # with the name of that product and remove it from inventoy
        inventory_data.remove_stock(item_name,unit_price,amount)
        dat = datetime.now()
        date_time = f"{dat.year}-{dat.month}-{dat.day} {dat.hour}:{dat.minute}:{dat.second}"
        self.add_record(item_name,unit_price*amount,date_time,ignore_name)
    def search_by_name(self,item_name:str):
        records = []
        for record in self.expances:
            if record['name'] == item_name:
                records.append(record)
        return records         
    def search_by_name_and_date_time(self,item_name:str,date_time:str):
        try:
            dat = datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
            dat = f"{dat.year}-{dat.month}-{dat.day} {dat.hour}:{dat.minute}:{dat.second}"
            for record in self.expances:
               if record['date'] == dat and record['name'] == item_name:
                   return record
            return None       
        except Exception:
            raise shope_managment_system_exception(" invalid date time it should be yyyy-mm-dd hh:mm:ss ")    
    def search_all(self):
        return self.expances
    def get_expance_worth(self):
        worth = 0
        for record in self.expances:
            worth += record["amount"]
        return worth
