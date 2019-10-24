from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import geocoder
from urllib.parse import urljoin
import urllib.request
import json

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(100))

	def __init__(self, firstname, lastname, email, password):
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.setpassword(password)

	def setpassword(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.pwdhash,password)

class Place(object):
  def meters_to_walking_time(self, meters):
    # 80 meters is one minute walking time
    return int(meters / 80)  

  def wiki_path(self, slug):
    return urljoin("https://en.wikipedia.org/wiki/", slug.replace(' ', '_'))
  

  def query(self, address):
    
    print("address:", address)
    lat, lng = address.split(',')

    print("latitude and longitude are {}, {}".format(lat,lng))
    
    query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat, lng)
    g = urllib.request.urlopen(query_url)
    results = g.read()
    g.close()

    data = json.loads(results)
    
    places = []
    for place in data['query']['geosearch']:
      name = place['title']
      meters = place['dist']
      lat = place['lat']
      lng = place['lon']

      wiki_url = self.wiki_path(name)
      walking_time = self.meters_to_walking_time(meters)

      d = {
        'name': name,
        'url': wiki_url,
        'time': walking_time,
        'lat': lat,
        'lng': lng
      }

      places.append(d)

    return places