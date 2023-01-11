"""Performs general tests."""
import time
from audiometer import audiometer


def test_audiometer():
    """Test audiometer thread creation"""
    exam = audiometer.ExamThread()
    assert exam is not None


def test_hearing_exam_combinations():
    """Tests the creation of a set of hearing tests"""
    exam = audiometer.ExamThread()
    assert exam.exam_array is not None


def test_audiometer_run():
    """Test audiometer thread run and stop"""
    exam = audiometer.ExamThread()
    exam.daemon = True
    exam.start()
    time.sleep(0.5)
    exam.sound_is_heard("left")
    time.sleep(0.5)
    assert exam.sound_thread.frequency == 400
    exam.stop()
