import  uuid
from typing import List
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from app.infrastructure.database import Base
    
class User(Base):
  __tablename__= "users"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4())
  name : Mapped[str]= mapped_column(String(60), nullable=False)
  email : Mapped[str]= mapped_column(String, nullable=True, unique=True)
  password : Mapped[str] = mapped_column(String, nullable= True )
  status : Mapped[bool] = mapped_column(Boolean, nullable=False , default=True)
  id_role: Mapped[str] = mapped_column(ForeignKey("roles.id"))
  role : Mapped["Role"] = relationship()
    
class Role(Base):
  __tablename__= "roles"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4())
  name : Mapped[str]= mapped_column(String(60), nullable=False)
  status : Mapped[bool] = mapped_column(Boolean, nullable=False , default=True)
  Permissions: Mapped[List["Association"]]= relationship()
    
class Permission(Base):
  __tablename__= "permissions"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4())
  name : Mapped[str]= mapped_column(String(60), nullable=False)
  
class Association(Base):
  __tablename__ ="permission_role"
  
  id_role : Mapped[str] = mapped_column(ForeignKey("roles.id"), primary_key=True)
  id_permission: Mapped[str] = mapped_column(ForeignKey(ForeignKey("pemissions.id"), primary_key=True))
  Permission: Mapped["Permission"] = relationship()