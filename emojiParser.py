#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-07-29 11:56:24
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2017-07-29 12:34:58

from fuzzywuzzy import process

weather_nouns = ['cleary sky', 'fair', 'cloudy', 'rain showers', 'rain', 'sleet',
	'sleet showers', 'snow showers', 'thunder', 'sleet', 'snow']

# Find the first word, if it is a noun or a adjective. 
# Remove the adjective and split if there is a AND
# Then match the first noun to list and add that emoji
# and then match the second to list and add that emoji 
# REGEX this bitch up

# Splits and lowers the condition text for easier parsing
def splitCondition(condition):
	condition = condition.lower()
	return condition.split()

# Trying to analyze the semantics of the condition text
def findConditionContext(condition_text):
	condition_expression = splitCondition(condition_text)

	# Iterate over each word and find what matches 100%
	for expression_value in condition_expression:
		noun_matches = process.extract(expression_value, weather_nouns)
		print(expression_value + ': ' + str(noun_matches))


def emojiParser(condition_text):
	findConditionContext(condition_text)


def main():
	emojiParser('Rain showers')


if __name__ == '__main__':
	main()