#!/bin/bash
echo "Installing required dependencies. This may take some time (10-20 minutes-ish)..."
sudo apt-get update && sudo apt-get install python3-dev python3-pip python3-pillow libxml2-dev libxslt-dev -y
sudo pip3 install pytz tzlocal requests
echo "Running rgbmatrix installation..."
mkdir submodules
cd submodules
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git matrix
cd matrix
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
echo "If you didn't see any errors above, everything should be installed!"
echo "Installation complete! Play around with the examples in matrix/bindings/python/samples to make sure your matrix is working."