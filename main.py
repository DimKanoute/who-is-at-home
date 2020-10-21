import machine
import network
import uctypes
import urandom
import uselect
import usocket
import ustruct
import utime

# Define Users, IP's and LED's

# this is an example

config = {
    "user1": {
        "ip": "192.168.2.76",
        "led": machine.Pin(18, machine.Pin.OUT)
    },
    "user2": {
        "ip": "192.168.2.2",
        "led": machine.Pin(2, machine.Pin.OUT)
    },
}

# Network settings
ssid = "your_wifi_ssid"
password = "your_wifi_password"


def checksum(data):
    if len(data) & 0x1:  # Odd number of bytes
        data += b'\0'
    cs = 0
    for pos in range(0, len(data), 2):
        b1 = data[pos]
        b2 = data[pos + 1]
        cs += (b1 << 8) + b2
    while cs >= 0x10000:
        cs = (cs & 0xffff) + (cs >> 16)
    cs = ~cs & 0xffff
    return cs


def ping(host, count=4, timeout=7000, interval=10, quiet=False, size=32):
    # prepare packet
    assert size >= 16, "pkt size too small"
    pkt = b'Q' * size
    pkt_desc = {
        "type": uctypes.UINT8 | 0,
        "code": uctypes.UINT8 | 1,
        "checksum": uctypes.UINT16 | 2,
        "id": uctypes.UINT16 | 4,
        "seq": uctypes.INT16 | 6,
        "timestamp": uctypes.UINT64 | 8,
    }

    #packet header descriptor
    h = uctypes.struct(uctypes.addressof(pkt), pkt_desc, uctypes.BIG_ENDIAN)
    h.type = 8  # ICMP_ECHO_REQUEST
    h.code = 0
    h.checksum = 0
    h.id = urandom.randomint(0, 65355)
    h.seq = 1

    # init socket
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_RAW, 1)
    sock.setblocking(0)
    sock.settimeout(timeout / 1000)
    addr = usocket.getaddrinfo(config[host]["ip"], 1)[0][-1][0]  # ip address
    sock.connect((addr, 1))
    not quiet and print("PING %s (%s): %u data bytes" % (config[host]["ip"], addr, len(pkt)))

    seqs = list(range(1, count + 1))  # [1,2,...,count]
    c = 1
    t = 0
    n_trans = 0
    n_recv = 0
    finish = False
    while t < timeout:
        if t == interval and c <= count:
            # send packet
            h.checksum = 0
            h.seq = c
            h.timestamp = utime.ticks_us()
            h.checksum = checksum(pkt)
            if sock.send(pkt) == size:
                n_trans += 1
                t = 0  # reset timeout
            else:
                seqs.remove(c)
            c += 1

        # recv packet
        while 1:
            socks, _, _ = uselect.select([sock], [], [], 0)
            if socks:
                resp = socks[0].recv(4096)
                resp_mv = memoryview(resp)
                h2 = uctypes.struct(uctypes.addressof(resp_mv[20:]), pkt_desc, uctypes.BIG_ENDIAN)

                # TODO: validate checksum (optional)
                seq = h2.seq
                if h2.type == 0 and h2.id == h.id and (seq in seqs):  # 0: ICMP_ECHO_REPLY
                    t_elasped = (utime.ticks_us() - h2.timestamp) / 1000
                    ttl = ustruct.unpack('!B', resp_mv[8:9])[0]  # time-to-live
                    n_recv += 1
                    not quiet and print(
                        "%u bytes from %s: icmp_seq=%u, ttl=%u, time=%f ms" % (len(resp), addr, seq, ttl, t_elasped))
                    seqs.remove(seq)
                    if len(seqs) == 0:
                        finish = True
                        break
            else:
                break

        if finish:
            break

        utime.sleep_ms(1)
        t += 1

    # close
    sock.close()
    ret = (n_trans, n_recv)
    not quiet and print("%u packets transmitted, %u packets received" % (n_trans, n_recv))

    return n_trans, n_recv


def check_if_connected(send, receive, host):
    print("enter: ")
    print(send)
    print(receive)
    if send == receive or receive == 3:
        print("Phone is connected")
        config[host]["led"].value(1)

    else:
        print("Phone is not connected")
        config[host]["led"].value(0)


def connect_to_wifi(wifi_ssid, wifi_password):

    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(wifi_ssid, wifi_password)
        while not sta_if.isconnected():
            pass

    print('Network Config:', sta_if.ifconfig())

    while sta_if.isconnected():

        # Display connection details
        print("Connected!")
        print("My IP Address:", sta_if.ifconfig()[0])

        utime.sleep_ms(5000)

        for key in config:
            print('I ping ' + key + " :")
            if config[key]['ip']:
                n_trans, n_recv = ping(host=key)
                check_if_connected(n_trans, n_recv, key)
                utime.sleep_ms(5000)

        utime.sleep(50000) # ping every 5 minutes

    # If we lose connection, repeat this main.py and retry for a connection
    print("Connection lost. Trying again...")
    main()


def main():
    connect_to_wifi(ssid, password)


main()

