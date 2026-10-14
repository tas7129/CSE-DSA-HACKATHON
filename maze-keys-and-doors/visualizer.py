"""Tkinter interface, maze rendering, and non-blocking animation."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from maze import Maze, DOOR_TO_KEY
from solver import shortest_path
from generator import generate_maze, generate_unsolvable_maze, minimum_size
from csv_handler import read_maze, export_solution

KEY_COLORS={'a':'#f4c542','b':'#62c7c1','c':'#bd8be8','d':'#ff9b62','e':'#87c96f','f':'#ef8ea8'}

class MazeApp:
    def __init__(self, root):
        self.root=root; root.title('Maze Solver with Keys and Doors'); root.minsize(760,560)
        self.maze=None; self.path=None; self.index=0; self.after_id=None; self.paused=False
        self.collected=set(); self.opened=set(); self.path_seen=set()
        self._build(); self._generate()

    def _build(self):
        root=self.root
        shell=ttk.Frame(root,padding=14); shell.pack(fill='both',expand=True)
        ttk.Label(shell,text='Maze Solver with Keys and Doors',font=('TkDefaultFont',18,'bold')).pack(anchor='w')
        body=ttk.Frame(shell); body.pack(fill='both',expand=True,pady=(12,0))
        self.canvas=tk.Canvas(body,width=540,height=520,bg='#e8edf3',highlightthickness=0)
        self.canvas.pack(side='left',fill='both',expand=True)
        self.canvas.bind('<Configure>',lambda _event:self._draw())
        panel=ttk.Frame(body,width=220,padding=(14,0)); panel.pack(side='right',fill='y')
        ttk.Label(panel,text='Maze controls',font=('TkDefaultFont',12,'bold')).pack(anchor='w',pady=(0,8))
        row=ttk.Frame(panel); row.pack(fill='x')
        ttk.Label(row,text='N').pack(side='left'); self.size=tk.IntVar(value=12); ttk.Spinbox(row,from_=5,to=60,textvariable=self.size,width=5).pack(side='left',padx=(4,12))
        ttk.Label(row,text='T').pack(side='left'); self.types=tk.IntVar(value=2); ttk.Spinbox(row,from_=1,to=6,textvariable=self.types,width=4).pack(side='left',padx=4)
        self.unsolvable=tk.BooleanVar(value=False)
        ttk.Checkbutton(panel,text='Generate an unsolvable maze',variable=self.unsolvable).pack(anchor='w',pady=(5,2))
        self._button(panel,'Generate random maze',self._generate)
        self._button(panel,'Load maze from CSV',self._load)
        ttk.Separator(panel).pack(fill='x',pady=8)
        self._button(panel,'Solve maze',self._solve)
        self._button(panel,'Animate solution',self._animate)
        controls=ttk.Frame(panel); controls.pack(fill='x',pady=2)
        ttk.Button(controls,text='Pause',command=self._pause).pack(side='left',expand=True,fill='x')
        ttk.Button(controls,text='Resume',command=self._resume).pack(side='left',expand=True,fill='x',padx=(4,0))
        self._button(panel,'Reset maze',self._reset)
        self._button(panel,'Export solved maze',self._export)
        ttk.Label(panel,text='Animation speed (ms / move)').pack(anchor='w',pady=(10,0))
        self.speed=tk.IntVar(value=250); ttk.Scale(panel,from_=60,to=1000,variable=self.speed,orient='horizontal').pack(fill='x')
        ttk.Separator(panel).pack(fill='x',pady=8)
        self.status=tk.StringVar(value='Generate a maze or load a CSV file.')
        ttk.Label(panel,textvariable=self.status,wraplength=200,justify='left').pack(anchor='w')
        self.stats=tk.StringVar(value='Shortest path: —\nMoves made: 0\nKeys: none\nSolvable: —')
        ttk.Label(panel,textvariable=self.stats,wraplength=200,justify='left').pack(anchor='w',pady=12)
        ttk.Label(panel,text='Legend: S start · E exit · # wall\nKeys and doors share a colour.',wraplength=200).pack(anchor='w',side='bottom')

    def _button(self,parent,label,command): ttk.Button(parent,text=label,command=command).pack(fill='x',pady=3)
    def _generate(self):
        try:
            t=self.types.get(); n=self.size.get()
            if self.unsolvable.get():
                maze=generate_unsolvable_maze(n,t)
                self._set_maze(maze); self.status.set(f'Generated an unsolvable {n}×{n} maze with {t} key-and-door types.')
            else:
                maze=generate_maze(n,t)
                self._set_maze(maze); self.status.set(f'Generated a solvable {n}×{n} maze with {t} key-and-door types.')
        except (ValueError,tk.TclError) as e: messagebox.showerror('Cannot generate maze',str(e),parent=self.root)
    def _load(self):
        name=filedialog.askopenfilename(title='Load maze CSV',filetypes=[('CSV files','*.csv'),('All files','*.*')],parent=self.root)
        if not name:return
        try:self._set_maze(read_maze(name)); self.status.set(f'Loaded {name}.')
        except (OSError,ValueError) as e:messagebox.showerror('Invalid maze CSV',str(e),parent=self.root)
    def _set_maze(self,maze): self._cancel(); self.maze=maze; self.path=None; self.index=0; self.collected=set(); self.opened=set(); self.path_seen=set(); self._draw(); self._update_stats()
    def _solve(self):
        if not self.maze:return
        self._cancel(); self.path=shortest_path(self.maze); self.index=0; self.path_seen=set(self.path or []); self._draw(); self._update_stats()
        if self.path is None:self.status.set('No valid route reaches the exit.')
        else:self.status.set(f'Shortest path found: {len(self.path)-1} moves.')
    def _animate(self):
        if not self.maze:return
        if self.path is None:self._solve()
        if self.path is None:return
        self._cancel(); self.index=0; self.collected=set(); self.opened=set(); self.path_seen=set(); self.paused=False; self._tick()
    def _tick(self):
        if self.path is None:return
        if self.index>=len(self.path):
            self.status.set('Animation complete.'); self.after_id=None; self._draw(); self._update_stats(); return
        pos=self.path[self.index]; tile=self.maze.grid[pos[0]][pos[1]]
        if tile in 'abcdef':self.collected.add(tile)
        if tile in 'ABCDEF':self.opened.add(tile)
        self.path_seen.add(pos); self.index+=1; self._draw(); self._update_stats()
        self.status.set(f'Animating move {max(0,self.index-1)} of {len(self.path)-1}.')
        if not self.paused:self.after_id=self.root.after(max(40,int(self.speed.get())),self._tick)
    def _pause(self):
        self.paused=True
        if self.after_id:self.root.after_cancel(self.after_id); self.after_id=None
        self.status.set('Animation paused.')
    def _resume(self):
        if self.path and self.index<len(self.path):self.paused=False; self._tick()
    def _cancel(self):
        if self.after_id:
            try:self.root.after_cancel(self.after_id)
            except tk.TclError:pass
        self.after_id=None; self.paused=False
    def _reset(self):
        self._cancel(); self.path=None; self.index=0; self.path_seen=set(); self.collected=set(); self.opened=set(); self._draw(); self._update_stats(); self.status.set('Maze reset.')
    def _export(self):
        if not self.maze: return
        if self.path is None:self._solve()
        if self.path is None:messagebox.showinfo('No solution','There is no solution to export.',parent=self.root); return
        filename=filedialog.asksaveasfilename(title='Export original maze and path overlay',defaultextension='.csv',initialfile='maze.csv',filetypes=[('CSV files','*.csv')],parent=self.root)
        if not filename:return
        try:
            original,overlay=export_solution(self.maze,self.path,filename)
            messagebox.showinfo('Export complete',f'Original maze: {original}\nPath overlay: {overlay}\nThe overlay uses 1 for path cells and 0 otherwise.',parent=self.root)
        except OSError as e:messagebox.showerror('Export failed',str(e),parent=self.root)
    def _update_stats(self):
        distance='—' if self.path is None else ('-1' if not self.path else str(len(self.path)-1))
        keys=', '.join(sorted(self.collected)) or 'none'
        solvable='—' if self.path is None else ('Yes' if self.path else 'No')
        self.stats.set(f'Shortest path: {distance}\nMoves made: {max(0,self.index-1)}\nKeys: {keys}\nSolvable: {solvable}')
    def _draw(self):
        self.canvas.delete('all')
        if not self.maze:return
        n=self.maze.size; w=max(1,self.canvas.winfo_width()); h=max(1,self.canvas.winfo_height()); cell=min(w/n,h/n)
        ox=(w-cell*n)/2; oy=(h-cell*n)/2
        for r,row in enumerate(self.maze.grid):
            for c,tile in enumerate(row):
                x1=ox+c*cell; y1=oy+r*cell; x2=x1+cell; y2=y1+cell
                fill='#ffffff'; label=tile
                if tile=='#':fill='#202734'
                elif tile=='S':fill='#54b56c'
                elif tile=='E':fill='#e65c5c'
                elif tile in 'abcdef':fill=KEY_COLORS[tile]
                elif tile in DOOR_TO_KEY:fill='#ffffff' if tile in self.opened else KEY_COLORS[DOOR_TO_KEY[tile]]
                if (r,c) in self.path_seen and tile not in 'SE':fill='#a8e3ff'
                self.canvas.create_rectangle(x1,y1,x2,y2,fill=fill,outline='#9da8b5',width=1)
                if tile=='#':label=''
                elif tile in 'abcdef' and tile in self.collected:label='✓'
                elif tile in DOOR_TO_KEY and tile in self.opened:label='✓'
                if label:self.canvas.create_text((x1+x2)/2,(y1+y2)/2,text=label,fill='#fff' if tile=='#' else '#17212b',font=('TkDefaultFont',max(8,int(cell*.4)),'bold'))
        if self.path and self.index:
            r,c=self.path[min(self.index-1,len(self.path)-1)]; x=ox+(c+.5)*cell; y=oy+(r+.5)*cell
            self.canvas.create_oval(x-cell*.28,y-cell*.28,x+cell*.28,y+cell*.28,fill='#3169e8',outline='white',width=2)
