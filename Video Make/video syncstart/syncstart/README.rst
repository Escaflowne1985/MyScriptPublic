=======================================
syncstart(1) Version 1.0.1 \| syncstart
=======================================

SYNOPSIS
========

Command line help::

    usage: stpl [-h] [--version] [-t TAKE] [-s] [-n] [-d] [-l LOWPASS] in1 in2
    
    CLI interface to sync two media files using their audio streams.
      ffmpeg needs to be available.
      
    
    positional arguments:
      in1                   First media file to sync with second, using audio.
      in2                   Second media file to sync with first, using audio.
    
    options:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -t TAKE, --take TAKE  Take X seconds of the inputs to look at. (default: 20)
      -s, --show            Turn off "show diagrams", in case you are confident.
      -n, --normalize       Turn on normalize. It turns on by itself in a second pass, if sampling rates
                            differ.
      -d, --denoise         Turns on denoise, as experiment in case of failure.
      -l LOWPASS, --lowpass LOWPASS
                            lowpass, just in case, because like with manual sync'ing, the low frequencies
                            matter more. 0 == off. (default: 0)


DESCRIPTION
===========


The steps taken by ``syncstart``:

- extract start audio as ``.wav`` using ffmpeg
- optionally normalize, denoise, lowpass the two ``.wav``
- compute offset via correlation using scipy ifft/fft
- print result and optionally show in diagrams

Requirements:

- ffmpeg installed
- Python3 with tk (tk is separate on Ubuntu: python3-tk)

References:

- https://ffmpeg.org/ffmpeg-all.html
- https://github.com/slhck/ffmpeg-normalize
- https://dsp.stackexchange.com/questions/736/how-do-i-implement-cross-correlation-to-prove-two-audio-files-are-similar

Within Python:

from syncstart import file_offset
file_offset




INSTALLATION
============

To install for user only, do::

   pip install --user syncstart

EXAMPLES
--------

::

  syncstart from_s10.m4a from_gopro.m4p
  syncstart from_s10.m4a from_gopro.m4p -t 10
  syncstart from_s10.m4a from_gopro.m4p -t 30
  syncstart from_s10.m4a from_gopro.m4p -sndl 0


License
-------

MIT

