gmt begin coba png 
	gmt basemap -R107.0/109.0/-9.0/-7.0 -JM20c -Ba
	gmt grdcontour @earth_relief_15s -A250 -C50 -Wathin,gray50 -Wcfaint,gray90
gmt end