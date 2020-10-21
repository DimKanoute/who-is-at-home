# who-is-at-home

This application created in order to help people living in the same house know when someone is in or out.

Stop hanging your keys around :)

## Requirements

For development:

    ESP-WROOM-32 
    Miropython

Rest:

    Led's
    Breadboard
    Cables
    
##Authors and acknowledgment

For pinging [u Ping](https://gist.github.com/shawwwn/91cc8979e33e82af6d99ec34c38195fb) library has been used.
 

##Instalation

   ###Step No. 1 - Erase/ Burning The Firware
  
  At first erase the firmware that your board has and burn the micropython firmware.
 
  After that, you will be able to use micropython to develop micropython code on your board.
 
  For this one I used a stable firmware build, and more specific the version: <b>esp32-idf3-20200902-v1.13.bin</b>.
 
  For erase and burning process you can use [esptool.py](https://github.com/espressif/esptool)
  
  ###Step No. 2 - Set up the circuit
  
  Now is the time to set up your circuit and pick up the GPIO that you will use to connect your LED's.
  
  Every person in the house has his/ her own GPIO which later we pass to the script.
  
  Be careful a LED needs a GPIO as well as the ground pin connected. Set up your circuit carefully so all LED's can fit
  
  ###Step No. 3 - Get the script ready
  
  Go on and pass the variables needed in the script.
  
  These are your Wi-Fi credentials as well as the information about each user.
  
  For the user's configuration you need to visit your router homepage and get the static ip for each user device (preferably mobile phone as is the most common use in a house and the Wi-Fi is always open)
  
  Set up the config file with this info according with LED's info for each user. Example you can find at the beginning of main.py file.
  
  ###Step No. 4 - Run the script into your board
  
   Pick any micropython IDE or use CMD to pass the script into the board.
   
   Boot the board, connect and disconnect each device to make sure everything works properly.
   
   Here is strongly recommended to use a termina as [Realterm](https://sourceforge.net/projects/realterm/) to get feedback from the board for any problems which might occurred.
   
   
   
   
  
  
