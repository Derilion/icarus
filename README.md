![](https://img.shields.io/static/v1.svg?label=Language&message=Python&color=green) ![](https://img.shields.io/static/v1.svg?label=Version&message=Alpha&color=lightgrey)

# Icarus

A project to create a modular digital assistant with voice support.

_Notice: This program is still very much under development. Everything is provided as is and will probably change a lot by later versions._

## Installation
Setting up a Python virtual environment as described [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) is strongly recommended. Only tested for Python >= 3.8.

1. Clone the repository to a place of your liking
2. Install requirements from requirements.txt `pip install -r requirements.txt`
    - Windows needs to install pyaudio using winpip
        ``` bash
            pip install pipwin
            pipwin install pyaudio
        ```
    - OSX needs to install pyaudio using brew 
        ``` bash
            brew install portaudio
            pip install pyaudio
        ```
3. Download [Porcupine](https://github.com/Picovoice/porcupine) and place it in `icarus_base/porcupine`
4. Set up given tokens and configurations in `icarus_base/settings.ini`
5. Run `python icarus_base/main.py`

## Usage

For general usage a given text or speech input will be processed and a response will be given on the same channel. By default a command line client is included and can respond to text queries based on the installed skills.

### Installation of Skills
Skill files need to be copied to the `icarus_base/skills/` directory. When Icarus is restarted it will automatically recognize skills and enable them.

### Installation of Clients
Client files need to be copied to the `icarus_base/src/Clients/` directory. When Icarus is restarted it will automatically recognize clients and enable them.

## How to write new Skills

For Skills a straightforward API is given via inheritance. Inherit from `skills.superclient.SuperClient` and set values for self.id and the skill can be loaded. 

General parameters which should be set are:
- self.id: unique id
- self.name: skill name shown in userspace
- self.version: version revision of the skill
- self.creator: credit to yourself (and to blame you ofc)
- self.phrases: array of example sentences used to recognize if a phrase should be mapped to your skill

Functions you should implement are:
- def setup(self):  Function is loaded before the skill is used, use to set up skill tokens etc.
- def main(self, message): Function is called if a new message has been received and given to the skill. A `Context` object will be given, which offers message information in `Context.msg` and the option to respond in text via `Context.send(str)`

Configuration data can be loaded using `self.get_config('ID_HERE')`. A dictionary can be saved between program runs using `self.save_dict(DICTIONARY)` and later be loaded using `self.load_dict(DICTIONARY)`