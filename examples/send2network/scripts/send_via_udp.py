import click
from big_example.Polygon import Polygon
from mdsd.item.printto import printto
from mdsd.item.io import copy_to_mem, count_bytes
from mdsd.item_support import adjust_array_sizes_and_variants
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
        data.n=3+x
        adjust_array_sizes_and_variants(data)
        for p in range(data.n):
            data.p[p].x=  p+0.99
            data.p[p].y= -p-.33
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