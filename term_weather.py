#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-07-27 21:26:53
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2017-07-27 22:13:22

# TOD LIST
# Get coordinates from IP
# Fetch coordinates from YR
# Parse return data
# Match wheater description to icons 
# Check internet connection in a strict way

import fire
import geoip2.database
# from urllib2 import Request, urlopen, URLError
from requests import get


class Location(object):
	def __init__(self):
		self.reader = geoip2.database.Reader('conf/GeoLite2-City.mmdb')
		self.latitude = None
		self.longitude = None

	def getIP(self):
		ip = get('https://api.ipify.org').text
		return ip

	def getCoordinates(self):
		ip = self.getIP()
		print(self.reader.city(ip))


class TermWeather(object):
	
	def fetch(self, town):
		print(town)
		location = Location()
		location.getCoordinates()

if __name__ == '__main__':
	fire.Fire(TermWeather())