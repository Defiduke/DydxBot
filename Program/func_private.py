import time
from datetime import datetime, timedelta
from pprint import pprint
from func_utils import format_number


# Place market order
def place_market_order(client, market, side, size, price, reduce_only):
    # Get position id
    account_response = client.private.get_account()
    position_id = account_response.data["account"]["positionId"]

    # get Expiration time
    server_time = client.public.get_time()
    expiration = datetime.fromisoformat(server_time.data["iso"].replace("Z", "")) + timedelta(seconds=70)

    # place as order
    placed_order = client.private.create_order(
        position_id=position_id,
        market=market,
        side=side,
        order_type="MARKET",
        post_only=False,
        size=size,
        price=price,
        limit_fee='0.015',
        expiration_epoch_seconds=time.time() + 70,
        time_in_force="FOK",
        reduce_only=reduce_only
    )
    return placed_order.data


def abort_all_positions(client):
    # Cancel all order

    client.private.cancel_all_orders()
    # delay
    time.sleep(0.5)
    # Get markets for ref
    markets = client.public.get_markets().data
    # delay
    time.sleep(0.5)
    pprint(markets)
    # get all open pos
    positions = client.private.get_positions(status="OPEN")
    all_positions = positions.data["positions"]
    close_orders = []
    if len(all_positions) > 0:
# Loop thru all pos
        for position in all_positions:
            # deter market
            market = position["market"]
            # determine side
            side = "BUY"
            if position["side"] == "LONG":
                side = "SELL"
            # Get price
            price = float(position["entryPrice"])
            accept_price = price * 1.7 if side == "BUY" else price * 0.3
            tickSize = markets["markets"][market]["tickSize"]
            accept_price = format_number(accept_price, tickSize)

            # Place market order to close
            order = place_market_order(client, market, side, position["sumOpen"], accept_price, True)
            # Closed orders
            close_orders.append(order)
            # Protect API
            time.sleep(0.2)
        # return closed orders
        return close_orders
