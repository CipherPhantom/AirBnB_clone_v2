#!/usr/bin/python3
"""
Unittest for console

This module contains the required tests for the specified file
"""
import unittest
import os
from io import StringIO
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from models import storage
from unittest.mock import patch
from console import HBNBCommand


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
def tearDownModule():
    FileStorage._FileStorage__objects = {}
    if os.path.exists("file.json"):
        os.remove("file.json")


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestDoCreateMethodFileStorage(unittest.TestCase):
    def setUp(self):
        FileStorage._FileStorage__objects = {}

    def testCreateState(self):
        cmd = 'create State name="Arizona"'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "State")
            self.assertEqual(obj.name, "Arizona")
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))

    def testCreatePlace(self):
        cmd = 'create Place city_id="0001" user_id="0001" \
               name="My_little_house" number_rooms=4 number_bathrooms=2 \
               max_guest=10 price_by_night=300 latitude=37.773972 \
               longitude=-122.431297'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "Place")
            self.assertEqual(obj.max_guest, 10)
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))

    def testCreateCity(self):
        cmd = 'create City state_id="95a5abab-aa65-4861-9bc6-1da4a36069aa" \
               name="San_Francisco"'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "City")
            self.assertEqual(obj.name, "San Francisco")
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))

    def testCreateUser(self):
        cmd = 'create User email="gui@hbtn.io" password="guipwd" \
               first_name="Guillaume" last_name="Snow"'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "User")
            self.assertEqual(obj.password, "guipwd")
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))

    def testCreateReview(self):
        cmd = 'create Review place_id="ed72aa02-3286-4891-acbc-9d9fc80a1103" \
               user_id="d93638d9-8233-4124-8f4e-17786592908b" \
               text="Amazing_place,_huge_kitchen"'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "Review")
            self.assertEqual(obj.text, "Amazing place, huge kitchen")
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))

    def testCreateAmenity(self):
        cmd = 'create Amenity name="Wifi"'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "Amenity")
            self.assertEqual(obj.name, "Wifi")
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))

    def testCreateBaseModel(self):
        cmd = 'create BaseModel'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "BaseModel")
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))
