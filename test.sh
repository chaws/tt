#!/bin/bash

set -xe

# TODO: add ability to run single tests
env python3 -m unittest tests
