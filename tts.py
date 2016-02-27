# make sure to Brew install easyspeak

import subprocess

def espeak(a):
    subprocess.call(['espeak', "-s", "100", a])
