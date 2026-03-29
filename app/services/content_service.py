from app.repositories.content_repository import *

def add_content(content):
    return create_content(content.dict())

def get_content():
    return get_all_content()