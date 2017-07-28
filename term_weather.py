#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-07-27 21:26:53
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2017-07-28 13:58:43

# TODO LIST
# Get coordinates from IP ✔
# Fetch coordinates from YR ✔
# Convert coordinates to place name w/ google GeoCode api
# Parse return data
# Match weather description to icons 
# Check internet connection in a strict way

import fire, json, geoip2.database, ssl
from yr.libyr import Yr
from requests import get
from pprint import pprint


class Location(object):
	def __init__(self):
		self.reader = geoip2.database.Reader('conf/GeoLite2-City.mmdb')
		self.getIP()

	def getIP(self):
		ip = get('https://api.ipify.org').text
		self.ip = self.reader.city(ip)

	def getCoordinates(self):
		lat = self.ip.location.latitude
		long = self.ip.location.longitude
		return [lat, long]


class WeatherForcast(object):
	def __init__(self, area=None):
		# TODO search for area coordinates in a map
		self.area = area

	def now(self):
		location = Location()
		lat, long = location.getCoordinates()
		print('Coords: ', lat, long)
		print(' - - - - - - - - ')

		weather = Yr(coordinates=(lat, long, 10))
		now = json.loads(weather.now(as_json=True))

		temp = now['location']['temperature']
		print(temp['@value'] + ' ' + temp['@unit'])
		


class TermWeather(object):
	# Add now, forcast as args
	def auto(self):
		WeatherForcast.now(self)

	def fetch(self, area=None):
		weatherForcast = WeatherForcast(area)
		weatherForcast.now()
		

if __name__ == '__main__':
	ssl._create_default_https_context = ssl._create_unverified_context
	
	fire.Fire(TermWeather())