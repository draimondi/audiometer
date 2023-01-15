# audiometer

## Description
This project aims to perform a very simple python-based hearing test with different frequencies and volumes on randomized on left/right channels of your audio device. The exam is not in any way official.

The project uses [PySimpleGUI](PySimpleGUI) to create a basic user interface, [numpy](https://numpy.org/) to generate the sine wave patterns at different frequencies, and [PyAudio](https://pypi.org/project/PyAudio/) to stream the generated sine waves.

I created this project to practice putting in place all the best practices in a Python software project using industry standard tools. Fortunately, there are already wonderful Cookiecutter templates that help put this in place, and thus it was quite easy to have:
1. Development environment setup with [pipenv](https://pypi.org/project/flake8/)
2. Auto-formatting with [Black](https://pypi.org/project/black/)
3. Style Guide enforcement with [flake8](https://pypi.org/project/flake8/)
4. Unit testing and code coverage with [pytest](https://pytest.org/)
5. [Docker](Docker) image generation
6. CI setup for test and Docker with GitHub


## Setup
```sh
# Install dependencies
pipenv install --dev

# Setup pre-commit and pre-push hooks
pipenv run pre-commit install -t pre-commit
pipenv run pre-commit install -t pre-push
```
I also included the .vscode directory with my preferred VSCode settings and launch configuration due to the ubiquitous usage of this IDE. 

## Running
```sh
pipenv run python -m audiometer
```

## Credits
This package was created with Cookiecutter and the [sourcery-ai/python-best-practices-cookiecutter](https://github.com/sourcery-ai/python-best-practices-cookiecutter) project template.
