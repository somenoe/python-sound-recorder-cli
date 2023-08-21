import sounddevice as sd
import numpy as np
import time
import threading
import keyboard
import soundfile as sf

STOP_KEY = "|"

class SoundRecorder:
    def __init__(self):
        self.recording = False
        self.frames = []
        self.start_time = None

    def start_recording(self):
        self.recording = True
        self.frames = []
        self.start_time = time.time()

        def callback(indata, frames, time, status):
            if status:
                print(status)
            if self.recording:
                self.frames.append(indata.copy())

        with sd.InputStream(callback=callback):
            print(f"Recording... Press '{STOP_KEY}' to stop recording.")
            while self.recording:
                if keyboard.is_pressed(STOP_KEY):
                    self.stop_recording()

    def stop_recording(self):
        self.recording = False
        if self.frames:
            audio_data = np.concatenate(self.frames, axis=0)
            duration = time.time() - self.start_time
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            filename = f"{timestamp}_{int(duration)}s.wav"
            samplerate = int(sd.query_devices(None, 'input')['default_samplerate'])
            sf.write(f"records/{filename}", audio_data, samplerate)
            print(f"Recording saved as {filename}")

if __name__ == "__main__":
    recorder = SoundRecorder()
    recorder.start_recording()
    while True:
        if keyboard.is_pressed(STOP_KEY):
            break
