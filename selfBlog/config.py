from environs import Env
from dataclasses import dataclass


@dataclass
class DataBase:
    name: str
    user: str
    password: str
    host: str
    port: int

@dataclass
class SocialAuth:
    vk_key: str
    vk_secret: str
    google_key: str
    google_secret: str

@dataclass
class SMTP:
    email_host: str
    email_host_user: str
    email_host_password: str
    email_port: int

@dataclass
class RedisDB:
    host: str
    port: int
    db: int

@dataclass
class Config:
    db: DataBase
    sauth: SocialAuth
    smtp: SMTP
    redis: RedisDB



def config(path=None):
    env = Env()
    env.read_env(path)

    return Config(db=DataBase(name=env('DB_NAME'),
                    user=env('DB_USER'),
                    password=env('DB_PASSWORD'),
                    host=env('DB_HOST'),
                    port=env.int('DB_PORT')),
                  sauth=SocialAuth(vk_key=env('VK_KEY'),
                                   vk_secret=env('VK_SECRET'),
                                   google_key=env('GOOGLE_KEY'),
                                   google_secret=env('GOOGLE_SECRET')),
                  smtp=SMTP(email_host=env('EMAIL_HOST'),
                            email_host_user=env('EMAIL_HOST_USER'),
                            email_host_password=env('EMAIL_HOST_PASSWORD'),
                            email_port=env.int('EMAIL_PORT')),
                  redis=RedisDB(host=env('REDIS_HOST'),
                                port=env.int('REDIS_PORT'),
                                db=env.int('REDIS_DB'))
                  )
