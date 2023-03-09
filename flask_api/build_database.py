from datetime import datetime

from config import app, db
from models import Modifier, Item, Section


MENU_ITEMS = [
    {
        "name": "Lunch Specials",
        "description": "Specials for lunch",
        "items": [
            {
                "name": "Sandwich Lunch",
                "description": "Meatball Sandwich",
                "price": 1.99,
                "timestamp": "2022-01-06 17:10:24",
            },
            {
                "name": "Soup Lunch",
                "description": "Tomato Soup",
                "price": 2.99,
                "timestamp": "2022-03-05 22:17:54",
                "modifiers": [
                    {
                        "id": 1, 
                        "description": "Extra Spicy"
                    },
                    {
                        "id": 2, 
                        "description": "Regular Spice"
                    },
                    {
                        "id": 3, 
                        "description": "No Spice"
                    },
                ]
            },
            {
                "name": "Half Sandwich Half Soup",
                "description": "Half Meatball Sandwich and Half Tomato Soup",
                "price": 3.99,
                "timestamp": "2022-03-05 22:18:10"
            },
        ],
    },
    {
        "name": "Dinner Specials",
        "description": "Specials for dinner",
        "items": [
            {
                "name": "Steak",
                "description": "Bone-in Ribeye",
                "price": 4.99,
                "timestamp": "2022-01-01 09:15:03",
            },
            {
                "name": "Lobster",
                "description": "Steamed Lobster",
                "price": 5.99,
                "timestamp": "2022-02-06 13:09:21",
            },
        ],
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for data in MENU_ITEMS:
        new_section = Section(
            name=data.get("name"), 
            description=data.get("description")
        )
        for item in data.get("items", []):
            item_modifiers = item.get("modifiers", [])
            item = Item(
                name=item.get('name'),
                description=item.get('description'),
                price=item.get('price'),
                timestamp=datetime.strptime(
                    item.get('timestamp'), "%Y-%m-%d %H:%M:%S"
                ),
            )

            for item_modifier in item_modifiers:
                item.modifiers.append(
                    Modifier(
                        id=item_modifier.get("id"),
                        description=item_modifier.get("description"),
                    )
                )

            new_section.items.append(item)
            
        db.session.add(new_section)
    db.session.commit()
