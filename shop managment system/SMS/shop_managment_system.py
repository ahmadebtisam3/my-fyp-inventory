from custom_exceptions import shope_managment_system_exception
from expances import expances_records
from inventory import inventory_records
from liquid_aced import liquid_aced_records
from on_account import on_account_records
from purchase import purchase_records
from sales import sales_records
from accountant import accounts
class shope_managment_system:
    def __init__(self,business_name:str):
        self.ignore_account_name = "ignore_transaction"
        self.business_name = business_name
        self.inventory = inventory_records()
        self.purchases = purchase_records()
        self.sales = sales_records()
        self.on_account = on_account_records(self.business_name)
        self.liquid_aced = liquid_aced_records(self.ignore_account_name)
        self.expances = expances_records()
    def load(self):
        ""
    def store(self):
        ""    
    def set_business_name(self,business_name:str):
        self.business_name = business_name
    def get_business_name(self):
        return self.business_name    
    def purchase(self,account_name:str,item_name:str,amount:int,purchase_price:int,type_of_sale:int):
        self.purchases.add_purchase(account_name,item_name,amount,purchase_price,
        type_of_sale,self.on_account,self.liquid_aced,self.inventory)
    def purchase_return(self,item_name:str,date_time:str,amount:int):
        self.purchases.remove_purchases(item_name,date_time,amount
        ,self.on_account,self.liquid_aced,self.inventory)
    def show_purchases(self):
        return self.purchases.search_all()
    def show_purchase_by_name(self,name):
        return self.purchases.search_by_name(name)
    def sale(self,account_name:str,item_name:str,unit_price:int,whole_sale_price:int,
    amount:int):
        self.sales.add_sales(account_name,item_name,unit_price,whole_sale_price,amount
        ,self.inventory,self.on_account,self.liquid_aced)  
    def sale_return(self,item_name:str,date_time:str,amount:int):
        self.sales.remove_sales(item_name,date_time,amount,
        self.inventory,self.on_account,self.liquid_aced)    
    def show_sales(self):
        return self.sales.search_all(self.inventory)
    def show_sales_by_name(self,name):
        return self.sales.search_by_name(name,self.inventory)
    def add_liquid_aced_account(self,account_name:str,amount:int):
        self.liquid_aced.add_liquid_aced(account_name,amount)
    def remove_amount_from_liquid_aced(self,account_name:str,amount:int):
        self.liquid_aced.remove_liquid_aced(account_name,amount)    
    def show_liquid_aced(self):
        return self.liquid_aced.search_all()
    def show_liquid_aced_by_name(self,name):
        return self.liquid_aced.search_by_name(name)        
    def on_account_payment(self,account_name:str,amount:int):    
        self.on_account.payed_payment(account_name,amount,self.liquid_aced)
    def show_on_accounts(self):
        return self.on_account.search_all()
    def show_on_account_by_name(self,account_name:str):
        return self.on_account.search_by_name(account_name)
    def show_unsettle_account(self):
        return self.on_account.search_unsettle_account()    
    def add_expance(self,account_name,expance_name:str,amount:int):
        self.expances.add_expance(account_name,expance_name,amount,self.liquid_aced)            
    def remove_expance(self,expance_name:str,date_time:str,amount:int):
        self.expances.remove_expance(expance_name,date_time,amount,self.liquid_aced)   
    def discard_stock(self,item_name,unit_price,amount):
        self.expances.discard_product_in_inventory(item_name,unit_price,amount
        ,self.inventory,self.ignore_account_name)     
    def show_expances(self):
        return self.expances.search_all()
    def show_expance_by_name(self,expance_name:str):
        return self.expances.search_by_name(expance_name)        
    def profit_and_loss(self):
        return accounts(self.sales,self.inventory,self.expances).calculate_sales_profit()
    def net_profit_and_loss(self):
        return accounts(self.sales,self.inventory,self.expances).calculate_net_profit() 
    def show_inventory(self):
        return self.inventory.search_all()
    def show_inventory_by_name(self,name):
        return self.inventory.search_by_name(name)        

def print_dict(label:str,dic:list):
    print(label)
    for i in dic:
        print(i)
sms = shope_managment_system("my shop")
sms.add_liquid_aced_account("cash",100000)
sms.add_liquid_aced_account("sales",0)
#sms.remove_amount_from_liquid_aced("cash",1000)
sms.purchase("cash","laptop",3,3000,1)
sms.purchase(sms.get_business_name(),'laptop',3,3000,1)
sms.purchase("cash","laptop_repair",1,1000,0)
sms.sale('sales',"laptop",1000.0,1200,1)
sms.sale("bilal","laptop_repair",1000,400,1)
date_time = sms.show_sales_by_name("laptop")[0]['date']
sms.sale_return('laptop',date_time,1)
date_time = sms.show_purchase_by_name("laptop")[0]['date']
sms.purchase_return('laptop',date_time,2)
sms.sale("sales","laptop",1000.0,2500,2)
sms.on_account_payment("bilal",400)
sms.sale("bilal","laptop_repair",1000,400,1)
#sms.on_account_payment("bilal",400)
sms.on_account_payment(sms.business_name,1000)
sms.on_account_payment("bilal",400)
#sms.discard_stock('laptop',1000,1)
sms.add_expance("cash","sofa",200)
sms.remove_expance("sofa",sms.show_expance_by_name("sofa")[0]['date'],200)
print_dict("liquid aced: ",sms.show_liquid_aced())
print_dict("purchases: ",sms.show_purchases())
print_dict("sales:",sms.show_sales())
print_dict("inventory :",sms.show_inventory())
print_dict("on account: ",sms.show_on_accounts())
print_dict("un settle account: ",sms.show_unsettle_account())
print_dict("expances :",sms.show_expances())
print("net profit",sms.net_profit_and_loss())
print("income from sale",sms.profit_and_loss())