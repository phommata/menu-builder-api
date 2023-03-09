from flask import abort, make_response

from config import db
from models import Section, menu_schema, section_schema


def read_all():
    menu = Section.query.all()
    return menu_schema.dump(menu)


def create(section):
    name = section.get("name")
    existing_section = Section.query.filter(Section.name == name).one_or_none()

    if existing_section is None:
        new_section = section_schema.load(section, session=db.session)
        db.session.add(new_section)
        db.session.commit()
        return section_schema.dump(new_section), 201
    else:
        abort(406, f"Section with name {name} already exists")


def read_one(section_id):
    section = Section.query.filter(Section.id == section_id).one_or_none()

    if section is not None:
        return section_schema.dump(section)
    else:
        abort(404, f"Section with ID: {section_id} not found")


def update(section_id, section):
    existing_section = Section.query.filter(Section.id == section_id).one_or_none()

    if existing_section:
        update_section = section_schema.load(section, session=db.session)
        
        existing_section.name = update_section.name
        existing_section.description = update_section.description
        
        db.session.merge(existing_section)
        db.session.commit()
        
        return section_schema.dump(existing_section), 200
    else:
        abort(404, f"Section with ID: {section_id} not found")


def delete(section_id):
    existing_section = Section.query.filter(Section.id == section_id).one_or_none()

    if existing_section:
        db.session.delete(existing_section)
        db.session.commit()
        return make_response(f"{section_id} successfully deleted", 204)
    else:
        abort(404, f"Section with ID: {section_id} not found")
