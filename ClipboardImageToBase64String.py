#!/usr/bin/env python3
import os
import time
import subprocess
from PIL import ImageGrab , Image
from pathlib import Path
import io
import codecs
import tempfile
import pyperclip

def run_bash_command( options ):
	try:
		result = subprocess.run( options , cwd=os.getcwd() , shell=False , capture_output=True , universal_newlines=True )
		if result.returncode != 0:
			return result.stderr
		else:
			return result.stdout
	except Exception as e:
		return False

def get_clipboard_image_windows():
	# https://www.devdungeon.com/content/grab-image-clipboard-python-pillow
	return ImageGrab.grabclipboard()


def get_clipboard_image_osx():
	# https://apple.stackexchange.com/a/375353
	# https://docs.python.org/3/library/tempfile.html#tempfile.gettempdir
	# https://docs.python.org/3/library/codecs.html#text-encodings
	# https://github.com/python-pillow/Pillow/issues/4097
	# https://www.devdungeon.com/content/grab-image-clipboard-python-pillow
	try:
		# image_data = run_bash_command([ "osascript" , "-e" , "get the clipboard as «class PNGf»" ])
		# image = Image.open( io.BytesIO( bytes( image_data , encoding='raw_unicode_escape' ) ) )
		# image.show()
		with tempfile.TemporaryDirectory() as temp_dir:
			temp_dir_posix = Path( temp_dir )
			with tempfile.NamedTemporaryFile( suffix='.png' , prefix=temp_dir ) as tf:
				temp_image_path = temp_dir_posix.joinpath( tf.name )
				print( temp_image_path )
				cmd = f'''/usr/bin/osascript -e \'tell application "get the clipboard as «class PNGf»"\' | xxd -r -p > "{temp_image_path}"'''
				subprocess.check_output( [ 'bash' ,'-c' , cmd ] )
				image = Image.open( temp_image_path )
				#image.show()
				img_bytes = io.BytesIO()
				image.save( img_bytes , format='PNG' )
				base64_string = codecs.decode( codecs.encode( img_bytes.getvalue() , "base64" ) , "ascii" )
				return base64_string.replace( '\n' , '' ).replace( '\r' , '' )
	except Exception as e:
		try:
			with tempfile.TemporaryDirectory() as temp_dir:
				temp_dir_posix = Path( temp_dir )
				with tempfile.NamedTemporaryFile( suffix='.jpeg' , prefix=temp_dir ) as tf:
					# temp_image_path = temp_dir_posix.joinpath( tf.name ).absolute()
					temp_image_path = temp_dir_posix.joinpath( tf.name )
					print( temp_image_path )
					cmd = f'''/usr/bin/osascript -e \'tell application "System Events" to get the clipboard as JPEG picture\' | sed "s/«data JPEG//; s/»//" | xxd -r -p > "{temp_image_path}"'''
					subprocess.check_output( [ 'bash' , '-c' , cmd ] )
					image = Image.open( temp_image_path )
					#image.show()
					img_bytes = io.BytesIO()
					# image.save( img_bytes , format='JPEG' )
					image.save( img_bytes , format='PNG' )
					base64_string = codecs.decode( codecs.encode( img_bytes.getvalue() , "base64" ) , "ascii" )
					return base64_string.replace( '\n' , '' ).replace( '\r' , '' )
		except Exception as e:
			# print( image_data )
			return False
	return False

def get_clipboard_image_linux():
	# https://stackoverflow.com/a/59862864
	#import tkinter
	# python3 -m pip install tk
	# brew install python-tk
	tk = tkinter.Tk()
	image_types = [ "png" , "jpeg" , "jpg" , "gif" ]
	for index , image_type in enumerate( image_types ):
		try:
			type_string = f'image/{image_type}'
			print( type_string )
			#test = tk.clipboard_get( type=f'image/{image_type}' )
			b = bytearray()
			h = ''
			for c in tk.clipboard_get( type=type_string ):
				print( c )
				if c == ' ':
					try:
						b.append( int( h , 0 ) )
					except Exception as e:
						print('Exception:{}'.format(e))
					h = ''
				else:
					h += c
			print( f"image type was {image_type}" )
			tk.destroy()
			return b
		except Exception as e:
			print( e )
			pass
	tk.destroy()
	return False

if __name__ == "__main__":
	image_b64_string = get_clipboard_image_osx()
	pyperclip.copy( f"![](data:image/png;base64,{image_b64_string})" )
	print( image_b64_string )