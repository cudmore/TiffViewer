import os
import pygame as pg
import tiffstack as ts
import viewer
import Tkinter as Tk
import tkFileDialog


class StackBrowser:
    """
    Main program for user interaction with the TIFF stack browser.
    First goal is to add functionality incrementally, while keeping
    the program speedy and bug-free. Then image analysis done elsewhere
    can be ported into the viewer for viewing.
    """
    def __init__(self):
        """
        Create the stack browser by picking a file to load.
        """
        # self.open_stacks = []
        self.viewers = []  # if at some point we port to another library

        root = Tk.Tk()
        root.withdraw()
        fpath = tkFileDialog.askopenfilename(
            initialdir=os.path.expanduser('~/Desktop/test'))
        t = ts.TiffStack(fpath)
        v = viewer.Viewer(t)
        # self.open_stacks.append(t)
        self.viewers.append(v)

    def _handle_events(self, events):
        """
        Helper method for event handling. Allows user interaction.

        :param events: The PyGame event queue

        :type events: pygame.event.Event[]

        :rtype: None
        """
        for event in events:
            # Check for exit:
            if event.type == pg.QUIT:
                pg.quit()
                quit(0)

            # Check for window resize (and
            # preserve aspect ratio)
            elif event.type == pg.VIDEORESIZE:
                # New size
                (w, h) = event.dict['size']
                # Old size
                (w0, h0) = self.viewers[0].screen.get_size()
                # Check for width change
                if w != w0:
                    # Adjust height to match
                    h = h0 * w / w0
                else:
                    # Check for height change
                    if h != h0:
                        # Adjust width to match
                        w = h * w0 / h0

                self.viewers[0].resize((w, h))

            # Check for scroll
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.viewers[0].scroll('up')
                elif event.button == 5:
                    self.viewers[0].scroll('down')

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.viewers[0].pan('up')
                elif event.key == pg.K_DOWN:
                    self.viewers[0].pan('down')
                elif event.key == pg.K_LEFT:
                    self.viewers[0].pan('left')
                elif event.key == pg.K_RIGHT:
                    self.viewers[0].pan('right')

        # TODO: Currently too fast -> need to add a delay between keypresses

        # pressed = pg.key.get_pressed()
        #
        # if pressed[pg.K_UP]:
        #     self.viewers[0].pan('up')
        # elif pressed[pg.K_DOWN]:
        #     self.viewers[0].pan('down')
        # elif pressed[pg.K_LEFT]:
        #     self.viewers[0].pan('left')
        # elif pressed[pg.K_RIGHT]:
        #     self.viewers[0].pan('right')

    def start(self):
        """
        Main event loop; handle all events and then update the display.

        :rtype: None
        """
        while True:
            self._handle_events(pg.event.get())
            pg.display.flip()


def main():
    browser = StackBrowser()
    browser.start()


if __name__ == '__main__':
    main()
