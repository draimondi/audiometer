"""
This python script will simulate a hearing exam, with distinct frequencies and volumes
"""
import logging
import threading
import time

import numpy

from audiometer import tone_generator

INITIAL_VOLUME = 0.0001  # Volume at which to start each tone test
VOLUME_DELTA = 0.0001  # Amount to increment the volume until sound is detected


class ExamThread(threading.Thread):
    """Class that handles the thread which runs the exam"""

    EXAM_FREQUENCIES = [100, 400, 800, 1600, 3200, 6400, 12800, 14000]

    def __init__(self):
        super().__init__()
        self.exam_array = None
        self.exam_result_array = []
        self._stop_event = threading.Event()
        self.sound_thread = tone_generator.ToneThread(volume=INITIAL_VOLUME)
        self.sound_thread.daemon = True
        self.sound_thread.mute()
        self.sound_detected = False
        self.tone = None
        self.running = False
        self.generate_exam_combinations()

    def generate_exam_combinations(self, randomize=False):
        """Generates the combinations of frequencies and channels used for the exam"""
        channel_array = [
            tone_generator.LEFT_CHANNEL,
            tone_generator.RIGHT_CHANNEL,
        ]
        exam_combinations = [
            (channel_array[i], self.EXAM_FREQUENCIES[j])
            for i in range(len(channel_array))
            for j in range(len(self.EXAM_FREQUENCIES))
        ]
        self.exam_array = (
            numpy.random.permutation(exam_combinations)
            if randomize
            else exam_combinations
        )

    def sound_is_heard(self, side):
        """Records when sounds have been heard by the user"""
        if side == self.sound_thread.channel:
            self.exam_result_array.append(
                (self.sound_thread.frequency, side, self.sound_thread.volume)
            )
            self.sound_detected = True
        return self.sound_detected

    def run(self):
        self.running = True
        self.sound_thread.start()
        for channel, frequency in self.exam_array:
            self.sound_detected = False
            self.sound_thread.set_volume(INITIAL_VOLUME)
            self.sound_thread.set_channel(channel)
            self.sound_thread.set_frequency(frequency)
            self.sound_thread.unmute()
            while self.running and self.sound_thread.volume < 1:
                logging.debug(
                    "Current frequency: %s Current volume: %s  Current Speaker: %s",
                    self.sound_thread.frequency,
                    self.sound_thread.volume,
                    self.sound_thread.channel,
                )
                self.sound_thread.run()
                self.sound_thread.set_volume(
                    round(self.sound_thread.volume + VOLUME_DELTA, 5)
                )
                time.sleep(self.sound_thread.get_duration() / 10)
                if self.sound_detected:
                    self.sound_thread.mute()
                    break

    def stop(self):
        """Stops running the exam thread"""
        self.running = False
        self.sound_thread.mute()
        print(f"Exam results:\n{self.exam_result_array}")
