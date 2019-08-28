# Videonode

An overhead pi3 with fisheye lens running [pikrellcam](https://github.com/billw2/pikrellcam)

# Setup

0. Install os, etc. Copy ssh key:
```bash
cat ~/.ssh/id_rsa.pub | ssh pi@videonode.local 'cat >> .ssh/authorized_keys'
```

1. clone software: 
```bash
git clone https://github.com/billw2/pikrellcam
```

2. install:
```sh
cd pikrellcam
./install_pikrellcam.sh
```

3. Copy custom config file:
```bash
cp pikrellcam.conf ~/.pikrellcam
```

4. Reboot
