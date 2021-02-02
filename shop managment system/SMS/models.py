from datetime import date,datetime
from custom_exceptions import shope_managment_system_exception
from inventory import inventory_records
from sales import sales_records
from purchase import purchase_records
from on_account import on_account_records
from accountant import accounts
import os
class load_and_store_models:
    base_dir_name = "resources"
    sub_files = [
        "purchases.txt",
        "total_purchase_worth.txt",
        "sales.txt",
        "total_sales_worth.txt",
        "inventory.txt",
        "total_inventory_worth.txt",
        "on_account.txt",
        "profit_and_loss.txt"
    ]

    def __init__(self,selected_year=None):
        self.dir_list:list
        self.load_dir_path:str
        self.selected_year = selected_year
        self.verify_dir_path(selected_year)
        self.inventory:inventory_records
        self.sales:sales_records
        self.purchases:purchase_records
        self.on_account:on_account_records
    def load(self):
        ""
    def store(self):
        ""    
    def end_turn(self):
        ""    
    def verify_dir_path(self,selected_year=None):
        if os.path.isdir(load_and_store_models.base_dir_name):
            self.dir_list = os.listdir(load_and_store_models.base_dir_name)
            if selected_year and self.dir_list.__contains__(selected_year):
                self.load_dir_path = os.path.join(load_and_store_models.base_dir_name,selected_year)
                self.verify_files(self.load_dir_path)
            elif self.dir_list != []:
                self.selected_year = self.dir_list.pop()
                self.load_dir_path = os.path.join(load_and_store_models.base_dir_name,self.selected_year)                
                self.verify_files(self.load_dir_path)
            else:
                self.start_new_season()
        else:
            os.mkdir(load_and_store_models.base_dir_name)
            self.start_new_season()  
    def verify_files(self,path):
        lis = os.listdir(path)
        if lis == []:
            for files_name in load_and_store_models.sub_files:
                open(os.path.join(path,files_name),'w').close() 
        elif len(lis) == len(load_and_store_models.sub_files):
            for file_name in load_and_store_models.sub_files:
                if not lis.__contains__(file_name):
                    raise shope_managment_system_exception(" invalid files in "+path)        
        else:    
            raise shope_managment_system_exception(" invalid files in "+path)
    def start_new_season(self):
        self.selected_year = str(datetime.now())
        path = os.path.join(load_and_store_models.base_dir_name,self.selected_year)
        os.mkdir(path)
        self.verify_files(path)                    

lo = load_and_store_models()
