# Voice-2-Text
Voice Recognize
## Explanation
1:AudioMonitor Class:

This class inherits from QThread to run the audio monitoring in a separate thread.
It continuously monitors the microphone input for sound above a specified threshold.
When the threshold is exceeded, it records a 5-second audio clip, transcribes it using the Whisper model, and emits the transcription result using a PyQt5 signal (update_transcription).

2:App Class:

Sets up the PyQt5 GUI with start and stop buttons and a text display area.
Connects the start and stop buttons to the respective methods to control the audio monitoring.
Connects the update_transcription signal from AudioMonitor to a method that updates the text display with the transcription results.

3:Main Function:
Initializes and runs the PyQt5 application.
# Usage
1: Start Monitoring:

Click the "Start Monitoring" button to begin monitoring the microphone input.
When the input sound exceeds the threshold, the program will record a 5-second clip, transcribe it, and display the transcription in real-time.

2: Stop Monitoring:

Click the "Stop Monitoring" button to stop monitoring the microphone input.
This script allows for real-time audio monitoring, recording, transcription, and display in a GUI using PyQt5 and OpenAI Whisper. Ensure your microphone is properly set up and accessible by the pyaudio library.
