#Space Invaders - Part 2
#Move the Player
#Python 2.7 on Mac
import turtle
import os
import time
import math
import random


#============= Inizialization
#speed of the player
playerspeed = 10
enemyspeed = 0.05
bulletspeed = 5
refreshAlienImage = 120
#Define bullet state
#ready - ready to fire
#fire - bulllet is firing
bulletstate = "ready"

#============= Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.register_shape("crab1.gif")
wn.register_shape("crab2.gif")
wn.register_shape("cannon.gif")
wn.register_shape("bullet.gif")
wn.register_shape("explosion.gif")
wn.tracer(0)

#============= Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
	border_pen.fd(600)
	border_pen.lt(90)
border_pen.hideturtle()	

#set score to 0
score = 0

#draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,280)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal") )
score_pen.hideturtle()

#============= OBJECTS
#player
player = turtle.Turtle()
player.shape("cannon.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)


#chose a number of enemies
number_of_enemies = 30
#create an empty list of enemies
enemies = []

#Add enemies in the list
for i in range (number_of_enemies):
	enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0

for enemy in enemies:
	#enemy
	#enemy.color("red")
	enemy.shape("crab1.gif")
	enemy.penup()
	enemy.speed(0)
	x = enemy_start_x + (50 * enemy_number)
	y = enemy_start_y
	enemy.setposition(x, y)
	#update enemy number
	enemy_number += 1
	if enemy_number == 10:
		enemy_number = 0
		enemy_start_y -= 50


#player's bullet
bullet = turtle.Turtle()
#bullet.color("yellow")
bullet.shape("bullet.gif")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
#bullet.shapesize(0.5,0.5)
bullet.hideturtle()

#============= FUNCTION
#Move the player left and right
def move_left():
	x = player.xcor()
	x -= playerspeed
	if x < -270:
		x = - 270
	player.setx(x)
	
def move_right():
	x = player.xcor()
	x += playerspeed
	if x > 270:
		x = 270
	player.setx(x)    

#fire
def fire_bullet():
	#Declare bulletstate as a global 
	global bulletstate
	#move the bullet just above the playe
	if bulletstate == "ready":
		#& is to avoid to pause the program
		os.system("afplay bullet.wav&")
		bulletstate = "fire"
		x = player.xcor()
		y = player.ycor() + 30
		bullet.setposition(x,y)
		bullet.showturtle()

#function to detect collisions between player bullets and enemies
def isCollision(t1,t2):
	distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
	if distance < 15:
		return True
	else:
		return False

#============= Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

#============= MAIN GAME LOOP
counterChange = 0
flagMusEneMov = True
while True: 
	wn.update()
	#move the enemy
	
	counterChange += 1   
	for enemy in enemies:
		x = enemy.xcor()
		x += enemyspeed
		enemy.setx(x)

		#move the enemy back
		if ( (enemy.xcor() > 270 ) or (enemy.xcor() < -270 )  ) :
			#revert the direction and move all enemy down
			enemyspeed *= -1
			for e in enemies:
				y = e.ycor()	
				y -= 40
				e.sety(y)

		#Check for a collision between the bullet and the enemy
		if isCollision(bullet, enemy):
			os.system("afplay enemy_explosion.wav&")
			#reset the bullet
			bullet.hideturtle()
			bulletstate = "ready"
			bullet.setposition(0, -400)
			#reset the enemy
			enemy.shape("explosion.gif")
			time.sleep(0.2)
			#x = random.randint (-200, 200)
			#y = random.randint (100, 250)
			#ser alien fired out of screen
			enemy.setposition(0, 10000)
			#update the score
			score += 10
			scorestring = "Score: %s" %score
			score_pen.clear()
		  	score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal") )
		
		if isCollision(player, enemy):
			player.hideturtle()
			enemy.hideturtle()
			print ("Game Over")
			break
	
	if ( counterChange == refreshAlienImage ):	
		if flagMusEneMov:
			os.system("afplay enemy_move1.wav&")
			flagMusEneMov = False
		else:
			os.system("afplay enemy_move2.wav&")
			flagMusEneMov = True
		counterChange = 0
		for enemy in enemies:
			if ( enemy.shape() == "crab1.gif" ):
				enemy.shape("crab2.gif")
			else:
				enemy.shape("crab1.gif")
	 
	#move the bullet       
	if bulletstate == "fire":
		y = bullet.ycor()
		y += bulletspeed
		bullet.sety(y)

	#Check to see if the bullet has gone to the top
	if bullet.ycor() > 275:
		bullet.hideturtle()
		bulletstate = "ready"
