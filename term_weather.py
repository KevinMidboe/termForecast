#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-07-27 21:26:53
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2017-07-29 18:36:36

# TODO LIST
# Get coordinates from IP ✔
# Fetch coordinates from YR ✔
# Convert coordinates to place name w/ google GeoCode api ✔
# Parse return data
# Match weather description to icons ✔
# Check internet connection in a strict way
# Add table for time periode

import fire, json, geoip2.database, ssl
from yr.libyr import Yr
from requests import get
from pprint import pprint
from emojiParser import EmojiParser


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

	def getAreaName(self):
		lat, long = self.getCoordinates()
		coordinates = ','.join([str(lat), str(long)])
		areaURL = 'https://maps.googleapis.com/maps/api/geocode/json?&latlng='

		areaAPIResponse = json.loads(get(areaURL + coordinates).text)
		closestArea = areaAPIResponse['results'][0]['address_components']

		area = {}

		for item in closestArea:
			if 'route' in item['types']:
				area['street'] = item['long_name']

			if 'locality' in item['types']:
				area['town'] = item['long_name']

			if 'administrative_area_level_1' in item['types']:
				area['municipality'] = item['long_name']

			if 'country' in item['types']:
				area['country'] = item['long_name']

		return area


class WeatherForcast(object):
	def __init__(self, area=None):
		# TODO search for area coordinates in a map
		self.area = area
		self.symbol_table = {
			'Clear sky': '☀️',
			'Fair': '🌤',
			'Partly cloudy': '⛅️',
			'Cloudy': '☁️',
			
			'Light rain showers': '🌦',
			'Rain showers': '🌦 ☂️',
			'Heavy rain showers': '🌦 ☔️',
			
			'Light rain showers and thunder': '',
			'Rain showers AND thunder': '',
			'Heavy rain showers and thunder': '',
			
			'Light sleet showers': '',
			'Sleet showers': '',
			'Heavy sleet showers': '',
			
			'Light sleet showers and thunder': '',
			'Sleet showers and thunder': '',
			'Heavy sleet showers and thunder': '',
			
			'Light snow showers': '',
			'Snow showers': '',
			'Heavy snow showers': '',
			
			'Light snow showers and thunder': '',
			'Snow showers and thunder': '',
			'Heavy snow showers and thunder': '',
			
			'Light rain': '',
			'Rain': '',
			'Heavy rain': '',
			
			'Light rain and thunder': '',
			'Rain and thunder': '',
			'Heavy rain and thunder': '',
			
			'Light sleet': '',
			'Sleet': '',
			'Heavy sleet': '',
			
			'Light sleet and thunder': '',
			'Sleet and thunder': '',
			'Heavy sleet and thunder': '',
			
			'Light Snow': '',
			'Snow': '',
			'Heavy Snow': '',
			'Light snow and thunder': '',
			'Snow and thunder': '',
			'Heavy snow and thunder': '',
			'Fog': ''


		}
		self.name = None
		self.number = None
		self.variable = None

	def symbolVariables(self, symbol_obj):
		self.name = symbol_obj['@name']
		self.number = symbol_obj['@number']
		self.variable = symbol_obj['@var']

	def now(self):
		location = Location()
		self.area = location.getAreaName()
		# print('Area: ', self.area)
		# print(' - - - - - - - - ')

		# Create seperate function for formatting
		locationName = '/'.join([self.area['country'], self.area['municipality'], self.area['town'], self.area['street']])

		weather = Yr(location_name=locationName)
		now = json.loads(weather.now(as_json=True))
		
		self.symbolVariables(now['symbol'])

		emojiParser = EmojiParser(now['symbol']['@name'])
		print(emojiParser.convertSematicsToEmoji())
		temp = now['temperature']
		print(temp['@value'] + ' ' + temp['@unit'] + ' ' + self.symbol_table[self.name])

		


class TermWeather(object):
	# Add now, forcast as args
	def auto(self):
		weatherForcast = WeatherForcast()
		weatherForcast.now()

	def fetch(self, area=None):
		weatherForcast = WeatherForcast(area)
		weatherForcast.now()
		

if __name__ == '__main__':
	ssl._create_default_https_context = ssl._create_unverified_context
	
	fire.Fire(TermWeather())