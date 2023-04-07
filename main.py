import curses as cs
import math


def addstr2(scr, s, *args):
    try:
        scr.addstr(s, *args)
    except:
        scr.insstr(s[-1], *args)


class Win:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def draw(self, scr, y, x, h, w):
        for _y in range(y, y + h):
            scr.move(_y, x)
            addstr2(scr, ' ' * w, self.kwargs['background_color'])


class FlexWin(Win):

    def __init__(self, wins = [], **kwargs):
        self.wins = wins
        super().__init__(**kwargs)

    def draw(self, scr, y, x, h, w):
        if len(self.wins) == 0: return
        flex_sum = sum(map(lambda win: win.kwargs['flex_grow'], self.wins))
        used_space = 0
        for win in self.wins[:-1]:
            res_space = math.floor(w * win.kwargs['flex_grow'] / flex_sum)
            win.draw(scr, y, x + used_space, h, res_space)
            used_space += res_space
        res_space = w - used_space
        self.wins[-1].draw(scr, y, x + used_space, h, res_space)


def main(scr):
    cs.start_color()
    cs.use_default_colors()
    cs.curs_set(0)
    
    w1 = Win(flex_grow = 1, background_color = cs.A_REVERSE)
    w2 = Win(flex_grow = 2, background_color = cs.A_NORMAL)
    w3 = Win(flex_grow = 1, background_color = cs.A_REVERSE)
    w4 = Win(flex_grow = 1, background_color = cs.A_NORMAL)
    w5 = Win(flex_grow = 1, background_color = cs.A_REVERSE)

    wpe = FlexWin(wins = [w3, w4, w5], flex_grow = 1)
    wp = FlexWin(wins = [w1, w2, wpe])
    scr.addstr("hello")
    while True:
        my, mx = scr.getmaxyx()
        scr.move(0, 0)
        wp.draw(scr, 1, 1, my - 1, mx - 1)
        scr.box()
        ch = scr.getch()


if __name__ == '__main__':
    cs.wrapper(main)

