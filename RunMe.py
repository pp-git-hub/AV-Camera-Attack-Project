from Detection.Signs.SignDetectionApi import detect_Signs
import paho.mqtt.client as mqtt
import config
import cv2
import time
import requests
import numpy as np

MQTT_TOPIC = "car/speed"
MQTT_BROKER = "192.168.137.20"

def publish_speed(speed):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, 1883, 60)
    client.publish(MQTT_TOPIC, str(speed))
    client.disconnect()

def main():
    print("cv2.__version__ =", cv2.__version__)

    frame_no = 0
    Mode = "Detection"
    Tracked_class = 0

    while True:
        start_detection = time.time()

        if config.debugging:
            FLASK_STREAM_URL = "http://192.168.137.20:5000/video_feed"
            stream = requests.get(FLASK_STREAM_URL, stream=True, timeout=5)
            bytes_data = b""

            for chunk in stream.iter_content(chunk_size=1024):
                bytes_data += chunk
                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')

                if a != -1 and b != -1:
                    jpg = bytes_data[a:b+2]
                    bytes_data = bytes_data[b+2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if frame is None:
                        print("Failed to decode frame.")
                        continue
                    break

        frame = cv2.resize(frame, (config.Resized_width, config.Resized_height))
        frame_orig = frame.copy()

        Mode, Tracked_class = detect_Signs(frame_orig, frame)

        speed = 50
        if Tracked_class == "speed_sign_70":
            speed = 30
        elif Tracked_class == "speed_sign_80":
            print("Speed up to 80")
            speed = 95
        elif Tracked_class == "stop":
            speed = 0

        if config.debugging:
            publish_speed(speed)

        FPS_str = str(int(1 / (time.time() - start_detection))) + " FPS "
        cv2.putText(frame, FPS_str, (frame.shape[1] - 70, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1)

        cv2.imshow("Car Camera view", frame)
        if cv2.waitKey(config.waitTime) == 27:
            break

        frame_no += 1

        if config.Profiling:
            config.loopCount += 1
            if config.loopCount == 150:
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
