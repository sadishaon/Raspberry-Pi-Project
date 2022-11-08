from flask import Flask, render_template, Response, request, jsonify
from task1_opencv_control.opencv_controller import OpenCVController
from task2_motor_control.motor_controller import MotorController
from task3_sensor_control.sensor_controller import SensorController                      

app = Flask(__name__)

motor_controller  = MotorController()
opencv_controller = OpenCVController()
sensor_controller = SensorController()

# Server method to process the video captured by a camera (Raspberry Pi or Fake camera)
def get_frame():
    while True:
        frame = opencv_controller.process_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')  

# Server view to access the app and display the index template
@app.route('/')
def index():
    return render_template('index.html')           

# Server view to stream the video captured by the available camera
@app.route('/video_feed')
def video_feed():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Server view to determine the current color zone using the opencv_controller
@app.route('/get_color_from_opencv')
def get_color_from_opencv():
    return jsonify(opencv_controller.get_current_color())

# Server view to calculate the current distance using the sensor_controller
@app.route('/get_distance')
def get_distance():
    sensor_controller.track_rod()
    return jsonify({"distance":sensor_controller.get_distance()})

# Server view to determine the current color zone using the sensor_controller
@app.route('/get_color_from_distance')
def get_color_from_distance():
    return jsonify(sensor_controller.get_color_from_distance())

# Server view to start the motor
@app.route('/start_motor')
def start_motor():
    motor_controller.start_motor()  
    return { 'success': True }

# Server view to stop the motor
@app.route('/stop_motor')
def stop_motor():
    motor_controller.motor_stopped() 
    return { 'success': True }

# Server view to get status of the motor (working or not working) with Boolean indicationg
@app.route('/motor_status')
def motor_status():
    while motor_controller.is_working() == True:
        return { 'success': True } 
    else:
        return { 'success': False }
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)