
# python-pdf-audio

## Info
Quick rewrite of [Tiff In Tech's](https://github.com/TiffinTech) [python-pdf-audo](https://github.com/TiffinTech/python-pdf-audo) project based on the YouTube tutorial.
Re-written on Windows 11, using [Python 3.12](https://www.python.org/downloads/release/python-3120/) in [VS Code](https://code.visualstudio.com/download)
Only tested on Windows as of now.

## Usage:
```
usage: main.py [-h] (-p | -s) [-v VOICE] [-r RATE] [--output OUTPUT] file_name

Convert PDF files to audio

positional arguments:
  file_name             Name of the PDF file

options:
  -h, --help            show this help message and exit
  -p, --play            Play the PDF file as audio
  -s, --save            Save the PDF file as an audio file
  -v VOICE, --voice VOICE
                        ID of the voice to use for audio playback
  -r RATE, --rate RATE  Rate of speech in words per minute
  --output OUTPUT       Output file name when using --save
```
### Example Usage:
```
python .\main.py .\book.pdf --play -r 200 -v 1
python .\main.py .\book.pdf --save --output output.mp3 
```


## Useful Links:

* [Automating My Life with Python: The Ultimate Guide | Code With Me]()
* [PyPDF2](https://pypi.org/project/PyPDF2/)
* [pyttsx3](https://pypi.org/project/pyttsx3/)
* [pywin32](https://www.youtube.com/watch?v=LXsdt6RMNfY) (For Windows)
