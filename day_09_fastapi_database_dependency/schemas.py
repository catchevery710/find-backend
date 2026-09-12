from pydantic import BaseModel, ConfigDict

##API 收到和返回的数据应该长什么样？
class UserCreate(BaseModel):
    name: str


class UserUpdate(BaseModel):
    name: str


class UserResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )