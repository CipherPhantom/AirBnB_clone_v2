#!/usr/bin/python3
"""Defines a Place class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """Represents a place"""

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship(
            "Review",
            backref="place",
            cascade="all, delete-orphan")

    @property
    def reviews(self):
        """Gets the attribute"""
        reviews = models.storage.all("Review")
        return [review for review in reviews if review.place_id == self.id]
