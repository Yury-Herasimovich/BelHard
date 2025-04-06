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
        if not bool(re.fullmatch(r'[а-яА-ЯёЁ\s]+', v)):
            raise ValueError("Имя должно содержать только русские буквы")
        return v.title()
    
    @field_validator('login')
    def validate_login(cls, v):
        if not bool(re.fullmatch(r'^[a-zA-Z0-9_]+$', v)):
            raise ValueError("Логин может содержать только латинские буквы, цифры и подчеркивание")
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")
        if not any(c.isupper() for c in v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not any(c.isdigit() for c in v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return v

class UserLogin(BaseModel):
    login: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=100)