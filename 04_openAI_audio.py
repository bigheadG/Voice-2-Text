import sys
import threading
import pyaudio
import numpy as np
import wave
import whisper
import warnings
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

class AudioMonitor(QThread):
    update_transcription = pyqtSignal(str)

    def __init__(self, threshold=500, record_seconds=5, output_filename="tmp.wav"):
        super().__init__()
        self.threshold = threshold
        self.record_seconds = record_seconds
        self.output_filename = output_filename
        self.is_monitoring = False
        self.audio = pyaudio.PyAudio()
        self.stream = None
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.model = whisper.load_model("tiny")

    def run(self):
        self.start_monitoring()

    def start_monitoring(self):
        self.is_monitoring = True
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        while self.is_monitoring:
            data = self.stream.read(1024, exception_on_overflow=False)
            amplitude = np.frombuffer(data, dtype=np.int16).max()
            if amplitude > self.threshold:
                self.record_and_transcribe()

    def stop_monitoring(self):
        self.is_monitoring = False
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()

    def record_and_transcribe(self):
        frames = []
        for _ in range(0, int(16000 / 1024 * self.record_seconds)):
            data = self.stream.read(1024, exception_on_overflow=False)
            frames.append(data)
        wave_file = wave.open(self.output_filename, 'wb')
        wave_file.setnchannels(1)
        wave_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(16000)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()
        transcription = self.transcribe_audio()
        self.update_transcription.emit(transcription)

    def transcribe_audio(self):
        result = self.model.transcribe(self.output_filename)
        return result["text"]

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.audio_monitor = AudioMonitor()
        self.audio_monitor.update_transcription.connect(self.update_text_edit)

    def initUI(self):
        self.setWindowTitle('Real-Time Audio Monitor and Transcriber')
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.start_button = QPushButton('Start Monitoring', self)
        self.start_button.clicked.connect(self.start_monitoring)

        self.stop_button = QPushButton('Stop Monitoring', self)
        self.stop_button.clicked.connect(self.stop_monitoring)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.text_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_monitoring(self):
        self.audio_monitor.start()
        self.text_edit.append("Monitoring started...")

    def stop_monitoring(self):
        self.audio_monitor.stop_monitoring()
        self.text_edit.append("Monitoring stopped.")

    def update_text_edit(self, text):
        self.text_edit.append(text)

def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

