import numpy as np

def generate_v(x,y,z):
	return "v {:.6f} {:.6f} {:.6f}\n".format(x,y,z)

def generate_vt(x,y):
	return "vt {:.6f} {:.6f}\n".format(x,y)	

def generate_vn(x,y,z):
	return "vn {:.6f} {:.6f} {:.6f}\n".format(x,y,z)

def generate_f(*f):
	if len(f)==3:
		return f"f {f[0]}/{f[0]}/{f[0]} {f[1]}/{f[1]}/{f[1]} {f[2]}/{f[2]}/{f[1]}\n"
	elif len(f)==4:
		return f"f {f[0]}/{f[0]}/1 {f[1]}/{f[1]}/1 {f[2]}/{f[2]}/1 {f[3]}/{f[3]}/1\n"
	else:
		raise
	
def generate(name):
	segment = 32
	ring = 16
	# create mtl file
	f = open(f"model/{name}.mtl", "w")
	text = '''
# Material Count: 1

newmtl None
Ns 500
Ka 0.8 0.8 0.8
Kd 0.8 0.8 0.8
Ks 0.8 0.8 0.8
d 1
illum 2
map_Kd 4K360_{:s}.JPG
	'''.format(name[0].upper())
	f.write(text)
	f.close()
	# create obj file
	f = open(f"model/{name}.obj", "w")
	f.write(f"mtllib {name}.mtl\n\n")
	# v
	for phi in np.linspace(0,1,ring):
		for theta in np.linspace(0,1,segment+1):
			z = np.cos(1/2*np.pi*phi)
			x = np.sin(1/2*np.pi*phi)*np.cos(2*np.pi*theta)
			y = np.sin(1/2*np.pi*phi)*np.sin(2*np.pi*theta)
			f.write(generate_v(100*x,100*y,-100*z))
	# vt
	for phi in np.linspace(0,1,ring):
		for theta in np.linspace(0,1,segment+1):
			x = np.sin(1/2*np.pi*phi)*np.cos(2*np.pi*theta)
			y = np.sin(1/2*np.pi*phi)*np.sin(2*np.pi*theta)		
			f.write(generate_vt(0.5+0.5*x,0.5+0.5*y))
	# vn
	for i in range(ring*(segment+1)):
		f.write(generate_vn(0,0,1))
	# f
	f.write('usemtl None\ns off\n')
	sp = segment + 1
	for j in range(ring-1):
		for i in range(segment):
			f.write(generate_f(i+j*sp+2,i+j*sp+1,i+(j+1)*sp+1,i+(j+1)*sp+2))
	f.close()

# generate('left_hemisphere')
# generate('right_hemisphere')