#!/usr/bin/env python3
import sys
import os
import pwd
from pathlib import Path
import json

ALLOWED_EXTENSIONS = [ ".sublime-snippet" ]
USERNAME = pwd.getpwuid( os.getuid() )[ 0 ]
OUTPUT_BASE_PATH = Path.cwd().joinpath( "vscode-snippets" )
OUTPUT_BASE_PATH.mkdir( exist_ok=True , parents=True )

def write_text( file_path , text_lines_list ):
	#with open( file_path , 'a', encoding='utf-8' ) as f:
	with open( file_path , 'w', encoding='utf-8' ) as f:
		f.writelines( text_lines_list )

def read_text( file_path ):
	with open( file_path ) as f:
		# return f.read().splitlines()
		return f.read()

def write_json( file_path , python_object ):
	with open( file_path , 'w', encoding='utf-8' ) as f:
		json.dump( python_object , f , ensure_ascii=False , indent=4 )

def read_json( file_path ):
	with open( file_path ) as f:
		return json.load( f )

if __name__ == "__main__":
	BaseDirectoryPosixPath = Path( sys.argv[1] if len(sys.argv) > 1 else f"/Users/{USERNAME}/Library/Application Support/Sublime Text 3/Packages/User" )
	FilesPosixInBaseDirectory = BaseDirectoryPosixPath.glob( '**/*' )
	FilesPosixInBaseDirectory = [ x for x in FilesPosixInBaseDirectory if x.is_file() ]
	FilesPosixInBaseDirectory = [ x for x in FilesPosixInBaseDirectory if x.suffix in ALLOWED_EXTENSIONS ]
	for index , file in enumerate( FilesPosixInBaseDirectory ):
		file_name = file.stem
		sublime_snippet = read_text( str( file ) )
		contents = sublime_snippet.split( "<content><![CDATA[" )[ 1 ].split( "]]></content>" )[ 0 ]
		contents = "\n".join( [ x.rstrip() for x in contents.splitlines() if x.strip() ] ).split( "\n" )
		tab_trigger = sublime_snippet.split( "<tabTrigger>" )[ 1 ].split( "</tabTrigger>" )[ 0 ].strip()
# 		vscode_string = f'''"{file_name}": {{
# 	"prefix": "{tab_trigger}" ,
# 	"body": [
# 		{contents}
# 	] ,
# 	"description": "{file_name}"
# }}'''

		output_path = OUTPUT_BASE_PATH.joinpath( f"{file_name}.json" )
		json_data = {}
		json_data[ file_name ] = {
			"prefix": tab_trigger ,
			"body": contents ,
			"description": file_name
		}
		write_json( str( output_path ) , json_data )
