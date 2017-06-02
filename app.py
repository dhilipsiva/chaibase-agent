#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: app.py
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2017-06-01
"""

from time import time
from json import dumps
from itertools import cycle
from fake_data import fake_data
from flask import Flask, request
from serial.tools.list_ports import comports
from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE

app = Flask(__name__)

fake_cycle = cycle(fake_data)


def _get_float(request, param):
    """
    Get float value
    """
    val = request.args.get("param")
    if val:
        return float(val)


def _port_info_serializer(port_info):
    """
    Serialize port info
    """
    return dict(
        device=port_info.device, name=port_info.name, hwid=port_info.hwid,
        description=port_info.description, manufacturer=port_info.manufacturer,
        vid=port_info.vid, pid=port_info.pid, product=port_info.product,
        serial_number=port_info.serial_number, location=port_info.location,
        interface=port_info.interface,
    )


@app.route('/')
def serial_ports():
    """
    Lists serial port names
    """
    ports = [_port_info_serializer(port_info) for port_info in comports()]
    return dumps({"ports": ports})


@app.route('/ping')
def ping():
    """
    Health Check
    """
    return "pong"


@app.route('/read')
def read():
    """
    Read a data from serial port
    """
    kwargs = dict(
        port=request.args.get("port", None),
        baudrate=int(request.args.get("baudrate", 9600)),
        bytesize=int(request.args.get("bytesize", EIGHTBITS)),
        parity=request.args.get("parity", PARITY_NONE),
        stopbits=int(request.args.get("stopbits", STOPBITS_ONE)),
        timeout=_get_float(request, "timeout"),
        xonxoff=request.args.get("xonxoff") == "true",
        rtscts=request.args.get("rtscts") == "true",
        write_timeout=_get_float(request, "write_timeout"),
        dsrdtr=request.args.get("dsrdtr") == "true",
        inter_byte_timeout=_get_float(request, "inter_byte_timeout"),
    )
    with Serial(**kwargs) as ser:
        return ser.readline()


@app.route('/fake')
def fake():
    """
    Fake reading from serial port
    """
    return "%s" % next(fake_cycle)


def generate_fake_data():
    """
    docstring for generate_fake_data
    """
    f = open("fake-data.txt", "w")
    with Serial(port='COM3', timeout=1, baudrate=9600) as ser:
        f.write("%n:%n\n" % time(), ser.readline())


# uncomment `generate_fake_data` call to log data to testing purpose
# generate_fake_data()
app.run()
