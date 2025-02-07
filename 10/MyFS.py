#!/usr/bin/env python3

# 2110352 Operating System
# FUSE/Filesystem exercise
# By Krerk Piromsopa, Ph.D. <Krerk.P@chula.ac.th>
#    Department of Computer Engineering
#    Chulalongkorn University.

import os
import stat
import errno
import fuse
import requests

from fuse import Fuse

fuse.fuse_python_api = (0, 2)

PARTICIPATION_URL = "https://mis.cp.eng.chula.ac.th/krerk/teaching/2022s2-os/status.php"
CHECKIN_URL = "https://mis.cp.eng.chula.ac.th/krerk/teaching/2022s2-os/checkIn.php"


class MyStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0


class WebServiceFS(Fuse):
    def getattr(self, path):
        st = MyStat()
        if path == "/":
            st.st_mode = stat.S_IFDIR | 0o755
            st.st_nlink = 2
        elif path == "/participation":
            st.st_mode = stat.S_IFREG | 0o666  # Read and write
            content = self.myRead()
            st.st_nlink = 1
            st.st_size = len(content)
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path, offset):
        for entry in [".", "..", "participation"]:
            yield fuse.Direntry(entry)

    def open(self, path, flags):
        if path != "/participation":
            return -errno.ENOENT
        return 0

    def read(self, path, size, offset):
        if path != "/participation":
            return -errno.ENOENT

        content = self.myRead()
        slen = len(content)

        if offset < slen:
            if offset + size > slen:
                size = slen - offset
            buf = content[offset : offset + size]
        else:
            buf = b""
        return buf

    def write(self, path, buf, offset):
        if path != "/participation":
            return -errno.ENOENT

        written = self.myWrite(buf.decode("utf-8"))
        return written

    def myRead(self):
        req = requests.get(PARTICIPATION_URL)
        return req.text.encode("utf-8")

    def myWrite(self, buf):
        raw = buf.strip().split(":")
        if len(raw) != 3:
            return -errno.EINVAL  # Invalid argument

        params = {"studentid": raw[0], "name": raw[1], "email": raw[2]}
        requests.post(CHECKIN_URL, data=params)
        return len(buf)


def main():
    usage = "WebService Filesystem" + Fuse.fusage
    server = WebServiceFS(
        version="WebServiceFS 1.0", usage=usage, dash_s_do="setsingle"
    )
    server.parse(errex=1)
    server.main()


if __name__ == "__main__":
    main()
