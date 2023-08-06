from environs import Env
from dataclasses import dataclass


@dataclass
class DataBase:
    name: str
    user: str
    password: str
    host: str
    port: int


def db_config(path=None):
    env = Env()
    env.read_env(path)

    return DataBase(name=env('NAME'),
                    user=env('USER'),
                    password=env('PASSWORD'),
                    host=env('HOST'),
                    port=env('PORT'))
