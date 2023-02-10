#Compiled on IDLE 3.9.2 ( Python version 3.9.2)

import numpy as np
import matplotlib.pyplot as plt
import re

#---------------------------------------------------------------------------------------
# printer.cfg parser

tag_found = False
tag = '#*# [bed_mesh default]'
separator = ','
j=0
u=0

try:
    f = open('printer.cfg',encoding="utf8")
except:
    print('ERROR: printer.cfg not found in local directory')
    exit()

# Get mesh x,y dimensions

counter = 0


for line in f:
    
    if line.startswith('mesh_min:'):
        pattern = r"#\*#|\s|mesh_min\:|\="
        buf = re.sub(pattern, '', line)
        y_mesh_start = float(buf.split(separator, 1)[1])
        x_mesh_start = float(buf.split(separator, 1)[0])
        counter+=1
        
    if line.startswith('mesh_max:'):
        pattern = r"#\*#|\s|mesh_max\:|\="
        buf = re.sub(pattern, '', line)
        y_mesh_end = float(buf.split(separator, 1)[1])
        x_mesh_end = float(buf.split(separator, 1)[0])
        counter+=1
        
    if tag in line:
        tag_found = True
        tag = '%&/'
        print('Bed mesh´s name found !\n')
        
    if tag_found and 'y_count' in line:
        pattern = r"#\*#|\s|y_count|="
        buf = re.sub(pattern, '', line)
        mesh_y = int(buf)
        counter+=1
        
    if tag_found and 'x_count' in line:
        pattern = r"#\*#|\s|x_count|="
        buf = re.sub(pattern, '', line)
        mesh_x = int(buf)
        counter+=1

    if counter == 4:
        break

if tag_found == False:
    print('ERROR: Bed mesh´s name not found in printer.cfg')
    exit()

# Get mesh z heights

try:
    f = open('printer.cfg',encoding="utf8")
except:
    print('ERROR: printer.cfg not found in local directory')
    exit()

tag = '#*# [bed_mesh default]'
tag_found = False
pattern = r"#\*#|\s"
zb=np.zeros((mesh_x,mesh_y), dtype=float)


for line in f:
    
    if tag in line:
        tag_found = True
        #Do not edit this tag.
        tag = '%&/'
        
    if tag_found and ',' in line:
        buf = re.sub(pattern, '', line)
        j=0
        
        for i in buf.split(','):
            zb[u,j]=i
            j+=1
            
        u+=1
    if u == mesh_y:
        break


# printer.cfg parser end
#---------------------------------------------------------------------------------------

# GCODE file parser

try:
    f = open('problem.gcode',encoding="utf8")
except:
    print('ERROR: problem.gcode not found in local directory')
    exit()

#start_tag = ';TYPE:Skirt'
#start_tag ='; Internal perimeter'
start_tag = ';WIDTH:'
tag_found = False
#end_tag =';LAYER:1'
end_tag =';LAYER_CHANGE'
layer_tag=0
pattern = r"G1\sX|E.*$|\s|;.*$"
separator_e = 'Y'
gx = []
gy = []

for line in f:

    if start_tag in line:
        tag_found = True
        #Do not edit this start_tag.
        start_tag = '@€¬'
        
    #if tag_found and line.startswith(';LAYER_CHANGE'):
    if tag_found and line.startswith(end_tag):
        layer_tag += 1
    if layer_tag == 2:
        break
        
    if tag_found and line.startswith('G1 X') and "E" in line:
        if "F" in line:
            continue
        buf = re.sub(pattern, '', line)
        
        bufY = buf.split(separator_e, 1)[1]
        bufX = buf.split(separator_e, 1)[0]
        gx.append(float(bufX))
        gy.append(float(bufY))
        
if not tag_found:
    print ('ERROR: start_tag tag not found! \nAnalyze your problem.gcode and give me a valid start_tag')
    exit()

if layer_tag != 2:
    print('ERROR: end_tag not found! \nAnalyze your problem.gcode and give me a valid end_tag ')
    exit()



# GCODE parser end
#---------------------------------------------------------------------------------------

xb = []
yb = []

xb.append(round(x_mesh_start,1))
x_iterations = mesh_x - 1

x_delta = (x_mesh_end - x_mesh_start)/x_iterations
for i in range(x_iterations):
    x_mesh_start=round(x_mesh_start+x_delta,1)
    xb.append(x_mesh_start)

yb.append(y_mesh_start)
y_iterations = mesh_y - 1
y_delta = (y_mesh_end - y_mesh_start)/y_iterations
for i in range(y_iterations):
    y_mesh_start=round(y_mesh_start+y_delta,1)
    yb.append(y_mesh_start)


xb,yb = np.meshgrid(xb,yb)

fig = plt.figure()

plt.plot(gx,gy)
plt.plot(xb,yb , linewidth=0.1, marker='o',markersize=2)
plt.plot(np.transpose(xb), np.transpose(yb), linewidth=0.1)
plt.title('Klipper´s bed mesh grid & Z height nodes [mm]\n', fontweight ="bold")
plt.xlabel('X-FRONT',fontsize =12)
plt.ylabel('Y-LEFT',fontsize =12)

#[row,collumn]
#first_element = z[0,0]

for j in range (mesh_y):
    for i in range(mesh_x):
        plt.text(xb[i,j], yb[i,j], zb[i,j], color='black',fontsize =14)
#fig.canvas.manager.full_screen_toggle()
plt.show()

