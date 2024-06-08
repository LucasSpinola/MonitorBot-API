from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    email: EmailStr = Field(default=None, title="email", description="email of the user")
    username: str = Field(default=None, title="username", description="username of the user")
    id_discord: str = Field(default=None, title="id_discord", description="id_discord of the user")
    password: str = Field(default=None, title="password", description="password of the user")

class UserLogin(BaseModel):
    email: EmailStr = Field(default=None, title="email", description="email of the user")
    password: str = Field(default=None, title="password", description="password of the user")
