# Tracker
Overhead tracking software running headless on pi3. Video files are saved and played with omxplayer. 

# Setup

0a. Install os. In _raspi-config_ enable ssh login, camera, and change hostname. 

0b. Copy ssh key:
```bash
cat ~/.ssh/id_rsa.pub | ssh pi@tracker.local 'cat >> .ssh/authorized_keys'
```

0c. Install git, avahi-daemon, clone repos:
```bash
sudo apt-get install git
sudo apt-get install netatalk
git clone https://github.com/roberttwomey/housemachine-aura
ln -s housemachine-aura housmachine
```

# Install Opencv

Following [these instructions](https://raspberrypi.stackexchange.com/questions/95982/how-to-install-opencv-on-raspbian-stretch)

_Update and Install Requirements_

```bash
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install build-essential cmake unzip pkg-config
sudo apt-get -y install libjpeg-dev libpng-dev libtiff-dev
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get -y install libxvidcore-dev libx264-dev
sudo apt-get -y install libgtk-3-dev
sudo apt-get -y install libcanberra-gtk*
sudo apt-get -y install libatlas-base-dev gfortran
sudo apt-get -y install python3-dev
```

_Download OpenCV Source_

```bash
cd ~
sudo rm -r -f opencv
git clone https://github.com/opencv/opencv.git
sudo rm -r -f opencv_contrib
git clone https://github.com/Itseez/opencv_contrib.git
```

_Install numpy_

```bash
sudo apt-get install python3-pip
pip3 install numpy
```

_Build OpenCV_

```bash
cd ~/opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..

make -j3
sudo make install
sudo ldconfig
```
