import imp
from database import engine, base
from models import User, Order

base.metadata.create_all(bind=engine)