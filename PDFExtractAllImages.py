#!/usr/bin/env python3
# pip install tqdm pdfminer.six Pillow
import io
import sys
import os
import subprocess
from pathlib import Path
from tqdm import tqdm
from pprint import pprint

from pdfminer.high_level import extract_pages
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import resolve1

from PIL import Image

# def run_bash_command( commands ):
# 	try:
# 		# https://docs.python.org/3/library/subprocess.html
# 		result = subprocess.run( commands , cwd=os.getcwd() , shell=False , capture_output=True , universal_newlines=True )
# 		if result.returncode != 0:
# 			print( result.stderr )
# 			return result.stderr
# 		else:
# 			print( result.stdout )
# 			return result.stdout
# 	except Exception as e:
# 		print( e )
# 		return False

def run_bash_command( bash_command ):
	try:
		p = subprocess.Popen( bash_command , stdout=subprocess.PIPE , stderr=subprocess.STDOUT )
		print( iter( p.stdout.readline , b'' ) )
	except Exception as e:
		print( e )
		return False

def save_lt_figures( pdf_file_path ):

	# 1.) Open and Get Metadata
	pdf_file_path_posix = Path( pdf_file_path )
	output_directory = pdf_file_path_posix.parent.joinpath( f"{pdf_file_path_posix.stem}-Images" )
	output_directory.mkdir( parents=True , exist_ok=True )
	file = open( pdf_file_path , "rb" )
	parser = PDFParser( file )
	document = PDFDocument( parser )
	total_pages = resolve1( document.catalog[ "Pages" ] )[ "Count" ]

	# 2.) Rate-Limiting Step , Find Page Layouts
	page_layouts = []
	generator = extract_pages( pdf_file_path )
	print( "Scanning Page Layouts" )
	for page_layout in tqdm( generator , total=total_pages ):
		page_layouts.append( page_layout )

	# 3.) Iterate Each Element in the Page Layout
	# We only care about LTFigures apparently?
	# You could probably make LTCurves construct images
	for page_layout_index , page_layout in enumerate( page_layouts ):
		images = []
		paragraphs = []
		for element_index , element in enumerate( page_layout ):
			class_name = type( element ).__name__
			if class_name == "LTTextBoxHorizontal":
				pass
			elif class_name == "LTRect":
				pass
			elif class_name == "LTFigure":
				try:
					image = Image.open( io.BytesIO( element._objs[ 0 ].stream.rawdata ) )
					save_path = output_directory.joinpath( f"LTFigure - Page - {str( page_layout_index + 1 ).zfill( 3 )} - Element - {str( element_index + 1 ).zfill( 3 )}.jpeg" )
					print( save_path )
					image_info = {
						"type": "image" ,
						"width": element._objs[ 0 ].width ,
						"height": element._objs[ 0 ].height ,
						"bounding_box": {
							"x1": element._objs[ 0 ].x0 , "y1": element._objs[ 0 ].y0 ,
							"x2": element._objs[ 0 ].x1 , "y2": element._objs[ 0 ].y1 ,
						}
					}
					#pprint( image_info )
					image.save( save_path , format="JPEG" )
					return image_info
				except Exception as e:
					continue
			elif class_name == "LTCurve":
				pass
			elif class_name == "LTLine":
				pass
			else:
				print( class_name )

def convert_pdf_to_high_res_image( pdf_file_path ):
	# # https://stackoverflow.com/a/13784772
	pdf_file_path_posix = Path( pdf_file_path )
	output_directory = pdf_file_path_posix.parent.joinpath( f"{pdf_file_path_posix.stem}-Images" )
	output_directory.mkdir( parents=True , exist_ok=True )
	save_path = output_directory.joinpath( f"HighRes - {pdf_file_path_posix.stem}.jpeg" )
	run_bash_command( f'''convert -density 2000 -trim "{pdf_file_path}" -quality 100 "{str(save_path)}"''' )

def convert_pdf_to_images( pdf_file_path ):
	# # https://stackoverflow.com/a/13784772
	pdf_file_path_posix = Path( pdf_file_path )
	output_directory = pdf_file_path_posix.parent.joinpath( f"{pdf_file_path_posix.stem}-Images" )
	output_directory.mkdir( parents=True , exist_ok=True )
	#run_bash_command( f'''cd "{str(output_directory.absolute())}" && mkdir -p images && pdftoppm -jpeg -r 1200 "{pdf_file_path}" images/pg''' )

if __name__ == "__main__":
	save_lt_figures( sys.argv[1] )
	convert_pdf_to_high_res_image( sys.argv[1] )
	convert_pdf_to_images( sys.argv[1] )