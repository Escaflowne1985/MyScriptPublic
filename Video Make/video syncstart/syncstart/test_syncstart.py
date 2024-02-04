#!/usr/bin/env python

"""
Tests for `syncstart` package.
"""

import pytest

from syncstart import *
from scipy.io import wavfile
import numpy as np


def to_files(fs, s1, s2, p):
    wav1 = p / "wav1.wav"
    wav2 = p / "wav2.wav"
    wavfile.write(wav1, fs, s1.astype(np.int16))
    wavfile.write(wav2, fs, s2.astype(np.int16))
    return (wav1, wav2)


@pytest.fixture
def rndwav(tmp_path):
    rng = np.random.RandomState(0)
    fs = 32000
    s1 = rng.standard_normal(fs)
    s2 = np.concatenate([rng.standard_normal(fs // 2), s1])
    return to_files(fs, s1, s2, tmp_path)


def test_rnd0(rndwav):
    file, offset = file_offset(
        in1=rndwav[1]
        , in2=rndwav[0]
        , take=1.5
        , normalize=False
        , denoise=False
        , lowpass=0
        , show=False
    )
    assert offset == 0.5 and file == rndwav[1]


def test_rnd1(rndwav):
    file, offset = file_offset(
        in1=rndwav[0]
        , in2=rndwav[1]
        , take=1.5
        , normalize=False
        , denoise=False
        , lowpass=0
        , show=False
    )
    assert offset == 0.5 and file == rndwav[1]


def test_rnd00(rndwav):
    file, offset = file_offset(
        in1=rndwav[0]
        , in2=rndwav[0]
        , take=1.5
        , normalize=False
        , denoise=False
        , lowpass=0
        , show=False
    )
    assert offset == 0.0 and file == rndwav[0]


def test_rnd11(rndwav):
    file, offset = file_offset(
        in1=rndwav[1]
        , in2=rndwav[1]
        , take=1.5
        , normalize=False
        , denoise=False
        , lowpass=0
        , show=False
    )
    assert offset == 0.0 and file == rndwav[1]


test_wav_offset = 2.3113832199546485


@pytest.fixture
def tstwav(tmp_path):
    fs, s = wavfile.read('test.wav')
    lens2 = len(s) // 2
    # lens2/fs # 2.3113832199546485
    s1 = s
    s2 = np.concatenate([s1[lens2:, :], s1])
    # wavfile.write('test2.wav', fs, s2.astype(np.int16))
    # mono:
    # wavfile.write('test1.wav', fs, s[:,1].astype(np.int16))
    return to_files(fs, s1, s2, tmp_path)


def test_tst0(tstwav):
    file, offset = file_offset(
        in1=tstwav[0]
        , in2=tstwav[1]
        , show=False
    )
    assert abs(offset - test_wav_offset) < 0.001 and file == tstwav[1]


def test_tst1(tstwav):
    file, offset = file_offset(
        in1=tstwav[0]
        , in2=tstwav[1]
        , show=False
    )
    assert abs(offset - test_wav_offset) < 0.001 and file == tstwav[1]
