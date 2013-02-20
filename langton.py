# A simple and usable Langton's Ant implementation in python.

import pyglet, sys, random
from pyglet import window
from pyglet import clock
from pyglet import font

class Ant:

	def __init__(self,x,y,columns,rows):
		# Initial positions of the ant.
		self.columns = columns; self.rows = rows;
		self.x = x ; self.y = y

		# set random direction where 0: west, 1: north, 2: east, 3: south
		self.dir = random.choice([0,1,2,3])

		# the direction coordinate offsets; respectively: move west, north, east, or south
		self.dirs = ((-1,0), (0,1),(1,0), (0,-1))

	def turn(self, direction):
		# orient right (clockwise)
		if   direction is 'right': self.dir = (self.dir + 1) % 4
		# orient left (counter-clockwise)
		elif direction is  'left': self.dir = (self.dir + 3) % 4
		# Move the ant forward one square
		self.forward()

	def forward(self):
		self.x = (self.x + self.dirs[self.dir][0]) % self.columns
		self.x = (self.y + self.dirs[self.dir][1]) % self.rows

class Grid(pyglet.window.Window):

	def __init__(self, n_ants):

		window.Window.__init__(self,fullscreen=True)

		# Initialize screen resolution
		self.cell_size = 10
		platform = pyglet.window.get_platform()
		display = platform.get_default_display()
		screen = display.get_default_screen()
		self.screen_width = screen.width
		self.screen_height = screen.height
		self.columns = self.screen_width / 10
		self.rows = self.screen_height / 10

		# Initialize ants
		self.ants = []
		offset_x = (self.columns-1) / n_ants;
		offset_y = (self.rows-1) / n_ants;
		for nth_ant in range(1, n_ants+1):
			ant = Ant(nth_ant * offset_x, nth_ant * offset_y, self.columns, self.rows)
			self.ants.append(ant)

		# Initialize all cells to False
		self.cells = [[False] * self.columns for i in range(self.rows)]

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
		self.draw_cell(5,10)
		# Draw the active cells
		pyglet.gl.glColor3ub(255,255,255) # white
		for row in range(len(self.cells)):
			current_row = self.cells[row]
			for col in range(len(current_row)):
				if current_row[col]: self.draw_cell(col,row)
		self.draw_grid()
		# Draw ants
		pyglet.gl.glColor4f(1.0,0.23,0.23,1.0) # blue
		for ant in self.ants:
			self.draw_cell(ant.x, ant.y)

	def run(self):
		clock.set_fps_limit(2)
		pyglet.clock.schedule(self.move_all)
		pyglet.app.run()

	def move_all(self,delta_t):
			for ant in self.ants: self.move(ant)
			self.draw()

	def move(self, ant):
		# Is the ant on a white cell?
		current_cell = self.cells[ant.y][ant.x]
		if current_cell: # is True
			print "current cell is true"
			current_cell = False
			ant.turn('right')
		else: # current_cell is False
			print "current cell is false"
			self.cells[ant.y][ant.x] = True
			ant.t/urn('left')


if __name__ == "__main__":
		h = Grid(int(sys.argv[1]))
		h.run()
