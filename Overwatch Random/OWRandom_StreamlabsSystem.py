import clr
import sys
import json
import os
import ctypes
import codecs
import random
from random import shuffle
# coding=utf-8
ScriptName = "Overwatch Random"
Website = "https://www.domekologe.eu"
Description = "Pick Random Heroes for Overwatch"
Creator = "Domekologe"
Version = "1.0.0"

configFile = "config.json"
settings = {}

owheroes = ["Ana","Ashe","Bastion","Brigitte","D.Va","Doomfist","Genji","Hanzo","Junkrat","Lúcio","McCree","Mei","Mercy","Moira","Orisa","Pharah","Reaper","Reinhardt","Roadhog","Soldier: 76","Sombra","Symmetra","Torbjörn","Tracer","Widowmaker","Winston","Wrecking Ball","Zarya","Zenyatta"] 

def ScriptToggled(state):
	return

def Init():
	global settings

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": true,
			"command": "!owrandom",
			"permission": "Everyone",
			"useCooldown": true,
			"useCooldownMessages": true,
			"cooldown": 120,
			"onCooldown": "$user, $command is on Cooldown $cd seconds!",
			"userCooldown": 120,
			"onUserCooldown": "$user, please wait $cd seconds before you can start a next random pick!",
			"response": "$user = $hero",
			"TooMuch": "Too Many Names. Please stay below 7!",
			"FirstMessage": "The following users must pick the following hero!"
		}

def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and data.GetParamCount() < 7 and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""
		userId = data.User			
		username = data.UserName
		i = 2
		pickedHeroes = []
		users = data.GetParamCount()
		
		if(data.GetParamCount() == 1):
			userparam = username
		else:
			userparam = 1
			
		if settings["useCooldown"] and (Parent.IsOnCooldown(ScriptName, settings["command"]) or Parent.IsOnUserCooldown(ScriptName, settings["command"], userId)):
			if settings["useCooldownMessages"]:
				if Parent.GetCooldownDuration(ScriptName, settings["command"]) > Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId):
					cdi = Parent.GetCooldownDuration(ScriptName, settings["command"])
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
					outputMessage = settings["onCooldown"]
				else:
					cdi = Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId)
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
					outputMessage = settings["onUserCooldown"]
				outputMessage = outputMessage.replace("$cd", cd)
				outputMessage = outputMessage.replace("$command", settings["command"])
				outputMessage = outputMessage.replace("$user", username)
				Parent.SendStreamMessage(outputMessage)
			else:
				outputMessage = ""
		else:
			Parent.SendStreamMessage(settings["FirstMessage"])
			
			while True:
				shuffle(owheroes)
				hero = random.choice(owheroes)
				while True:
					if(hero in pickedHeroes):
						hero = random.choice(owheroes)
					if(hero not in pickedHeroes):
						break
				pickedHeroes.append(hero)
				outputMessage = settings["response"].replace("$hero",hero)
				
				if(data.GetParamCount() == 1):
					userparam = username
					outputMessage = outputMessage.replace("$user",userparam)
				else:
					outputMessage = outputMessage.replace("$user",data.GetParam(userparam))
					userparam = userparam+1
					
				i = i + 1
				Parent.SendStreamMessage(outputMessage)
				if(i > users):
					break
			
			if settings["useCooldown"]:
				Parent.AddUserCooldown(ScriptName, settings["command"], userId, settings["userCooldown"])
				Parent.AddCooldown(ScriptName, settings["command"], settings["cooldown"])
			
			
		
		
	elif(data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and data.GetParamCount() > 7):	
		Parent.SendStreamMessage(settings["TooMuch"])
	return

def ReloadSettings(jsonData):
	Init()
	return

def Tick():
	return
