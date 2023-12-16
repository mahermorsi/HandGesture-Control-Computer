import cv2
import mediapipe as mp
import keyboard
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
import pyautogui
import time
import subprocess
import psutil
import speech_recognition as sr
import threading

lefty_is_locked = False
lock = threading.Lock()

# Initialize the recognizer
recognizer = sr.Recognizer()

# Get a list of monitors (usually there's just one)
#monitors = get_monitors()

# Get the width and height of the primary monitor
#primary_monitor = monitors[0]
#width, height = primary_monitor.width, primary_monitor.height
width, height = 1600, 1300

mouse = MouseController()  # Initialize the mouse controller

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

###############
smoothening = 2
prev_x, prev_y = 0,0
###############
def listen_to_speech_and_process():
    global lefty_is_locked
    with lock:
        lefty_is_locked=True
    with sr.Microphone() as source:
        print("Listening...")
        try:
            # Set a timeout to limit how long it listens (adjust as needed)
            audio = recognizer.listen(source,phrase_time_limit=4)
            print("Processing...")
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    try:
        # Recognize speech using Google Speech Recognition
        recognized_text = recognizer.recognize_google(audio)
        process_text(recognized_text)
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    finally:
        with lock:
            lefty_is_locked = False


def open_process(text):
    if 'chrome' in text.lower():
        google_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([google_path])

def write_text(text):
    pyautogui.write(text)


def process_text(text):
    if 'open' in text:
        open_process(text)
    elif 'text' in text:
        word_index=text.find('text')
        text_to_write= text[word_index + len('text'):]
        write_text(text_to_write)
def count_fingers(hand_landmarks, hand_side):
    finger_tip_ids = [8, 12, 16, 20]  # Finger landmarks for tips
    thumb_tip_id = 4
    finger_count = 0
    count=0
    thumb_flag=0

    # Check each finger
    for tip_id in finger_tip_ids:
        # Check if the finger is extended based on its position relative to other landmarks
        if hand_landmarks[tip_id].y < hand_landmarks[tip_id - 2].y:
            finger_count += 1
            count+=tip_id

    # Special case for the thumb
    if hand_side=="Left" and hand_landmarks[thumb_tip_id].x > hand_landmarks[thumb_tip_id - 1].x:
        finger_count += 1
        thumb_flag=1
    elif hand_side=="Right" and hand_landmarks[thumb_tip_id].x < hand_landmarks[thumb_tip_id - 1].x:
        finger_count+=1
        thumb_flag=1
    return finger_count,count,thumb_flag


def is_point_finger_up(fingers):
    if fingers[0]==1 and fingers[1]==8:
        return True
    return False

def is_pinky_and_point_fingers_up(fingers):
    if fingers[0]==2 and fingers[1]==28:
        return True
    return False


last_click_time = 0  # Initialize the time of the last click
def control_mouse(handLms,fingers):
    global last_click_time
    global prev_y, prev_x
    curr_x, curr_y = int(handLms.landmark[8].x * width), int(handLms.landmark[8].y * height)

    if is_point_finger_up(fingers):
        try:
            cursor_x = prev_x + (curr_x - prev_x)/smoothening
            cursor_y = prev_y + (curr_y - prev_y) / smoothening
            mouse.position = (cursor_x,cursor_y)
            prev_x, prev_y=cursor_x, cursor_y
        except Exception as e:
            print(f'Error {e} occurred')
    current_time=time.time()
    if current_time - last_click_time >=1.0:
        if is_pinky_and_point_fingers_up(fingers):
            mouse.click(Button.left, 2)
            last_click_time=current_time
        elif fingers[2] == 1:
            last_click_time=current_time
            mouse.press(Button.left)
            mouse.release(Button.left)

def open_keyboard():
    global keyboard_is_shown
    subprocess.Popen('osk.exe')
    keyboard_is_shown=True

keyboard_is_shown = False
def close_keyboard():
    global keyboard_is_shown
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'] == 'osk.exe':
            process.terminate()
    keyboard_is_shown=False
def main():
    global keyboard_is_shown
    global lefty_is_locked
    threads = []
    ptime=0
    while True:
        success, unflipped_image = cap.read()
        image = cv2.flip(unflipped_image, 1)
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(imageRGB)
        if results.multi_hand_landmarks: # if hand was detected
            for handLms, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Determine the handedness (left or right hand)
                hand_side = handedness.classification[0].label
                fingers = count_fingers(handLms.landmark, hand_side)
                with lock:
                    if hand_side == "Left" and lefty_is_locked:
                        continue
                if hand_side=="Right":
                    control_mouse(handLms,fingers)
                if hand_side=="Left" and not keyboard_is_shown:
                    if fingers[0]==3 and fingers[1]==36: # if three fingers are raised
                        open_keyboard()

                elif hand_side=="Left" and keyboard_is_shown==True:
                    if fingers[0] == 2 and fingers[1]==20:
                        close_keyboard()
                if hand_side=="Left":
                    if fingers[0]==2 and fingers[1]==28: # if spiderman gesture is recognized
                        #listen_to_speech_and_process()
                        t = threading.Thread(target=listen_to_speech_and_process)
                        threads.append(t)
                        t.start()



                #connect all joints
                for id, lm in enumerate(handLms.landmark):
                    mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
                #h, w, c = image.shape
                # Print hand side
                #cv2.putText(image, hand_side, (int(handLms.landmark[12].x * w - 70), int(handLms.landmark[12].y * h) - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # Update the display
        # ctime=time.time()
        # fps=1/(ctime-ptime)
        # fps=int(fps)
        # cv2.putText(image, f'fps {str(fps)}', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        # cv2.imshow("Output", image)
        # ptime=ctime
        # cv2.waitKey(1)

        if keyboard.is_pressed('q'):
            print("Exiting the program.")
            for thr in threads:
                thr.join()
            break


if __name__ == "__main__":
    main()
