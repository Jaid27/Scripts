import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random
from matplotlib.animation import FuncAnimation
from functools import partial


def show_all_pairs(i, fig, ax, invisible, text, size):
    patch_list = []

    if i < 5:
        for axis in fig.get_axes():
            if axis != ax and not axis.get_label() in invisible:
                if axis.get_label().startswith(size):
                    for patch in axis.patches:
                        patch.set_visible(True)
                        patch_list.append(patch)
                    for line in axis.lines:
                        line.set_visible(True)
                        patch_list.append(line)
            if axis.get_label() == 'block_click':
                axis.set_visible(True)
                patch_list.append(axis)

        text.set_text(text.get_text()[:-1] + str(5-i))
        patch_list.append(text)

    else:
        for axis in fig.get_axes():
            if axis != ax and not axis.get_label() in invisible:
                if axis.get_label().startswith(size):
                    for patch in axis.patches:
                        patch.set_visible(False)
                        patch_list.append(patch)
                    for line in axis.lines:
                        line.set_visible(False)
                        patch_list.append(line)
            if axis.get_label() == 'block_click':
                axis.set_visible(False)
                patch_list.append(axis)                

        text.set_text('Guess count: 0')
        patch_list.append(text)

    return patch_list

class Buttons:

    def __init__(self, fig, ax, remove=[], invisible=[]):
        
        self.fig = fig
        self.ax = ax
        self.remove = remove
        self.invisible = invisible


    def start_3x4(self, event):

        global anim

        size = '3x4'

        for txt in self.ax.texts:
            if txt.get_label() in self.remove:
                txt.remove()
            elif txt.get_label() in self.invisible:
                txt.set_visible(False)
        for patch in self.ax.patches:
            if patch.get_label().startswith(size):
                patch.set_visible(True)
        for axis in self.fig.get_axes():
            if axis != self.ax and not axis.get_label() in self.invisible:
                if axis.get_label().startswith(size) or axis.get_label() == 'block_click':
                    axis.set_visible(True)
            elif axis != self.ax:
                axis.set_visible(False)

        text = self.ax.text(self.ax.get_xlim()[1]/2, self.ax.get_ylim()[1]-4, f'Time left: 5', fontsize=20, horizontalalignment='center', visible=True)
        anim = FuncAnimation(self.fig, partial(show_all_pairs, fig=self.fig, ax=self.ax, invisible=self.invisible, text=text, size=size), interval=1000, frames=6, repeat=False, blit=True)

    def start_4x5(self, event):

        global anim

        size = '4x5'

        for txt in self.ax.texts:
            if txt.get_label() in self.remove:
                txt.remove()
            elif txt.get_label() in self.invisible:
                txt.set_visible(False)
        for patch in self.ax.patches:
            if patch.get_label().startswith(size):
                patch.set_visible(True)
        for axis in self.fig.get_axes():
            if axis != self.ax and not axis.get_label() in self.invisible:
                if axis.get_label().startswith(size) or axis.get_label() == 'block_click':
                    axis.set_visible(True)
            elif axis != self.ax:
                axis.set_visible(False)

        text = self.ax.text(self.ax.get_xlim()[1]/2, self.ax.get_ylim()[1]-4, f'Time left: 5', fontsize=20, horizontalalignment='center', visible=True)
        anim = FuncAnimation(self.fig, partial(show_all_pairs, fig=self.fig, ax=self.ax, invisible=self.invisible, text=text, size=size), interval=1000, frames=6, repeat=False, blit=True)


    def start_5x6(self, event):

        global anim

        size = '5x6'

        for txt in self.ax.texts:
            if txt.get_label() in self.remove:
                txt.remove()
            elif txt.get_label() in self.invisible:
                txt.set_visible(False)
        for patch in self.ax.patches:
            if patch.get_label().startswith(size):
                patch.set_visible(True)
        for axis in self.fig.get_axes():
            if axis != self.ax and not axis.get_label() in self.invisible:
                if axis.get_label().startswith(size) or axis.get_label() == 'block_click':
                    axis.set_visible(True)
            elif axis != self.ax:
                axis.set_visible(False)

        text = self.ax.text(self.ax.get_xlim()[1]/2, self.ax.get_ylim()[1]-4, f'Time left: 5', fontsize=20, horizontalalignment='center', visible=True)
        anim = FuncAnimation(self.fig, partial(show_all_pairs, fig=self.fig, ax=self.ax, invisible=self.invisible, text=text, size=size), interval=1000, frames=6, repeat=False, blit=True)

    def return_(self, event):

        draw_board(self.fig, self.ax)

    def close(self, event):
        
        plt.close()

def starting_screen(title, x_size, y_size):            

    fig, ax = plt.subplots()
    fig.subplots_adjust(top=0.9)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(0,x_size)
    ax.set_ylim(0,y_size)
    ax.axis('off')
    ax.margins(x=1, y=1)
    text = ax.text(x_size/2, y_size*0.8, title, fontsize=30, horizontalalignment='center', label='title')
    text = ax.text(0, y_size*0.3, 'Best:  ', fontsize=11, label='s3x4')
    text = ax.text(x_size*0.4, y_size*0.3, 'Best:  ', fontsize=11, label='s4x5')
    text = ax.text(x_size*0.8, y_size*0.3, 'Best:  ', fontsize=11, label='s5x6')

    size_3x4 = fig.add_axes([0.2,0.4,0.16,0.1], label='b3x4')
    button = Buttons(fig, ax, ['title'], ['b3x4', 'b4x5', 'b5x6', 'block_click', 'close', 'return', 's3x4', 's4x5', 's5x6'])
    b_3x4 = Button(size_3x4, '3x4')
    b_3x4.on_clicked(button.start_3x4)

    size_4x5 = fig.add_axes([0.42,0.4,0.16,0.1], label='b4x5')
    button = Buttons(fig, ax, ['title'], ['b3x4', 'b4x5', 'b5x6', 'block_click', 'close', 'return', 's3x4', 's4x5', 's5x6'])
    b_4x5 = Button(size_4x5, '4x5')
    b_4x5.on_clicked(button.start_4x5)

    size_5x6 = fig.add_axes([0.64,0.4,0.16,0.1], label='b5x6')
    button = Buttons(fig, ax, ['title'], ['b3x4', 'b4x5', 'b5x6', 'block_click', 'close', 'return', 's3x4', 's4x5', 's5x6'])
    b_5x6 = Button(size_5x6, '5x6')
    b_5x6.on_clicked(button.start_5x6)

    close = fig.add_axes([0.42,0.1,0.16,0.1], visible=True, label='close')
    button = Buttons(fig, ax)
    bclose = Button(close, 'Close')
    bclose.on_clicked(button.close)

    return_ = fig.add_axes([0.4,0.25,0.2,0.1], visible=False, label='return', zorder=5)
    button = Buttons(fig, ax, ['count', '3x4', '4x5', '5x6', 'correct'], ['block_click', 'return'])
    breturn = Button(return_, 'Return')
    breturn.on_clicked(button.return_)

    return fig, ax, b_3x4, b_4x5, b_5x6, bclose, breturn


def draw_board(fig, ax):

    ax_bounds = ax.get_position().bounds
    height = ax_bounds[3] * 60/65
    width = ax_bounds[2]

    r = 4
    c = 3
    shapes = {'square':['red','blue','green']*2, 'circle':['red','blue','green']*2}
    for row in range(r):
        for col in range(c):
            rect = plt.Rectangle((row*60/r+1,col*60/c+1), 60/r-2, 60/c-2, linewidth=4, fill=False, color='black', visible=False, label='3x4')
            ax.add_patch(rect)
            x = ax_bounds[0]+width/60+row*width/r
            y = ax_bounds[1]+height/60+col*height/c
            w = width/r-width*2/60
            h = height/c-height*2/60
            position = fig.add_axes([x, y, w, h], visible=False, label=f'3x4', facecolor='m')
            position.set_xlim(0,60/r-2)
            position.set_ylim(0,60/c-2)
            position.axis('off')
            shape = random.choice([shape for shape in shapes.keys() if len(shapes[shape]) > 0])
            colour = random.choice(shapes[shape])
            shapes[shape].remove(colour)
            if shape == 'square':
                size_factor = 0.6
                length = (60/r-2) * size_factor
                x = ((60/r-2) - (60/r-2) * size_factor) / 2
                y = ((60/c-2) - (60/r-2) * size_factor) / 2
                square = plt.Rectangle((x,y), length, length, color=colour, fill=False, linewidth=4, visible=False, label=f'{colour}_{shape}')
                position.add_patch(square)
            elif shape == 'circle':
                size_factor = 0.7
                diameter = (60/r-2) * size_factor
                x = (60/r-2) / 2
                y = (60/c-2) / 2
                circle = plt.Circle((x,y), diameter/2, color=colour, fill=False, linewidth=4, visible=False, label=f'{colour}_{shape}')
                position.add_patch(circle)

    r = 5
    c = 4
    shapes = {'square':['red','blue','green','orange','purple']*2, 'circle':['red','blue','green','orange','purple']*2}
    for row in range(r):
        for col in range(c):
            rect = plt.Rectangle((row*60/r+1,col*60/c+1), 60/r-2, 60/c-2, linewidth=4, fill=False, color='black', visible=False, label='4x5')
            ax.add_patch(rect)
            x = ax_bounds[0]+width/60+row*width/r
            y = ax_bounds[1]+height/60+col*height/c
            w = width/r-width*2/60
            h = height/c-height*2/60
            position = fig.add_axes([x, y, w, h], visible=False, label=f'4x5')
            position.set_xlim(0,60/r-2)
            position.set_ylim(0,60/c-2)
            position.axis('off')
            shape = random.choice([shape for shape in shapes.keys() if len(shapes[shape]) > 0])
            colour = random.choice(shapes[shape])
            shapes[shape].remove(colour)
            if shape == 'square':
                size_factor = 0.6
                length = (60/r-2) * size_factor
                x = ((60/r-2) - (60/r-2) * size_factor) / 2
                y = ((60/c-2) - (60/r-2) * size_factor) / 2
                square = plt.Rectangle((x,y), length, length, color=colour, fill=False, linewidth=4, visible=False, label=f'{colour}_{shape}')
                position.add_patch(square)
            elif shape == 'circle':
                size_factor = 0.7
                diameter = (60/r-2) * size_factor
                x = (60/r-2) / 2
                y = (60/c-2) / 2
                circle = plt.Circle((x,y), diameter/2, color=colour, fill=False, linewidth=4, visible=False, label=f'{colour}_{shape}')
                position.add_patch(circle)

    r = 6
    c = 5
    shapes = {'square':['red','blue','green','orange','purple']*2, 'circle':['red','blue','green','orange','purple']*2, 'triangle':['red','blue','green','orange','purple']*2}
    for row in range(r):
        for col in range(c):
            rect = plt.Rectangle((row*60/r+1,col*60/c+1), 60/r-2, 60/c-2, linewidth=4, fill=False, color='black', visible=False, label='5x6')
            ax.add_patch(rect)
            x = ax_bounds[0]+width/60+row*width/r
            y = ax_bounds[1]+height/60+col*height/c
            w = width/r-width*2/60
            h = height/c-height*2/60
            position = fig.add_axes([x, y, w, h], visible=False, label=f'5x6')
            position.set_xlim(0,60/r-2)
            position.set_ylim(0,60/c-2)
            position.axis('off')
            shape = random.choice([shape for shape in shapes.keys() if len(shapes[shape]) > 0])
            colour = random.choice(shapes[shape])
            shapes[shape].remove(colour)
            if shape == 'square':
                size_factor = 0.6
                length = (60/r-2) * size_factor
                x = ((60/r-2) - (60/r-2) * size_factor) / 2
                y = ((60/c-2) - (60/r-2) * size_factor) / 2
                square = plt.Rectangle((x,y), length, length, color=colour, fill=False, linewidth=4, visible=False, label=f'{colour}_{shape}')
                position.add_patch(square)
            elif shape == 'circle':
                size_factor = 0.7
                diameter = (60/r-2) * size_factor
                x = (60/r-2) / 2
                y = (60/c-2) / 2
                circle = plt.Circle((x,y), diameter/2, color=colour, fill=False, linewidth=4, visible=False, label=f'{colour}_{shape}')
                position.add_patch(circle)
            elif shape == 'triangle':
                size_factor = 0.6
                length = (60/r-2) * size_factor
                x1 = ((60/r-2) - (60/r-2) * size_factor) / 2
                y1 = ((60/c-2) - (60/r-2) * size_factor) / 2
                x2 = x1 + length
                y2 = y1
                x3 = x1 + length/2
                y3 = y1 + length
                position.plot([x1,x2,x3,x1], [y1,y2,y3,y1], color=colour, linewidth=4, visible=False, label=f'{colour}_{shape}')

    block_click = fig.add_axes(ax_bounds, visible=False, alpha=0.5, facecolor='m', label='block_click')
    block_click.axis('off')


class Select_card:

    def __init__(self, fig, ax):
        self.press_id = fig.canvas.mpl_connect('button_press_event', self.click)
        self.fig = fig
        self.ax = ax
        self.i = 0 
        self.total = None
        self.correct = 0
        self.label = None
        self.guess1 = None
        self.guess1 = None
        self.count = 0
        self.guessed = []
        self.best = {'3x4':float('inf'),'4x5':float('inf'),'5x6':float('inf')}


    def click(self, event):

        if not event.inaxes is None and event.inaxes.get_label() == 'return':

            remove = ['count', '3x4', '4x5', '5x6', 'correct']
            invisible = ['block_click', 'return']


            for txt in self.ax.texts:
                if txt.get_label() in remove:
                    txt.remove()
                elif txt.get_label() in invisible:
                    txt.set_visible(False)
                else:
                    txt.set_visible(True)
            for patch in self.ax.patches:
                if patch.get_label() in remove:
                    patch.remove()
            for axis in self.fig.get_axes():
                if axis.get_label() in remove:
                    axis.remove()
                elif axis != self.ax and axis.get_label() != 'block_click' and not axis.get_label() in invisible:
                    axis.set_visible(True)
                elif axis != self.ax and axis.get_label() != 'block_click':
                    print(axis.get_label())
                    axis.set_visible(False)

            text = self.ax.text(self.ax.get_xlim()[1]/2, self.ax.get_ylim()[1]*0.8, 'Matching', fontsize=30, horizontalalignment='center', label='title')
            plt.draw()

        elif not event.inaxes is None and len(event.inaxes.get_label()) == 4 and event.inaxes.get_label()[0] == 'b' and event.inaxes.get_label()[2] == 'x':
            self.total = int(event.inaxes.get_label()[1]) * int(event.inaxes.get_label()[-1])
            self.label = event.inaxes.get_label()[1:]

        elif not event.inaxes is None and event.inaxes.get_label() == self.label:

            if self.i % 2 == 0:

                if len(self.guessed) > 0:
                    for axis in self.guessed:
                        for patch in axis.patches:
                            patch.set_visible(False)
                        for line in axis.lines:
                            line.set_visible(False)
                    self.guessed = []

                self.i += 1  
                self.guessed.append(event.inaxes)

                for patch in event.inaxes.patches:
                    patch.set_visible(True)
                    self.guess1 = patch.get_label() if not patch is None else ''
                for line in event.inaxes.lines:
                    line.set_visible(True)
                    self.guess1 = line.get_label() if not line is None else ''
                event.inaxes.set_label('guessed') 

            elif self.i % 2 == 1:
                self.i += 1  
                self.count += 1
                self.guessed.append(event.inaxes)

                for text in self.ax.texts:
                    if len(text.get_label()) == 0 or not text.get_label()[1:] in ['3x4','4x5','5x6']:
                        text.remove()
                self.ax.text(self.ax.get_xlim()[1]/2, self.ax.get_ylim()[1]-4, f'Guess count: {self.count}', fontsize=20, horizontalalignment='center', visible=True, label='count')

                for patch in event.inaxes.patches:
                    patch.set_visible(True)
                    self.guess2 = patch.get_label() if not patch is None else ''
                for line in event.inaxes.lines:
                    line.set_visible(True)
                    self.guess2 = line.get_label() if not line is None else ''
                event.inaxes.set_label('guessed')

                if self.guess1 == self.guess2:
                    for axis in self.guessed:
                        axis.set_label('correct')
                    self.guessed = []
                    self.correct += 2

                    if self.correct == self.total:
                        for axis in self.fig.get_axes():
                            if axis.get_label() == 'return':
                                axis.set_visible(True)

                        if self.count < self.best[self.label]:
                            self.best[self.label] = self.count
                            for text in self.ax.texts:
                                if text.get_label().endswith(self.label):
                                    text.set_text(text.get_text()[:6] + str(self.best[self.label]))

                        self.i = 0 
                        self.total = None
                        self.correct = 0
                        self.label = None
                        self.guess1 = None
                        self.guess1 = None
                        self.count = 0
                        self.guessed = []

                else:
                    for axis in self.guessed:
                        axis.set_label(self.label)

            plt.draw()
                    

def main():

    fig, ax, b_3x4, b_4x5, b_5x6, bclose, breturn = starting_screen('Matching', 60, 65)

    draw_board(fig, ax) 

    select = Select_card(fig, ax)

    plt.show()

if __name__ == "__main__":
    main()