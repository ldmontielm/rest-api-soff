from fastapi import status, HTTPException
from app.products.adapters.services.services import GetProductById, GetDetailsProduct
from app.supplies.adapters.services.services import GetOneSupply
from app.sales.domain.pydantic.sale_pydantic import (SalesOrdersCreate)
from app.supplies.domain.pydantic.supply import Supply
from app.products.domain.pydantic.product import RecipeDatail
from app.infrastructure.database import ConectDatabase
from app.supplies.adapters.sqlalchemy.supply import Supply as SupplySQLAlchemy
from app.sales.adapters.sqlalchemy.sale import SalesOrders
from app.sales.adapters.exceptions.exceptions import NoContentInOrder, OrderNotAvailability


session = ConectDatabase.getInstance()

def SupplyAvailability(supply:Supply, detail:RecipeDatail, amount_product: int) -> bool:
  if supply.quantity_stock < (detail.amount_supply * amount_product):
    return False
  return True

def UpdateStockSupply(supply: Supply, detail:RecipeDatail, amount_product: int):
  supply_obt = session.get(SupplySQLAlchemy, supply.id)
  supply_obt.quantity_stock = supply_obt.quantity_stock - (detail.amount_supply * amount_product)
  session.add(supply_obt)
  session.commit()
  session.refresh(supply_obt)
  return supply_obt

# OrderProcessing se encarga de verificar si la orden se puede realizar, debido a que se tiene que realizar
# un descuento del producto en stock.
def OrderProcessing(order: SalesOrdersCreate):
  if not order:
    NoContentInOrder()
  product = GetProductById(order.product_id)
  details = GetDetailsProduct(product.id)

  for detail in details:
    supply = GetOneSupply(detail.supply_id)
    availability = SupplyAvailability(supply, detail, order.amount_product)
    if availability == False:
      OrderNotAvailability()

  return order

def AddOrder(order: SalesOrdersCreate):
  product = GetProductById(order.product_id)
  total = product.sale_price *  order.amount_product
  order_sqlalchemy = SalesOrders(sale_id=order.sale_id, product_id=order.product_id, amount_product=order.amount_product, total=total)
  session.add(order_sqlalchemy)
  session.commit()
  session.refresh(order_sqlalchemy)
  return order_sqlalchemy