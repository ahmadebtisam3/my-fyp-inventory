from custom_exceptions import shope_managment_system_exception
class on_account_records:
    def __init__(self,business_name:str):
        self.accounts = []
        self.business_name = business_name
    def add_record(self,account_name:str,payed:int,have_to_pay:int):
        self.accounts.append(
            {
                'account_name':account_name,
                'payed':payed,
                'have_to_pay':have_to_pay
            }
        )    
    def is_business(self,account_name):
        # check if this loan belongs to business or customers
        if account_name == self.business_name:
            return True
        return False   
    def add_to_aced_and_liability(self,liquid_aced,account_name:str
    ,have_to_pay:int):
    # in case of a loan if this loan is for business than it add that same amount
    # in liquid_aced model liability account name else add it with debters name
        if self.is_business(account_name):
            liquid_aced.add_liquid_aced("liability",have_to_pay)
        else:
            liquid_aced.add_liquid_aced("debters",have_to_pay)   
    def recover_to_aced_and_liability(self,liquid_aced,account_name:str
    ,have_to_pay:int):
    # in case of a settlement if this loan was for business than it remove that same amount
    # in liquid_aced model liability account name else remove it from debters and add amount in
    # recover account    
        if self.is_business(account_name):
            liquid_aced.remove_liquid_aced("liability",have_to_pay)
        else:
            liquid_aced.remove_liquid_aced("debters",have_to_pay) 
            liquid_aced.add_liquid_aced("recover",have_to_pay)               
    def add_account_loan(self,account_name,have_to_pay,liquid_aced):
        # this method add a have_to_pay amount in accounts have_to_pay if that account 
        # not exist than create a new one with this amount
        record = self.search_by_name(account_name)
        if record == {}:
            self.add_to_aced_and_liability(liquid_aced,account_name,have_to_pay)
            self.add_record(account_name,0,have_to_pay)
        else:            
            self.add_to_aced_and_liability(liquid_aced,account_name,have_to_pay)            
            record['have_to_pay'] += have_to_pay
    def payed_payment(self,account_name,payed,liquid_aced):
        # this method settle account by adding the amount in accounts payed amount
        # the result must not excced have_to_pay amount if that account not exist than
        # throw an error 
        record = self.search_by_name(account_name)
        if record != {}:
            price = record['payed']
            price += payed
            if price <= record['have_to_pay']:
                self.recover_to_aced_and_liability(liquid_aced,account_name,payed)
                record['payed'] += payed
            else:
                raise shope_managment_system_exception(" account "+account_name+" did not owe  "+price+" but it accually owe "+record['have_to_pay'])    
        else:
            raise shope_managment_system_exception("account with name "+account_name+" doesnot exist ")        
    def search_by_name(self,account_name):
        for record in self.accounts:
            if record['account_name'] == account_name:
                return record
        return {}
    def search_all(self):
        return self.accounts 
    def search_unsettle_account(self):
        records = []
        for record in self.accounts:
            if record['have_to_pay'] > record['payed']:
                records.append(record)
        return records            