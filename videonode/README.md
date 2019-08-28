# Videonode

An overhead pi3 with fisheye lens running [pikrellcam](https://github.com/billw2/pikrellcam)

# Setup

0a. Install os. In _raspi-config_ enable ssh login, camera, and change hostname. 

0b. Copy ssh key:
```bash
cat ~/.ssh/id_rsa.pub | ssh pi@videonode.local 'cat >> .ssh/authorized_keys'
```

0c. Install git, avahi-daemon, clone repos:
```bash
sudo apt-get install git
sudo apt-get install netatalk
git clone https://github.com/roberttwomey/housemachine-aura
```

1. clone software: 
```bash
cd housemachine-aura/software
git clone https://github.com/billw2/pikrellcam
```

2. install:
```sh
cd pikrellcam
./install_pikrellcam.sh
```

3. Copy custom config file:
```bash
cp ~/housemachine-aura/videonode/config/* ~/.pikrellcam
```

4. Reboot
