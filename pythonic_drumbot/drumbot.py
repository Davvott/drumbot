"""Drumbot v1.1"""
import requests
import random
URL = "https://api.noopschallenge.com/drumbot/patterns"

class DrumBot:
    """Everything a DrumBot needs.
    Random pattern chosen from DrumBot for DrumBot
    Brought to you by: DrumBot"""

    def __init__(self):

        self.patterns = [pattern['name'] for pattern in self.fetch_patterns()]
        self.pattern = random.choice(self.patterns)
        self.info = self.get_drumbot_pattern()
        self.step_count = self.info['stepCount']
        self.bpm = self.info['beatsPerMinute']
        self.sleep_time = 15 / self.bpm
        self.tracks = [Track(track) for track in self.info['tracks']]

    def __str__(self):
        return "Name: {}, BPM: {}, step: {}, tracks: {}".format(self.pattern, self.bpm, self.step_count,
                                                       [track.__str__() for track in self.tracks])

    def key_change(self):
        """Reset Drumbot pattern"""
        self.pattern = random.choice(self.patterns)
        self.info = self.get_drumbot_pattern()
        self.step_count = self.info['stepCount']
        self.bpm = self.info['beatsPerMinute']
        self.sleep_time = 15 / self.bpm
        self.tracks = [Track(track) for track in self.info['tracks']]

    @staticmethod
    def fetch_patterns():
        req = requests.get(URL)
        result = req.json()
        return result

    def get_drumbot_pattern(self):
        req = requests.get(URL + "/{}".format(self.pattern))
        result = req.json()
        return result


class Track:
    """Keepin' track of the Tracks"""
    def __init__(self, track_dict):
        self.name = track_dict['instrument']
        self.beat = track_dict['steps']

    def __str__(self):
        return "{}, {}".format(self.name, self.beat)


if __name__ == '__main__':
    drumbot = DrumBot()
    print(drumbot)
