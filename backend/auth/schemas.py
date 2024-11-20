from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class RegisterFormSchema(BaseModel):
    name: str
    email: str
    password: str
    password_again: str


class LoginFormSchema(BaseModel):
    name: str
    password: str
