#!/bin/bash
Xvfb :0 -screen 0 1024x768x16 &
exec "$@"