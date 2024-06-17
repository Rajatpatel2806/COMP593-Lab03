import sys
import os
import pandas as pd
from datetime  import datetime

# Get path of sales data CSV file from the command line
def main():
    sales_csv = get_sales_csv()
    orders_dir = create_orders_dir(sales_csv)
    process_sales_data(sales_csv, orders_dir)



def get_sales_csv(): # Check whether command line parameter provided
    if len(sys.argv) != 2:
        print("Error: Wrong Command line parameter Provided")
        sys.exit(1)
    
    sales_csv = sys.argv[1]  # Check whether provide parameter is valid path of file
    if not os.path.isfile(sales_csv):
        print(f"Error: The file '{sales_csv}' does not exist. Provide proper File.")
        sys.exit(1)
    
    return sales_csv
    

# Create the directory to hold the individual order Excel sheets
def create_orders_dir(sales_csv):
    sales_dir = os.path.dirname(sales_csv)                         # Get directory in which sales data CSV file resides
    today_date = datetime.today().strftime('%Y-%m-%d')
    orders_dir = os.path.join(sales_dir, f"Orders_{today_date}")   # Determine the name and path of the directory to hold the order data files
    
    if not os.path.exists(orders_dir):                             # Create the order directory if it does not already exist
        os.makedirs(orders_dir)
    
    return orders_dir
   

# Split the sales data into individual orders and save to Excel sheets
def process_sales_data(sales_csv, orders_dir):                                             # Import the sales data from the CSV file into a DataFrame
    sales_data = pd.read_csv(sales_csv)
    sales_data['TOTAL PRICE'] = sales_data['ITEM QUANTITY'] * sales_data['ITEM PRICE']     # Insert a new "TOTAL PRICE" column into the DataFrame
    
    order_ids = sales_data['ORDER ID'].unique()                                            # Remove columns from the DataFrame that are not needed
    
    for order_id in order_ids:                                                             # Group the rows in the DataFrame by order ID
        order_data = sales_data[sales_data['ORDER ID'] == order_id]
        order_data = order_data.sort_values(by='ITEM NUMBER')
        
        total_price = order_data['TOTAL PRICE'].sum()
        total_row = pd.DataFrame([['', '', '', '', '', 'Total', total_price]], columns=order_data.columns)
        order_data = pd.concat([order_data, total_row], ignore_index=True)
        

    # For each order ID:
        # Remove the "ORDER ID" column
        # Sort the items by item number
        # Append a "GRAND TOTAL" row
        # Determine the file name and full path of the Excel sheet
        # Export the data to an Excel sheet
        # Format the Excel sheet (
        # Define format for the money columns
        # Format each colunm
        # close the sheet



if __name__ == '__main__':
    main()