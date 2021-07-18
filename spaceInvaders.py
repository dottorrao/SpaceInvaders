#Space Invaders - Part 2
#Move the Player
#Python 2.7 on Mac
import turtle
import os
import time
import math
from random import randint

#==================================================================
# INITIALIZATION
#==================================================================
#speed of the player
playerspeed = 20
#speed of the enemies
enemyspeed = 0.015
#speed of player's bullet 
bulletspeed = 1.5
#speed of enemies bullet
enemy_bullet_speed = 0.3
#this variable indicates the cicles after that alien image is refreshed. For the animation.
refreshAlienImage = 120
#this variable indicates the cicles after that bullet enemies image is refreshed. For the animation.
refreshBulletImage = 25
#how many enememies are present in the "alien team".
number_of_enemies = 55
#this variable is increased every time that an alien is killed.
enemies_killed = 0
#set score to 0
score = 0
#refresh mistery ship sound: how many main loop cicle play the soud for mistery ship
mistery_ship_sound = 45
#manage mistery ship explosion in order explosion will remain at screen for some while
mistery_ship_explosion = 500
#speed of mistery ship
mistery_ship_speed = 0.3

#enemies can shot at maximum 3 bullet at time.
#this list is update at real time and take note of which bullets are fired and "live"
#into screem
#enemy_fires = [0,0,0]

#Define bullet state
#ready - ready to fire
#fire - bulllet is firing
bulletstate = "ready"

#==================================================================
# SETTING UP OF THE SCREEN
#==================================================================
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
#registration of images
wn.register_shape("crab1.gif")
wn.register_shape("crab2.gif")
wn.register_shape("binky1.gif")
wn.register_shape("binky2.gif")
wn.register_shape("skoob1.gif")
wn.register_shape("skoob2.gif")
wn.register_shape("cannon.gif")
wn.register_shape("bullet.gif")
wn.register_shape("explosion.gif")
wn.register_shape("enemy_laser.gif")
wn.register_shape("enemy_laser_2.gif")
wn.register_shape("mistery_ship.gif")
wn.register_shape("explosion_mistery_ship.gif")
wn.register_shape("bullet_explosion.gif")
wn.register_shape("enemy_bullet_explosion.gif")
wn.tracer(0)

#Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-350,-350)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
	border_pen.fd(700)
	border_pen.lt(90)
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pencolor("green")
border_pen.fd(600)
border_pen.hideturtle()	

#draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-200,300) 
score_pen.write("Score<1>", False, align="left", font=("Space Invaders", 20, "normal") )
score_pen.setposition(-180,270)
score_pen.write(score, False, align="left", font=("Space Invaders", 20, "normal") )
score_pen.setposition(-50,300)
score_pen.write("HI-SCORE", False, align="left", font=("Space Invaders", 20, "normal") )
score_pen.setposition(110,300)
score_pen.write("Score<2>", False, align="left", font=("Space Invaders", 20, "normal") )
score_pen.hideturtle()

'''
#draw the screen message (press start to play... game over...)
diplay_message_pen = turtle.Turtle()
diplay_message_pen.speed(0)
diplay_message_pen.color("white")
diplay_message_pen.penup()
diplay_message_pen.setposition(0,0)
diplay_message_pen.write("PRESS A BOTTON TO START", False, align="left", font=("Arial", 14, "normal") )
'''

#==================================================================
# OBJECTS 
#==================================================================
#player
player = turtle.Turtle()
player.shape("cannon.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
player.shapesize(0.1,0.1)

#ENEMIES TEAM
#chose a number of enemies create an empty list of enemies
enemies = []
#Add enemies in the list
for i in range (number_of_enemies):
	enemies.append(turtle.Turtle())

#where the enemy team starts to be displayed
enemy_start_x = -225
enemy_start_y = 180
#this variable is used to dispose the enemy in matrix
enemy_number_for_matrix = 0
#this variable is used to change the shape of the enemy
enemy_number_for_shape = 0

for enemy in enemies:
	enemy_number_for_shape += 1
	#setting attribute fired to understand if an alien has been killed or not
	setattr(enemy, "fired", False)
	#disposition on row of 11 with related pictures
	if ( enemy_number_for_shape <= 11 ):
		enemy.shape("binky1.gif")
	elif ( enemy_number_for_shape >= 12 and  enemy_number_for_shape <= 33 ) :
		enemy.shape("crab1.gif")
	else:
		enemy.shape("skoob1.gif")
	
	#creation of the alien "matrix"
	enemy.penup()
	enemy.speed(0)
	x = enemy_start_x + (40 * enemy_number_for_matrix)
	y = enemy_start_y
	enemy.setposition(x, y)
	#update enemy number
	enemy_number_for_matrix += 1
	if enemy_number_for_matrix == 11:
		enemy_number_for_matrix = 0
		enemy_start_y -= 40

#player's bullet
bullet = turtle.Turtle()
#bullet.color("yellow")
bullet.shape("bullet.gif")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
#bullet.shapesize(0.5,0.5)
bullet.hideturtle()
setattr (bullet,"top",False)

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
setattr(enemy_bullet1,"ground",False)

#enemy fire bullet 2
enemy_bullet2 = turtle.Turtle()
enemy_bullet2.shape("enemy_laser.gif")
enemy_bullet2.penup()
enemy_bullet2.speed(0)
enemy_bullet2.setheading(90)
enemy_bullet2.hideturtle()
#this attribute is used to define if bullet has been already shooted
setattr(enemy_bullet2,"fired",False)
setattr(enemy_bullet2,"ground",False)

#enemy fire bullet 3
enemy_bullet3 = turtle.Turtle()
enemy_bullet3.shape("enemy_laser.gif")
enemy_bullet3.penup()
enemy_bullet3.speed(0)
enemy_bullet3.setheading(90)
enemy_bullet3.hideturtle()
#this attribute is used to define if bullet has been already shooted
setattr(enemy_bullet3,"fired",False)
setattr(enemy_bullet3,"ground",False)

#mistery_ship
mistery_ship = turtle.Turtle()
mistery_ship.penup()
mistery_ship.setposition(330,240)
mistery_ship.shape("mistery_ship.gif")
mistery_ship.speed(0)
mistery_ship.setheading(90)
#mistery_ship.hideturtle()
#this attribute is used to define if bullet has been already shooted
setattr(mistery_ship,"fired",False)
setattr(mistery_ship,"displayed",False)
mistery_ship.hideturtle()

#==================================================================
# FUNCTIONS
#==================================================================
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

#fire (PLAYER)
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
		setattr (bullet,"top",False) 

#fire (aliens)
def fire_bullet_enemy(enemy,bullet):
	x = enemy.xcor()
	y = enemy.ycor() - 30
	bullet.setposition(x,y)
	bullet.showturtle()
	setattr(bullet,"ground",False)

#function to detect collisions between player bullets and enemies
def isCollision(t1,t2):
	distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
	if distance < 15:
		return True
	else:
		return False

#reate keyboard bindings to functions
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

#==================================================================
# MAIN LOOP GAME!!
#==================================================================
counterChange = 0
counterChangeEnemyBullet = 0
counterChangeMisteryShipSound = 0
couterExplosionMisteryShip = 0
flagMusEneMov = True

while True: 
	wn.update()
	#move the enemy
	
	#these vaiables are used in combination with...
	#to manage the animation (shape changing)
	counterChange += 1   
	counterChangeEnemyBullet += 1

	#==================================================================
	# MANAGING OF THE ENEMIES: movement, collision, animation, firing
	#==================================================================
	for enemy in enemies:
		x = enemy.xcor()
		x += enemyspeed
		#an enemy must be moved only if it's not fired, othervise it cause a problem into global enemy moviment.
		#an enemy fired is moved on position (0,10000) but without this if it will continue to move causing a wrong
		#descending of whole alien "team"
		if not(getattr(enemy,"fired")):
			enemy.setx(x)
			#print (getattr(enemy,"fired"))

		#print ( str(enemy.xcor()) + ' - ' + str ( enemy.ycor() ) ) 

		#move the enemy back
		if ( (enemy.xcor() > 270 ) or (enemy.xcor() < -270 )  ) :
			#print ("revert!")
			#print ( enemy.xcor() )
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
				#print ("this enemy is upper to player!")
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
			enemies_killed += 1
			setattr(enemy, "fired", True)
			os.system("afplay enemy_explosion.wav&")
			enemy.shape("explosion.gif")
			wn.update()
			time.sleep(0.01)
			#reset the bullet
			bullet.hideturtle()
			bulletstate = "ready"
			bullet.setposition(0, -400)
			#reset the enemy
			#time.sleep(0.2)
			#x = random.randint (-200, 200)
			#y = random.randint (100, 250)
			#set alien fired out of screen
			enemy.setposition(0,100000)
			enemy.setposition(enemy.xcor(), enemy.ycor())
			#update the score
			score += 10
			score_pen.clear()
			score_pen.setposition(-200,300) 
			score_pen.write("Score<1>", False, align="left", font=("Space Invaders", 20, "normal") )
			score_pen.setposition(-180,270)
			score_pen.write(score, False, align="left", font=("Space Invaders", 20, "normal") )
			score_pen.setposition(-50,300)
			score_pen.write("HI-SCORE", False, align="left", font=("Space Invaders", 20, "normal") )
			score_pen.setposition(110,300)
			score_pen.write("Score<2>", False, align="left", font=("Space Invaders", 20, "normal") )
			score_pen.hideturtle()
			#checking for enemies speed increase.
			#if number of enemnies killed is equal to a certain target, the enemy speed is increased.
			if ( enemies_killed ) == ( number_of_enemies // 5 ):
				enemyspeed *= 1.3
			if ( enemies_killed ) == ( number_of_enemies // 4 ):
				enemyspeed *= 1.4
			if ( enemies_killed ) == ( number_of_enemies // 3 ):
				enemyspeed *= 1.5
			if ( enemies_killed ) == ( number_of_enemies // 2 ):
				enemyspeed *= 1.6
			if ( enemies_killed ) == ( number_of_enemies - 3 ):
				enemyspeed *= 1.7
			if ( enemies_killed ) == ( number_of_enemies - 2 ):
				enemyspeed *= 2
			if ( enemies_killed ) == ( number_of_enemies - 1 ):
				enemyspeed *= 2
		
		#check collision between player and enemy bullet
		#if isCollision(enemy_bullet1, player):
		if 1==0:
			player.hideturtle()
			enemy.hideturtle()
			print ("Game Over")
			break

		#if isCollision(enemy_bullet2, player):
		if 1==0:	
			player.hideturtle()
			enemy.hideturtle()
			print ("Game Over")
			break

		#if isCollision(enemy_bullet3, player):
		if 1==0:
			player.hideturtle()
			enemy.hideturtle()
			print ("Game Over")
			break

		if isCollision(player, enemy):
			player.hideturtle()
			enemy.hideturtle()
			print ("Game Over")
			break
	
	#check collision between player bullet and mistery ship
	if isCollision(bullet, mistery_ship) and not ( getattr(mistery_ship,"fired") ):
		mistery_ship.shape("explosion_mistery_ship.gif")
		bullet.setposition(0,10000)
		os.system("afplay mistery_ship2.wav&")
		setattr(mistery_ship,"fired",True)
		score_pen.clear()
		score += 100
		score_pen.setposition(-200,300) 
		score_pen.write("Score<1>", False, align="left", font=("Space Invaders", 20, "normal") )
		score_pen.setposition(-180,270)
		score_pen.write(score, False, align="left", font=("Space Invaders", 20, "normal") )
		score_pen.setposition(-50,300)
		score_pen.write("HI-SCORE", False, align="left", font=("Space Invaders", 20, "normal") )
		score_pen.setposition(110,300)
		score_pen.write("Score<2>", False, align="left", font=("Space Invaders", 20, "normal") )
		wn.update()

	#to manage mistery ship explosion	
	if 	getattr(mistery_ship,"fired"):
		couterExplosionMisteryShip +=1
		if ( couterExplosionMisteryShip == mistery_ship_explosion ):
			couterExplosionMisteryShip = 0
			setattr(mistery_ship,"displayed",False)
			setattr(mistery_ship,"fired",False)
			mistery_ship.hideturtle()
			mistery_ship.setposition(330,240)	
			mistery_ship.shape("mistery_ship.gif")
			wn.update()	
			counterChangeMisteryShipSound = 0


	#section to change the picture of animations
	if ( counterChange == refreshAlienImage ):	
		counterChange = 0
		
		if flagMusEneMov:
			os.system("afplay enemy_move1.wav&")
			flagMusEneMov = False
		else:
			os.system("afplay enemy_move2.wav&")
			flagMusEneMov = True
		
		for enemy in enemies:
			if ( enemy.shape() == "crab1.gif" ):
				enemy.shape("crab2.gif")
			elif ( enemy.shape() == "crab2.gif" ):
				enemy.shape("crab1.gif")
		
		for enemy in enemies:
			if ( enemy.shape() == "binky1.gif" ):
				enemy.shape("binky2.gif")
			elif ( enemy.shape() == "binky2.gif" ):
				enemy.shape("binky1.gif")

		for enemy in enemies:
			if ( enemy.shape() == "skoob1.gif" ):
				enemy.shape("skoob2.gif")
			elif ( enemy.shape() == "skoob2.gif" ):
				enemy.shape("skoob1.gif")


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

#==================================================================
# MANAGING OF THE BULLETS: for enemy and player
#==================================================================

	#move the bullet       
	if bulletstate == "fire":
		y = bullet.ycor()
		y += bulletspeed
		bullet.sety(y)
	
	#Check to see if the bullet has gone to the top
	if bullet.ycor() > 310:
		if ( not getattr (bullet,"top") ):
			setattr (bullet,"top",True) 
			bullet.shape("bullet_explosion.gif") 
			wn.update()
			time.sleep(0.02)
			bullet.shape("bullet.gif")
		bullet.hideturtle()
		bulletstate = "ready"
		bullet.setposition(0,10000)

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

	#Check to see if the enemy bullet has gone to the groud
	#If the enemy bullet touch the groud, explosion image is displayd.
	#Then the bullet is hided, original shape is re-set, 
	#bullet1
	if enemy_bullet1.ycor() < -290:
		if (not getattr(enemy_bullet1,"ground")):
			print(1)
			setattr(enemy_bullet1,"ground",True)
			enemy_bullet1.shape("enemy_bullet_explosion.gif")
			wn.update()
			time.sleep(0.01)
			enemy_bullet1.shape("enemy_laser.gif")
			#every time that an enemy bullet hit the grund, a hole is generated!
			border_pen.penup()
			border_pen.setposition(enemy_bullet1.xcor(),-300)
			border_pen.pendown()
			border_pen.pencolor("black")
			border_pen.dot()
			border_pen.penup()
		
		enemy_bullet1.hideturtle()
		setattr(enemy_bullet1,"fired",False)

	#bullet2
	if enemy_bullet2.ycor() < -290:
		if (not getattr(enemy_bullet2,"ground")):
			print(2)
			setattr(enemy_bullet2,"ground",True)
			enemy_bullet2.shape("enemy_bullet_explosion.gif")
			wn.update()
			time.sleep(0.01)
			enemy_bullet2.shape("enemy_laser.gif")
			#every time that an enemy bullet hit the grund, a hole is generated!
			border_pen.penup()
			border_pen.setposition(enemy_bullet2.xcor(),-300)
			border_pen.pendown()
			border_pen.pencolor("black")
			border_pen.dot()
			border_pen.penup()
		
		enemy_bullet2.hideturtle()
		setattr(enemy_bullet2,"fired",False)

	#bullet3
	if enemy_bullet3.ycor() < -290:
		if (not getattr(enemy_bullet3,"ground")):
			print(3)
			setattr(enemy_bullet3,"ground",True)
			enemy_bullet3.shape("enemy_bullet_explosion.gif")
			wn.update()
			time.sleep(0.01)
			enemy_bullet3.shape("enemy_laser.gif")
			#every time that an enemy bullet hit the grund, a hole is generated!
			border_pen.penup()
			border_pen.setposition(enemy_bullet3.xcor(),-300)
			border_pen.pendown()
			border_pen.pencolor("black")
			border_pen.dot()
			border_pen.penup()
			
		enemy_bullet3.hideturtle()
		setattr(enemy_bullet3,"fired",False)

#==================================================================
# MANAGING OF MISTERY ship
#==================================================================

	#check if mistery ship must start or not: only id mistery ship is not
	#already displayed and if the random number is ok!
	if not ( getattr(mistery_ship,"displayed") ) and not ( getattr(mistery_ship,"fired") ):
		random = randint(0, 100000) 
		#print ( random )
		if ( random > 99950):
			mistery_ship.showturtle()
			setattr(mistery_ship,"displayed",True)
	
	if ( getattr(mistery_ship,"displayed") ) and not ( getattr (mistery_ship,"fired") ) :
		counterChangeMisteryShipSound += 1
		x = mistery_ship.xcor() - mistery_ship_speed
		mistery_ship.setx(x)
		#print (counterChangeMisteryShipSound)
		if ( counterChangeMisteryShipSound == mistery_ship_sound ):
			counterChangeMisteryShipSound = 0
			os.system("afplay mistery_ship.wav&")
	
	if ( mistery_ship.xcor() < -330 ):
		setattr(mistery_ship,"displayed",False)
		setattr(mistery_ship,"fired",False)
		mistery_ship.hideturtle()
		mistery_ship.setposition(330,240)
		counterChangeMisteryShipSound = 0