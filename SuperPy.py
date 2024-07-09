import sys
import csv
import os
from texttable import Texttable
from datetime import timedelta, datetime
import tkinter as tk
from tkinter import messagebox 
import argparse

#Function to get inventory items
def get_inventory():
   dir_path = os.path.dirname(os.path.realpath(__file__))
   file_path = os.path.join(dir_path, "bought.csv")
   with open(file_path, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    all_rows = []
    for row in csv_reader:
       all_rows.append(row)
    return all_rows


def validate_date(date_string):
   try:
      datetime.strptime(date_string, '%Y-%m-%d')
      return True
   except ValueError:
      sys.stdout.write("Invalid expiration date. It must be formatted like YYYY-MM-DD")
      return False


def get_date():
   dir_path = os.path.dirname(os.path.realpath(__file__))
   file_path = os.path.join(dir_path, "current_date.txt")
   file_contents = open(file_path, "r").read()
   return file_contents


def buy_product(id, product_name, price, expiry, buy_date):
   with open('bought.csv', mode='a', newline='') as file:
       writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
       writer.writerow([id, product_name, buy_date, price, expiry])
   sys.stdout.write("OK")
   messagebox.showinfo("Buy", "Item bought successfully!")


def sell_product(id, product_name, product_price, inventory, current_date):
   product = None
   for item in inventory:
      if item[1] == product_name:
         product = item

   if product == None:
      sys.stdout.write("ERROR: Product not in stock")
   else:
      with open('sold.csv', mode='a', newline='') as file:
       writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
       writer.writerow([id, product[0], current_date, product_price])
       sys.stdout.write("OK")
       messagebox.showinfo("Sell", "Item sold successfully!")

def buy_item_cli(args):
    print(f"Buying item: {args.item_name}")

def sell_item_cli(args):
    print(f"Selling item: {args.item_name}")


def report_inventory(current_date, inventory, day):
   inventory_to_display = []
   inventory_to_display.append(inventory[0])
   if day == "--yesterday":
      dt = datetime.strptime(current_date, '%Y-%m-%d')
      yesterday = dt - timedelta(days = 1)
      current_date = yesterday.strftime('%Y-%m-%d')
   for item in inventory:
      if item[2] == current_date:
         inventory_to_display.append(item)
   t = Texttable()
   t.add_rows(inventory_to_display)
   sys.stdout.write(t.draw())


def advance_time(days_to_increase):
   current_date = get_date()
   dt = datetime.strptime(current_date, '%Y-%m-%d')
   yesterday = dt + timedelta(days = days_to_increase)
   current_date = yesterday.strftime('%Y-%m-%d')
   file = open("current_date.txt", "w")
   file.write(current_date)
   file.close()
   sys.stdout.write("OK")


def report_revenue(report_date, current_date):
   revenue = 0
   if report_date[0] == "--yesterday":
      current_date = get_date()
      dt = datetime.strptime(current_date, '%Y-%m-%d')
      yesterday = dt + timedelta(days = days_to_increase)
      current_date = yesterday.strftime('%Y-%m-%d')
   elif report_date[0] == "--date":
      current_date = report_date[1]
   with open('sold.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
       if row[2] == current_date:
         revenue += float(row[-1])

   sys.stdout.write("Revenue so far: " + str(revenue))



def main():
   #Holds current date frin the text file
   current_date = get_date()

   #Holds the inventory
   inventory = get_inventory()
   try:
      last_item_id = int(inventory[-1][0])
   except ValueError:
      last_item_id = 1
   args = sys.argv
   if len(args) > 1 and args[1] == "buy":
      product_name = args[3]
      price = args[5]
      expiry = args[7]
      buy_date = current_date
      if validate_date(expiry):
         buy_product(last_item_id + 1, product_name, price, expiry, buy_date)

   elif len(args) > 1 and args[1] == "report":
      if args[2] == "inventory":
         report_inventory(current_date, inventory, args[3])
      elif args[2] == "revenue":
         if args[3] == "--date":
            report_revenue([args[3], args[4]], current_date)
         else:
            report_revenue([args[3]], current_date)
   elif len(args) > 1 and args[1] == "sell":
      product_name = args[3]
      product_price = args[5]
      sell_product(last_item_id, product_name, product_price, inventory, current_date)

   elif len(args) > 1 and args[1] == "--advance-time":
      advance_time(int(args[2]))
if __name__ == "__main__":
   if __name__ == "__main__":
    import sys
    if "--gui" in sys.argv:
        # GUI code
        app = tk.Tk()
        app.title("SuperPy Market")

        buy_button = tk.Button(app, text="Buy Item", command=buy_item)
        buy_button.pack(pady=10)

        sell_button = tk.Button(app, text="Sell Item", command=sell_item)
        sell_button.pack(pady=10)

        app.mainloop()
    else:
        # CLI logic
        parser = argparse.ArgumentParser(description="SuperPy Market Operations")
        subparsers = parser.add_subparsers()

        # Buy command
        parser_buy = subparsers.add_parser('buy', help='Buy an item')
        parser_buy.add_argument('item_name', type=str, help='Name of the item to buy')
        parser_buy.set_defaults(func=buy_item_cli)

        # Sell command
        parser_sell = subparsers.add_parser('sell', help='Sell an item')
        parser_sell.add_argument('item_name', type=str, help='Name of the item to sell')
        parser_sell.set_defaults(func=sell_item_cli)

        args = parser.parse_args()
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()
