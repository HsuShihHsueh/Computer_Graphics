# Project3

1. File Import

A. use pywavefront.Wavefront to import obj file
B. visualization.draw to display it
C. use np to import xyz file, return numpy.ndarray
there are three information about it
v(t) ：the car location on this point (t=t)
v(t-1)：the car location on last point (t=t-1)
dv ：the vector between v(t) v(t-1) two point
vt(t) ：the car's normal vector on this point (t=t)

2. count from 0 to max of route point(351) and routine
3. Transmation matrix for car (L48~55)
L30. scale the car size 
L29. rotate to X axis
L28. translate to right lane

dx = v(t) – v(t-1) 轉向 x 軸
vt (normal vector) 轉向 z 軸
vt, dv 的外積轉向 y 軸

4. Result
5. 
