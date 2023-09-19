#!/usr/bin/python3
"""Defines an Amenity class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """Represents an amenity"""

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenties = relationship(
            "Place",
            secondary=place_amenity
            )
