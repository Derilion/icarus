from icarus.skills.SuperSkill import SuperSkill
from mpris2 import get_players_uri
from mpris2 import Player
from dbus.mainloop.glib import DBusGMainLoop


class MPRISMusicPlayer(SuperSkill):

    id = 'Music Player'
    name = "Music Skill"
    version = "1.0"
    creator = "columbarius"
    tokens = ['player', "music", "audio"]
    phrases = ["Toggle music", "Play audio", "Next track"]

    _response = "Music {}"
    _actions = [["play", 1], ["pause", 2], ["toggle", 3], ["next", 4], ["previous", 5], ["info", 6]]

    def main(self, message):
        action = 0
        DBusGMainLoop(set_as_default=True)

        for unit in self._actions:
            if unit[0] in message.tokens:
                action = unit[1]
        if action == 0:
            message.run_next_skill()
            return
        uri = next(get_players_uri())
        player = Player(dbus_interface_info={'dbus_uri': uri})
        if action == 1:
            player.Play()
        elif action == 2:
            player.Pause()
        elif action == 3:
            player.PlayPause()
        elif action == 4:
            player.Next()
        elif action == 5:
            player.Previous()
        elif action == 6:
            message.send(player.Metadata)

        message.send("Action accomplished")

