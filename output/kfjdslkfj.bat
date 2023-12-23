gmt begin kfjdslkfj png 
	gmt basemap -R105.0/115.0/-9.0/-6.0 -JM20c -Ba
	gmt coast -Sazure -Glightgreen
	gmt  plot D:\my_drive\gmt_script\gmt_py_plotter/data/fault_sukamto2011 -W1p,black,solid -Sf+1i/0.2i+l+t
gmt end