#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-07-29 11:56:24
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2017-07-29 18:36:55

from fuzzywuzzy import process

# Find the first word, if it is a noun or a adjective. 
# Remove the adjective and split if there is a AND
# Then match the first noun to list and add that emoji
# and then match the second to list and add that emoji 
# REGEX this bitch up

symbol_table = {
	'clear sky': '☀️',
	'fair': '🌤',
	'partly cloudy': '⛅️',
	'cloudy': '☁️',
	'thunder': '⚡️',
	
	'rain showers': '🌦',
	'rain': '🌧',
	'sleet showers': '🌦 💦',
	'sleet': '🌨 💦',
	'snow showers': '⛅ ❄️',
	'snow': '🌨',

	'rain': '🌧',
	'sleet': '🌧',
	'snow': '🌨',

	'showers': '🌤'
	}

severity = {
		'rain': ['💧', ' ☂️', ' ☔️'],
		'sleet': [' 💦 ', ' 💧 ', ' 💧 💦 '],
		'snow': [' ❄️ ', ' ❄️ ❄️ ', ' ❄️ ❄️ ❄️ ']
		}

class EmojiParser(object):
	def __init__(self, condition_text):
		self.condition_expression = condition_text
		self.severity = None
		self.nouns = []

		self.weather_nouns = ['cleary sky', 'fair', 'cloudy', 'rain', 'rain showers', 'sleet',
			'sleet showers', 'snow showers', 'thunder', 'snow']
		self.weather_adjectives = {'light': 0, 'normal': 1, 'heavy': 2}

	def __str__(self):
	 	return str([self.condition_expression, self.severity, self.nouns])

	# Splits and lowers the condition text for easier parsing
	def splitCondition(self, condition):
		condition = condition.lower()
		return condition.split()

	def findAdjective(self, sentence=None):
		if sentence is None:
			sentence = self.condition_expression

		expression = self.splitCondition(sentence)
		for word in expression:
			if word in self.weather_adjectives:
				return word

		return None

	def severityValue(self):
		adjective = self.findAdjective()

		if adjective:
			self.severity = self.weather_adjectives[adjective]
		else:
			self.severity = self.weather_adjectives['normal']


	def removeAdjective(self):
		adjective = self.findAdjective()
		if adjective:
			expression = self.splitCondition(self.condition_expression)
			expression.remove(adjective)
			return ' '.join(expression)
		else:
			return self.condition_expression

	def findWeatherTokens(self):
		sentence = self.removeAdjective()
		
		if 'and' in sentence:
			self.nouns = sentence.split(' and ')
		else:
			self.nouns = [sentence]


	def emojify(self, noun):
		return symbol_table[noun]

	def emojifyList(self, noun_list):
		returnList = []
		
		for noun in noun_list:
			returnList.append(self.emojify(noun))

		return '  '.join(returnList)



	# Trying to analyze the semantics of the condition text
	def emojifyWeatherForecast(self):
		self.findWeatherTokens()
		
		noun_list = self.nouns

		primary_forcast = noun_list.pop(0)
		primary_severity = severity[primary_forcast][self.severity]
		secondary_forcast = self.emojifyList(noun_list)
		
		return ('%s %s  %s' % (self.emojify(primary_forcast), primary_severity, secondary_forcast))


	def convertSematicsToEmoji(self):
		self.severityValue()
		emojiForcast = self.emojifyWeatherForecast()
		return emojiForcast


def main():
	emojiParser = EmojiParser('Light rain')
	emojiParser.convertSematicsToEmoji()
	print(emojiParser)


if __name__ == '__main__':
	main()