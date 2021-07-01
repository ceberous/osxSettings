#!/usr/bin/env python3
import sys
import urllib
import requests
from pprint import pprint

# curl -H "Accept: application/vnd.github.mercy-preview+json" https://api.github.com/search/repositories?q=topic:magenta+topic:deep-learning+topic:music | jq ".items[] | {url:.url, description:.description
def get_topics( topic_list ):
	headers = { 'Accept': 'application/vnd.github.mercy-preview+json' }
	query_string = ""
	for index , topic in enumerate( topic_list ):
		query_string += f"topic:{topic} "
	query_string = urllib.parse.quote( query_string )
	# params = (
	#     ('q', query_string ),
	# )
	#response = requests.get( 'https://api.github.com/search/repositories/' , headers=headers , params=params )
	response = requests.get( f'https://api.github.com/search/repositories?q={query_string}' , headers=headers )
	response.raise_for_status()
	return response.json()

# https://gist.github.com/usametov/af8f13a351a66fb05a9895f11417dd9d
if __name__ == "__main__":
	results = get_topics( sys.argv[1:] )
	for index , result in enumerate( results["items"] ):
		print( f"{index} === {result['html_url']}" )