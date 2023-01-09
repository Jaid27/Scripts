import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from textwrap import wrap
import random

def main():

    length = 10
    height = length/2 * np.sqrt(3)
    plt_time = 10
    triangle = [[0,0], [length/2,height], [length,0]]
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.set_aspect('equal', adjustable='box')
    ax.plot([point[0] for point in triangle]+[triangle[0][0]], [point[1] for point in triangle]+[triangle[0][1]], color='blue')
    for point in triangle:
        ax.plot(point[0], point[1], marker='o', color='blue')

    def plt_txt(string):
        return ax.text(0, height+1,'\n'.join(wrap(string, width=52)))

    class Next:
        ind = 0
        temp_text = None
        temp_vertex = None
        selected_point = None
        temp_line = None
        new_coords = None
        new_point = None
        count = 0

        def next(self, event):

            self.ind += 1

            if self.ind == 1:
                ax.texts[0].remove()
                self.temp_text = plt_txt('Now, one of the three triangle points are selected at random and the points are connected. Click Next.')
                idx = random.randint(0,2)
                self.temp_vertex = ax.plot(triangle[idx][0], triangle[idx][1], marker='o', color='red')[0]
                for line in ax.lines:
                    if 0 < line.get_xdata()[0] < length and 0 < line.get_ydata()[0] < height:
                        self.selected_point = line
                self.temp_line = ax.plot([self.temp_vertex.get_data()[0][0],self.selected_point.get_xdata()[0]], 
                                            [self.temp_vertex.get_data()[1][0],self.selected_point.get_ydata()[0]], color='red')[0]

            elif self.ind == 2:
                self.temp_text.remove()
                self.temp_text = plt_txt('Now, a point is placed in the middle of this line. Click Next.')
                self.new_coords = [(self.temp_vertex.get_data()[0][0]+self.selected_point.get_xdata()[0])/2, 
                                    (self.temp_vertex.get_data()[1][0]+self.selected_point.get_ydata()[0])/2]
                self.new_point = ax.plot(self.new_coords[0], self.new_coords[1], marker='o', color='black')[0]

            elif self.ind == 3:
                self.temp_text.remove()
                self.temp_text = plt_txt('The point will be left here, and the process repeated. Click Next.')
                self.new_point.remove()
                self.temp_vertex.remove()
                self.temp_line.remove()
                self.selected_point.remove()
                ax.plot(self.new_coords[0], self.new_coords[1], marker='o', color='black', markersize='0.7')
                self.count += 1

            elif self.ind == 4:
                self.temp_text.remove()
                self.temp_text = plt_txt('Selecting a random vertex again, a line is then drawn and a point placed in the middle. Click Next.')
                idx = random.randint(0,2)
                self.temp_vertex = ax.plot(triangle[idx][0], triangle[idx][1], marker='o', color='red')[0]
                self.selected_point = ax.plot(self.new_coords[0], self.new_coords[1], marker='o', color='red')[0]  
                self.temp_line = ax.plot([self.temp_vertex.get_data()[0][0],self.selected_point.get_data()[0][0]], 
                                            [self.temp_vertex.get_data()[1][0],self.selected_point.get_data()[1][0]], color='red')[0] 
                self.new_coords = [(self.temp_vertex.get_data()[0][0]+self.selected_point.get_data()[0][0])/2, 
                                    (self.temp_vertex.get_data()[1][0]+self.selected_point.get_data()[1][0])/2]
                self.new_point = ax.plot(self.new_coords[0], self.new_coords[1], marker='o', color='black')[0]

            elif self.ind == 5:
                self.temp_text.remove()
                self.temp_text = plt_txt('The midpoint will be left here again. What happens if this is done 100 times? Click Next.')
                self.new_point.remove()
                self.temp_vertex.remove()
                self.temp_line.remove()
                self.selected_point.remove()
                ax.plot(self.new_coords[0], self.new_coords[1], marker='o', color='black', markersize='0.7')
                self.count += 1

            elif self.ind == 6:
                self.temp_text.remove()
                self.temp_text = plt_txt('How about 1,000 times? Click Next.')
                while self.count < 100:
                    idx = random.randint(0,2)
                    self.temp_vertex = triangle[idx]
                    self.selected_point = self.new_coords  
                    self.new_coords = [(self.temp_vertex[0]+self.selected_point[0])/2, 
                                        (self.temp_vertex[1]+self.selected_point[1])/2]
                    ax.plot(self.new_coords[0], self.new_coords[1], marker='o', color='black', markersize='0.7')
                    self.count += 1

            elif self.ind == 7:
                self.temp_text.remove()
                self.temp_text = plt_txt('How about 10,000 times? Click Next ONCE and wait.')
                while self.count < 1000:
                    idx = random.randint(0,2)
                    self.temp_vertex = triangle[idx]
                    self.selected_point = self.new_coords  
                    self.new_coords = [(self.temp_vertex[0]+self.selected_point[0])/2, 
                                        (self.temp_vertex[1]+self.selected_point[1])/2]
                    ax.plot(self.new_coords[0], self.new_coords[1], marker='o', color='black', markersize='0.7')
                    self.count += 1

            elif self.ind == 8:
                self.temp_text.remove()
                self.temp_text = plt_txt('How about 25,000 times? Click Next ONCE and wait.')
                while self.count < 10000:
                    idx = random.randint(0,2)
                    self.temp_vertex = triangle[idx]
                    self.selected_point = self.new_coords  
                    self.new_coords = [(self.temp_vertex[0]+self.selected_point[0])/2, 
                                        (self.temp_vertex[1]+self.selected_point[1])/2]
                    ax.plot(self.new_coords[0], self.new_coords[1], marker='o', color='black', markersize='0.7')
                    self.count += 1
                
            elif self.ind == 9:
                self.temp_text.remove()
                self.temp_text = plt_txt('Sierpinski\'s Triangle!')
                while self.count < 25000:
                    idx = random.randint(0,2)
                    self.temp_vertex = triangle[idx]
                    self.selected_point = self.new_coords  
                    self.new_coords = [(self.temp_vertex[0]+self.selected_point[0])/2, 
                                        (self.temp_vertex[1]+self.selected_point[1])/2]
                    ax.plot(self.new_coords[0], self.new_coords[1], marker='o', color='black', markersize='0.7')
                    self.count += 1
                bnext.label.set_text('Close')

            if self.ind == 10:
                plt.close()
            else:
                plt.draw()

    class Select_point:
        
        temp_text = plt_txt('Start by clicking any point inside of the equilateral triangle below.')

        def __init__(self, selected):
            self.cid = fig.canvas.mpl_connect('button_press_event', self)
            self.x = None
            self.y = None
            self.selected = selected

        def __call__(self, event):
            if not self.selected and event.inaxes == ax:
                x = event.xdata
                y = event.ydata
                if 0 < x <= 5:
                    if 0 < y <= x * np.sqrt(3):
                        self.x = x
                        self.y = y
                        self.selected = True
                elif 5 < x < 10:
                    if 0 < y <= (10-x) * np.sqrt(3):
                        self.x = x
                        self.y = y
                        self.selected = True
                if self.selected:
                    bnext.on_clicked(button.next)
                    location.set_visible(True)
                    ax.plot(self.x, self.y, marker='o', color='red')
                    self.temp_text.remove()
                    temp_text = plt_txt('Great! Click Next.')
                    plt.draw()
                       

    point = Select_point(selected = False)
    button = Next()
    location = fig.add_axes([0.7, 0.05, 0.1, 0.075])
    bnext = Button(location, 'Next')
    location.set_visible(False)

    ax.axis('off')
    plt.show()


if __name__ == '__main__':
    main()