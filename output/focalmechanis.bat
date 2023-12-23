gmt begin focalmechanis png 
	gmt basemap -R105.0/115.0/-12.0/-5.0 -JM20c -Ba
	gmt coast -Sazure -Glightgreen
	gmt makecpt -Cred,green,blue -T0,70,150,10000 -N
	gmt meca ../data/focalmechanis_gcmt.csv -Sd0.4c+f0 -C -W0.1p,gray50
gmt end 