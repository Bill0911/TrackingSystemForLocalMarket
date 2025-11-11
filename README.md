SuperPy: Inventory & Sales Tracker
This is a command-line application named SuperPy designed for tracking product inventory and sales for a local market.

Instead of a database, it uses simple CSV files (bought.csv and sold.csv) to log all transactions. The application also simulates time by reading and writing to a current_date.txt file, allowing you to move time forward for reporting purposes.

Core Features
buy: Add new products to the inventory. This logs the product name, price, and expiration date into bought.csv.

sell: Record a product sale. This checks against the inventory and adds a record to sold.csv.

report: Generate reports on either:

Inventory: Shows products in stock that were bought on a specific date (e.g., today or yesterday).

Revenue: Calculates and displays the total revenue from sales on a specific date.

--advance-time: A utility command to change the application's "current date" by a specified number of days.

Dependencies
The script uses several standard Python libraries:

argparse for command-line argument parsing

csv for reading/writing data files

datetime for handling dates

texttable for displaying reports in the console

tkinter for showing pop-up message boxes
