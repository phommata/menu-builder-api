from flask import abort, make_response

from config import db
from models import ItemModifier, Modifier, Item, item_modifier_schema, item_modifiers_schema


def create(item_modifier):
    item, modifier = __validate(item_modifier)    

    item_modifier = ItemModifier(modifier_id=modifier.id, item_id=item.id)

    db.session.add(item_modifier)
    db.session.commit()

    return item_modifier_schema.dump(item_modifier), 201


def __validate(item_modifier):
    item_id = item_modifier.get('item_id')
    modifier_id = item_modifier.get('modifier_id')

    item = Item.query.get(item_id)
    modifier = Modifier.query.get(modifier_id)
    
    if not item:
        abort(404, f"Item not found for ID: {item_id}")

    if not modifier:
        abort(404, f"Modifier not found for ID: {modifier_id}")
        
    existing_item_modifier = ItemModifier.query.filter(ItemModifier.item_id == item_id).filter(ItemModifier.modifier_id == modifier_id).one_or_none()

    if existing_item_modifier:
        abort(422, f"Item modifier already exists")
    return item, modifier


def read_all():
    items_modifiers = ItemModifier.query.all()
    return item_modifiers_schema.dump(items_modifiers)


def read_one(item_modifier_id):
    existing_item_modifier = ItemModifier.query.get(item_modifier_id)

    if existing_item_modifier:
        return item_modifier_schema.dump(existing_item_modifier)
    else:
        abort(404, f"Item Modifier with ID {item_modifier_id} not found")


def update(item_modifier_id, item_modifier):
    existing_item_modifier = ItemModifier.query.get(item_modifier_id)
    
    if existing_item_modifier:
        __validate(item_modifier)
        update_modifier = item_modifier_schema.load(item_modifier, session=db.session)
        
        existing_item_modifier.item_id = update_modifier.item_id
        existing_item_modifier.modifier_id = update_modifier.modifier_id
        
        db.session.merge(existing_item_modifier)
        db.session.commit()
        return item_modifier_schema.dump(existing_item_modifier), 200
    else:
        abort(404, f"Item Modifier with ID {item_modifier_id} not found")


def delete(item_modifier_id):
    existing_item_modifier = ItemModifier.query.get(item_modifier_id)

    if existing_item_modifier:
        db.session.delete(existing_item_modifier)
        db.session.commit()
        return make_response(f"{item_modifier_id} successfully deleted", 204)
    else:
        abort(404, f"Item Modifier with ID {item_modifier_id} not found")
