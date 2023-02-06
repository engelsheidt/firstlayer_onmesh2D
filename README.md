# firstlayer_onmesh2D
Python script that plots(2D) Klipper´s bed mesh z height nodes and the first layer of a gcode file on top of them.

The script parses your printer.cfg and a problem.gcode to plot (2D)  a Klipper´s bed mesh´s z height nodes and the first layer of your problem.gcode to help you find problem zones your bed may have if you encounter dificulties adjusting your first layer height after automatic bed leveling and global z offset adjust.


Instructions:


Rename your filename.gcode to problem.gcode

Run the script by:

1)  Open and run it using your favorite IDE

2)  Open and run(F5) it using IDLE (64 bit)

3) Using powershell(as admin) , cd into the directory that contains the script, printer.cfg and
problem.cfg then execute py -3 .\firstlayer_onmesh2D.py or python3 .\firstlayer_onmesh2D.py

Notes:

The script parses printer.cfg to find mesh_min, mesh_max , your default bed mesh´s y_count, x_count and the z heights of the nodes that define your bed mesh.

If you wish to load a different bed mesh , you need to open the script and change the bed mesh´s default name to the new one:

	tag = '#*# [bed_mesh default]'
	
  tag = '#*# [bed_mesh your_mesh]'



The script parses your problem.gcode to find start_tag = ';WIDTH:' , end_tag =  ';LAYER_CHANGE' and generates gx and gy, lists that contain your first layer instructions.

If you do not use Superslicer , analyze your gcode file to find appropiate starting and finishing flags and edit the strings on the GCODE file parser section of the script first.

The script uses the data obtained to plot the top view of the selected bed mesh , the z height of the nodes that define that mesh, and the first layer of your problem.gcode.

The script does not take into consideration any offsets. It is up to you to analyze the results of your physical first layer and decide if it´s necessary or not to edit the z heights of the nodes of your bed mesh inside printer.cfg, or specify new problem zones.



