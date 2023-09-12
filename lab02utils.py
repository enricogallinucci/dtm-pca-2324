from itertools import product
import time
from ipywidgets import Image
from ipycanvas import Canvas, hold_canvas
from lab_utils import *

_WALL = "▮"
_EMPTY = "▯"

_maze = ['▮▮▮▮▮▮▮▮▮▮',
         '▮▯▮▯▮▮▯▯▯▮',
         '▮▯▮▯▯▮▯▮▯▮',
         '▮▯▮▯▮▮▮▮▯▮',
         '▮▯▯▯▯▯▯▮▯▮',
         '▮▯▮▮▮▮▯▮▯▯',
         '▮▯▮▯▯▮▯▮▯▮',
         '▮▯▮▯▮▮▯▮▯▮',
         '▮▯▮▯▯▯▯▯▯▮',
         '▮▯▮▮▮▮▮▮▮▮']


def _create_canvas_with_image(path, w, h):
    c = Canvas(width=w, height=h)
    c.draw_image(Image.from_file(path))
    return c

_maze_h, _maze_w = len(_maze), len(_maze[0])
_all_directions = "NESO"
_SPRITE_SIZE = 32
_cell_size = _SPRITE_SIZE
_ANIM_STEPS = 8
_anim_time = 0.5
_TARGET_POS = (4, 6)
_EXIT_POS = (9, 5)
_target_enabled = False

_cell_sprites = None
_hero_sprites = None
_target_sprite = None

_steps = {'N': ( 0, -1), 
          'E': ( 1,  0),
          'S': ( 0,  1),
          'O': (-1,  0)}

_pos_x, _pos_y, _direction = None, None, None
_canvas = None

def _create_canvas():
    c = Canvas(width = _maze_w * _cell_size, height = _maze_h * _cell_size)
    c.layout.width = '100%'
    c.layout.height = 'auto'
    return c

def _draw_maze_cell(x, y):
    _canvas.draw_image(_cell_sprites[_maze[y][x]], x * _cell_size, y * _cell_size, _cell_size, _cell_size)
    if _target_enabled and (x, y) == _TARGET_POS:
        _canvas.draw_image(_target_sprite, x * _cell_size, y * _cell_size, _cell_size, _cell_size)

def _draw_maze():
    with hold_canvas(_canvas):
        for x, y in product(range(_maze_w), range(_maze_h)):
            _draw_maze_cell(x, y)
            
def _draw_hero():
    _canvas.draw_image(_hero_sprites[_direction][0], _pos_x * _cell_size, _pos_y * _cell_size, _cell_size, _cell_size)

def _valid_move(new_pos_x, new_pos_y):
    return 0 <= new_pos_x < _maze_w and 0 <= new_pos_y < _maze_h and _maze[new_pos_y][new_pos_x] == _EMPTY
    
def _rotate_direction(left):
    d = -1 if left else +1
    return _all_directions[(_all_directions.index(_direction)+d) % 4]
    
def _hero_rotate(left):
    global _direction    
    with hold_canvas(_canvas):
        _draw_maze_cell(_pos_x, _pos_y)
        _direction = _rotate_direction(left)
        _draw_hero()
    
def _hero_move_start():
    global _pos_x, _pos_y, _direction
    _pos_x, _pos_y, _direction = 1, len(_maze) - 1, 'S'
    _draw_maze()
    _draw_hero()
    
    
#########################################################################################################################    

def start_maze(scale = 1, speed = 1):
    """
    Initializes the maze and returns a canvas object to display it in a Jupyter notebook. 
    Parameters scale and speed allow to change the display size and the animation speed, respectively.
    """
    global _canvas, _cell_size, _anim_time, _cell_sprites, _hero_sprites, _target_sprite
    _cell_size = int(_SPRITE_SIZE * scale)
    _anim_time = 0.5 / speed
    _canvas = _create_canvas()

    # Load sprites
    _cell_sprites = {_WALL: _create_canvas_with_image('sprites/wall.png', _SPRITE_SIZE, _SPRITE_SIZE), _EMPTY: _create_canvas_with_image('sprites/ground.png', _SPRITE_SIZE, _SPRITE_SIZE)}
    _hero_sprites = {d: [_create_canvas_with_image(f'sprites/hero_{d}_{i}.png', _SPRITE_SIZE, _SPRITE_SIZE) for i in range(4)] for d in _all_directions }
    _target_sprite = _create_canvas_with_image('sprites/target.png', _SPRITE_SIZE, _SPRITE_SIZE)
    
    _hero_move_start()
    return _canvas    
    
    
def hero_rotate_left():
    """
    The hero turns to the left.
    """
    _hero_rotate(True)
    
    
def hero_rotate_right():
    """
    The hero turns to the right.
    """
    _hero_rotate(False)
    
    
def hero_move():
    """
    The hero attempts to move forward: returns True if the movement was succesfull, otherwise False.
    """
    global _pos_x, _pos_y, _direction
    new_pos_x, new_pos_y = _pos_x + _steps[_direction][0], _pos_y + _steps[_direction][1]
    if _valid_move(new_pos_x, new_pos_y):        
        for i in range(_ANIM_STEPS):
            with hold_canvas(_canvas):
                _draw_maze_cell(_pos_x, _pos_y)
                _draw_maze_cell(new_pos_x, new_pos_y)
                _canvas.draw_image(_hero_sprites[_direction][i % 4], 
                                   _pos_x * _cell_size + (new_pos_x - _pos_x) * i * _cell_size//_ANIM_STEPS, 
                                   _pos_y * _cell_size + (new_pos_y - _pos_y) * i * _cell_size//_ANIM_STEPS, 
                                   _cell_size, _cell_size)
            time.sleep(_anim_time/_ANIM_STEPS)
        with hold_canvas(_canvas):
            _draw_maze_cell(_pos_x, _pos_y)
            _draw_maze_cell(new_pos_x, new_pos_y)
            _pos_x, _pos_y = new_pos_x, new_pos_y
            _draw_hero()
        return True
    else:
        return False           
       
        
def wall_in_front():
    """
    True if there is a wall in front of the hero.
    """
    return not _valid_move(_pos_x + _steps[_direction][0], _pos_y + _steps[_direction][1])


def wall_at_right():
    """
    True if there is a wall on the right of the hero.
    """
    d = _rotate_direction(False)
    return not _valid_move(_pos_x + _steps[d][0], _pos_y + _steps[d][1])


def wall_at_left():
    """
    True if there is a wall on the left of the hero.
    """
    d = _rotate_direction(True)
    return not _valid_move(_pos_x + _steps[d][0], _pos_y + _steps[d][1])


def maze_solved():
    """
    True if there hero finally exited the maze!
    """
    return (_pos_x, _pos_y) == _EXIT_POS

def show_target(visible = True):
    global _target_enabled
    _target_enabled = visible
    _hero_move_start()
    _draw_maze_cell(*_TARGET_POS)

def test_target_found():
    ok = (_pos_x, _pos_y) == _TARGET_POS
    if ok:
        show_target(False)
    _hero_move_start()
    test_cases((f'Target {"" if ok else "not "}reached', ok))
