#!/bin/bash

export PYTHONPATH=src-gen/python
python scripts/send_via_udp.py --count=3
