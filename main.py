import wave
import os
import time
import threading
import tkinter
import pyaudio
import datetime


class VoiceRecorder():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.button = tkinter.Button(
            text='🎙',
            font=('Arial', 120, "bold"),
            command=self.click_hendler
        )
        self.button.pack()
        self.lable = tkinter.Label(text='00:00:00')
        self.lable.pack()
        self.recording = False
        self.root.mainloop()

    def click_hendler(self):
        if self.recording:
            self.recording = False
        else:
            self.recording = True
            threading.Thread(target=self.record).start()

    # If you have problem with recognition input device run script from check_input_device and uncomment "input_device_index"
    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
        # input_device_index=9,
    )

        frames = []
        current_time = datetime.datetime.now().strftime("%d.%m.%Y_%H:%M")
        start = time.time()

        while self.recording:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.lable.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        sound_file = wave.open(f'recording_{current_time}.wav', 'wb')
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()


VoiceRecorder()