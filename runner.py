import pygame
from sudoku import Sudoku
import time

SIZE = 3
WIDTH = 540
HEIGHT = 540
SPEED = 0.015


def main():
    sudoku = Sudoku(SIZE,WIDTH, HEIGHT,SPEED)
    key = None
    run = True
    start = time.time()
    gameOver = False

    while run:
        if not gameOver: play_time = round(time.time() - start)

        for event in pygame.event.get():
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
                
                if event.key == pygame.K_i:
                    sudoku.select(0,0)
                    sudoku.inputBoard()
                    start = time.time()
                    play_time = round(time.time() - start)
                    gameOver = False
                
                if event.key == pygame.K_LEFT and sudoku.selected:
                    (j, i) = sudoku.selected
                    sudoku.selected = ((j - 1) % (sudoku.cols ** 2), i)


                if event.key == pygame.K_RIGHT and sudoku.selected:
                    (j, i) = sudoku.selected
                    sudoku.selected = ((j + 1) % (sudoku.cols ** 2), i)

                if event.key == pygame.K_UP and sudoku.selected:
                    (j, i) = sudoku.selected
                    sudoku.selected = (j, (i - 1) % (sudoku.rows ** 2))

                if event.key == pygame.K_DOWN and sudoku.selected:
                    (j, i) = sudoku.selected
                    sudoku.selected = (j, (i + 1) % (sudoku.rows ** 2))

                if event.key == pygame.K_r:
                    sudoku.reset()
                    start = time.time()
                    play_time = round(time.time() - start)
                    gameOver = False
                    break
                if event.key  == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    sudoku.clear()
                    key = None
                if event.key == pygame.K_SPACE and not gameOver:
                    gameOver = True
                    sudoku.solve(sudoku.curr,False,True,False, play_time)
                    sudoku.selected = None
                    break
                if event.key == pygame.K_RETURN:
                    (j, i) = sudoku.selected
                    if sudoku.curr[i][j] == 0 and sudoku.pencils[i][j]:
                        if sudoku.pencils[i][j][0] != sudoku.full[i][j]:
                            sudoku.addStrike()
                            sudoku.clear()
                        else:
                            sudoku.curr[i][j] = sudoku.pencils[i][j][0]
                            sudoku.pencils[i][j] = sudoku.pencils[i][j][0]

                        key = None
                        if sudoku.strikes == 3:
                            gameOver = True
                            sudoku.solve(sudoku.curr,False,True,False, play_time)
                            sudoku.selected = None
                            break

                        if not sudoku.findEmpty(sudoku.curr):
                            gameOver = True
                            sudoku.selected = None
                            break
                     
            if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                pos = pygame.mouse.get_pos()
                clicked = sudoku.click(pos)
                if clicked:
                    sudoku.select(clicked[1], clicked[0])
                    key = None
                else:
                    sudoku.selected = None

        if sudoku.selected and key != None and not gameOver:
            sudoku.sketch(key)
            key = None

        sudoku.drawBoard(play_time, gameOver)

main()
pygame.quit()




