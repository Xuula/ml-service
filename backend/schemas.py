from dataclasses import dataclass

@dataclass
class Credentials:
    name: str
    email: str
    password: str

@dataclass
class PublicUserInfo:
    name: str
    idx: int
    email: str
    coins: int

@dataclass    
class User(PublicUserInfo):
    password: str

@dataclass    
class Session:
    session_idx: str