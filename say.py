import subprocess
# reads out output
def say(string):
    subprocess.call(['say', string])
