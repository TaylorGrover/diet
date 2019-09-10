import curses
from curses import wrapper
from database import Database
import numpy as np
import os
from serving import Serving
import sys
import time

def get_screen_size():
    return np.array(scr.getmaxyx())-2


def main(stdscr):
    database = Database(dirname=".foods",filename="foods.dat",fieldname="name")
    stdscr.clear()

wrapper(main)
