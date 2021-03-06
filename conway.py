import pyglet
import game_of_life


class GoL_Window(pyglet.window.Window):
    def __init__(self, width, height, cell_size, seed):
        super().__init__(width, height)      # calls the inherited constructor

        # constructing a GoL object and assigning to an attribute
        self.gameOfLife = game_of_life.GameOfLife(width, height, cell_size, seed)

        # scheduling updated states
        pyglet.clock.schedule_interval(self.update, 1.0/20.0)       # 20fps

    # overriding
    def on_draw(self):
        self.clear()                # clears screen before re-drawing
        self.gameOfLife.draw()

    def update(self, dt):                   # dt needed for pyglet.clock.schedule_interval in constructor
        self.gameOfLife.run_rules()


if __name__ == "__main__":
    window = GoL_Window(1280, 1080, 15, 0.6)
    pyglet.app.run()
