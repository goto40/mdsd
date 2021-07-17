import click
from big_example.OnOff import OnOff
from big_example.ABC import ABC
from big_example.MultiMessage import MultiMessage
from big_example.TypeSelector import TypeSelector
from mdsd.item.printto import printto
from mdsd.item.io import copy_to_mem, count_bytes
from mdsd.item_support import adjust_array_sizes_and_variants,set_length_field
import numpy as np
import sys
import socket

@click.command()
@click.option('--count', default=1, help='Number of messages.')
@click.option('--host', default='224.0.0.1')
@click.option('--port', type=int, default='60000')
def send_via_udp(count, host, port):
    """Simple program that send data for a total of COUNT times."""

    MULTICAST_TTL = 2
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

    for x in range(count):
        data = MultiMessage()
        if x%3==0:
            data.header.id = TypeSelector.POLY
            adjust_array_sizes_and_variants(data)
            data.code=np.int32(-99)
            data.onoff[0]=OnOff.ON
            data.onoff[1]=OnOff.OFF
            data.onoff[2]=OnOff.OFF
            data.onoff[3]=OnOff.ON
            data.onoff[4]=OnOff.ON
            data.onoff[5]=OnOff.ON
            data.abc=ABC.C
            data.payload.n=3+x
            adjust_array_sizes_and_variants(data)
            for p in range(data.payload.n):
                data.payload.p[p].x=  p+0.99
                data.payload.p[p].y= -p-.33
        elif x%3==1:
            data.header.id = TypeSelector.POINT
            adjust_array_sizes_and_variants(data)
            data.code=np.int32(100+x)
            data.payload.x=1
            data.payload.y=2
        else:
            data.header.id = TypeSelector.TRIANGLE
            data.code=np.int32(100+x)
            adjust_array_sizes_and_variants(data)

        set_length_field(data)
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
