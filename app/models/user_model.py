from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    email: EmailStr = Field(default=None, title="email", description="email of the user")
    password: str = Field(default=None, title="password", description="password of the user")

class UserLogin(BaseModel):
    email: EmailStr = Field(default=None, title="email", description="email of the user")
    password: str = Field(default=None, title="password", description="password of the user")
