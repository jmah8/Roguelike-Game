import game
import pygame
import pstats, io
import cProfile
import config


def profile(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner


@profile
def start():
    g = game.Game()
    while g.running:
        try:
            game.load_game()
        except:
            game.populate_map()
        g.run()
    pygame.quit()


start()
