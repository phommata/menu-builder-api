from flask import abort, make_response

from config import db
from models import Modifier, modifier_schema, modifiers_schema


def read_all():
    modifiers = Modifier.query.all()
    return modifiers_schema.dump(modifiers)


def read_one(modifier_id):
    modifier = Modifier.query.get(modifier_id)

    if modifier is not None:
        return modifier_schema.dump(modifier)
    else:
        abort(404, f"Modifier with ID {modifier_id} not found")


def update(modifier_id, modifier):
    existing_modifier = Modifier.query.get(modifier_id)

    if existing_modifier:
        update_modifier = modifier_schema.load(modifier, session=db.session)
        existing_modifier.description = update_modifier.description
        db.session.merge(existing_modifier)
        db.session.commit()
        return modifier_schema.dump(existing_modifier), 200
    else:
        abort(404, f"Modifier with ID {modifier_id} not found")


def delete(modifier_id):
    existing_modifier = Modifier.query.get(modifier_id)

    if existing_modifier:
        db.session.delete(existing_modifier)
        db.session.commit()
        return make_response(f"{modifier_id} successfully deleted", 204)
    else:
        abort(404, f"Modifier with ID {modifier_id} not found")


def create(modifier):
    description = modifier.get("description")
    
    existing_modifier = Modifier.query.filter(Modifier.description == description).one_or_none()

    if existing_modifier:
        abort(422, f"Modifier already exists")    

    new_modifier = modifier_schema.load(modifier, session=db.session)
    db.session.add(new_modifier)
    db.session.commit()

    return modifier_schema.dump(new_modifier), 201
