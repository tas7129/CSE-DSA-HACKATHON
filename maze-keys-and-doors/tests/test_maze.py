import tempfile
import unittest
from pathlib import Path
from maze import Maze
from solver import shortest_path, shortest_distance
from generator import generate_maze, generate_unsolvable_maze
from csv_handler import read_maze, export_solution

class SolverTests(unittest.TestCase):
    def test_plain_shortest_path(self):
        g=Maze.from_rows(['S...','##..','....','...E'])
        self.assertEqual(shortest_distance(g),6)
    def test_key_door_and_exit_after_key(self):
        g=Maze.from_rows(['S.aAE','#####','.....','.....','.....'])
        self.assertEqual(shortest_distance(g),4)
    def test_multiple_pairs(self):
        g=Maze.from_rows(['S.aA','...b','...B','...E'])
        self.assertIsNotNone(shortest_path(g))
    def test_key_collected_via_alternate_route(self):
        g=Maze.from_rows(['S.AE','a###','....','....'])
        self.assertIsNotNone(shortest_path(g))
    def test_unreachable_exit(self):
        g=Maze.from_rows(['S#..','####','..E.','....'])
        self.assertEqual(shortest_distance(g),-1)
    def test_exit_immediately_after_key_and_door(self):
        g=Maze.from_rows(['SaAE','####','....','....'])
        self.assertEqual(shortest_distance(g),3)
    def test_revisiting_cell_with_new_inventory(self):
        g=Maze.from_rows(['S..#','.#aA','...E','....'])
        self.assertIsNotNone(shortest_path(g))
    def test_invalid_csv(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv'; p.write_text('S,.,.\nE,.\n')
            with self.assertRaises(ValueError): read_maze(p)
    def test_invalid_dimensions_symbols_and_markers(self):
        for rows in (['S..','..'], ['S?','E.'], ['..','E.'], ['SS','E.']):
            with self.assertRaises(ValueError): Maze.from_rows(rows)
    def test_generator_always_solvable(self):
        for seed in range(10):
            g=generate_maze(8,2,seed)
            path=shortest_path(g)
            self.assertIsNotNone(path)
    def test_generated_keys_and_doors_are_spread_along_route(self):
        maze=generate_maze(16,4,seed=23)
        key_positions=[]; door_positions=[]
        for r,row in enumerate(maze.grid):
            for c,tile in enumerate(row):
                if tile in 'abcdef': key_positions.append((r,c))
                elif tile in 'ABCDFG': door_positions.append((r,c))
        self.assertEqual(len(key_positions),4)
        self.assertEqual(len(door_positions),4)
        self.assertGreater(max(r+c for r,c in door_positions), min(r+c for r,c in key_positions))

    def test_unsolvable_generator(self):
        for types in (1, 3, 6):
            maze=generate_unsolvable_maze(max(14, 2*types+2),types,seed=types)
            self.assertIsNone(shortest_path(maze))

    def test_maximum_six_types_and_reject_seven(self):
        g=generate_maze(16,6,31)
        self.assertEqual(len(g.key_types),6)
        with self.assertRaises(ValueError): generate_maze(16,7)
    def test_zero_move_not_permitted_by_grid(self):
        with self.assertRaises(ValueError): Maze.from_rows(['S'])
    def test_export_preserves_grid_and_writes_overlay(self):
        g=Maze.from_rows(['S..','...','..E']); path=shortest_path(g)
        with tempfile.TemporaryDirectory() as d:
            original,overlay=export_solution(g,path,Path(d)/'solved.csv')
            self.assertEqual(read_maze(original).grid,g.grid)
            with overlay.open(newline='') as f:
                self.assertEqual(sum(int(v) for row in __import__('csv').reader(f) for v in row),5)

if __name__=='__main__': unittest.main()
