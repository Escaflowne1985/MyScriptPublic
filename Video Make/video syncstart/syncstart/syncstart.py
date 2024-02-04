#!/usr/bin/env python3

"""
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

"""

import matplotlib

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np
from scipy import fft
from scipy.io import wavfile
import tempfile
import os
import pathlib
import sys

__version__ = "1.0.1"
__author__ = """Roland Puntaier"""
__email__ = 'roland.puntaier@gmail.com'

# global
ax = None
take = 20
normalize = False
denoise = False
lowpass = 0

ffmpegwav = 'ffmpeg -i "{}" -t %s -c:a pcm_s16le -map 0:a "{}"'
ffmpegnormalize = ('ffmpeg -y -nostdin -i "{}" -filter_complex ' +
                   "'[0:0]loudnorm=i=-23.0:lra=7.0:tp=-2.0:offset=4.45:linear=true:print_format=json[norm0]' " +
                   "-map_metadata 0 -map_metadata:s:a:0 0:s:a:0 -map_chapters 0 -c:v copy -map '[norm0]' " +
                   '-c:a:0 pcm_s16le -c:s copy "{}"')
ffmpegdenoise = 'ffmpeg -i "{}" -af' + " 'afftdn=nf=-25' " + '"{}"'
ffmpeglow = 'ffmpeg -i "{}" -af' + " 'lowpass=f=%s' " + '"{}"'
o = lambda x: '%s%s' % (x, '.wav')


def in_out(command, infile, outfile):
    hdr = '-' * len(command)
    print("%s\n%s\n%s" % (hdr, command, hdr))
    ret = os.system(command.format(infile, outfile))
    if 0 != ret:
        sys.exit(ret)


def normalize_denoise(infile, outname):
    with tempfile.TemporaryDirectory() as tempdir:
        outfile = o(pathlib.Path(tempdir) / outname)
        in_out(ffmpegwav % take, infile, outfile)
        if normalize:
            infile, outfile = outfile, o(outfile)
            in_out(ffmpegnormalize, infile, outfile)
        if denoise:
            infile, outfile = outfile, o(outfile)
            in_out(ffmpegdenoise, infile, outfile)
            infile, outfile = outfile, o(outfile)
            in_out(ffmpegdenoise, infile, outfile)
        if int(lowpass):
            infile, outfile = outfile, o(outfile)
            in_out(ffmpeglow % lowpass, infile, outfile)
        r, s = wavfile.read(outfile)
        if len(s.shape) > 1:  # stereo
            s = s[:, 0]
        return r, s


def fig1(title=None):
    fig = plt.figure(1)
    plt.margins(0, 0.1)
    plt.grid(True, color='0.7', linestyle='-', which='major', axis='both')
    plt.grid(True, color='0.9', linestyle='-', which='minor', axis='both')
    plt.title(title or 'Signal')
    plt.xlabel('Time [seconds]')
    plt.ylabel('Amplitude')
    axs = fig.get_axes()
    global ax
    ax = axs[0]


def show1(fs, s, color=None, title=None, v=None):
    if not color: fig1(title)
    if ax and v: ax.axvline(x=v, color='green')
    plt.plot(np.arange(len(s)) / fs, s, color or 'black')
    if not color: plt.show()


def show2(fs, s1, s2, title=None):
    fig1(title)
    show1(fs, s1, 'blue')
    show1(fs, s2, 'red')
    plt.show()


def read_normalized(in1, in2):
    global normalize
    r1, s1 = normalize_denoise(in1, 'out1')
    r2, s2 = normalize_denoise(in2, 'out2')
    if r1 != r2:
        old, normalize = normalize, True
        r1, s1 = normalize_denoise(in1, 'out1')
        r2, s2 = normalize_denoise(in2, 'out2')
        normalize = old
    assert r1 == r2, "not same sample rate"
    fs = r1
    return fs, s1, s2


def corrabs(s1, s2):
    ls1 = len(s1)
    ls2 = len(s2)
    padsize = ls1 + ls2 + 1
    padsize = 2 ** (int(np.log(padsize) / np.log(2)) + 1)
    s1pad = np.zeros(padsize)
    s1pad[:ls1] = s1
    s2pad = np.zeros(padsize)
    s2pad[:ls2] = s2
    corr = fft.ifft(fft.fft(s1pad) * np.conj(fft.fft(s2pad)))
    ca = np.absolute(corr)
    xmax = np.argmax(ca)
    return ls1, ls2, padsize, xmax, ca


def cli_parser(**ka):
    import argparse
    parser = argparse.ArgumentParser(description=file_offset.__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)

    if 'in1' not in ka:
        parser.add_argument(
            'in1',
            help='First media file to sync with second, using audio.')
    if 'in2' not in ka:
        parser.add_argument(
            'in2',
            help='Second media file to sync with first, using audio.')
    if 'take' not in ka:
        parser.add_argument(
            '-t', '--take',
            dest='take',
            action='store',
            default=20,
            help='Take X seconds of the inputs to look at. (default: 20)')
    if 'show' not in ka:
        parser.add_argument(
            '-s', '--show',
            dest='show',
            action='store_false',
            default=True,
            help='Turn off "show diagrams", in case you are confident.')
    if 'normalize' not in ka:
        parser.add_argument(
            '-n', '--normalize',
            dest='normalize',
            action='store_true',
            default=False,
            help='Turn on normalize. It turns on by itself in a second pass, if sampling rates differ.')
    if 'denoise' not in ka:
        parser.add_argument(
            '-d', '--denoise',
            dest='denoise',
            action='store_true',
            default=False,
            help='Turns on denoise, as experiment in case of failure.')
    if 'lowpass' not in ka:
        parser.add_argument(
            '-l', '--lowpass',
            dest='lowpass',
            action='store',
            default=0,
            help="lowpass, just in case, because like with manual sync'ing,\
      the low frequencies matter more. 0 == off. (default: 0)")
    return parser


def file_offset(**ka):
    """CLI interface to sync two media files using their audio streams.
    ffmpeg needs to be available.
    """

    parser = cli_parser(**ka)
    args = parser.parse_args().__dict__
    ka.update(args)

    global take, normalize, denoise, lowpass
    in1, in2, take, show = ka['in1'], ka['in2'], ka['take'], ka['show']
    normalize, denoise, lowpass = ka['normalize'], ka['denoise'], ka['lowpass']
    fs, s1, s2 = read_normalized(in1, in2)
    ls1, ls2, padsize, xmax, ca = corrabs(s1, s2)
    if show: show1(fs, ca, title='Correlation', v=xmax / fs)
    sync_text = """
==============================================================================
%s needs 'ffmpeg -ss %s' cut to get in sync
==============================================================================
"""
    if xmax > padsize // 2:
        if show: show2(fs, s1, s2[padsize - xmax:], title='1st=blue;2nd=red=cut(%s;%s)' % (in1, in2))
        file, offset = in2, (padsize - xmax) / fs
    else:
        if show: show2(fs, s1[xmax:], s2, title='1st=blue=cut;2nd=red (%s;%s)' % (in1, in2))
        file, offset = in1, xmax / fs
    print(sync_text % (file, offset))
    return file, offset


main = file_offset
if __name__ == '__main__':
    main()
