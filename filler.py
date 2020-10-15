"""
Author: Laina Chin
Created: 12 May 2020
"""
import random

WIDTH = 500
HEIGHT = 650
r = 7
c = 8

grid = Rect(50,40,400,350)
boxes = []
# pink, blue, yellow, green, purple, grey
colors = [(245,76,173), (66,158,245), (255,241,48), \
(102,245,66), (158,45,235), (45,41,46)]
blinks = [(245,135,198), (135,194,250), (247,238,106), \
(145,247,119), (181,101,235), (90,84,82)]

"""
create randomly colored boxes to fill the grid, ensuring that no two colors are
adjacent and that players start out with different colors
"""
for j in range(r):
	row = []
	for i in range(c):
		x = 50+50*i
		y = 40+50*j
		color = random.choice(range(len(colors)))

		if j == 0 and i > 0:	# check adjacent boxes for top row
			while row[i-1][1] == color:
				color = random.choice(range(len(colors)))
		if i == 0 and j > 0:	# check adjacent boxes for first column
			while boxes[j-1][i][1] == color:
				color = random.choice(range(len(colors)))
			if j == r-1:	# check with opposite corner
				while boxes[0][c-1][1] == color or boxes[j-1][i][1] == color:
					color = random.choice(range(len(colors)))
		if i > 0 and j > 0:	# check other cases
			while boxes[j-1][i][1] == color or row[i-1][1] == color:
				color = random.choice(range(len(colors)))

		row.append([Rect(x,y,50,50), color])
	boxes.append(row)

#create color box options at the bottom of the screen
color_boxes = []
for k in range(6):
	color_boxes.append((Rect(35+74*k, 430, 60, 60), colors[k]))

score_box1 = Rect(100,550,75,50)
color1 = boxes[r-1][0][1]
player1 = [(r-1,0)]
color_boxes[color1][0].inflate_ip(-20,-20)

score_box2 = Rect(325,550,75,50)
color2 = boxes[0][c-1][1]
player2 = [(0,c-1)]
color_boxes[color2][0].inflate_ip(-20,-20)

p1_turn = True
blink = True
game_over = False


def draw():
	if not game_over:
		screen.fill('white')
		for row in boxes:
			for box in row:
				screen.draw.filled_rect(box[0], colors[box[1]])
		
		for square in color_boxes:
			screen.draw.filled_rect(square[0], square[1])

		screen.draw.filled_rect(score_box1,colors[color1])
		screen.draw.text(str(len(player1)), center=score_box1.center, \
			color='white', fontsize=30, owidth=.2, ocolor='black')

		screen.draw.filled_rect(score_box2,colors[color2])
		screen.draw.text(str(len(player2)), center=score_box2.center, \
			color='white', fontsize=30, owidth=.2, ocolor='black')

		if blink:
			if p1_turn:
				#screen.draw.rect(Rect(90,540,95,70),'black')
				screen.draw.filled_rect(score_box1,blinks[color1])
				screen.draw.text(str(len(player1)), center=score_box1.center, \
			color='white', fontsize=30, owidth=.2, ocolor='black')
				for a,b in player1:
					screen.draw.filled_rect(boxes[a][b][0],blinks[color1])
			else:
				screen.draw.rect(Rect(315,540,95,70),'black')
				for a,b in player2:
					screen.draw.filled_rect(boxes[a][b][0],blinks[color2])

		screen.draw.rect(grid, 'gainsboro')

	else:	# game over
		for row in boxes:
			for box in row:
				screen.draw.filled_rect(box[0],blinks[box[1]])
		screen.draw.text('Game Over', center=grid.center, color='black', fontsize=50)
		
		if len(player1) > len(player2):
			screen.draw.text('Player 1 wins!', center=(grid.center[0],grid.center[1]+50), color='black')
		elif len(player2) > len(player1):
			screen.draw.text('Player 2 wins!', center=(grid.center[0],grid.center[1]+50), color='black')
		else:
			screen.draw.text('It\'s a tie!', center=(grid.center[0],grid.center[1]+50), color='black')

def on_mouse_down(pos):
	global player1, player2, color1, color2, p1_turn, boxes, color_boxes, game_over, blink

	temp = []

	for i in range(len(color_boxes)):
		if color_boxes[i][0].collidepoint(pos) and \
		color_boxes[i][0].width == 60:
			if p1_turn:
				for j,k in player1:
					boxes[j][k][1] = i 	# set color to new choice
					temp += add_boxes(j,k,i)
				color_boxes[color1][0].inflate_ip(20,20)
				color_boxes[i][0].inflate_ip(-20,-20)
				color1 = i
				player1 += temp
				player1 = list(set(player1))
				p1_turn = False
			else:
				for j,k in player2:
					boxes[j][k][1] = i 	# set color to new choice
					temp += add_boxes(j,k,i)
				color_boxes[color2][0].inflate_ip(20,20)
				color_boxes[i][0].inflate_ip(-20,-20)
				color2 = i
				player2 += temp
				player2 = list(set(player2))
				p1_turn = True

	if len(player1) + len(player2) == r*c:
		blink = False
		game_over = True

def add_boxes(row, col, color):
	ls = []

	# check (row-1,col), (row+1,col), (row,col-1), (row,col+1)
	if row > 0:
		if boxes[row-1][col][1] == color:
			ls.append((row-1,col))
	if row < r-1:
		if boxes[row+1][col][1] == color:
			ls.append((row+1,col))
	if col > 0:
		if boxes[row][col-1][1] == color:
			ls.append((row,col-1))
	if col < c-1:
		if boxes[row][col+1][1] == color:
			ls.append((row,col+1))

	return ls

def light_up():
	global blink
	if not game_over:
		if blink:
			blink = False
		else:
			blink = True

clock.schedule_interval(light_up,.5)