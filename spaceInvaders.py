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
bulletspeed = 2
enemy_bullet_speed = 1
refreshAlienImage = 120
refreshBulletImage = 25
number_of_enemies = 30

#enemies can shot at maximum 3 bullet at time.
#this list is update at real time and take note of which bullets are fired and "live"
#into screem
#enemy_fires = [0,0,0]

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
wn.register_shape("enemy_laser.gif")
wn.register_shape("enemy_laser_2.gif")
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
	setattr(enemy, "fired", False)
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

#we have at maximum three bullets for enemy displayed into screen.
# it's needed to define all three bullets differently in order to manage them. 
#enemy fire bullet 1
enemy_bullet1 = turtle.Turtle()
enemy_bullet1.shape("enemy_laser.gif")
enemy_bullet1.penup()
enemy_bullet1.speed(0)
enemy_bullet1.setheading(90)
enemy_bullet1.hideturtle()
#this attribute is used to define if bullet has been already shooted
setattr(enemy_bullet1,"fired",False)

enemy_bullet2 = turtle.Turtle()
enemy_bullet2.shape("enemy_laser.gif")
enemy_bullet2.penup()
enemy_bullet2.speed(0)
enemy_bullet2.setheading(90)
enemy_bullet2.hideturtle()
#this attribute is used to define if bullet has been already shooted
setattr(enemy_bullet2,"fired",False)

enemy_bullet3 = turtle.Turtle()
enemy_bullet3.shape("enemy_laser.gif")
enemy_bullet3.penup()
enemy_bullet3.speed(0)
enemy_bullet3.setheading(90)
enemy_bullet3.hideturtle()
#this attribute is used to define if bullet has been already shooted
setattr(enemy_bullet3,"fired",False)

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

#...
def fire_bullet_enemy(enemy,bullet):
	x = enemy.xcor()
	y = enemy.ycor() - 30
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
counterChangeEnemyBullet = 0
flagMusEneMov = True

while True: 
	wn.update()
	#move the enemy
	
	counterChange += 1   
	counterChangeEnemyBullet += 1

	for enemy in enemies:
		x = enemy.xcor()
		x += enemyspeed
		enemy.setx(x)
		print (getattr(enemy,"fired"))

		#move the enemy back
		if ( (enemy.xcor() > 270 ) or (enemy.xcor() < -270 )  ) :
			#revert the direction and move all enemy down
			enemyspeed *= -1
			for e in enemies:
				y = e.ycor()	
				y -= 40
				e.sety(y)
		
		#enemy shoting process...
		#for each enemie first check if the enemie is killed or not
		if not ( getattr(enemy, "fired") ): 
			#only the enemies upper to player can shoot.
			#this check is acheived checking x coorinate of the player.
			val = player.xcor() - enemy.xcor()
			if ( abs(val) < 50):
			#if (1==1):
				print ("this enemy is upper to player!")
				#checking if there are enemy bullets available: only three at same time can be shooted
				if not ( getattr(enemy_bullet1,"fired") ):
					fire_bullet_enemy (enemy,enemy_bullet1)
					setattr(enemy_bullet1,"fired",True) 
				elif not ( getattr(enemy_bullet2,"fired") ):
					fire_bullet_enemy (enemy,enemy_bullet2)
					setattr(enemy_bullet2,"fired",True) 
				elif not ( getattr(enemy_bullet3,"fired") ): 
					fire_bullet_enemy (enemy,enemy_bullet3)
					setattr(enemy_bullet3,"fired",True) 

		#Check for a collision between the bullet and the enemy
		if isCollision(bullet, enemy):
			setattr(enemy, "fired", True)
			os.system("afplay enemy_explosion.wav&")
			enemy.shape("explosion.gif")
			#reset the bullet
			bullet.hideturtle()
			bulletstate = "ready"
			bullet.setposition(0, -400)
			#reset the enemy
			#time.sleep(0.2)
			#x = random.randint (-200, 200)
			#y = random.randint (100, 250)
			#set alien fired out of screen
			enemy.setposition(0,10000)
			enemy.setposition(enemy.xcor(), enemy.ycor())
			#update the score
			score += 10
			scorestring = "Score: %s" %score
			score_pen.clear()
		  	score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal") )

		#check collision between player and enemy bullet
		if isCollision(enemy_bullet1, player):
			player.hideturtle()
			enemy.hideturtle()
			print ("Game Over")
			break

		if isCollision(enemy_bullet2, player):
			player.hideturtle()
			enemy.hideturtle()
			print ("Game Over")
			break

		if isCollision(enemy_bullet3, player):
			player.hideturtle()
			enemy.hideturtle()
			print ("Game Over")
			break

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

	#refresh the image for animatio of enemy bullet
	if ( counterChangeEnemyBullet == refreshBulletImage ):
		counterChangeEnemyBullet = 0
		if ( enemy_bullet1.shape() == "enemy_laser.gif" ):
			enemy_bullet1.shape("enemy_laser_2.gif")
			enemy_bullet2.shape("enemy_laser_2.gif")
			enemy_bullet3.shape("enemy_laser_2.gif")
		else:
			enemy_bullet1.shape("enemy_laser.gif")
			enemy_bullet2.shape("enemy_laser.gif")
			enemy_bullet3.shape("enemy_laser.gif")

	#move the bullet       
	if bulletstate == "fire":
		y = bullet.ycor()
		y += bulletspeed
		bullet.sety(y)

	#move enemy bullets
	if getattr (enemy_bullet1,"fired"):
		y = enemy_bullet1.ycor()
		y -= enemy_bullet_speed
		enemy_bullet1.sety(y)
	
	if getattr (enemy_bullet2,"fired"):
		y = enemy_bullet2.ycor()
		y -= enemy_bullet_speed
		enemy_bullet2.sety(y)

	if getattr (enemy_bullet3,"fired"):
		y = enemy_bullet3.ycor()
		y -= enemy_bullet_speed
		enemy_bullet3.sety(y)

	#Check to see if the bullet has gone to the top
	if bullet.ycor() > 275:
		bullet.hideturtle()
		bulletstate = "ready"

	#Check to see if the enemy bullet has gone to the groud
	if enemy_bullet1.ycor() == -250:
		enemy_bullet1.hideturtle()
		setattr(enemy_bullet1,"fired",False)
	if enemy_bullet2.ycor() == -250:
		enemy_bullet2.hideturtle()
		setattr(enemy_bullet2,"fired",False)
	if enemy_bullet3.ycor() == -250:
		enemy_bullet3.hideturtle()
		setattr(enemy_bullet3,"fired",False)