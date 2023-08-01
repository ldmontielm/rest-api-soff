from app.sales.adapters.sqlalchemy.sale import Sale, SalesOrders, Client

def saleSchema(sale: Sale) -> dict:
  return {
    "id": sale.id,
    "sale_date": sale.sale_date,
    "amount_order": sale.amount_order,
    "payment_method": sale.pyment_method,
    "id_client": sale.id_client,
    "total": sale.total,
    "type_sale": sale.type_sale,
    "status": sale.status
  }
  
def salesSchema(sales: list[Sale]) -> list:
  return [saleSchema(sale) for sale in sales]

def orderSchema(order: SalesOrders) -> dict:
  return {
    "sale_id": order.sale_id,
    "product_id": order.product_id,
    "amount_product": order.amount_product,
    "total": order.total
  }


def ordersSchema(orders: list[SalesOrders]) -> list:
  return [orderSchema(order) for order in orders]

def clientSchema(client: Client) -> dict:
  return  {
    "id": client.id,
    "name": client.name,
    "direction": client.direction,
    "phone": client.phone,
    "email": client.email
  }
  
def clientsSchema(clients: list[Client]) -> list:
  return [clientSchema(client) for client in clients]