from on_account import on_account_records
from custom_exceptions import shope_managment_system_exception
class liquid_aced_records:
    def __init__(self,ignore_account_name):
        self.liquid_aced = []
        self.ignore_account_name = ignore_account_name
    def add_record(self,account_name:str,amount:int):
        self.liquid_aced.append(
            {
                'name':account_name,
                'amount':amount
            }
        )
    def add_liquid_aced(self,account_name:str,amount:int):
        # find the account_name if exist add the amount else make new record
        record = self.search_by_name(account_name) 
        if record == {}:
            self.add_record(account_name,amount)
        else:
            record['amount'] += amount
    def remove_liquid_aced(self,account_name:str,amount:int):
        # search the record if exist than validate the value than subract the amount from
        # account in such a way result would be zero else give error i
        record = self.search_by_name(account_name)
        if record != {}:
            price = record['amount'] - amount
            if price >= 0:
                record['amount'] -= amount
                return True
            raise shope_managment_system_exception(" account can not support  "+amount+" to spend ")
        raise shope_managment_system_exception(" liquid aced account name "+account_name+" not exist ")                
 
    def purchase_on_account(self,account_name:str,amount:int,on_account:on_account_records):
        # used by purchase model it remove the amount used by an account for purchasing 
        # if that account does not exist than it make this account a liability or loan
        if account_name != self.ignore_account_name:
            record = self.search_by_name(account_name)
            if record == {}:
                on_account.add_account_loan(account_name,amount,self)
            else:
                price = record['amount'] - amount
                # if account exist but result if smaller than zero than it give error
                if price >= 0:
                    record['amount'] = price 
                else:
                    raise shope_managment_system_exception(" account  "+account_name," dosnot have enough credit to support the transection")    
    def purchase_return_on_account(self,account_name:str,amount:int,on_account:on_account_records):
        # used by only purchase model in case of purchase return if account exist as a liquid
        # aced it add the purchase amount to that account if not than settle tha account in 
        # on_account model
        if account_name != self.ignore_account_name:
            record = self.search_by_name(account_name)
            if record == {}:
                on_account.payed_payment(account_name,amount,self)
            else:
                record['amount'] += amount 

    def sale_on_account(self,account_name:str,amount:int,on_account:on_account_records):
        # this thing used only by sales method and add the amount in the ased account
        # is that account doesnot exist than make it a load or debters
        if account_name != self.ignore_account_name:
            record = self.search_by_name(account_name)
            if record == {}:
                on_account.add_account_loan(account_name,amount,self)
            else:
                record['amount'] += amount 
    def sale_return_on_account(self,account_name:str,amount:int,on_account:on_account_records):
        # remove amount from the aced account in case of sales return if account not exist than
        # settle the loan if exist than the resulting value must be >= 0
        if account_name != self.ignore_account_name:
            record = self.search_by_name(account_name)
            if record == {}:
                on_account.payed_payment(account_name,amount,self)
            else:
                price = record['amount'] - amount
                if price >= 0:
                    record['amount'] = price 
                else:
                    raise shope_managment_system_exception(" account  "+account_name," dosnot have enough credit to support the transection")    

    def search_by_name(self,account_name):
        for record in self.liquid_aced:
            if record['name'] == account_name:
                return record
        return {}            
    def search_all(self):
        return self.liquid_aced    