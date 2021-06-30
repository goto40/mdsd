import click
from big_example.Polygon import Polygon
from mdsd.item.printto import printto
from mdsd.item.io import copy_to_mem, count_bytes
import sys
import socket

@click.command()
@click.option('--count', default=1, help='Number of messages.')
@click.option('--host', default='224.0.0.1')
@click.option('--port', type=int, default='50000')
def send_via_udp(count, host, port):
    """Simple program that send data for a total of COUNT times."""

    MULTICAST_TTL = 2
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

    for x in range(count):
        data = Polygon()
        data.p[2].x=1.2
        data.p[2].y=3.4
        n = count_bytes(data)
        click.echo(f"send {x}: {n} bytes...")
        #printto(data, sys.stdout)
        b = bytearray(n)
        m = copy_to_mem(data, b)
        assert(n==m)
        #print(b)

        sock.sendto(b, (host, port))

if __name__ == '__main__':
    send_via_udp()