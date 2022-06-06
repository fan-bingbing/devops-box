#!/bin/bash

sudo sysctl -w net.core.wmem_max=2500000

python run.py
