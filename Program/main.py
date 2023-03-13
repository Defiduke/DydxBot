# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import  construct_market_prices

#Connect to client
try:
    print("Connecting to clients")
    client =connect_dydx()
except Exception as e:
    print(e)
    print("Error connecting to client",e)
    exit(1)

#Abort all open positions

if ABORT_ALL_POSITIONS:
    try:
        print("Closing all positions")
        close_orders= abort_all_positions(client)
    except Exception as e:
        print(e)
        print("Error closing all positions", e)
        exit(1)

#Find Cointegrated pairs
if FIND_COINTEGRATED:
    try:
        print("Fetching market prices can take upto 3 minutes")
        df_market_prices=construct_market_prices(client)
    except Exception as e:
        print(e)
        print("Error constructing market prices", e)
        exit(1)





