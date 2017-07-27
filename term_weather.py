#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-07-27 21:26:53
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2017-07-27 23:03:19

# TOD LIST
# Get coordinates from IP
# Fetch coordinates from YR
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
		self.lat = None
		self.long = None

	def getIP(self):
		ip = get('https://api.ipify.org').text
		return ip

	def getCoordinates(self):
		ip = self.getIP()
		ip_locaiton = self.reader.city(ip)

		self.lat = ip_locaiton.location.latitude
		self.long = ip_locaiton.location.longitude


class WeatherForcast(object):
	"""docstring for WeatherForcast"""
	def __init__(self, location):
		self.location = location

	def now(self):
		lat = self.location.lat
		long = self.location.long
		print(lat, long)

		weather = Yr(coordinates=(lat, long, 10))
		now = json.loads(weather.now(as_json=True))
		pprint(now)
		


class TermWeather(object):
	# Add now, forcast as args
	def auto(self):
		location = Location()
		location.getCoordinates()

		weatherForcast = WeatherForcast(location)
		weatherForcast.now()

if __name__ == '__main__':
	ssl._create_default_https_context = ssl._create_unverified_context
	
	fire.Fire(TermWeather())