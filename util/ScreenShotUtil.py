import pyscreenshot as ImageGrab
import PhoneScreen as PS
import time

ps = PS.PhoneScreen()
counter = 1
timeout = 1200
while (timeout>0) and not (counter>5):
    try:
        while True:
            time.sleep(0.5)
            timeout-=0.5
    except KeyboardInterrupt:
        print("taking screen shot!")
        im = ImageGrab.grab(bbox=ps.getbbox(), childprocess=False)
        im.save("search_area"+str(counter)+".png","PNG")
        counter+=1