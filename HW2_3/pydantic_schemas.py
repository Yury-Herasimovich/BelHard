from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class UserRegister(BaseModel):
    username: str = Field(min_length=2, max_length=30)
    login: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    age: int = Field(gt=0, lt=120)
    
    @field_validator('username')
    def validate_username(cls, v):
        if not bool(re.fullmatch(r'[а-яА-ЯёЁa-zA-Z\s]+', v)):
            raise ValueError("Name must have only letters")
        return v.title()
    
    @field_validator('login')
    def validate_login(cls, v):
        if not bool(re.fullmatch(r'^[a-zA-Z0-9_\s]{3,20}$', v)):
            raise ValueError("Password must have only latin letters, digits and underscores.")
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must have at least 8 symbols")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must have at least one capital letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must have at least one digit")
        return v

class UserLogin(BaseModel):
    login: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=100)