import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from config import SQLALCHEMY_DATABASE_URI,SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy()

def setup_db(app, database_path=None):
    
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
    return db


def db_reset():
    db.drop_all()
    db.create_all()
    drink_water = Drinking(
        title='water lemon',
        recipe='[{"name": "water lemon", "color": "green", "parts": 1}]'
    )

    drink_lemonade = Drinking(
        title='lemonade',
        recipe='[{"name": "lemonade", "color": "blue", "parts": 1}]'
    )

    matel_water_lemon = Drinking(
        name='water lemon',
        density='100%'
    )

    ingredient_lemonade = Drinking(
        name='lemonade',
        density='80%'
    )

    new_property_water = Property.insert().values(
        drink_id=drink_water.id,
        ingredient_id=matel_water_lemon.id,
    )

    new_property_lemonade = Property.insert().values(
        drink_id=drink_water.id,
        ingredient_id=matel_water_lemon.id,
    )

    drink_water.insert()
    drink_lemonade.insert()
    matel_water_lemon.insert()
    ingredient_lemonade.insert()
    db.session.execute(new_property_water)
    db.session.execute(new_property_lemonade)
    db.session.commit()


Property = db.Table(
    'Property', db.Model.metadata,
    Column('drink_id', Integer, db.ForeignKey('drinks.id')),
    Column('ingredient_id', Integer, db.ForeignKey('metals.id'))
)

'''
Metal
'''


class Metals(db.Model):
    __tablename__ = 'metals'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    density = Column(String(4), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'density': self.density
        }



class Drinking(db.Model):
    __tablename__ = 'drinks'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True)
    recipe = Column(String(180), nullable=False)
    ingredients = db.relationship(
        'Metals',
        secondary=Property,
        backref=db.backref('drinks', lazy=True)
    )

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    def short(self):
        short_recipe = [{'color': r['color'], 'parts': r['parts']}
                        for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }
    
    def __repr__(self):
        return json.dumps(self.short())

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': self.recipe
        }
