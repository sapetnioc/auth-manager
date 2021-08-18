from uuid import UUID, uuid4

from fastapi import APIRouter
from pydantic import BaseModel, constr

router = APIRouter()


class NewAccount(BaseModel):
    login: constr(min_length=3, max_length=50)
    password: constr(min_length=8, max_length=50)
    first_name: constr(max_length=50)
    last_name: constr(max_length=50)


@router.post('/')
async def create_account(new_account: NewAccount) -> UUID:
    return uuid4()
