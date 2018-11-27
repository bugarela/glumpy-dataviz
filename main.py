import numpy as np
import pandas as pd
from glumpy import app, gl, gloo
from glumpy.transforms import PanZoom

df = pd.read_csv(
    'data/sp.csv', parse_dates=['mdct'], index_col=['mdct']).drop(columns=['Unnamed: 0'])
# df[df['city'] == 'São Paulo'].reindex(
#     columns=['mdct', 'temp']).to_csv('sp.csv')

frequencies = ['H', '12H', 'D', 'W', '15D', 'M', '3M']
periods = [8784, 732, 366, 52, 26, 12, 4]


def get_temps(i):
    temps = []

    for year in range(2006, 2017):
        idx = pd.date_range(str(year) + '-1-1',
                            periods=periods[i], freq=frequencies[i])
        data = df[df.index.year == year]
        data = data.reindex(idx, fill_value=0)
        temps.append(data)
    return temps


temps = []
for i in range(len(frequencies)):
    temps.append(get_temps(i))

window = app.Window(width=1024, height=512)

quad_vertex = """
attribute vec2 position;
void main (void) { gl_Position = vec4(position,0,1); }
"""
quad_fragment = """
void main(void) { gl_FragColor = vec4(1,1,1,1.0/10.0); }
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

    n = periods[frequency]
    line = gloo.Program(line_vertex, line_fragment, count=n)
    line["position"][:, 0] = np.linspace(-1, 1, n)

    if time >= len(temps):
        time = 0

    line["position"][:, 1] = temps[frequency][int(time)]['temp'] / 20.0 - 1
    time += acc

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


@window.event
def on_key_press(key, modifiers):
    global frequency
    global acc

    if key == app.window.key.UP:
        frequency = min(frequency+1, len(frequencies)-1)
    if key == app.window.key.DOWN:
        frequency = max(frequency-1, 0)

    if key == app.window.key.RIGHT:
        acc = min(acc*2, 1)
    if key == app.window.key.LEFT:
        acc /= 2.0


quad = gloo.Program(quad_vertex, quad_fragment, count=4)
quad['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]

time = 0
frequency = 0
acc = 0.05
app.run()
