# Hand Gesture Controlled Mouse and Speech Recognition Interface

This project implements a hand gesture-controlled mouse and speech recognition interface using computer vision and media input libraries. The system allows users to control mouse movements and perform specific actions like opening a keyboard or executing speech commands based on hand gestures recognized through a webcam.

## Project Overview

### Key Features

- **Hand Gesture Control**: 
  - The system tracks hand movements using a webcam and controls the mouse cursor based on the detected gestures.
  - Gestures such as raising specific fingers can trigger different actions, like moving the mouse cursor or clicking.

- **Speech Recognition**:
  - The system listens for voice commands when a specific hand gesture is detected (e.g., the "Spiderman" gesture).
  - It can execute specific commands, such as opening Chrome or typing text.

- **On-Screen Keyboard**:
  - The virtual keyboard can be shown or hidden based on specific hand gestures.
  
- **Real-Time Feedback**:
  - The system provides real-time visual feedback by displaying the detected hand gestures and frames per second (FPS) on the screen.

### Technologies Used

- **OpenCV**: For video capture and image processing.
- **Mediapipe**: For hand landmark detection.
- **Pynput**: For controlling the mouse programmatically.
- **PyAutoGUI**: For automating GUI interactions like typing text.
- **SpeechRecognition**: For processing and recognizing voice commands.
- **Python Threading**: For handling concurrent speech recognition while allowing mouse control to continue uninterrupted.

## How It Works

1. **Hand Gesture Recognition**:
   - The program captures video from a webcam.
   - It uses Mediapipe to detect hand landmarks and identify which fingers are raised.
   - Specific gestures control mouse movements and clicks.

2. **Mouse Control**:
   - Moving the index finger controls the mouse cursor.
   - Raising both the pinky and index fingers triggers a double-click.

3. **Speech Recognition**:
   - When the "Spiderman" gesture (index and pinky fingers raised) is detected with the left hand, the system listens for a voice command.
   - Commands such as "open Chrome" or "type text" can be processed.

4. **On-Screen Keyboard**:
   - A gesture with three fingers raised (left hand) opens the on-screen keyboard.
   - A gesture with two fingers raised (left hand) closes the keyboard.

### Usage Instructions

1. **Install Dependencies**:
   - Ensure you have Python installed.
   - Install the required packages using the `requirements.txt` or manually with `pip`:

   pip install opencv-python mediapipe pynput pyautogui SpeechRecognition psutil screeninfo

2. **Run the Program**:
   - Start the program by executing the script:

   python main.py

3. **Control the System**:
   - Use the gestures to control the mouse or open the on-screen keyboard.
   - Use the "Spiderman" gesture to activate speech recognition.

4. **Exit the Program**:
   - Press the `q` key to safely exit the program.

## Important Notes
- **Gesture Sensitivity**: The gestures are recognized based on the positions of specific hand landmarks. Ensure the webcam has a clear view of your hand.
- **Speech Recognition**: The speech recognition feature requires an active internet connection to work with Google’s speech recognition service.
- **Threading**: The program uses threading to handle speech recognition without interrupting the gesture-based mouse control.
