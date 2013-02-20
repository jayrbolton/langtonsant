# A simple and usable Langton's Ant implementation in python.

import pyglet, sys, random
from pyglet import window
from pyglet import clock
from pyglet import font

class Ant:

	def __init__(self,col,row,columns,rows):
		# Initial positions of the ant.
		self.columns = columns; self.rows = rows;
		self.col = col; self.row = row;

		# set random direction where 0: west, 1: north, 2: east, 3: south
		self.dir = random.choice([0,1,2,3])

		# the direction coordinate offsets; respectively: move west, north, east, or south
		self.dirs = ((-1,0), (0,1),(1,0), (0,-1))

	def turn(self, direction):
		# orient right (clockwise)
		if direction is 'right': self.dir = (self.dir + 1) % 4
		# orient left (counter-clockwise)
		elif direction is  'left': self.dir = (self.dir + 3) % 4
		# Move the ant forward one square
		self.forward()

	def forward(self):
		self.col = (self.col + self.dirs[self.dir][0]) % self.columns
		self.row = (self.row + self.dirs[self.dir][1]) % self.rows

class Grid(pyglet.window.Window):

	def __init__(self,cell_size=10): #n_ants):

		window.Window.__init__(self,fullscreen=True)

		# Initialize screen resolution
		self.cell_size = cell_size
		platform = pyglet.window.get_platform()
		display = platform.get_default_display()
		screen = display.get_default_screen()
		self.screen_width = screen.width
		self.screen_height = screen.height
		self.columns = self.screen_width / self.cell_size
		self.rows = self.screen_height / self.cell_size


		# Initialize ants
		self.ants = []
		# for nth_ant in range(1, n_ants+1):
		# 	ant = Ant(self.columns/2+nth_ant, self.rows/2+nth_ant, self.columns, self.rows)
		# 	self.ants.append(ant)

		# Initialize all cells to False
		self.cells = [[False] * self.columns for i in range(self.rows)]

	def translate(self,pixel_x, pixel_y):
		"Translate pixel coordinates (pixel_x,pixel_y), into grid coordinates"
		x = pixel_x * self.columns / self.screen_width + 1
		y = pixel_y * self.rows / self.screen_height  + 1
		return x,y

	def on_mouse_release(self,x,y,button,modifiers):
		x,y = self.translate(x,y)
		print('x,y = ' + str((x,y)))
		self.ants.append(Ant(x, y, self.columns, self.rows))

	def draw_cell(self, col, row):
		# Draw an OpenGL rectangle
		x1,y1 = (col-1) * self.cell_size, (row-1) * self.cell_size
		x2,y2 = (col-1) * self.cell_size + self.cell_size, (row-1) * self.cell_size + self.cell_size
		pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

	def draw_grid(self):
		pyglet.gl.glColor4f(0.23,0.23,0.23,1.0) # gray
		# Horizontal lines
		for i in range(self.rows):
			pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (0, i * self.cell_size, self.screen_width, i * self.cell_size)))
		# Vertical lines
		for j in range(self.columns):
			pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (j * self.cell_size, 0, j * self.cell_size, self.screen_height)))

	def draw(self):
		self.clear() # clear graphics
		# Draw the active cells
		pyglet.gl.glColor3ub(255,255,255) # white
		for row in range(len(self.cells)):
			current_row = self.cells[row]
			for col in range(len(current_row)):
				if current_row[col]: # square is True
					self.draw_cell(col,row) # make white
		self.draw_grid()
		# Draw ants
		pyglet.gl.glColor4f(1.0,0.23,0.23,1.0) # blue
		for ant in self.ants:
			self.draw_cell(ant.col, ant.row)

	def run(self):
		pyglet.clock.schedule(self.move_all)
		pyglet.app.run()

	def move_all(self,delta_t):
			for ant in self.ants: self.move(ant)
			self.draw()

	def move(self, ant):
		# Is the ant on a white cell?
		if self.cells[ant.row][ant.col]: # is True
			self.cells[ant.row][ant.col] = False
			ant.turn('right')
		else: # current_cell is False
			self.cells[ant.row][ant.col] = True
			ant.turn('left')


if __name__ == "__main__":
	try: size = int(sys.argv[1])
	except: size = 10
	h = Grid(size)
	h.run()
