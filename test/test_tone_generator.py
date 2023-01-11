"""Performs general tests."""
from audiometer import tone_generator


def test_stereo_tone_generator():
    """Test tone generation"""
    sound_thread = tone_generator.ToneThread()
    sound_thread.make_stereo_tone()
    stereo_tone = sound_thread.tone
    assert stereo_tone[2] != 0
    assert stereo_tone[3] != 0


def test_channels():
    """Test tone generation only on left channel"""
    sound_thread = tone_generator.ToneThread()
    sound_thread.set_channel(tone_generator.LEFT_CHANNEL)
    sound_thread.make_stereo_tone()
    stereo_tone = sound_thread.tone
    assert stereo_tone[1] == 0
    assert stereo_tone[2] != 0


def test_volume():
    """Checks volume of the tone"""
    sound_thread = tone_generator.ToneThread()
    sound_thread.set_volume(0.75)
    assert sound_thread.get_volume() == 0.75


def test_mute():
    """Checks the mute/unmute functions"""
    sound_thread = tone_generator.ToneThread()
    sound_thread.mute()
    sound_thread.unmute()


def test_duration():
    """Checks duration of the tone"""
    sound_thread = tone_generator.ToneThread()
    assert sound_thread.get_duration() == tone_generator.DEFAULT_PERIOD


def test_frequency():
    """Checks volume of the tone"""
    sound_thread = tone_generator.ToneThread()
    sound_thread.set_frequency(6000)
    assert sound_thread.frequency == 6000


def test_run():
    """Checks duration of the tone"""
    sound_thread = tone_generator.ToneThread(
        period=0.001, loops=2, sleep_between_loops=True
    )
    sound_thread.run()
