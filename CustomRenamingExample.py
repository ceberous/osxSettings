import requests
import json
import os
import sys
import unicodedata
import re
from titlecase import titlecase
from shutil import copyfile

# https://docs.python.org/3/library/pathlib.html#correspondence-to-tools-in-the-os-module

base_path = sys.argv[ 1 ]
output_directory_path = sys.argv[ 2 ]
os.makedirs( output_directory_path , exist_ok=True )

sorted_file_list_io_tuples = []
nameing_index = 0
def traverse_directory( base_path ):
	global nameing_index

	# Get All of 'This' Locations Directories
	sorted_dirs = [ f.name for f in os.scandir( base_path ) if f.is_dir() ]
	sorted_dirs.sort()
	sorted_dirs = [ os.path.join( base_path , directory ) for directory in sorted_dirs ]

	# Get All of 'This' Locations Files
	sorted_files = [ f.name for f in os.scandir( base_path ) if f.is_file() ]
	sorted_files = [ file for file in sorted_files if file.endswith( ".pdf" ) ]
	sorted_files.sort()
	sorted_files = [ os.path.join( base_path , directory ) for directory in sorted_files ]

	for index , file_path in enumerate( sorted_files ):
		folder_name = os.path.basename( os.path.dirname( file_path ) )
		#print( folder_name )
		#print( file_path )
		this_files_output_name = str( nameing_index ).zfill( 3 ) + " - " + folder_name + " - " + os.path.basename( file_path )
		this_files_output_path = os.path.join( output_directory_path , this_files_output_name )
		#print( this_files_output_path )
		sorted_file_list_io_tuples.append( ( file_path , this_files_output_path ) )
		nameing_index += 1

	for index , directory in enumerate( sorted_dirs ):
		traverse_directory( directory )


traverse_directory( base_path )

for index , item in enumerate( sorted_file_list_io_tuples ):
	print( item[ 1 ] )
	#renamed = os.path.splitext( item[ 1 ] )[0] + ".pdf"
	#print( renamed )
	#copyfile( item[ 0 ] , renamed )
	copyfile( item[ 0 ] , item[ 1 ] )
