from enum import Enum
from pydantic import BaseModel
from typing import Optional



class UserBase(BaseModel):
    name : str
    email : str
    password : str
    id_role: str
    
        
class User(UserBase):
    id: Optional[str]
    status:bool = True
    
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass