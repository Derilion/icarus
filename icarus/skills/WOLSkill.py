from icarus.skills.SuperSkill import SuperSkill
import socket


class WOLSkill(SuperSkill):

    id = 'WOLSkill'
    name = "WakeOnLan Skill"
    version = "1.0"
    creator = "Derilion"
    tokens = ['lan', 'wake', 'wol']
    phrases = ["Start my Computer"]

    _response = "I am starting your computer"
    _broadcast_address = ['192.168.178.255']
    _wol_port = 9
    _ethernet_address = '00:11:32:6e:96:72'

    def main(self, message):
        try:
            self._wake_on_lan()
            message.send(self._response)
        except ValueError:
            message.send("Could not send message")

    def _wake_on_lan(self):

        mac_address = self.get_config('mac address')
        broadcast_address = self.get_config('broadcast range')
        port = int(self.get_config('port'))

        if port == '':
            port = 9

        if len(mac_address) == 17:
            sep = mac_address[2]
            mac_address = mac_address.replace(sep, "")
        elif len(mac_address) != 12:
            raise ValueError("Incorrect MAC address format")

        msg = bytes.fromhex("F" * 12 + mac_address * 16)

        # Send packet to broadcast address using configured port

        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # for i in broadcast_address:
        # old implementation for set of networks, could also use 255.255.255.255 in general
        soc.sendto(msg, (broadcast_address, port))
        soc.close()
