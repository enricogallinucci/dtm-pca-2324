import time
import random
import asyncio
from ipywidgets import Image
from ipycanvas import Canvas, hold_canvas
import ipywidgets as widgets
from lab_utils import *


class Pong:
    def __init__(self, game_initializer, game_updater, interval = 0.06, width = 800, height = 500, show_paddles = True, show_scores = True):
        self._interval = interval
        self._initializer = game_initializer
        self._updater = game_updater
        self._show_paddles = show_paddles
        self._show_scores = show_scores
        
        self.width = width
        self.height = height
        self.running = False
        
        self._canvas = Canvas(width = width, height = height)
        self._canvas.stroke_style = "white"
        self._canvas.fill_style = "white"
        
        self._font_size = 32
        self._score_offset = 30
        self._canvas.font = f"{self._font_size}px monospace"

        self.paddle_size = 50
        self.ball_radius = 4
        self.paddle_offset = 3
        self.paddle_width = 10
        
        self.max_ball_speed = self.paddle_width - 2

        self.max_paddle_y = self.height - self.paddle_size - 1

        self.paddle1_y = (self.height - self.paddle_size) // 2
        self.paddle2_y = (self.height - self.paddle_size) // 2

        self.ball_x, self.ball_y = self.width // 2, self.height // 2
        self.ball_dx, self.ball_dy = -1, 1
        self.ball_speed_x, self.ball_speed_y = 4, 4
    
        self._start_match()

        self._slider = widgets.IntSlider(orientation='vertical', readout = False, value = self.paddle1_y, 
                                      min = 0, max = self.max_paddle_y, 
                                      layout = widgets.Layout(height=f"{self.height-self.paddle_size}px", margin=f"{self.paddle_size//2}px 0 {self.paddle_size//2}px 0"))
        self._button = widgets.Button(description = "Start")
        self._button.on_click(self._on_button_clicked)
        wl = [self._slider, self._canvas] if self._show_paddles else [self._canvas]
        self.error_output = widgets.Output()
        self.output = widgets.VBox([self.error_output, self._button, widgets.HBox(wl)])        
        
        
    def _on_button_clicked(self, b):
        if self.running:
            self._stop()
            b.description = "Start"
        else:
            self._initializer(self)
            self._start()
            b.description = "Stop"

                
    async def _timer(self):
        while True:
            await asyncio.sleep(self._interval)
            self._draw()
            try:
                self._updater(self)
            except Exception as ex:
                self.error_output.append_stdout("ERROR:\n")
                self.error_output.append_stdout(str(ex))
                self.error_output.append_stdout("\n")
                break

    def _start(self):
        self.running = True
        self._start_match()
        self._task = asyncio.create_task(self._timer())

        
    def _stop(self):
        self.running = False
        self._task.cancel()    

        
    def _draw(self):
        with hold_canvas(self._canvas):
            self._canvas.clear()
            self._canvas.fill_style = "black"
            self._canvas.fill_rect(0, 0, self.width, self.height)
            self._canvas.fill_style = "white"
            self._canvas.stroke_rect(0, 0, self.width, self.height)
            if self._show_paddles:
                self._canvas.fill_rect(self.paddle_offset, self.paddle1_y, self.paddle_width, self.paddle_size)
                self._canvas.fill_rect(self.width - self.paddle_offset - self.paddle_width, self.paddle2_y, self.paddle_width, self.paddle_size)
            self._canvas.fill_circle(self.ball_x, self.ball_y, self.ball_radius)
            if self._show_scores:
                self._canvas.text_align = "start"
                self._canvas.fill_text(f"{self.score1}", self._score_offset, self._font_size)
                self._canvas.text_align = "right"
                self._canvas.fill_text(f"{self.score2}", self.width - self._score_offset, self._font_size)        
            

    def _start_match(self):
        self.score1, self.score2 = 0, 0
        self._initializer(self)
        self._draw()
        
        
    def get_slider_position(self):
        return self.max_paddle_y - self._slider.value

    
    def random_choice(self, *values):
        return random.choice(values)
    
########################################################################################


def test_es_1(g):
    function_test_cases(g, "interval_contains_interval", 
       ((0, 15, 1, 4), True),
       ((0, 15, 1, 15), True),
       ((0, 15, 1, 16), False),
       ((10, 20, 30, 40), False),
       ((10, 20, 4, 6), False),
       ((10, 20, 10, 11), True),
       ((10, 20, 9, 20), False),
       ((10, 20, 19, 21), False),
       ((10, 20, 19, 20), True),
       ((1, 4, 0, 15), False),
    )
    
    
def test_es_2(g):
    function_test_cases(g, "circle_intersects_rectangle", 
         ((25, 35, 5, 20, 30, 10, 50), True),
         ((35, 25, 5, 20, 30, 10, 50), False),
         ((33, 27, 5, 20, 30, 10, 50), True),
         ((45, 35, 5, 20, 30, 10, 50), False),
         ((33, 45, 5, 20, 30, 10, 50), True),
         ((38, 45, 5, 20, 30, 10, 50), False),
         ((38, 80, 5, 20, 30, 10, 50), False),
         ((33, 80, 5, 20, 30, 10, 50), True),
         ((25, 80, 5, 20, 30, 10, 50), True),
         ((25, 90, 5, 20, 30, 10, 50), False),
         ((15, 90, 5, 20, 30, 10, 50), False),
         ((12, 80, 5, 20, 30, 10, 50), False),
         ((17, 80, 5, 20, 30, 10, 50), True),
         ((17, 40, 5, 20, 30, 10, 50), True),
         ((11, 40, 5, 20, 30, 10, 50), False),
         ((11, 27, 5, 20, 30, 10, 50), False),
         ((17, 27, 5, 20, 30, 10, 50), True),
         ((25, 15, 5, 20, 30, 10, 50), False),
         ((25, 25, 5, 20, 30, 10, 50), True),
         ((25, 50, 25, 20, 30, 10, 50), True),
    )
    

def _get_initializer_and_updater(g, initializer_name, updater_name):
    initializer = g.get(initializer_name)
    if not callable(initializer):
        print(f"Funcion '{initializer_name}' not defined.")
        return None, None
    updater = g.get(updater_name)
    if not callable(updater):
        print(f"Funcion '{updater_name}' not defined.")
        return None, None 
    return initializer, updater
    
pong3, pong4, pong5 = None, None, None    
    
def es_3(g):
    initializer, updater = _get_initializer_and_updater(g, "start_ball", "move_ball")
    if not initializer or not updater:
        return
    global pong3
    pong3 = Pong(initializer, updater, width = 500, height = 300, show_paddles = False, show_scores = False)
    return pong3.output

    
def es_4(g):    
    initializer, updater = _get_initializer_and_updater(g, "start_ball", "move_ball_and_paddles")
    if not initializer or not updater:
        return
    global pong4
    pong4 = Pong(initializer, updater, show_scores = False)
    return pong4.output


def es_5(g):    
    initializer, updater = _get_initializer_and_updater(g, "start_game", "update_game")
    if not initializer or not updater:
        return
    global pong5
    pong5 = Pong(initializer, updater)
    return pong5.output

