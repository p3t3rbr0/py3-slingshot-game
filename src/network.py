import socket
import sys

try:
    import cPickle as pickle
except:
    import pickle


class Network:
    def __init__(self, port, buf_size=4096):
        self.port = port
        self.buf_size = buf_size

    def wait_for_cnct(self):
        try:
            for res in socket.getaddrinfo(
                None,
                self.port,
                socket.AF_UNSPEC,
                socket.SOCK_STREAM,
                0,
                socket.AI_PASSIVE,
            ):
                af, socktype, proto, canonname, sa = res
                try:
                    connect_s = socket.socket(af, socktype, proto)
                except socket.error as msg:
                    connect_s = None
                    continue
                try:
                    connect_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    connect_s.bind(sa)
                    connect_s.listen(1)
                    connect_s.settimeout(2)
                except socket.error as msg:
                    connect_s.close()
                    connect_s = None
                    continue
                break
        except socket.error as msg:
            connect_s = None

        if connect_s is None:
            print(msg)
            return False

        try:
            (self.s, self.addr) = connect_s.accept()
            self.w_stream = self.s.makefile("wb")
            self.r_stream = self.s.makefile("rb")
            connect_s.close()
        except:
            connect_s.close()
            return -1

    def cnct(self, hostname):
        try:
            for res in socket.getaddrinfo(
                hostname, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM
            ):
                af, socktype, proto, canonname, sa = res
                try:
                    self.s = socket.socket(af, socktype, proto)
                except socket.error as msg:
                    self.s = None
                    continue
                try:
                    self.s.settimeout(3)
                    self.s.connect(sa)
                except socket.error as msg:
                    self.s.close()
                    self.s = None
                    continue
                break
        except socket.error as msg:
            self.s = None

        msg = ""
        if self.s is None:
            print(msg)
            return False
        else:
            self.s.settimeout(None)
            self.w_stream = self.s.makefile("wb")
            self.r_stream = self.s.makefile("rb")

    def send(self, data):
        #       print(data)
        try:
            pickle.dump(data, self.w_stream, 1)
            self.w_stream.flush()
        except:
            return False

    def recv(self):
        try:
            data = pickle.load(self.r_stream)
            #            print(data)
            return data
        except:
            return False

    def close(self):
        try:
            self.r_stream.close()
        except:
            pass
        try:
            self.w_stream.close()
        except:
            pass
        try:
            self.s.close()
        except:
            pass

    def __del__(self):
        self.close()
