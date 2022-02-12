#-------------------------------------------------
# ma librairie graphique...

import math
import random
from tkinter import *
import time

current_color={}

def open_graph( w, h):
	ca= Canvas( Tk(), width=w, height=h); 
	ca.pack()
	return ca

def draw_pdf( ca, name):
	#ca.writePDFfile( name)
	ca.postscript(file="IMG/"+name+".ps", colormode='color')
	#process = subprocess.Popen(["ps2pdf", "tmp.ps", "result.pdf"], shell=True)

def clamp_255( valeur):
	return max( 0, min( 255, valeur))

def str_rgb( rgb) :    # rgb = (red, green,blue)  rend la chaine en hexadecimale correspondante
	(r,g,b)=rgb
	(r, g, b)= (int(r), int(g), int(b))
	r=clamp_255(r); g=clamp_255(g); b=clamp_255(b) 
	return "#%02x%02x%02x" % (r,g,b)

def set_color( ca, name):
	if type( name) is str:
		current_color[ca]=name
	elif type( name) is tuple and 3==len( name) :
		(r,g,b)=name
		if type(r) is int and type(g) is int and type( b) is int :
			current_color[ca]= str_rgb( (r,g,b))
	else:
		print( "error in tool.set_color, parameter is neither a string nor a truple of int")
		current_color[ca]="black"

#attention, retourne une chaine en hexadecimale #rrggbb
def get_color( ca):
	if ca in current_color:
		return current_color[ca]
	return "black"

def get_rgb( name_hexa):
	if type( name_hexa) is str :	
		red  = int( name_hexa[1]+name_hexa[2], 16)
		green= int( name_hexa[3]+name_hexa[4], 16)
		blue = int( name_hexa[5]+name_hexa[6], 16)
		return (red,green,blue)
	if type( name) is tuple and 3==len( name) :
		return name_hexa
	print( "error in tool.get_rgb: parameter is neither (r,g,b)  nor '#rrggbb' in Hexa")
	return (0,0,0)

def draw_clear( ca):
	ca.delete('all')

def draw_line( ca, x1, y1, x2, y2):
	ca.create_line( x1, y1, x2, y2, fill=get_color( ca))

def draw_cercle( ca, x, y, r):
	ca.create_oval( x-r,y-r, x+r,y+r, outline=get_color( ca))

def fill_cercle( ca, x, y, r) :
	ca.create_oval( (x-r,y-r), (x+r,y+r), fill=get_color( ca)) 

def draw_rect( ca, x1, y1, x2, y2):
	ca.create_rectangle( x1, y1, x2, y2, outline=get_color( ca))

def fill_rect( ca, x1, y1, x2, y2):
	ca.create_rectangle( x1, y1, x2, y2, fill=get_color( ca)) 

def draw_refresh( ca):
	ca.update()
