import requests
import serial

url = "http://162.248.166.73:18000"
def make_request(sensor_value):
    """
    Pushes to the HTTP handler of the game server.
    The game server then pushes this HTTP request
    as a websocket push over the appropriate socket!.
    """
    payload= {'movement':sensor_value, 'game_id': instance_id}

    r = requests.post(url, headers=payload)
    return r.status_code
    
def setup_serial(baudrate=9600):
    arduino = serial.Serial()
    arduino.port = 2 # in reality this means COM3
    arduino.baudrate = 9600
    print arduino
    return arduino
    arduino.open()
    
def initialize_game():
    instance_id = 0
    while(instance_id == 0):
        print "Please enter your game id: "
        instance_id = raw_input()
        payload = {'query_id':instance_id}
        result = requests.post(url, headers=payload).status_code
        if result == 200:
            print "Game ID is correct!"
            return instance_id
        elif result == 400:
            print "Wrong Game ID!"
            instance_id = 0
    
def game_loop():
    while(1):
        raw_serial_result = arduino.readline()
        try:
            dial_value = int(raw_serial_result)
            
            result = make_request(dial_value)
            print "Pushing request, value={}".format(dial_value)
            
        except:
            print "Improperly formatted Serial data."
            print "Check Arduino code!"
            continue

arduino = setup_serial()
instance_id = initialize_game()
arduino.open()
game_loop()


        
    

