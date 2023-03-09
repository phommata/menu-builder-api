from datetime import datetime

from marshmallow_sqlalchemy import fields

from config import db, ma


class ItemModifier(db.Model):
    __tablename__ = 'item_modifier'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(
        db.Integer, 
        db.ForeignKey('item.id'), 
    )
    modifier_id = db.Column(
        db.Integer, 
        db.ForeignKey('modifier.id'), 
    )


class ItemModifierSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModifier
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Modifier(db.Model):
    __tablename__ = "modifier"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, unique=True, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class ModifierSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Modifier
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    modifiers = db.relationship(
        Modifier,
        secondary='item_modifier',
        backref="item",
        order_by="desc(Modifier.timestamp)",
    )


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True
        sqla_session = db.session
        include_fk = True
        include_relationships = True

    modifiers = fields.Nested(ModifierSchema, many=True)

class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String(32), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    items = db.relationship(
        Item,
        backref="section",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Item.timestamp)",
    )


class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Section
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    items = fields.Nested(ItemSchema, many=True)


item_modifier_schema = ItemModifierSchema()
item_modifiers_schema = ItemModifierSchema(many=True)
modifier_schema = ModifierSchema()
modifiers_schema = ModifierSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
section_schema = SectionSchema()
menu_schema = SectionSchema(many=True)
