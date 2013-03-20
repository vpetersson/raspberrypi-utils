"""
This script detects a Raspberry Pi's model, manufacturer and mb ram, based
on the cpu revision number. Data source:
http://www.raspberrypi.org/phpBB3/viewtopic.php?f=63&t=32733

You can instantiate the ModelInfo class either with a parameter `rev_hex`
(eg. `m = ModelInfo("000f")`), or without a parameter
(eg. `m = ModelInfo()`) in which case it will try to detect it via
`/proc/cpuinfo`. Accessible attributes:

    class ModelInfo:
        model = ''     # 'A' or 'B'
        revision = ''  # '1.0' or '2.0'
        ram_mb = 0     # integer value representing ram in mb
        vendor = ''    # manufacturer (eg. 'Qisda')
        info = ''      # additional info (eg. 'D14' removed)

Author: Chris Hager <chris@linuxuser.at>
License: MIT
URL: https://github.com/metachris/raspberrypi-utils
"""
import re
import json
import sys

model_data = {
    '2': ('B', '1.0', 256, '?', ''),
    '3': ('B', '1.0', 256, '?', 'Fuses mod and D14 removed'),
    '4': ('B', '2.0', 256, 'Sony', ''),
    '5': ('B', '2.0', 256, 'Qisda', ''),
    '6': ('B', '2.0', 256, 'Egoman', ''),
    '7': ('A', '2.0', 256, 'Egoman', ''),
    '8': ('A', '2.0', 256, 'Sony', ''),
    '9': ('A', '2.0', 256, 'Qisda', ''),
    'd': ('B', '2.0', 512, 'Egoman', ''),
    'e': ('B', '2.0', 512, 'Sony', ''),
    'f': ('B', '2.0', 512, 'Qisda', '')
}


class ModelInfo(object):
    """
    You can instantiate ModelInfo either with a parameter `rev_hex`
    (eg. `m = ModelInfo("000f")`), or without a parameter
    (eg. `m = ModelInfo()`) in which case it will try to detect it via
    `/proc/cpuinfo`
    """
    model = ''
    revision = ''
    ram_mb = 0
    vendor = ''
    info = ''
    serial = ''

    def __init__(self, rev_hex=None):
        if not rev_hex:
            with open("/proc/cpuinfo") as f:
                cpuinfo = f.read()
            rev_hex = re.search(r"(?<=\nRevision)[ |:|\t]*(\w+)", cpuinfo).group(1)
            self.serial = re.search(r"(?<=\nSerial)[ |:|\t]*(\w+)", cpuinfo).group(1)

        self.revision_hex = rev_hex[-4:] if rev_hex[:4] == "1000" else rev_hex
        self.model, self.revision, self.ram_mb, self.vendor, self.info = model_data[rev_hex.strip("0")]

    def as_json(self):
        s = {'model': self.model, 'revision': self.revision, 'ram': self.ram_mb, 'vendor': self.vendor, 'serial': self.serial}
        return s

    def __repr__(self):
        s = "%s: Serial: %s, Model %s, Revision %s, RAM: %s MB, Maker: %s%s" % (self.revision_hex, self.serial, self.model, self.revision, self.ram_mb, self.vendor, ", %s" % self.info if self.info else "")
        return s


if __name__ == "__main__":
    m = ModelInfo()

    if len(sys.argv) == 2:
        if sys.argv[1] == '--json':
            print json.dumps(m.as_json(), sort_keys=True, indent=4, separators=(',', ': '))
    else:
        print(m)
