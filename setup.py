from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='Icarus',
   version='0.1',
   description='A modular digital assistant',
   license="MIT",
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='derilion',
   url="http://www.github.com/derilion/icarus/",
   platforms=['nt', 'posix'],
   packages=find_packages(),
   include_package_data=True,
   install_requires=['pyaudio',
                     'pyttsx3',
                     'gtts',
                     'SpeechRecognition',
                     'playsound',
                     'pvporcupine',
                     # from here on skill dependencies are listed
                     'python-telegram-bot',
                     'wikipedia',
                     'caldav',
                     'icalendar'
                     ],  # todo: need to be updated to actual dependencies
   entry_points={
            'console_scripts': [
                'Icarus=icarus:run',
            ],
        },
   python_requires='>=3.7',
   keywords="modular, digital assistant, icarus, jarvis, raspberry",
)
