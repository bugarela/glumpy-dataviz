import numpy as np
import pandas as pd
from glumpy import app, gl, gloo
from glumpy.transforms import PanZoom

df = pd.read_csv(
    'data/sp.csv', parse_dates=['mdct'], index_col=['mdct']).drop(columns=['Unnamed: 0'])
# df[df['city'] == 'São Paulo'].reindex(
#     columns=['mdct', 'temp']).to_csv('sp.csv')


temps = []

for year in range(2006, 2017):
    idx = pd.date_range(str(year) + '-1-1', periods=366*24, freq='H')
    data = df[df.index.year == year]
    data = data.reindex(idx, fill_value=0)
    temps.append(data)

print(temps)


window = app.Window(width=1024, height=512)

quad_vertex = """
attribute vec2 position;
void main (void) { gl_Position = vec4(position,0,1); }
"""
quad_fragment = """
void main(void) { gl_FragColor = vec4(1,1,1,1.0/128.0); }
"""
line_vertex = """
attribute vec2 position;
void main (void) { gl_Position = vec4(position,0,1); }
"""
line_fragment = """
void main(void) { gl_FragColor = vec4(0,0,0,1); }
"""


@window.event
def on_draw(dt):
    global time

    if time >= len(temps):
        time = 0

    line["position"][:, 1] = temps[int(time)]['temp'] / 50
    time += 0.05

    quad.draw(gl.GL_TRIANGLE_STRIP)
    line.draw(gl.GL_LINE_STRIP)
    window.swap()
    quad.draw(gl.GL_TRIANGLE_STRIP)
    line.draw(gl.GL_LINE_STRIP)


@window.event
def on_init():
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_DST_ALPHA)


@window.event
def on_resize(width, height):
    window.clear()
    window.swap()
    window.clear()


n = 366*24
line = gloo.Program(line_vertex, line_fragment, count=n)
line["position"][:, 0] = np.linspace(-1, 1, n)

quad = gloo.Program(quad_vertex, quad_fragment, count=4)
quad['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]

time = 0
app.run()
