"""
This implements the main user interface using PySimpleGUI.
"""
import PySimpleGUI as sg

from audiometer import audiometer

PROGRAM_TITLE = "Hearing Exam"


def program_launch():
    """Create the initial window layout"""
    default_layout = [
        [sg.Button("Start Hearing Exam", key="start")],
        [sg.Checkbox("Randomize the Exam", default=False, key="randomize")],
    ]
    window = sg.Window(PROGRAM_TITLE, default_layout, grab_anywhere=True, finalize=True)
    window.Refresh()
    return window


def exam_start(randomize):
    """Starts the actual hearing exam"""
    test_layout = [
        [sg.Text("Which ear do you hear sound from?")],
        [
            [
                sg.Button("Left Ear", key="left"),
                sg.Button("Right Ear", key="right"),
            ]
        ],
        [sg.Text(size=(40, 1), key="output")],
        [sg.Button("Stop Exam", key="stop")],
    ]
    window = sg.Window(PROGRAM_TITLE, test_layout, grab_anywhere=True, finalize=True)
    window.Refresh()
    exam = audiometer.ExamThread()
    exam.daemon = True
    exam.generate_exam_combinations(randomize)
    exam.start()
    return window, exam


def detect_sound(window, exam, channel):
    """Detects if sound is heard in the correct channel"""
    if exam.sound_is_heard(channel):
        window["output"].update(
            f"Sound correctly detected from the {channel}", text_color="green"
        )
    else:
        window["output"].update(
            f"Incorrect. Sound is not coming from the {channel}",
            text_color="red",
        )


def main():
    """Creates the main user interface"""
    sg.theme("dark grey 8")
    window = None
    exam = None

    while True:
        if window:
            event, values = window.read()
        else:
            event = "program_launch"

        match event:
            case "program_launch" | "stop":
                # Stop running exam if it exists
                if window and exam:
                    exam.stop()
                    window.close()
                window = program_launch()

            case "start":
                window.close()
                window, exam = exam_start(randomize=(values["randomize"]))

            case "right" | "left":
                detect_sound(window, exam, event)

            case sg.WINDOW_CLOSED:
                break


if __name__ == "__main__":
    main()
