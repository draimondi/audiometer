"""
Class for running a thread which produces a Tone.
The tone can be changed in frequency and volume on the fly

Contains:
    - ToneThread
"""
import logging
import threading
import time

import numpy as np
import pyaudio

NO_DEVICE_ERROR = "No default audio device found. Unable to run this sound thread."
BOTH_CHANNELS = "both"
LEFT_CHANNEL = "left"
RIGHT_CHANNEL = "right"


class ToneThread(threading.Thread):
    """This class instantiates a thread which, when run, plays a sine wave audio tone."""

    TONE_ARRAY_TYPE = np.float32
    DEFAULT_SAMPLE_RATE = 44100  # frames or samples per second. Hz, must be integer
    DEFAULT_FREQUENCY = 440.0  # sine frequency, Hz, may be float
    DEFAULT_PERIOD = 0.2  # in seconds, may be float
    DEFAULT_LOOPS = 1  # number of times to play the tone. -1 for infinite
    DEFAULT_VOLUME = 1.0  # volume of the generated tone

    def generate_sine_wave(self, num_samples, array_type=TONE_ARRAY_TYPE):
        """Generates a sine wave array of the specified type"""
        # creates a template array
        sample_array = np.arange(num_samples, dtype=array_type)
        # applies sine wave pattern to the array
        sine_array = np.sin(
            2 * np.pi * sample_array * self.frequency / self.sample_rate
        )
        return sine_array

    def make_stereo_tone(self):
        """Generates a stereo tone compatible with pyaudio"""
        num_samples = int(round(self.duration * self.sample_rate))  # Sample count
        audio_wave = self.generate_sine_wave(num_samples, self.TONE_ARRAY_TYPE)
        left_wave = np.zeros(shape=num_samples, dtype=self.TONE_ARRAY_TYPE)
        right_wave = left_wave
        if self.channel in (LEFT_CHANNEL, BOTH_CHANNELS):
            left_wave = audio_wave
        if self.channel in (RIGHT_CHANNEL, BOTH_CHANNELS):
            right_wave = audio_wave
        self.tone = np.ravel([left_wave, right_wave], "F")

    def __init__(
        self,
        frequency=DEFAULT_FREQUENCY,
        rate=DEFAULT_SAMPLE_RATE,
        period=DEFAULT_PERIOD,
        loops=DEFAULT_LOOPS,
        volume=DEFAULT_VOLUME,
        sleep_between_loops=False,
    ):
        super().__init__()
        self.tone = None  # The array representing the audio tone
        self.frequency = frequency  # frequency in Hz, may be float
        self.sample_rate = rate  # sampling rate in Hz, must be integer
        self.duration = period  # in seconds, may be float
        self.volume = volume  # Volume of the tone. Float, between 0 and 1
        self.stopped = False  # Stop playing the tone
        self.channel = BOTH_CHANNELS  # The speaker on which to play the tone.
        self.loops = loops  # Number of times to play the tone. -1 means infinite
        self.sleep_between_loops = sleep_between_loops  # Pause between tone loops
        self.make_stereo_tone()
        try:
            self.stream = pyaudio.PyAudio().open(
                format=pyaudio.paFloat32, channels=2, rate=self.sample_rate, output=True
            )
        except OSError as error:  # nocover-local
            logging.error(error)
            logging.error(NO_DEVICE_ERROR)

    def get_duration(self):
        """Returns the duration of the generated tone"""
        return self.duration

    def get_volume(self):
        """Returns the current volume of the generated tone"""
        return self.volume

    def set_volume(self, volume):
        """Sets the volume of the generated tone"""
        self.volume = volume

    def set_frequency(self, hertz):
        """Sets the frequency of the generated tone"""
        self.frequency = int(hertz)
        self.make_stereo_tone()

    def mute(self):
        """Mutes the generated tone"""
        self.stopped = True

    def unmute(self):
        """Unmutes the generated tone"""
        self.stopped = False

    def set_channel(self, channel):
        """Sets the channel where to play the generated tone.
        'channel' parameter can be ''left', 'right' or 'both'
        """
        self.channel = channel
        self.make_stereo_tone()

    def run(self):
        """Generates the tone and plays it to the default audio device"""
        loop = 0
        audio_devices = (
            pyaudio.PyAudio().get_host_api_info_by_index(0).get("deviceCount")
        )

        # If there are no audio devices, avoid playing sounds. Skip code coverage in local.
        if audio_devices == 0:  # nocover-local
            logging.error(NO_DEVICE_ERROR)
            self.stopped = True

        # If there are audio devices, play sounds. Skip code coverage in CI builds.
        while not self.stopped and (
            loop < self.loops or self.loops == -1
        ):  # nocover-ci

            self.stream.write((self.tone * self.volume).tobytes())

            if self.loops != -1:
                loop = loop + 1
            if self.sleep_between_loops:
                time.sleep(self.duration * 2)
