#!/usr/bin/env python3
"""Launch the Maze Solver with Keys and Doors desktop application."""
import tkinter as tk
from visualizer import MazeApp

def main():
    root=tk.Tk(); MazeApp(root); root.mainloop()

if __name__=='__main__': main()
