import game_of_life_interface
import numpy as np
import matplotlib.pyplot as plt

class GameOfLife(game_of_life_interface.GameOfLife):  # This is the way you construct a class that inherits properties
    def __init__(self, size_of_board, board_start_mode, rules, rle, pattern_position):
        self.size_of_board = size_of_board
        self.board_start_mode = board_start_mode
        self.rules=rules.upper()
        self.rle=rle
        self.pattern_position=pattern_position
        bornList= []
        for i in range(self.rules.find('B')+1, self.rules.find('/')):
            bornList.append(int(self.rules[i]))
        self.bornList= bornList
        surviveList=[]
        for i in range(self.rules.find('S')+1, len(self.rules)):
            surviveList.append(int(self.rules[i]))
        self.surviveList= surviveList
        self.board=np.zeros(([size_of_board, size_of_board])).tolist()

        if self.rle == "":
            if self.board_start_mode == 1 or (self.board_start_mode<1 or self.board_start_mode > 4) :
                self.board = np.random.choice([0,255], size=(self.size_of_board,self.size_of_board) , p=(0.5,0.5))
            elif self.board_start_mode == 2:
                self.board = np.random.choice([0,255], size=(self.size_of_board,self.size_of_board), p=(0.2, 0.8))
            elif self.board_start_mode == 3:
                self.board = np.random.choice([0,255], size=(self.size_of_board,self.size_of_board), p=(0.8, 0.2))
            elif self.board_start_mode == 4:
                gun_rle = "24bo11b$22bobo11b$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o14b$2o8bo3bob2o4bobo11b$10bo5bo7bo11b$11bo3bo20b$12b2o!"
                gun_board = self.transform_rle_to_matrix(gun_rle)
                num_row = len(gun_board)
                num_col = len(gun_board[0])
                for i in range(10, num_row+10):
                    for k in range(10, num_col+10):
                        self.board[i][k] = gun_board[i-10][k-10]
        else:
            rle_board = self.transform_rle_to_matrix(self.rle)
            row_rle= len(rle_board)
            col_rle= len(rle_board[0])
            for i in range(pattern_position[0],row_rle + pattern_position[0]):
                for k in range(pattern_position[1], col_rle + pattern_position[1]):
                    self.board[i][k] = rle_board[i - pattern_position[0]][k - pattern_position[1]]


    def countNeighbors(self, row, col):
        count=0
        if row!=0 and row !=self.size_of_board-1 and col!=0 and col !=self.size_of_board-1:
            count = self.board[row-1][col-1]+self.board[row-1][col]+self.board[row-1][col+1]
            count += self.board[row][col+1]+self.board[row+1][col+1]+self.board[row+1][col]
            count +=self.board[row+1][col-1]+self.board[row][col-1]
            return int(count//255)
        elif row==0 :
            if col==0:
                count = self.board[row][col+1]+self.board[row+1][col+1]+self.board[row+1][col]
                count += self.board[row][self.size_of_board-1]+self.board[row+1][self.size_of_board-1]
                count +=self.board[self.size_of_board-1][self.size_of_board-1]
                count += self.board[self.size_of_board-1][col+1]+self.board[self.size_of_board-1][col]
                return int(count//255)
            elif col == self.size_of_board-1 :
                count = self.board[row+1][col]+self.board[row+1][col-1]+self.board[row][col-1]
                count += self.board[self.size_of_board-1][col]+self.board[self.size_of_board-1][col-1]
                count += self.board[self.size_of_board-1][0]+self.board[1][0]+self.board[0][0]
                return int(count//255)
            else:
                count = self.board[row][col+1] + self.board[row+1][col+1] + self.board[row+1][col]
                count += self.board[row+1][col-1] + self.board[row][col-1] + self.board[self.size_of_board-1][col+1]
                count += self.board[self.size_of_board-1][col] + self.board[self.size_of_board-1][col-1]
                return int(count//255)
        elif col == self.size_of_board-1:
            if row == self.size_of_board-1 :
                count = self.board[row][col-1]+self.board[row-1][col-1]+self.board[row-1][col]
                count += self.board[row][0]+self.board[row-1][0]+self.board[0][0]
                count += self.board[0][col-1]+self.board[0][col]
                return int(count//255)
            else:
                count = self.board[row+1][col]+self.board[row+1][col-1]+self.board[row][col-1]
                count += self.board[row-1][col-1]+self.board[row-1][col]
                count += self.board[row+1][0]+self.board[row][0]+self.board[row-1][0]
                return int(count//255)
        elif row == self.size_of_board-1 :
            if col == 0 :
                count = self.board[row-1][col]+self.board[row-1][col+1]+self.board[row][col+1]
                count += self.board[0][col]+self.board[0][col+1]+ self.board[0][self.size_of_board-1]
                count += self.board[row-1][self.size_of_board-1]+self.board[row][self.size_of_board-1]
                return int(count//255)
            else:
                count = self.board[row][col-1]+self.board[row-1][col-1]+self.board[row-1][col]
                count += self.board[row-1][col+1]+self.board[row][col+1]
                count += self.board[0][col-1]+self.board[0][col]+self.board[0][col+1]
                return int(count//255)
        else:
            count = self.board[row-1][col]+self.board[row-1][col+1]+self.board[row][col+1]
            count += self.board[row+1][col+1]+self.board[row+1][col] +self.board[row-1][self.size_of_board-1]
            count += self.board[row][self.size_of_board-1]+self.board[row+1][self.size_of_board-1]
            return int(count//255)

    def save_board_to_file(self, file_name):
        return plt.imsave(file_name, self.board, format="png")

    def update(self):
        next = np.zeros(([self.size_of_board, self.size_of_board])).tolist()
        for row in range(0, self.size_of_board):
            for col in range(0,self.size_of_board):
                neighbors = self.countNeighbors(row,col)
                if self.board[row][col] == 255:
                    if self.surviveList.count(neighbors) == 0 :
                        next[row][col] = 0
                    else:
                        next[row][col] = self.board[row][col]
                else:
                    if self.bornList.count(neighbors) != 0 :
                        next[row][col] = 255
                    else:
                        next[row][col] = self.board[row][col]
        self.board= next

    def transform_rle_to_matrix(self, rle):
        if rle.count('!') == 0:
            return []
        index = 0
        list = [[]]
        while rle[index] != '!':
            if rle[index].isdigit() == True:
                if rle[index + 1].isdigit() == True:
                    num = int(rle[index]) * 10 + int(rle[index + 1])
                    if rle[index + 2] == 'b':
                        cell = 0
                    elif rle[index + 2] == 'o':
                        cell = 255
                    else:
                        cell = []
                    index += 3
                else:
                    num = int(rle[index])
                    if rle[index + 1] == 'b':
                        cell = 0
                    elif rle[index + 1] == 'o':
                        cell = 255
                    else:
                        cell = []
                    index += 2
                if cell == []:
                    for i in range(num):
                        list.append([])
                else:
                    last_index = len(list) - 1
                    for i in range(num):
                        list[last_index].append(cell)
                last_index = len(list) - 1
            else:
                last_index = len(list) - 1
                if rle[index] == 'b':
                    list[last_index].append(0)
                elif rle[index] == 'o':
                    list[last_index].append(255)
                else:
                    list.append([])
                index += 1

        for i in range(len(list)):
            if list[i] == []:
                for k in range(len(list[0])):
                    list[i].append(0)
        last_index = len(list) - 1
        while len(list[last_index]) < len(list[0]):
            list[last_index].append(0)
        return list

    def display_board(self):
        plt.imshow(self.board)

    def return_board(self):
        return self.board

if __name__ == '__main__':  # You should keep this line for our auto-grading code.
    zmani = GameOfLife(100,1,'B3/S23',"",(0,0))
    plt.imshow(zmani.return_board())
    # add 2 second delay so we can see first plot
    plt.pause(2)
    for i in range(100):
        zmani.update()
        zmani.display_board()
        plt.pause(0.01)

    zmani.save_board_to_file('last_tmuna.png')
