from pydantic import BaseModel


class NjournalBase(BaseModel):
    url: str
    
class NjournalCreate(NjournalBase):
    pass

class Njournal(NjournalBase):
    id: int
    url: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True
