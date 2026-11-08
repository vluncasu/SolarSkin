#!/bin/zsh
set -e
cd -- "$(dirname -- "$0")"
if ! command -v pio >/dev/null; then
  print 'Install PlatformIO Core and try again.'
  exit 1
fi
print 'Building and flashing. Connect one ESP32 over USB.'
pio run -j 1 -t upload
