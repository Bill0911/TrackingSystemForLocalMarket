import sys
import csv
import os
from texttable import Texttable
from datetime import timedelta, datetime
import tkinter as tk
from tkinter import messagebox 
import argparse
from datetime import datetime

current_date_str = datetime.now().strftime('%Y-%m-%d')
with open('current_date.txt', 'w') as file:
    file.write(current_date_str)

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
   pass


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
    if report_date is None:
        print("No date filter provided. Please specify a date filter.")
        return
    revenue = 0
    if report_date[0] == "--yesterday":
        dt = datetime.strptime(current_date, '%Y-%m-%d')
        yesterday = dt + timedelta(days=-1)
        current_date = yesterday.strftime('%Y-%m-%d')
    elif report_date[0] == "--date":
        current_date = report_date[1]
    
    try:
        with open('sold.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[2] == current_date:
                    revenue += float(row[-1])
    except Exception as e:
        print(f"Failed to read 'sold.csv': {e}")
        return

    sys.stdout.write(f"Revenue so far: {revenue}")

def handle_buy(args, current_date, last_item_id, inventory):
    if validate_date(args.expiry):
       buy_product(last_item_id + 1, args.product_name, args.price, args.expiry, current_date)

def handle_report(args, current_date, last_item_id, inventory):
   if args.report_type == "inventory":
      report_inventory(current_date, inventory, args.filter)
   elif args.report_type == "revenue":
      report_revenue(args.filter, current_date)

def handle_sell(args, current_date, last_item_id, inventory):
   sell_product(last_item_id, args.product_name, args.product_price, inventory, current_date)

def handle_advance_time(args):
   advance_time(args.days)

def main():
   parser = argparse.ArgumentParser(description="Tracking prouduct system")
   subparsers = parser.add_subparsers(help='commands')

   #buy command
   buy_parser = subparsers.add_parser('buy', help='buy a product')
   buy_parser.add_argument('product_name')
   buy_parser.add_argument('price', type=float)
   buy_parser.add_argument('expiry')
   buy_parser.set_defaults(func=handle_buy)

   #report command
   report_parser = subparsers.add_parser('report', help='generate a report')
   report_parser.add_argument('report_type', choices=['inventory', 'revenue'])
   report_parser.add_argument('filter', nargs='?', default=None)
   report_parser.set_defaults(func=handle_report)

   #sell command
   sell_parser = subparsers.add_parser('sell', help='Sell a product')
   sell_parser.add_argument('product_name')
   sell_parser.add_argument('product_price', type=float)
   sell_parser.set_defaults(func=handle_sell)

   # advance-time command
   advance_time_parser = subparsers.add_parser('--advance-time', help='Advance time')
   advance_time_parser.add_argument('days', type=int)
   advance_time_parser.set_defaults(func=handle_advance_time)

   args = parser.parse_args(sys.argv[1:])

   current_date = get_date()
   inventory =get_inventory()
   try:
      last_item_id = int(inventory[-1][0])
   except ValueError:
      last_item_id = 1
   
   if hasattr(args, 'func'):
      args.func(args, current_date, last_item_id, inventory)
   else:
      parser.print_help()
if __name__ == "__main__":
    main()