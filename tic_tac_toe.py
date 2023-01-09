import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

class Buttons:

    def __init__(self, fig, ax, remove=[], invisible=[]):
        
        self.fig = fig
        self.ax = ax
        self.remove = remove
        self.invisible = invisible


    def start(self, event):

        for txt in self.ax.texts:
            if txt.get_label() in self.remove:
                txt.remove()
            else:
                txt.set_visible(True)
        for line in self.ax.lines:
            line.set_visible(True)
        for axis in self.fig.get_axes():
            if axis != self.ax and not axis.get_label() in self.invisible:
                axis.set_visible(True)
            elif axis != self.ax:
                axis.set_visible(False)
        plt.draw()

    def play_again(self, event):
        
        for txt in self.ax.texts:
            txt.remove()
        players_turn_txt(1, self.ax, True)
        for line in self.ax.lines:
            line.set_alpha(1)
        for axis in self.fig.get_axes():
            if axis != self.ax and not axis.get_label() in self.invisible:
                for line in axis.lines:
                    line.remove()
                for patch in axis.patches:
                    patch.remove()
            elif axis != self.ax:
                axis.set_visible(False)
        plt.draw()

    def close(self, event):
        
        plt.close()

def starting_screen(title, x_size, y_size):            

    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(0,x_size)
    ax.set_ylim(0,y_size)
    ax.axis('off')
    ax.margins(x=0, y=0)
    text = ax.text(x_size/2, y_size*0.8, title, fontsize=30, horizontalalignment='center', label='title')

    start = fig.add_axes([0.4,0.4,0.2,0.1], label='start')
    button = Buttons(fig, ax, ['title'], ['start', 'play_again', 'block_click', 'close'])
    bstart = Button(start, 'Start')
    bstart.on_clicked(button.start)

    return fig, ax, bstart

def players_turn_txt(num, axis, vis):
    icon_dict = {1:'X', 2:'O'}
    colour_dict = {1:'blue', 2:'red'}
    string = f'   Player {num}\'s turn     '
    icon = ' ' * len(string) + icon_dict[num]
    str_txt = axis.text(axis.get_xlim()[1]/2, axis.get_ylim()[1]+0.8, string, fontsize=20, horizontalalignment='center', visible=vis)
    icon_txt = axis.text(axis.get_xlim()[1]/2, axis.get_ylim()[1]+0.8, icon, fontsize=20, horizontalalignment='center', visible=vis, color=colour_dict[num], fontweight=1000)

def draw_board(fig, ax):

    ax_bounds = ax.get_position().bounds
    axes_dict = {}

    span = list(np.arange(0,10))
    line_at_3 = [3]*10
    line_at_6 = [6]*10
    line1 = ax.plot(line_at_3, span, color='black', linewidth=2, visible=False, label='board')
    line2 = ax.plot(line_at_6, span, color='black', linewidth=2, visible=False, label='board')
    line3 = ax.plot(span, line_at_3, color='black', linewidth=2, visible=False, label='board')
    line4 = ax.plot(span, line_at_6, color='black', linewidth=2, visible=False, label='board')

    players_turn_txt(1, ax, False)
    
    for vertical_pos in [2,1,0]:
        for horizontal_pos in [0,1,2]:
            width = ax_bounds[2]/3
            height = ax_bounds[3]/3
            x = ax_bounds[0] + horizontal_pos * width
            y = ax_bounds[1] + vertical_pos * height
            position = fig.add_axes([x, y, width, height], visible=False)
            position.set_xlim(0,1)
            position.set_ylim(0,1)
            position.axis('off')
            axes_dict[position] = float('nan')

    block_click = fig.add_axes(ax_bounds, visible=False, alpha=0, label='block_click')
    block_click.axis('off')

    play_again = fig.add_axes([0.28,0.45,0.2,0.1], visible=False, label='play_again')
    button = Buttons(fig, ax, [], ['start', 'play_again', 'block_click', 'close'])
    bplay_again = Button(play_again, 'Play again')
    bplay_again.on_clicked(button.play_again)

    close = fig.add_axes([0.55,0.45,0.2,0.1], visible=False, label='close')
    button = Buttons(fig, ax)
    bclose = Button(close, 'Close')
    bclose.on_clicked(button.close)

    return axes_dict, bplay_again, bclose

def draw_shape(shape, width, axis):
    assert width <= 1
    adjust = (1-width)/2
    if shape.upper() == 'X':
        axis.plot([adjust, width+adjust], [adjust, width+adjust], color='blue', linewidth=8)
        axis.plot([adjust, width+adjust], [width+adjust, adjust], color='blue', linewidth=8)
    elif shape.upper() == 'O':
        circle = plt.Circle((0.5, 0.5), width/2, fill=False, color='red', linewidth=8)
        axis.add_patch(circle)

def win_check(axes_dict):

    ax_list = list(axes_dict.keys())
    num_list = list(axes_dict.values())
    
    # horizontals
    if num_list[0] == num_list[1] == num_list[2]:
        for ax in [ax_list[0], ax_list[1], ax_list[2]]:
            ax.plot([0,1], [0.5,0.5], color='black', linewidth=4, label='win_line')
        plt.draw()
        return num_list[0]
    elif num_list[3] == num_list[4] == num_list[5]:
        for ax in [ax_list[3], ax_list[4], ax_list[5]]:
            ax.plot([0,1], [0.5,0.5], color='black', linewidth=4, label='win_line')
        plt.draw()
        return num_list[3]
    elif num_list[6] == num_list[7] == num_list[8]:
        for ax in [ax_list[6], ax_list[7], ax_list[8]]:
            ax.plot([0,1], [0.5,0.5], color='black', linewidth=4, label='win_line')
        plt.draw()
        return num_list[6]

    # verticals
    elif num_list[0] == num_list[3] == num_list[6]:
        for ax in [ax_list[0], ax_list[3], ax_list[6]]:
            ax.plot([0.5,0.5], [0,1], color='black', linewidth=4, label='win_line')
        plt.draw()
        return num_list[0]
    elif num_list[1] == num_list[4] == num_list[7]:
        for ax in [ax_list[1], ax_list[4], ax_list[7]]:
            ax.plot([0.5,0.5], [0,1], color='black', linewidth=4, label='win_line')
        plt.draw()
        return num_list[1]
    elif num_list[2] == num_list[5] == num_list[8]:
        for ax in [ax_list[2], ax_list[5], ax_list[8]]:
            ax.plot([0.5,0.5], [0,1], color='black', linewidth=4, label='win_line')
        plt.draw()
        return num_list[2]

    # diagonals
    elif num_list[0] == num_list[4] == num_list[8]:
        for ax in [ax_list[0], ax_list[4], ax_list[8]]:
            ax.plot([0,1], [1,0], color='black', linewidth=4, label='win_line')
        plt.draw()
        return num_list[0]
    elif num_list[2] == num_list[4] == num_list[6]:
        for ax in [ax_list[2], ax_list[4], ax_list[6]]:
            ax.plot([0,1], [0,1], color='black', linewidth=4, label='win_line')
        plt.draw()
        return num_list[2]

    else:
        return None


class Select_square:

    def __init__(self, fig, ax, axes_dict):
        self.cid = fig.canvas.mpl_connect('button_press_event', self.click)
        self.fig = fig
        self.ax = ax
        self.axes_dict = axes_dict
        self.i = 0

    def click(self, event):
        if event.inaxes in list(self.axes_dict.keys()) and self.axes_dict[event.inaxes] != self.axes_dict[event.inaxes]:
            
            if self.i % 2 == 0:
                draw_shape('X', 0.6, event.inaxes)
                plt.draw()
                self.axes_dict[event.inaxes] = 1
                self.i += 1
                for text in self.ax.texts:
                    text.remove()
                if win_check(self.axes_dict) is None:

                    if self.i < 8:
                        players_turn_txt(2, self.ax, True)
                    else:
                        for axis in self.fig.get_axes():
                            if axis in list(self.axes_dict.keys()) + [self.ax]:
                                for line in axis.lines:
                                    line.set_alpha(0.4)
                                for patch in axis.patches:
                                    patch.set_alpha(0.4)
                            elif axis.get_label() in ['play_again', 'block_click', 'close']:
                                axis.set_visible(True)
                        tie = f'Tie game.'
                        self.ax.text(self.ax.get_xlim()[1]/2, self.ax.get_ylim()[1]+0.8, tie, fontsize=20, horizontalalignment='center')
                        for key in self.axes_dict:
                            self.axes_dict[key] = float('nan')
                        self.i = 0

                else:
                    for axis in self.fig.get_axes():
                        if axis in list(self.axes_dict.keys()) + [self.ax]:
                            for line in axis.lines:
                                if line.get_label() != 'win_line':
                                    line.set_alpha(0.4)
                            for patch in axis.patches:
                                patch.set_alpha(0.4)
                        elif axis.get_label() in ['play_again', 'block_click', 'close']:
                            axis.set_visible(True)
                    winner = f'Player {win_check(self.axes_dict)} wins!'
                    self.ax.text(self.ax.get_xlim()[1]/2, self.ax.get_ylim()[1]+0.8, winner, fontsize=20, horizontalalignment='center')
                    for key in self.axes_dict:
                        self.axes_dict[key] = float('nan')
                    self.i = 0
                    
            elif self.i % 2 == 1:
                draw_shape('O', 0.7, event.inaxes)
                plt.draw()
                self.axes_dict[event.inaxes] = 2
                self.i += 1
                for text in self.ax.texts:
                    text.remove()
                if win_check(self.axes_dict) is None:
                    players_turn_txt(1, self.ax, True)
                else:
                    for axis in self.fig.get_axes():
                        if axis in list(self.axes_dict.keys()) + [self.ax]:
                            for line in axis.lines:
                                if line.get_label() != 'win_line':
                                    line.set_alpha(0.4)
                            for patch in axis.patches:
                                patch.set_alpha(0.4)
                        elif axis.get_label() in ['play_again', 'block_click', 'close']:
                            axis.set_visible(True)
                    winner = f'Player {win_check(self.axes_dict)} wins!'
                    self.ax.text(self.ax.get_xlim()[1]/2, self.ax.get_ylim()[1]+0.8, winner, fontsize=20, horizontalalignment='center')
                    for key in self.axes_dict:
                        self.axes_dict[key] = float('nan')
                    self.i = 0

def main():

    fig, ax, bstart = starting_screen('Tic-Tac-Toe', 9, 9)

    axes_dict, bplay_again, bclose = draw_board(fig, ax) 

    square = Select_square(fig, ax, axes_dict)

    print(square.i)

    plt.show()

if __name__ == "__main__":
    main()