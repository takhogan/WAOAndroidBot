Note: this project is incomplete but the bot-maker functionality is complete and is inside AssistantController.py, and there is a short working script in the file MapNavigato.py to demonstrate what a potential script will look like
BotController.py, TextMatcher.py, ScreenShotUtil.py, and MapManager.py are all incomplete
To configure the project for your system requires editing the SystemVars.py file where there will be screenx,screeny variables (the starting x & y location of your phone screen) and a screenwidth and screenheight variable
I reccomend using MEmu as the android simulator for this project
running this project will require installing:
opencv & associated libraries
pyscreenshot
PIL
pyautogui
& possibly more

Short explanation:
this program is based around "context" objects which represent anything accesible with a button
The different contexts are linked together in a map structure so even if the bot goes off track, it can return to it's intended destination
the main methods are:
get_context(name)
	gets a child context from the parent context
click()
	accesses the button associated with the context
detect()
	returns true if the context is present
wait_for_load()
	sleeps until context is loaded
return_context()
	tries to return the bot to the intended context