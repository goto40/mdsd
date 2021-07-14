#!/bin/bash

export PYTHONPATH=src-gen/python
python scripts/send_via_udp2.py --count=3
#python scripts/send_via_udp.py --count=3

