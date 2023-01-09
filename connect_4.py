import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
from functools import partial

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
        for patch in self.ax.patches:
            patch.set_visible(True)
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
        for patch in self.ax.patches:
            patch.set_alpha(1)
        for axis in self.fig.get_axes():
            if axis != self.ax and not axis.get_label() in self.invisible:
                for patch in axis.patches:
                    if True in list(map(lambda x: patch.get_label().startswith(x), self.remove)):
                        patch.remove()
            elif axis != self.ax:
                axis.set_visible(False)
        plt.draw()

    def close(self, event):
        
        plt.close()

def starting_screen(title, x_size, y_size):            

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.12)
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
    string = f'   Player {num}\'s turn     '
    str_txt = axis.text(axis.get_xlim()[1]/2, axis.get_ylim()[1], string, fontsize=20, horizontalalignment='center', visible=vis)

def draw_board(fig, ax):

    ax_bounds = ax.get_position().bounds
    height = ax_bounds[3] * 7 / 7.2
    width = ax_bounds[2] * 7 / 7.2

    rect = plt.Rectangle((0.1, 0.1), 7, 6, color='blue', visible=False)
    ax.add_patch(rect)

    for hpos in range(0,8):
        hpos += 0.1
        ax.plot([hpos]*2, [0.1,6.1], color='black', visible=False)

        if hpos < 7:

            x = ax_bounds[0] + hpos * width / 7
            y = ax_bounds[1] * 1.1
            position = fig.add_axes([x, y, width/7, height], visible=False, label=str(int(round(hpos-0.1,0))))
            position.set_xlim(0,1)
            position.set_ylim(0,7)
            position.axis('off')
            for colour in ['red', 'yellow']:
                circle = plt.Circle((0.5, 6.5), 0.45, fill=True, color=colour, visible=False, label=colour)
                position.add_patch(circle)
                circle = plt.Circle((0.5, 6.5), 0.45, fill=False, color='black', visible=False, label=colour)
                position.add_patch(circle)
                circle = plt.Circle((0.5, 6.5), 0.3, fill=False, color='black', visible=False, label=colour)
                position.add_patch(circle)
            
            for vpos in range(0,6):
                circle = plt.Circle((hpos+0.5, vpos+0.6), 0.45, fill=True, color='white', visible=False, label='white')
                ax.add_patch(circle)
                circle = plt.Circle((hpos+0.5, vpos+0.6), 0.45, fill=False, color='black', visible=False)
                ax.add_patch(circle)

    for vpos in [0,6]:
        vpos += 0.1
        ax.plot([0.1,7.1], [vpos]*2, 7, color='black', visible=False)
    
    players_turn_txt(1, ax, False)

    block_click = fig.add_axes(ax_bounds, visible=False, alpha=0, label='block_click')
    block_click.axis('off')

    play_again = fig.add_axes([0.28,0.01,0.2,0.1], visible=False, label='play_again')
    button = Buttons(fig, ax, ['dropped'], ['start', 'play_again', 'block_click', 'close'])
    bplay_again = Button(play_again, 'Play again')
    bplay_again.on_clicked(button.play_again)

    close = fig.add_axes([0.55,0.01,0.2,0.1], visible=False, label='close')
    button = Buttons(fig, ax)
    bclose = Button(close, 'Close')
    bclose.on_clicked(button.close)

    row = np.array([float('nan')]*7)
    matrix = row
    for i in range(5):
        matrix = np.vstack((matrix, row))

    return matrix, bplay_again, bclose

def drop_piece(i, colour, axis, distance):
    i += 1
    label = f'dropped_{distance-1}' if i == distance else 'dropped' 
    height = 6.5 - i
    circle1 = plt.Circle((0.5, height), 0.45, fill=True, color=colour, label=label)
    circle1 = axis.add_patch(circle1)
    circle2 = plt.Circle((0.5, height), 0.45, fill=False, color='black', label=label)
    circle2 = axis.add_patch(circle2)
    circle3 = plt.Circle((0.5, height), 0.3, fill=False, color='black', label=label)
    circle3 = axis.add_patch(circle3)

    return circle1, circle2, circle3

def win_check(board_matrix):

    # verticals
    for c in range(len(board_matrix)):
        col = board_matrix[c]
        for i in range(len(col[:-3])):
            win = True
            win_dict = {c:[i]}
            winner = col[i]
            for j in range(1,4):
                win = win and winner == col[i+j]
                win_dict[c] = win_dict.get(c, []) + [i+j]
            if win:
                return int(winner), win_dict

    # horizontals
    temp_matrix = np.transpose(board_matrix)
    for r in range(len(temp_matrix)):
        row = temp_matrix[r]
        for i in range(len(row[:-3])):
            win = True
            win_dict = {i:[r]}
            winner = row[i]
            for j in range(1,4):
                win = win and winner == row[i+j]
                win_dict[i+j] = win_dict.get(i+j, []) + [r]
            if win:
                return int(winner), win_dict

    # positive slope diagonals
    for row in range(len(board_matrix[0][:-3])):
        row = len(board_matrix[0]) - 1 - row
        for i in range(len(temp_matrix[row][:-3])):
            win = True
            win_dict = {i:[row]}
            winner = temp_matrix[row][i]
            for j in range(1,4):
                win = win and winner == temp_matrix[row-j][i+j]
                win_dict[i+j] = win_dict.get(i+j, []) + [row-j]
            if win:
                return int(winner), win_dict
                
    # negative slope diagonals
    temp_matrix = np.transpose(board_matrix)
    for row in range(len(board_matrix[0][:-3])):
        row = len(board_matrix[0]) - 1 - row
        for i in range(len(temp_matrix[row][:-3])):
            i = len(temp_matrix[row]) - 1 - i
            win = True
            win_dict = {i:[row]}
            winner = temp_matrix[row][i]
            for j in range(1,4):
                win = win and winner == temp_matrix[row-j][i-j]
                win_dict[i-j] = win_dict.get(i-j, []) + [row-j]
            if win:
                return int(winner), win_dict

    return None


class Select_column:

    def __init__(self, fig, ax, board_matrix):
        self.press_id = fig.canvas.mpl_connect('button_press_event', self.click)
        self.hover_id = fig.canvas.mpl_connect("motion_notify_event", self.hover)
        self.fig = fig
        self.ax = ax
        self.board_matrix = np.transpose(board_matrix)
        self.i = 0 

    def hover(self, event):
        colour = 'red' if self.i % 2 == 0 else 'yellow'
        for axis in self.fig.get_axes():
            if axis == event.inaxes and axis != self.ax:
                for patch in axis.patches:
                    if patch.get_label() == colour:
                        patch.set_visible(True)
                    elif not patch.get_label().startswith('dropped'):
                        patch.set_visible(False)
            elif axis != self.ax:
                for patch in axis.patches:
                    if not patch.get_label().startswith('dropped'):
                        patch.set_visible(False)
        plt.draw()  

    def click(self, event):

        global anim

        if not event.inaxes is None and event.inaxes.get_label().isdigit():

            label = int(event.inaxes.get_label())
            column = self.board_matrix[label]
            drop_distance = 0
            for spot in column:
                if spot != spot:
                    drop_distance += 1

            if drop_distance != 0:
            
                if self.i % 2 == 0:

                    colour = 'red' if self.i % 2 == 0 else 'yellow'
                    i = self.i % 2 + 1
                    self.board_matrix[label][drop_distance-1] = i

                    if self.i == 41:
                        drop_piece(0, colour=colour, axis=event.inaxes, distance=drop_distance)
                    else:
                        anim = FuncAnimation(self.fig, partial(drop_piece, colour=colour, axis=event.inaxes, distance=drop_distance), frames=drop_distance, interval=20, blit=True, repeat=False)
                    self.i += 1
                    for text in self.ax.texts:
                        text.remove()
                    if win_check(self.board_matrix) is None:
                        if self.i < 42:
                            players_turn_txt((self.i)%2+1, self.ax, True)
                            colour = 'red' if self.i % 2 == 0 else 'yellow'
                            for axis in self.fig.get_axes():
                                if axis == event.inaxes and axis != self.ax:
                                    for patch in axis.patches:
                                        if patch.get_label() == colour:
                                            patch.set_visible(True)
                                        elif not patch.get_label().startswith('dropped'):
                                            patch.set_visible(False)
                                elif axis != self.ax:
                                    for patch in axis.patches:
                                        if not patch.get_label().startswith('dropped'):
                                            patch.set_visible(False)
                            plt.draw()
                        else:
                            for axis in self.fig.get_axes():
                                if axis.get_label().isdigit() or axis == self.ax:
                                    for line in axis.lines:
                                        line.set_alpha(0.4)
                                    for patch in axis.patches:
                                        if patch.get_label() in ['red', 'yellow']:
                                            patch.set_visible(False)
                                        elif patch.get_label() != 'white':
                                            patch.set_alpha(0.4)
                                elif axis.get_label() in ['play_again', 'block_click', 'close']:
                                    axis.set_visible(True)
                            text = f'Tie game.'
                            self.ax.text(self.ax.get_xlim()[1]/2, self.ax.get_ylim()[1], text, fontsize=20, horizontalalignment='center')
                            for col in range(len(self.board_matrix)):
                                for row in range(len(self.board_matrix[col])):
                                    self.board_matrix[col][row] = float('nan')
                            self.i = 0
                    else:
                        win_dict = win_check(self.board_matrix)[1]
                        for axis in self.fig.get_axes():
                            if axis.get_label().isdigit() or axis == self.ax:
                                for line in axis.lines:
                                    line.set_alpha(0.4)
                                for patch in axis.patches:
                                    if patch.get_label() in ['red', 'yellow']:
                                        patch.set_visible(False)
                                    elif patch.get_label() != 'white':
                                        patch.set_alpha(0.4)
                                if axis.get_label() != '' and int(axis.get_label()) in list(win_dict.keys()):
                                    for patch in axis.patches:
                                        if patch.get_label() in list(map(lambda x: 'dropped_'+str(x), win_dict[int(axis.get_label())])):
                                            patch.set_alpha(1)
                            elif axis.get_label() in ['play_again', 'block_click', 'close']:
                                axis.set_visible(True)
                        text = f'Player {win_check(self.board_matrix)[0]} wins!'
                        self.ax.text(self.ax.get_xlim()[1]/2, self.ax.get_ylim()[1], text, fontsize=20, horizontalalignment='center')
                        for col in range(len(self.board_matrix)):
                            for row in range(len(self.board_matrix[col])):
                                self.board_matrix[col][row] = float('nan')
                        self.i = 0
                        
                elif self.i % 2 == 1:

                    colour = 'red' if self.i % 2 == 0 else 'yellow'
                    i = self.i % 2 + 1
                    self.board_matrix[label][drop_distance-1] = i

                    if self.i == 41:
                        drop_piece(0, colour=colour, axis=event.inaxes, distance=drop_distance)
                    else:
                        anim = FuncAnimation(self.fig, partial(drop_piece, colour=colour, axis=event.inaxes, distance=drop_distance), frames=drop_distance, interval=20, blit=True, repeat=False)
                    self.i += 1
                    for text in self.ax.texts:
                        text.remove()
                    if win_check(self.board_matrix) is None:
                        if self.i < 42:
                            players_turn_txt((self.i)%2+1, self.ax, True)
                            colour = 'red' if self.i % 2 == 0 else 'yellow'
                            for axis in self.fig.get_axes():
                                if axis == event.inaxes and axis != self.ax:
                                    for patch in axis.patches:
                                        if patch.get_label() == colour:
                                            patch.set_visible(True)
                                        elif not patch.get_label().startswith('dropped'):
                                            patch.set_visible(False)
                                elif axis != self.ax:
                                    for patch in axis.patches:
                                        if not patch.get_label().startswith('dropped'):
                                            patch.set_visible(False)
                            plt.draw()
                        else:
                            for axis in self.fig.get_axes():
                                if axis.get_label().isdigit() or axis == self.ax:
                                    for line in axis.lines:
                                        line.set_alpha(0.4)
                                    for patch in axis.patches:
                                        if patch.get_label() in ['red', 'yellow']:
                                            patch.set_visible(False)
                                        elif patch.get_label() != 'white':
                                            patch.set_alpha(0.4)
                                elif axis.get_label() in ['play_again', 'block_click', 'close']:
                                    axis.set_visible(True)
                            text = f'Tie game.'
                            self.ax.text(self.ax.get_xlim()[1]/2, self.ax.get_ylim()[1], text, fontsize=20, horizontalalignment='center')
                            for col in range(len(self.board_matrix)):
                                for row in range(len(self.board_matrix[col])):
                                    self.board_matrix[col][row] = float('nan')
                            self.i = 0
                    else:
                        win_dict = win_check(self.board_matrix)[1]
                        for axis in self.fig.get_axes():
                            if axis.get_label().isdigit() or axis == self.ax:
                                for line in axis.lines:
                                    line.set_alpha(0.4)
                                for patch in axis.patches:
                                    if patch.get_label() in ['red', 'yellow']:
                                        patch.set_visible(False)
                                    elif patch.get_label() != 'white':
                                        patch.set_alpha(0.4)
                                if axis.get_label() != '' and int(axis.get_label()) in list(win_dict.keys()):
                                    for patch in axis.patches:
                                        if patch.get_label() in list(map(lambda x: 'dropped_'+str(x), win_dict[int(axis.get_label())])):
                                            patch.set_alpha(1)
                            elif axis.get_label() in ['play_again', 'block_click', 'close']:
                                axis.set_visible(True)
                        text = f'Player {win_check(self.board_matrix)[0]} wins!'
                        self.ax.text(self.ax.get_xlim()[1]/2, self.ax.get_ylim()[1], text, fontsize=20, horizontalalignment='center')
                        for col in range(len(self.board_matrix)):
                            for row in range(len(self.board_matrix[col])):
                                self.board_matrix[col][row] = float('nan')
                        self.i = 0

def main():

    fig, ax, bstart = starting_screen('Connect 4', 7.2, 7.2)

    board_matrix, bplay_again, bclose = draw_board(fig, ax) 

    select = Select_column(fig, ax, board_matrix)

    plt.show()

if __name__ == "__main__":
    main()