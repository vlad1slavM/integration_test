from api.inventory import inventory_update_batch
from api.price import price_update_batch
from models.inventory import InventoryModel
from models.price import PriceModel
from parsers import inventory_parser, price_parser


def send_items(api_method, formatter_method, items, token, batch_size=1000):
    total_items = len(items)
    num_batches = total_items // batch_size + 1

    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, total_items)
        batch = items[start_idx:end_idx]

        # Call the API method to send the batch of items
        items_formatted = formatter_method(items)
        api_method(items_formatted, token)


def inventory_formatter(items: list[InventoryModel]):
    inventory_items = []
    for item in items:
        data = {
            "store_ext_id": item.store_ext_id,
            "price_ext_id": item.price_ext_id,
            "snapshot_datetime": item.snap_datetime,
            "in_matrix": item.in_matrix,
            "qty": item.qty,
            "sell_price": item.sell_price,
            "prime_cost": item.prime_cost,
            "min_stock_level": item.min_stock_level,
            "stock_in_days": item.stock_in_days
        }
        inventory_items.append(data)
    return inventory_items


def price_formatter(items: list[PriceModel]):
    price_items = []
    for item in items:
        data = {
            "name": item.name,
            "params": {
                "extId": item.price_ext_id,
                "sku_id": item.price_ext_id,
                "categories": [
                    item.categories
                ],
                "price": item.price,
                "vat": item.vat
            }
        }
        price_items.append(data)
    return price_items


if __name__ == '__main__':
    inventory1_items = inventory_parser.parse('csv/inventory1.csv')
    inventory2_items = inventory_parser.parse('csv/inventory2.csv')
    send_items(inventory_update_batch, inventory_formatter, inventory1_items,
               'token')
    send_items(inventory_update_batch, inventory_formatter, inventory2_items,
               'token')
    price_items = price_parser.parse('csv/price.csv')
    send_items(price_update_batch, price_formatter, price_items, 'token')
