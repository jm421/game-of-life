import pyglet
import random


class Cell:
    def __init__(self, state, previous_state):
        self.state = state
        self.previous_state = previous_state

    def get_state(self):
        return self.state

    def get_prev_state(self):
        return self.previous_state


class GameOfLife:
    def __init__(self, window_width, window_height, cell_size, seed):
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        self.seed = seed

        self.total_h_grids = int(window_width / cell_size)
        self.total_v_grids = int(window_height / cell_size)
        self.cells = []
        self.generate_cells()

    def generate_cells(self):
        """
        Generates a random 2D array (list of lists) of Cell objects, based on 'self.seed'. Each list 
        corresponds to each row of the grid, and Cell objects in rows corresponds to the cells on 
        that row (with indexes as the column number).
        :return: 2D array of Cell objects.
        """
        for row in range(0, self.total_v_grids):            # for row in number of rows

            self.cells.append([])                           # creating new row

            for col in range(0, self.total_h_grids):        # for col in number of cols

                r = random.random()                         # random float 0<=r<1
                if r < self.seed:
                    self.cells[row].append(Cell(1, 0))       # cell lives
                else:
                    self.cells[row].append(Cell(0, 0))       # cell dies

    def draw_grid(self):
        """
        Draws white grid-lines across entire window, with grid size corresponding to 'self.cell_size'.
        :return: None.
        """

        # drawing vertical lines
        for x in range(self.cell_size, self.window_width, self.cell_size):
            pyglet.graphics.draw_indexed(2, pyglet.gl.GL_LINE_STRIP, [0, 1], ("v2i", (x, 0, x, self.window_height)))

        # drawing horizontal lines
        for y in range(self.cell_size, self.window_height, self.cell_size):
            pyglet.graphics.draw_indexed(2, pyglet.gl.GL_LINE_STRIP, [0, 1], ("v2i", (0, y, self.window_width, y)))

    def draw_cell(self, colour, x0, y0, x1, y1, x2, y2, x3, y3):
        """
        Draws a cell. Takes an RGB tuple (colour) and four coordinates as parameters for where the square
        should be drawn.
        :return: None.
        """

        # drawing two triangles, first at (0, 1, 2) then at (1, 2, 3), and colouring both green
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 1, 2, 3], ("v2i",
                                                                                    (x0, y0,
                                                                                     x1, y1,
                                                                                     x2, y2,
                                                                                     x3, y3)),
                                                                                    ("c3B",
                                                                                     colour * 4))

    def draw(self):
        """
        The main draw method. When called, it draws the values of self.cells accordingly, and then
        draws a corresponding grid.
        
        Newborn => Green
        Alive => Grey
        Dying => Red
        Dead => Black
        
        :return: None
        """

        row_id = 0
        for row in self.cells:
            grid_id = 0
            for cell in row:
                grid_id += 1
                size = grid_id * self.cell_size

                if cell.get_state() == 1 and cell.get_prev_state() == 0:
                    self.draw_cell((0, 100, 0),
                                   size - self.cell_size, self.cell_size * row_id,
                                   size - self.cell_size, self.cell_size * (row_id + 1),
                                   size, self.cell_size * row_id,
                                   size, self.cell_size * (row_id + 1))

                elif cell.get_state() == 1 and cell.get_prev_state() == 1:
                    self.draw_cell((125, 125, 125),
                                   size - self.cell_size, self.cell_size * row_id,
                                   size - self.cell_size, self.cell_size * (row_id + 1),
                                   size, self.cell_size * row_id,
                                   size, self.cell_size * (row_id + 1))

                elif cell.get_state() == 0 and cell.get_prev_state() == 1:
                    self.draw_cell((100, 0, 0),
                                   size - self.cell_size, self.cell_size * row_id,
                                   size - self.cell_size, self.cell_size * (row_id + 1),
                                   size, self.cell_size * row_id,
                                   size, self.cell_size * (row_id + 1))

            row_id += 1

        self.draw_grid()

    def run_rules(self):
        """
        Applies GoL rules to Cell objects in "self.cells".
        :return: None.
        """
        temp = []
        for row in range(0, self.total_v_grids):
            temp.append([])
            for col in range(0, self.total_h_grids):

                # calculate sum of cells around current cell
                total_neighbours = sum([self.get_cell_value(col + 1, row - 1),
                                        self.get_cell_value(col + 1, row),
                                        self.get_cell_value(col + 1, row + 1),

                                        self.get_cell_value(col, row - 1),
                                        self.get_cell_value(col, row + 1),

                                        self.get_cell_value(col - 1, row - 1),
                                        self.get_cell_value(col - 1, row),
                                        self.get_cell_value(col - 1, row + 1)])

                # reproduction
                if self.get_cell_value(col, row) == 0 and total_neighbours == 3:
                    temp[row].append(Cell(1, 0))

                # stasis
                elif self.get_cell_value(col, row) == 1 and total_neighbours in [2, 3]:
                    temp[row].append(Cell(1, 1))

                # else the cell must be dead
                else:
                    temp[row].append(Cell(0, self.get_cell_value(col, row)))

        self.cells = temp

    def get_cell_value(self, col, row):
        """
        Searches "self.cells" for a Cell object at the specified row and column indices. If found, it will return
        the cell state (0 or 1), else it returns 0.
        :param row: Row index (y-coordinate)
        :param col: Column index (x-coordinate)
        :return: Cell state (0 or 1)
        """

        if 0 <= row < self.total_v_grids and 0 <= col < self.total_h_grids:     # if its valid (on the grid), get state
            return self.cells[row][col].get_state()

        return 0        # else its outside the grid, call it dead
