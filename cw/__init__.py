import pyaudio
import math
import struct
from cw.alphabet import CHARS

UNITS = dict(
    dit = 1,
    dah = 3,
    gap = 1,
    gap_char = 3,
    gap_word = 7,
)

class Morse(object):
    def __init__(self, speed=8, frequency=750.0, volume=0):
        self.speed = speed
        self.frequency = frequency
        self.rate = 44800
        self.sample = dict()
        self.volume = 10.0**(float(volume)/20.0) * 32767.0

        self._setup_audio()
        self._setup_wave()

    def set_frequency(self, frequency):
        self.frequency = frequency
        self._setup_wave()

    def set_speed(self, speed):
        self.speed = speed
        self._setup_save()

    def set_volume(self, volume):
        self.volume = 10.0**(float(volume)/20.0) * 32767.0
        self._setup_save()

    def _setup_audio(self):
        p = pyaudio.PyAudio()
        self.dev = p.open(
            format=pyaudio.paInt32,
            channels=1,
            rate=self.rate,
            output=True)

    def _setup_wave(self):
        omega = 2.0 * math.pi * self.frequency / self.rate
        # Period in frames
        period = 2.0 * self.rate / self.frequency

        # Lengths
        _dit_len = (60.0 * self.rate) / (50.0 * float(self.speed))
        _dit_len = int(math.floor(round(_dit_len / period) * period))
        _dah_len = (180.0 * self.rate) / (50.0 * float(self.speed))
        _dah_len = int(round(_dah_len / period) * period)

        # DIT
        self.sample['dit'] = str()
        w = 2.0 * math.pi * self.frequency / float(self.rate)
        for i in xrange(_dit_len):
            if i <= period:
                value = float(i) / period * self.volume * math.sin(omega * float(i))
            elif i >= _dit_len - period:
                value = float(_dit_len - i) / period * self.volume * math.sin(omega * float(i))
            else:
                value = self.volume * math.sin(omega * float(i))

            self.sample['dit'] += struct.pack('<h', value)
        self.sample['dit'] += struct.pack('<h', 0.0) * _dit_len

        # DAH
        self.sample['dah'] = str()
        for i in xrange(_dah_len):
            if i <= period:
                value = float(i) / period * self.volume * math.sin(omega * float(i))
            elif i >= _dah_len - period:
                value = float(_dah_len - i) / period * self.volume * math.sin(omega * float(i))
            else:
                value = self.volume * math.sin(omega * float(i))
            self.sample['dah'] += struct.pack('<h', value)
        self.sample['dah'] += struct.pack('<h', 0.0) * _dah_len

        # GAP
        self.sample['gap'] = struct.pack('<h', 0.0) * _dit_len

    def play(self, text):
        for char in text:
            char = char.upper()
            print char
            if char == ' ':
                self.gap(7)
            elif char in CHARS:
                for item in CHARS[char]:
                    if item == '.':
                        self.dit()
                        self.gap()
                    elif item == '-':
                        self.dah()
                        self.gap()

                # In between letters we have a 3 period gap
                self.gap(2)
                print

    def sine(self, units):
        for i in xrange(0, units):
            #self.dev.writeframes(self._wave)
            self.dev.write(self.wave)

    def dit(self):
        print 'dit'
        self.dev.write(self.sample['dit'])

    def dah(self):
        print 'dah'
        self.dev.write(self.sample['dah'])

    def gap(self, period=1):
        for x in xrange(period):
            print 'gap'
            self.dev.write(self.sample['gap'])

if __name__ == '__main__':
    import sys
    morse = Morse(speed=8, frequency=700)
    morse.play(' '.join(sys.argv[1:]))
