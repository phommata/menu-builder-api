from flask import abort, make_response

from config import db
from models import Item, Section, item_schema, items_schema

def read_all():
    items = Item.query.all()
    return items_schema.dump(items)

def read_one(item_id):
    item = Item.query.get(item_id)

    if item is not None:
        return item_schema.dump(item)
    else:
        abort(404, f"Item with ID {item_id} not found")


def update(item_id, item):
    existing_item = Item.query.get(item_id)

    if existing_item:
        update_item = item_schema.load(item, session=db.session)
        
        existing_item.section_id = update_item.section_id
        existing_item.name = update_item.name
        existing_item.description = update_item.description
        existing_item.price = update_item.price
        
        db.session.merge(existing_item)
        db.session.commit()
        return item_schema.dump(existing_item), 200
    else:
        abort(404, f"Item with ID {item_id} not found")


def delete(item_id):
    existing_item = Item.query.get(item_id)

    if existing_item:
        db.session.delete(existing_item)
        db.session.commit()
        return make_response(f"{item_id} successfully deleted", 204)
    else:
        abort(404, f"Item with ID {item_id} not found")


def create(item):
    existing_item = Item.query.filter(Item.name == item.get('name')).one_or_none()

    if existing_item:
        abort(422, f"Item name already exists: {item.get('name')}")
        
    section_id = item.get("section_id")
    section = Section.query.get(section_id)

    if section:
        new_item = item_schema.load(item, session=db.session)
        section.items.append(new_item)
        db.session.commit()
        return item_schema.dump(new_item), 201
    else:
        abort(404, f"Section not found for ID: {section_id}")
