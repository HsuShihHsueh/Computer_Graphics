## Project 2 - Transformations: Translation, Rotation, and Scaling of 3D model

### position p in 2D
<img src="https://latex.codecogs.com/svg.latex?\Large&space;\begin{bmatrix}x\\y\\1\end{bmatrix}" />

### Translation Matrix
<img src="https://latex.codecogs.com/svg.latex?\Large&space;\begin{bmatrix}1&0&T_x\\0&1&T_y\\0&0&1\end{bmatrix}" />

### Rotation Matrix
<img src="https://latex.codecogs.com/svg.latex?\Large&space;\begin{bmatrix}\cos(\theta)&\cos(\theta+\frac{\pi}{2})&0\\\sin(\theta)&\sin(\theta+\frac{\pi}{2})&0\\0&0&1\end{bmatrix}" />

### Scaling Matrix
<img src="https://latex.codecogs.com/svg.latex?\Large&space;\begin{bmatrix}S_x&0&0\\0&S_y&0\\0&0&1\end{bmatrix}" />

### Example： Scale x3, then Rotate 30degree, then Offset (12, 13)
<img src="https://latex.codecogs.com/svg.latex?\Large&space;\begin{bmatrix}x'\\y'\\1\end{bmatrix}=\begin{bmatrix}1&0&12\\0&1&13\\0&0&1\end{bmatrix}\begin{bmatrix}\cos(30\degree)&\cos(120\degree)&0\\\sin(30\degree)&\sin(120\degree)&0\\0&0&1\end{bmatrix}\begin{bmatrix}3&0&0\\0&3&0\\0&0&1\end{bmatrix}\begin{bmatrix}x\\y\\1\end{bmatrix}" />



## Demo：Clock Render by openGL
<img src="image/clock.gif" width=400><br>
👉 [Colab Link](https://colab.research.google.com/github/HsuShihHsueh/Computer_Graphics/blob/main/Project2/ClockByOpenGL.ipynb)
