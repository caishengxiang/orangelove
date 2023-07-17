# -*-coding:utf-8-*-
from dataclasses import dataclass, asdict


@dataclass
class User:
    jwt: str
    user_id: int


if __name__ == '__main__':
    user = User('111', 1)
    print(user.jwt)
    print(user.user_id)
