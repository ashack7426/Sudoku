import random
import copy
import pygame
import time
import numpy as np

class Sudoku:
    def __init__(self,size,width,height,speed,full,curr):
        self.strikes = 0
        self.count = 0

        if full and curr:
            self.full = []
            self.curr = []
            vals = {
                '0' : 0,
                'A' : 1,
                'B' : 2,
                'C' : 3,
                'D' : 4,
                'E' : 5,
                'F' : 6,
                'G' : 7,
                'H' : 8,
                'I' : 9,
                'J' : 10,
                'K' : 11,
                'L' : 12,
                'M' : 13,
                'N' : 14,
                'O' : 15, 
                'P' : 16,
                'Q' : 17,
                'R' : 18,
                'S' : 19,
                'T' : 20,
                'U' : 21,
                'V' : 22,
                'W' : 23,
                'X' : 24,
                'Y' : 25,
                'Z' : 26,
                '1' : 27,
                '2' : 28,
                '3' : 29,
                '4' : 30,
                '5' : 31,
                '6' : 32,
                '7' : 33,
                '8' : 34,
                '9' : 35,
                '$' : 36,
                '#' : 37,
                '+' : 38,
                'a': 39, 
                'b': 40, 
                'c': 41, 
                'd': 42, 
                'e': 43, 
                'f': 44, 
                'g': 45, 
                'h': 46, 
                'i': 47, 
                'j': 48, 
                'k': 49, 
                'm': 50, 
                'n': 51, 
                'o': 52, 
                'p': 53, 
                'q': 54, 
                'r': 55, 
                's': 56, 
                't': 57, 
                'u': 58, 
                'v': 59, 
                'w': 60, 
                'x': 61, 
                'y': 62, 
                'z': 63,
                '?' : 64 
            }

            self.size = int(full[0])


            for line in open(full, "r"):
                row = line.split(" ")

                for i in range(len(row)):
                    if self.size > 4:
                        row[i] = vals[row[i][0]]
                    else:
                        row[i] = int(row[i][0])
            
                self.full.append(row)

            for line in open(curr, "r"):
                row = line.split(" ")
               
                
                for i in range(len(row)):
                    if self.size > 4:
                        row[i] = vals[row[i][0]]
                    else:
                        row[i] = int(row[i][0])
            
                self.curr.append(row)

            
           
        else:
            self.size = size
            self.full, self.curr = self.__genBoard() #get a random board

        self.width = width // (self.size ** 2) * self.size ** 2
        self.speed = speed #delay between frames for solving animiation
        self.height = height
        
        self.pencils = self.__genPencils() 
        self.selected = (0,0)
        self.win = pygame.display.set_mode((self.width,self.height + 60))
        pygame.display.set_caption("Sudoku")
        pygame.font.init()
    
    
    #reset the board
    def reset(self):
        self.__init__(self.size,self.width,self.height,self.speed, None,None)
    
    #setup pencil marks
    def __genPencils(self):
        pencils = []
        for _ in range(self.size ** 2):
            pencils.append([0] * (self.size ** 2))

        for i in range(len(self.curr)):
            for j in range(len(self.curr[0])):
                if self.curr[i][j]:
                    pencils[i][j] = [self.curr[i][j]]
                else:
                    pencils[i][j] = []
        
        return pencils

    #generate random boards
    def __genBoard(self):
        full_board = []
        start_board = []
        for _ in range(self.size ** 2):
            full_board.append([0] * (self.size ** 2))
            start_board.append([0] * (self.size ** 2))
        
        print("Generating Full Board........")
        self.solve(full_board,True, False, False, None)
        print("Full Board Solved")
        print(full_board)

        for row in range(len(full_board)):
            for col in range(len(full_board[0])):
                start_board[row][col] = full_board[row][col]

        #remove from start board
        rounds = 3
        non_empty_cells = self.findNonEmpty(start_board)
        non_empty_cell_cnt = len(non_empty_cells)


        print("Removing Hints from Board.......")
        while rounds > 0 and non_empty_cells:
            #there should be at least 17 clues
            row,col = non_empty_cells.pop()
            removed_square = start_board[row][col]
            non_empty_cell_cnt -= 1
            start_board[row][col] = 0
		    #make a copy of the grid to solve
            board_copy = copy.deepcopy(start_board)
		    #initialize solutions counter to zero
            self.count = 0
            self.solve(board_copy,False, False, True, None)
		    #if there is more than one solution, put the last removed cell back into the grid
            if self.count!=1:
                start_board[row][col]=removed_square
                non_empty_cell_cnt += 1
                rounds -= 1
            print("Non Empty Cells: " + str(non_empty_cell_cnt))
            print("Rounds: " + str(rounds))

        return full_board,start_board

    #solve the board
    #cnt is a check for board uniqueness
    def solve(self,bo,rand,show,cnt, text):
        if cnt and self.count > 1:
            return False

        
        print(str(len(self.findNonEmpty(bo))) + "/" + str(self.size ** 4))

        nums = list(range(1,self.size * self.size + 1))
        if rand: random.shuffle(nums)

        for i in range(0,(self.size ** 4)):
            row = i // (self.size ** 2)
            col = i % (self.size ** 2)
            self.selected = (row,col)

            if bo[row][col] == 0:
                for num in nums:
                    if self.__valid(bo,num,(row,col)):
                        bo[row][col] = num

                        if show: 
                            pygame.event.pump()
                            self.drawBoard(text , True)
                            time.sleep(self.speed)
                           

                        if not self.findEmpty(bo):
                            if cnt:
                                self.count += 1
                                break
                            else:
                                return True
                        elif self.solve(bo,rand,show,cnt, text):
                            return True
                break
        
        bo[row][col] = 0
        if show: 
            self.drawBoard(text , True) 
            time.sleep(self.speed)
        return False
    
    #add pencil marks
    def sketch(self,key):
        (j, i) = self.selected
        if (not self.curr[i][j] and 
            key <= self.size ** 2 and key >= 1):

            if key in self.pencils[i][j]:
                self.pencils[i][j].remove(key)
            
            self.pencils[i][j].insert(0,key)

    #click a cell
    def click(self,pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / (self.size ** 2)
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    #draw helper
    def __draw(self,gameOver):
        lst = self.pencils
        if gameOver:
            lst = self.curr
        
        # Draw Grid Lines
        gap = self.width // (self.size ** 2)
        
        for i in range(len(lst)):
            for j in range(len(lst[0])):
                x = i * gap
                y = j * gap 
                write_text = True

                if gameOver:
                    #green if correct
                    #red if wrong and not zero
                    #nothing if zero
                    x,y = y,x # left to right up and down #remove for top to botoom solve
                
                    if self.curr[i][j] == self.full[i][j]:
                        color = (0,255,0)
                    
                    elif self.curr[i][j] != 0:
                        color = (255,0,0)
                    
                    else:
                        color = None

                    if color:
                        pygame.draw.rect(self.win, color, (x,y, gap ,gap), 0)


                offset = gap // 4
                fnt = pygame.font.SysFont("comicsans", int(gap / 1.5))
                if not lst[i][j]:
                    txt = "0"
                
                elif "[" in str(lst[i][j]):
                    if not self.curr[i][j]:
                        fnt = pygame.font.SysFont("comicsans", gap // self.size)
                        offset = 5

                        txt = ""
                        cnt = 0

                        xoffset = -1 * offset
                        for num in lst[i][j]:
                            if cnt == self.size:
                                self.win.blit(fnt.render(txt, 1, (128,128,128)), (y+offset, x+xoffset))
                                write_text = False
                                xoffset += gap // self.size
                                cnt = 0
                                txt = ""
                            
                            txt += str(num) + " "
                            cnt += 1
                        
                        if txt: 
                            write_text = False
                            self.win.blit(fnt.render(txt, 1, (128,128,128)), (y+offset, x+xoffset))

                    else:
                        txt = str(self.curr[i][j])
  
                else:
                    txt = str(lst[i][j])
                
                if write_text: 
                    fnt = pygame.font.SysFont("comicsans", int(gap / 1.5))
                    text = fnt.render(txt, 1, (128,128,128))
                    if not gameOver:
                        self.win.blit(text, (y+offset, x))
                    else:
                        self.win.blit(text, (x+offset, y))
            
            for i in range(self.size ** 2 +1):
                if i % self.size == 0 and i != 0:
                    thick = 4
                else:
                    thick = 1
                pygame.draw.line(self.win, (0,0,0), (0, i*gap), (gap * self.size ** 2, i*gap), thick)
                pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, gap * self.size ** 2), thick)
               

            if not gameOver:
                (i,j) = self.selected
                x = i * gap
                y = j * gap
                pygame.draw.rect(self.win, (0,0,255), (x,y, gap ,gap), 3)
    
   

    #draw the board
    def drawBoard(self,txt,gameOver):
        self.win.fill((255,255,255))
        fnt = pygame.font.SysFont("comicsans", 40)
        text = fnt.render(txt,1,(0,0,0))
        self.win.blit(text, (self.width - 220, self.height + 10))
        # Draw Strikes
        text = fnt.render("X " * self.strikes, 1, (255, 0, 0))
        self.win.blit(text, (20, self.height + 10))

        # Draw grid and board
        self.__draw(gameOver)
        pygame.display.update()
    
    #select a cell
    def select(self,row,col):
        self.selected = (row,col)

    #clear the selected cell
    def clear(self):
        (j, i) = self.selected
        self.pencils[i][j].clear()

    #add a strike
    #three stikes is gameover
    def addStrike(self):
        self.strikes += 1

    #is the board valid
    def __valid(self,bo,num,pos):
        # Check row
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(bo)):
            if bo[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // self.size
        box_y = pos[0] // self.size

        for i in range(box_y*self.size, box_y*self.size + self.size):
            for j in range(box_x * self.size, box_x*self.size + self.size):
                if bo[i][j] == num and (i,j) != pos:
                    return False

        return True

    #return first empty cell
    def findEmpty(self,bo):
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    return (i, j)  # row, col
              
        return None
    
    #input a custom board
    def inputBoard(self):
        key = None
        run = True
        fnt = pygame.font.SysFont("comicsans", 40)

        for i in range(len(self.curr)):
            for j in range(len(self.curr[0])):
                self.curr[i][j] = 0
                self.pencils[i][j] = []

        while run:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked = self.click(pos)
                    if clicked:
                        self.select(clicked[1], clicked[0])
                        key = None
                    else:
                        self.selected = None

                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        key = 1
                    if event.key == pygame.K_2:
                        key = 2
                    if event.key == pygame.K_3:
                        key = 3
                    if event.key == pygame.K_4:
                        key = 4
                    if event.key == pygame.K_5:
                        key = 5
                    if event.key == pygame.K_6:
                        key = 6
                    if event.key == pygame.K_7:
                        key = 7
                    if event.key == pygame.K_8:
                        key = 8
                    if event.key == pygame.K_9:
                        key = 9
                    if event.key  == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        self.clear()
                        key = None
                    if event.key == pygame.K_r:
                        self.reset()
                        run = False
                        break

                    if event.key == pygame.K_LEFT and self.selected:
                        (j, i) = self.selected
                        self.selected = ((j - 1) % (self.size ** 2), i)

                    if event.key == pygame.K_RIGHT and self.selected:
                        (j, i) = self.selected
                        self.selected = ((j + 1) % (self.size ** 2), i)

                    if event.key == pygame.K_UP and self.selected:
                        (j, i) = self.selected
                        self.selected = (j, (i - 1) % (self.size ** 2))

                    if event.key == pygame.K_DOWN and self.selected:
                        (j, i) = self.selected
                        self.selected = (j, (i + 1) % (self.size ** 2))

                    if event.key == pygame.K_RETURN:
                        (r,c) = self.selected
                        invalid_board = False
                        for i in range(len(self.curr)):
                            for j in range(len(self.curr[0])):
                                if self.curr[i][j] and not self.__valid(self.curr,self.curr[i][j], (i,j)):
                                    self.selected = (r,c)
                                    self.drawBoard(0,False)

                                    #Blit a message
                                    text = fnt.render("Invalid Board", 1, (0, 0, 0))
                                    self.win.blit(text, (20, self.height + 20))
                                    pygame.display.update() #update
                                    time.sleep(0.5)
                                    invalid_board = True
                                    break

                            if invalid_board:
                                break
                        
                        if invalid_board:
                            break
                        
                        #cnt for unique solution
                        self.full = []
                        for i in range(len(self.curr)):
                            row = []
                            for j in range(len(self.curr[0])):
                                row.append(self.curr[i][j])
                            self.full.append(row)

		                #initialize solutions counter to zero
                        self.count = 0
                        self.solve(self.full,False, False, True, None)
		                #if there is more than one solution, put the last removed cell back into the grid
                        if self.count!=1: 
                            self.selected = (r,c)
                            self.drawBoard(0,False)
                            text = fnt.render("Too many solutions", 1, (0, 0, 0))
                            self.win.blit(text, (20, self.height + 20))
                            pygame.display.update() #update 
                            time.sleep(0.5)
                            break

                        #find the full solution and make it the full board
                        self.solve(self.full,False, False, False, None)
                        run = False
                        key = None


            if key and self.selected:
                (j, i) = self.selected
                self.curr[i][j] = key
                self.pencils[i][j] = [key]
                key = None
            
            self.drawBoard(0,False)


        self.selected = (0,0)

    #return all nonempty cells
    def findNonEmpty(self,bo):
        cells = []

        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] != 0:
                    cells.append((i, j))  # row, col

        random.shuffle(cells)      
        return cells






    
