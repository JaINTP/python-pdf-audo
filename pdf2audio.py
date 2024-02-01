#!/usr/bin/env python3.12
"""
This module provides functionality for converting PDF files to audio files.
"""

import os
import argparse
import pyttsx3
from PyPDF2 import PdfReader


class VoiceAssistant:
    """
    A class representing a voice assistant that can speak text and save it to a file.

    Attributes:
        speaker (pyttsx3.engine.Engine): The text-to-speech engine used by the voice assistant.

    Methods:
        set_voice(voice_id: int): Sets the voice of the voice assistant.
        set_rate(rate: int): Sets the speaking rate of the voice assistant.
        save_to_file(text: str, output_file: str): Saves the spoken text to a file.
        say(text: str): Speaks the given text.
    """

    def __init__(self):
        """
        Initializes an instance of VoiceAssistant.

        This function initializes the speaker object using pyttsx3 library.

        Parameters:
            None

        Returns:
            None
        """
        self.speaker = pyttsx3.init()

    def set_voice(self, voice_id: int):
        """
        Sets the voice of the voice assistant.

        Args:
            voice_id (int): The index of the voice to be set.

        Raises:
            ValueError: If the voice_id is invalid.
        """
        voices = self.speaker.getProperty('voices')
        if voice_id < 0 or voice_id >= len(voices):
            raise ValueError(f"Invalid voice_id. It must be between 0 and {len(voices) - 1}")
        self.speaker.setProperty('voice', voices[voice_id].id)

    def set_rate(self, rate: int):
        """
        Sets the speaking rate of the voice assistant.

        Args:
            rate (int): The speaking rate in words per minute.

        Raises:
            ValueError: If the rate is invalid.
        """
        if 50 <= rate <= 400:
            self.speaker.setProperty('rate', rate)
        else:
            raise ValueError("Invalid rate. It must be between 50 and 400 words per minute")

    def save_to_file(self, text: str, output_file: str):
        """
        Saves the spoken text to a file.

        Args:
            text (str): The text to be spoken and saved.
            output_file (str): The path of the output file.

        Raises:
            pyttsx3.Error: If there is an error saving the file.
        """
        self.speaker.save_to_file(text, output_file)
        self.speaker.runAndWait()
        self.speaker.stop()

    def say(self, text: str):
        """
        Speaks the given text.

        Args:
            text (str): The text to be spoken.
        """
        self.speaker.say(text)
        self.speaker.runAndWait()
        self.speaker.stop()


class PdfToAudio:
    """
    A class that converts a PDF file to audio using a voice assistant.

    Attributes:
        pdf_file (str): The path to the PDF file.
        voice_assistant (VoiceAssistant): The voice assistant used for text-to-speech conversion.

    Methods:
        read_pdf_file() -> str:
            Reads the content of the PDF file and returns it as a string.

        save_audio_file(output_file: str = 'pdf.mp3', voice_id: int = 0, rate: int = 150):
            Converts the PDF file to audio and saves it to the specified output file.

        play_as_audio(voice_id: int = 0, rate: int = 150):
            Converts the PDF file to audio and plays it using the voice assistant.
    """

    def __init__(self, pdf_file: str, voice_assistant: VoiceAssistant):
        """
        Initializes a new instance of the PdfToAudio class.

        Args:
            pdf_file (str): The path to the PDF file.
            voice_assistant (VoiceAssistant): The voice assistant used for text-to-speech conversion.

        Raises:
            TypeError: If the pdf_file argument is not a string.
            FileNotFoundError: If the specified PDF file does not exist.
        """
        if not isinstance(pdf_file, str):
            raise TypeError("File name must be a string")
        if not os.path.isfile(pdf_file):
            raise FileNotFoundError(f"File '{pdf_file}' does not exist!")

        self.reader = PdfReader(open(pdf_file, 'rb'))
        self.voice_assistant = voice_assistant

    def read_pdf_file(self) -> str:
        """
        Reads the content of the PDF file and returns it as a string.

        Returns:
            str: The content of the PDF file.
        """
        content = ""
        for _, page in enumerate(self.reader.pages):
            content += page.extract_text().strip()
        return content

    def save_audio_file(self, output_file: str = 'pdf.mp3', voice_id: int = 0, rate: int = 150):
        """
        Converts the PDF file to audio and saves it to the specified output file.

        Args:
            output_file (str, optional): The path to the output audio file. Defaults to 'pdf.mp3'.
            voice_id (int, optional): The ID of the voice to use for text-to-speech conversion. Defaults to 0.
            rate (int, optional): The rate of speech in words per minute. Defaults to 150.
        """
        self.voice_assistant.set_voice(voice_id)
        self.voice_assistant.set_rate(rate)
        self.voice_assistant.save_to_file(self.read_pdf_file(), output_file)

    def play_as_audio(self, voice_id: int = 0, rate: int = 150):
        """
        Converts the PDF file to audio and plays it using the voice assistant.

        Args:
            voice_id (int, optional): The ID of the voice to use for text-to-speech conversion. Defaults to 0.
            rate (int, optional): The rate of speech in words per minute. Defaults to 150.
        """
        self.voice_assistant.set_voice(voice_id)
        self.voice_assistant.set_rate(rate)
        self.voice_assistant.say(self.read_pdf_file())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert PDF files to audio')
    parser.add_argument('file_name', type=str, help='Name of the PDF file')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--play', action='store_true', help='Play the PDF file as audio')
    group.add_argument('-s', '--save', action='store_true', help='Save the PDF file as an audio file')

    parser.add_argument('-v', '--voice', type=int, help='ID of the voice to use for audio playback', default=0)
    parser.add_argument('-r', '--rate', type=int, help='Rate of speech in words per minute', default=150)
    parser.add_argument("--output", help="Output file name when using --save")

    args = parser.parse_args()

    if args.save and not args.output:
        parser.error("--save requires --output argument")
    if args.play and args.output:
        parser.error("--play does not take any additional arguments")

    voice_assistant = VoiceAssistant()
    pdf_to_audio = PdfToAudio(args.file_name, voice_assistant)

    if args.play:
        print(f"Playing pdf file '{args.file_name}' as audio")
        pdf_to_audio.play_as_audio(voice_id=args.voice, rate=args.rate)
    if args.save:
        print(f"Saving pdf file '{args.file_name}' as '{args.output}'")
        pdf_to_audio.save_audio_file(args.output)
