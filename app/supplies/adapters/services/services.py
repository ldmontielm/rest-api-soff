import uuid
from sqlalchemy import select, desc
from fastapi import status, HTTPException
from app.infrastructure.database import ConectDatabase
from app.supplies.domain.pydantic.supply import SupplyCreate, SupplyUpdate, SupplyDelete
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.products.adapters.serializers.product_schema import recipeDetailsSchema
from app.purchases.adapters.serializers.purchase_schema import ordersSchema
from app.products.adapters.sqlalchemy.product import RecipeDetail
from app.purchases.adapters.sqlalchemy.purchase import PurchasesOrders
from app.supplies.adapters.exceptions.exceptions import (
  notsupply,
  requiredsupply,
  notcreatedsupply,
  notdeletesupply,
  notupdatesupply,
  nameisalreadyexist,
  supplyassociated,
  changeunitmeasure
)
from sqlalchemy.exc import PendingRollbackError


session = ConectDatabase.getInstance()



def GetAllSupplies(limit:int, offset: int, status:bool=True):
  try:
    supplies = session.scalars(select(Supply).where(Supply.status == status).offset(offset).limit(limit).order_by(desc(Supply.name))).all()
    if not supplies:
        []
    return supplies
  
  except PendingRollbackError as e:
      session.rollback()


def GetOneSupply(id:str):
  
  try:
    supplies = session.get(Supply, id)
    if not supplies:
      notsupply()
    return supplies
  except PendingRollbackError as e:
      session.rollback()



def AddSupply(supply: SupplyCreate):
  try:
    if not supply:
      notcreatedsupply()

    if supply.unit_measure == "Gramos":
      # Convertir la cantidad a kilogramos y redondear a 3 decimales
      convertor = (supply.quantity_stock / 1000)
      supply.price = round((supply.price / 1000) / convertor, 2)

    if supply.unit_measure == "Kilogramos":
      supply.unit_measure = "Gramos"
      supply.quantity_stock = supply.quantity_stock * 1000
      # Redondear el precio a 2 decimales
      supply.price = round((supply.price / 1000), 2)

    if supply.name == "" or supply.price == "" or supply.quantity_stock == "" or supply.unit_measure == "":
      requiredsupply()

    supply_name = session.scalars(select(Supply.name)).all()
    if supply.name in supply_name:
      nameisalreadyexist()
    else:
      # Calcular el total y redondear a 2 decimales
      total = round((supply.price * supply.quantity_stock), 2)
      new_supply = Supply(name=supply.name, price=supply.price, quantity_stock=supply.quantity_stock, unit_measure=supply.unit_measure, total=total)

      session.add(new_supply)
      session.commit()
      session.refresh(new_supply)
      return new_supply
  except PendingRollbackError as e:
      session.rollback()

    
def UpdateSupply(id: str, supply_update: SupplyUpdate):
  try:
      supply_id_update = GetOneSupply(id)
      if not supply_id_update:
          requiredsupply()

      existing_supply = session.query(Supply).filter(
          Supply.name == supply_update.name, Supply.id != id).first()

      if existing_supply:
          nameisalreadyexist()

      if supply_id_update.unit_measure != supply_update.unit_measure:
          if supply_id_update.total == supply_update.total:
              if supply_id_update.quantity_stock == supply_update.quantity_stock:
                  changeunitmeasure()

      supply_id_update.name = supply_update.name
      supply_id_update.total = round(supply_update.total, 2)
      supply_id_update.quantity_stock = round(
          supply_update.quantity_stock, 0)  # Redondear a 0 decimales
      supply_id_update.price = round(
          supply_update.total / supply_update.quantity_stock, 2)
      supply_id_update.unit_measure = supply_update.unit_measure
      session.commit()
      session.refresh(supply_id_update)
      return supply_id_update

  except PendingRollbackError as e:
      session.rollback()
      
def DeleteSupply(id: str):
  try:
    supply = session.query(Supply).filter(Supply.id == uuid.UUID(id)).first()
    
    statement = select(RecipeDetail).where(RecipeDetail.supply_id == id)
    details = recipeDetailsSchema(session.scalars(statement).all())
    
    if details:
      supplyassociated()
      
    statement = select(PurchasesOrders).where(PurchasesOrders.supply_id == id)
    details = ordersSchema(session.scalars(statement).all())
    
    if details:
      supplyassociated()
    
    if not supply:
      notdeletesupply()
    session.delete(supply)
    session.commit()
    return supply
  except PendingRollbackError as e:
      session.rollback()


def UpdateStatusSupply(id:str):
  try:
    supply = session.get(Supply, uuid.UUID(id))
    if not supply:
      notupdatesupply()
    supply.status= not supply.status
    session.add(supply)
    session.commit()
    return supply
  except PendingRollbackError as e:
      session.rollback()


# def UpdateSupply(supply: SupplyUpdate):
#   if not supply:
#     raise HTTPException(status_code=status.HTTP_401_BAD_REQUEST, detail="supply not Updated")


# def DeleteSupply(supply: SupplyDelete):
#   if not supply:
#     raise HTTPException(status_code=status.HTTP_402_BAD_REQUEST, detail="supply not Delete")

def ConfirmSupply():
  pass


def ChangeState():
  pass