from enum import Enum
from pydantic import BaseModel
from typing import Optional

class StatusSale(str, Enum):
  OPEN = "open"
  PAID = "paid"
  CANCEL = "cancel"
  PENDING = "pending"

class SaleBase(BaseModel):
  id_client: Optional[str]
  payment_method: str
  type_sale: str
  
class Sale(SaleBase):
  id: Optional[str]
  sale_date: Optional[str]
  amount_orders: int = 0
  total: float = 0.0
  status: Optional[str] = StatusSale.OPEN
  
  class Config:
    from_attributes = True
    
class SaleCreate(SaleBase):
  pass




class OrderBase(BaseModel):
  sale_id: str
  product_id: str
  amount_product: int
  
class SalesOrdersCreate(OrderBase):
  pass

class SalesOrders(OrderBase):
  total: float = 0.0
  
  class Config:
    from_attributes = True
    


class ClientBase(BaseModel):
  name: str
  direction: str
  phone: str
  email: str
  
class ClientCreate(ClientBase):
  pass
  
class Client(ClientBase):
  id: Optional[str]
    
  class Config:
    from_attributes = True