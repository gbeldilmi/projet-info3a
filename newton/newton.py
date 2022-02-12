import math
import random
import tool as G

def square( v):
	return v*v

def derivee( equation, X, iX):
	eps = 0.001
	X1= [ X[k] for k in range( 0, len( X))]; X1[iX] += eps
	X2= [ X[k] for k in range( 0, len( X))]; X2[iX] -= eps
	return  (equation( X1) - equation( X2))/ (2.*eps)

def vecteur( n, f):
	return [f(i) for i in range(0, n)]

def matrice( nl, nc, f):
	return vecteur( nl, (lambda l: vecteur( nc,  (lambda c: f(l, c)))))

def jacobien( fff, X):
	neq= len( fff); nx = len( X)
	if neq != nx:
		print( "bug in newton, nb inconnues different du nb equations"); return X
	return matrice( neq, nx, (lambda eq, ix: derivee( fff[eq], X, ix))) 
			
def pscal( U, V):
	assert( len(U)==len(V))
	s = 0.
	for k in range( 0, len( U)):
		s += U[k]*V[k]
	return s

def norme( X):
	return math.sqrt( pscal( X, X))

def transpose( M):
	return matrice( len(M[0]), len(M), (lambda l, c: M[c][l]))	

def gramschmit( M):
	nl= len( M)
	nc= len( M[0])
	for l1 in range( 0, nl-1):
		l1_l1= pscal( M[l1], M[l1])
		for l2 in range( l1+1, nl) :
			#enlever de la ligne l2 la projection orthogonale  de l2 sur l1
			t = pscal( M[l1], M[l2]) / l1_l1
			for c in range( 0, nc):
				M[l2][c] -= t*M[l1][c]
	return M

def solvelin( A, B):
	n= len(A)
	assert( len(A)==len(A[0]))
	assert( len(A)==len(B) )
	M=vecteur( n, (lambda l : A[ l ] + [ -B[l] ]))
	M = M + [vecteur( n+1, (lambda l: random.uniform(-10.,10)))]
	gramschmit( M)
	X= vecteur( n, (lambda c: M[n][c] / M[n][n]))
	return X

def eval_sys( fff, X):
	return vecteur( len(fff), (lambda l: (fff[l])( X) ))

def newton( handle_user, fff, X0, dessine):
	epsilon= 10**(-6)
	X= X0 ; date=0; dessine( handle_user, fff, X, date)
	while True :
		#F_X = [ (fff[l])( X) for l in range(0, len(fff)) ]
		F_X = eval_sys( fff, X)
		J_X = jacobien( fff, X)
		D_X = solvelin( J_X, F_X )
		X_next= [ X[k]-D_X[k] for k in range( 0, len(X)) ]
		X = X_next ; date += 1
		dessine( handle_user, fff, X, date)
		if norme( F_X) < epsilon or norme( D_X) < epsilon or date>=40:
			return X

def dessin_debug( handle_user, fff, X, t):
	print("iteration: "+str(t)+ " X="+str(X)+" F(X)="+str( eval_sys(fff, X))+" ||F(X)||="+str( norme( eval_sys(fff, X))))

sys0= [ (lambda X: square( X[0]) - 2.) ]
newton( None, sys0, [1.],  dessin_debug)

#un systeme lineaire
sys1= [ (lambda X: X[0]+2*X[1]-30), (lambda X: 2*X[0]+3*X[1]-50) ]
newton( None, sys1, [0.,0.], dessin_debug) 


#carre de la distance
def carre_dist( a, b) :
	(xa,ya)=a; (xb,yb)=b
	return square( xa-xb) + square( ya-yb)

#distance entre 2 points en 2D
def dist_pp( p1, p2):
	(x1,y1)=p1; (x2,y2)=p2
	return math.sqrt( carre_dist( p1, p2))

# distance de p à la droite passant par les 2 points a=(xa,ya) et b=(xb,yb)
def v_mod_u( v, u): #retourne le vecteur v modulo u, qui est orthogonal à u
	k= pscal( u, v) / pscal( u, u)
	return vecteur( len( v), (lambda i: v[i]-k*u[i]))

def dist_c_ab( c, a, b):
	(xa,ya)=a; (xb,yb)=b; (xc,yc)=c
	ab=[xb-xa, yb-ya] ; ac=[xc-xa,yc-ya]
	reste= v_mod_u( ac, ab) 
	return math.sqrt( pscal( reste, reste))

#dist_pp( (1, 2), (5, 9))
#dist_c_ab( (2.,1.), (-10.,0.), (20.,0.))
	
def ex1():
	a=(10, 20); b=(300, 20); c=(100, 350)
	centre_init = ( (a[0]+b[0]+c[0])/3., (a[1]+b[1]+c[1])/3.)
	rayon_init = dist_pp( centre_init, a)
	X_init= ( centre_init[0], centre_init[1],  rayon_init)
	fff= [   (lambda X: carre_dist( (X[0],X[1]), a) - X[2]*X[2]), \
                 (lambda X: carre_dist( (X[0],X[1]), b) - X[2]*X[2]), \
                 (lambda X: carre_dist( (X[0],X[1]), c) - X[2]*X[2]) ]
	handle_user= None
	return newton( handle_user,  fff, X_init, dessin_debug)

#	#-------------------------------------------------
#	# ma librairie graphique...
#	from tkinter import *
#	import time
#	
#	current_color={}
#	
#	def open_graph( w, h):
#		ca= Canvas( Tk(), width=w, height=h); 
#		ca.pack()
#		return ca
#	
#	def draw_pdf( ca, name):
#		#ca.writePDFfile( name)
#		ca.postscript(file="IMG/"+name+".ps", colormode='color')
#		#process = subprocess.Popen(["ps2pdf", "tmp.ps", "result.pdf"], shell=True)
#	
#	def set_color( ca, name):
#		current_color[ca]=name
#	
#	def get_color( ca):
#		if ca in current_color:
#			return current_color[ca]
#		return "black"
#	
#	def draw_clear( ca):
#		ca.delete('all')
#	
#	def draw_line( ca, x1, y1, x2, y2):
#		ca.create_line( x1, y1, x2, y2, fill=get_color( ca))
#	
#	def draw_cercle( ca, x, y, r):
#		ca.create_oval( x-r,y-r, x+r,y+r, outline=get_color( ca))
#	
#	def fill_cercle( ca, x, y, r) :
#		ca.create_oval( (x-r,y-r), (x+r,y+r), fill=get_color( ca)) #pas de couleur rvb...get_color( ca)
#	
#	def draw_rect( ca, x1, y1, x2, y2):
#		ca.create_rectangle( x1, y1, x2, y2)
#	
#	def fill_rect( ca, x1, y1, x2, y2):
#		ca.create_rectangle( x1, y1, x2, y2, fill='black') #pas de couleur (r,v,b)...get_color( ca))
#	
#	def draw_refresh( ca):
#		ca.update()
#	
#---------------------------------------------------------------
#cercle par 3 points donnes

def dessin_graphic( handle_user, fff, X, t):
	a=(10, 20); b=(300, 20); c=(100, 350)
	(ca)= handle_user
	G.draw_clear( ca)
	x=X[0]; y=X[1]; rayon=X[2]
	G.draw_cercle( ca, x, y, rayon)
	G.draw_line( ca, a[0], a[1], b[0], b[1])
	G.draw_line( ca, a[0], a[1], c[0], c[1])
	G.draw_line( ca, b[0], b[1], c[0], c[1])
	G.fill_cercle( ca, a[0], a[1], 2)
	G.fill_cercle( ca, b[0], b[1], 2)
	G.fill_cercle( ca, c[0], c[1], 2)
	G.draw_refresh( ca)
	G.draw_pdf( ca, "dessin_"+str(t))
	input("continue newton ?")
	#draw_pdf( ca, "dessin_tmp" )
	#os.system( "./afficher.sh dessin_tmp.pdf &")


def ex1_graphic():
	a=(10, 20); b=(300, 20); c=(100, 350)
	centre_init = ( (a[0]+b[0]+c[0])/3., (a[1]+b[1]+c[1])/3.)
	rayon_init = dist_pp( centre_init, a)
	X_init= [ centre_init[0], centre_init[1],  rayon_init]
	fff= [   (lambda X: carre_dist( (X[0],X[1]), a) - X[2]*X[2]), \
		 (lambda X: carre_dist( (X[0],X[1]), b) - X[2]*X[2]), \
		 (lambda X: carre_dist( (X[0],X[1]), c) - X[2]*X[2]) ]
	ca= G.open_graph( 500, 500); handle_user=(ca)
	return newton( handle_user, fff, X_init, dessin_graphic)

#---------------------------------------------------------------
#cercle tangent à 3 droites

#def str_rgb( rgb) :    # rgb = (red, green,blue)  rend la chaine en hexadecimale correspondante
#	(r,g,b)=rgb
#	(r, g, b)= (int(r), int(v), int(b))
#	r= max( 0, min( 255, r)); v=max( 0, min( 255, v)); b=max( 0, min( 255, b))
#	return "#%02x%02x%02x" % (r,g,b)

def dessin_graphic_ex2( handle_user, fff, X, t):
	a=(100,100); b=(495,495); c=(250, 490)
	(ca)=handle_user
	G.draw_clear( ca)
	G.set_color( ca, G.str_rgb( (120,150,200) ))
	G.draw_line( ca, a[0], a[1], b[0], b[1])
	G.draw_line( ca, a[0], a[1], c[0], c[1])
	G.draw_line( ca, b[0], b[1], c[0], c[1])
	G.draw_cercle( ca, X[0], X[1], X[2])
	G.draw_refresh( ca)
	G.draw_pdf( ca, "dessin_"+str(t))
	input("continue newton ?")
	
def ex2_graphic():
	a=(100,100); b=(495,495); c=(250, 490)
	centre_init = ( (a[0]+b[0]+c[0])/3., (a[1]+b[1]+c[1])/3.)
	rayon_init=  (dist_pp( centre_init, a) + dist_pp( centre_init, b)+dist_pp( centre_init,c))/3.
	X_init= [centre_init[0], centre_init[1], rayon_init]
	fff= [   (lambda X: dist_c_ab( (X[0],X[1]), a, b)-X[2]),
	        (lambda X: dist_c_ab( (X[0],X[1]), b, c)-X[2]),
	        (lambda X: dist_c_ab( (X[0],X[1]), c, a)-X[2])]
	ca= G.open_graph( 500, 500); handle_user=(ca)
	return newton( handle_user, fff, X_init, dessin_graphic_ex2)

#---------------------------------------------------------------
#mettre 3 cercles tangents entre eux dans un triangle, et tangents aux cotes du triangle

def dessin_graphic_ex3( handle_user, fff, X, t):
	a=(10,20) ;  b=(495,10); c=(250, 490)
	(ca)=handle_user
	G.draw_clear( ca)
	G.set_color( ca, "black")
	G.draw_line( ca, a[0], a[1], b[0], b[1])
	G.draw_line( ca, a[0], a[1], c[0], c[1])
	G.draw_line( ca, b[0], b[1], c[0], c[1])
	G.set_color( ca, "red")
	G.draw_cercle( ca, X[0], X[1], X[2])
	G.draw_cercle( ca, X[3], X[4], X[5])
	G.draw_cercle( ca, X[6], X[7], X[8])
	G.set_color( ca, "black")
	G.draw_refresh( ca)
	G.draw_pdf( ca, "dessin_ex3_"+str(t))
	input("continue newton ?")

def ex3_graphic():
	a=(10,20) ;  b=(495,10); c=(250, 490)
	X_init= [ 30,30, 10, 300, 30, 10, 250, 200, 15]
	fff= [   (lambda X: dist_c_ab( (X[0],X[1]), a,b)-X[2]), \
		 (lambda X: dist_c_ab( (X[3],X[4]), a,b)-X[5]), \
		 (lambda X: dist_c_ab( (X[3],X[4]), b,c)-X[5]), \
		 (lambda X: dist_c_ab( (X[6],X[7]), b,c)-X[8]), \
		 (lambda X: dist_c_ab( (X[6],X[7]), c,a)-X[8]), \
		 (lambda X: dist_c_ab( (X[0],X[1]), c,a)-X[2]), \
		 (lambda X: carre_dist( (X[0],X[1]), (X[3],X[4])) - square( X[2]+X[5])), \
		 (lambda X: carre_dist( (X[3],X[4]), (X[6],X[7])) - square( X[5]+X[8])),\
		 (lambda X: carre_dist( (X[6],X[7]), (X[0],X[1])) - square( X[8]+X[2])) ]
	ca= G.open_graph( 500, 500); handle_user=(ca)
	return newton( handle_user, fff, X_init, dessin_graphic_ex3)

#---------------------------------------------------------------
ex1_graphic()
ex2_graphic()
ex3_graphic()
