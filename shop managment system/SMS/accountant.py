from sales import sales_records
from inventory import inventory_records
from expances import expances_records
class accounts:
    def __init__(self,sales:sales_records,inventory:inventory_records,expances:expances_records):
        self.sales = sales
        self.inventory = inventory
        self.expances = expances
    def calculate_sales_profit(self):
        # subtract total revinew from sale with the investment on sale which become the income
        # from sale
        return (self.sales.get_sales_worth() - self.sales.get_sales_item_inventory_worth(self.inventory))    
    def calculate_net_profit(self):
        # if you substract the expances from income than it become the net profit
        sale_profit = self.calculate_sales_profit()
        return sale_profit - self.expances.get_expance_worth()    