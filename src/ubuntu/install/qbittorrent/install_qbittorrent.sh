#!/usr/bin/env bash
set -ex

# Install Qbittorrent
if [ "$DISTRO" = "alpine" ]; then
  apk add --no-cache qbittorrent
else
  apt-get update
  apt-get install -y software-properties-common
  add-apt-repository -y ppa:qbittorrent-team/qbittorrent-stable
  apt-get update
  apt-get install -y qbittorrent
fi

# Default settings and desktop icon
mkdir -p $HOME/.config/qBittorrent
cp /dockerstartup/install/qbittorrent/qBittorrent.conf $HOME/.config/qBittorrent || true
if [ -f /usr/share/applications/org.qbittorrent.qBittorrent.desktop ]; then
  cp /usr/share/applications/org.qbittorrent.qBittorrent.desktop $HOME/Desktop/
  chmod +x $HOME/Desktop/org.qbittorrent.qBittorrent.desktop
elif [ -f /usr/share/applications/qbittorrent.desktop ]; then
  cp /usr/share/applications/qbittorrent.desktop $HOME/Desktop/
  chmod +x $HOME/Desktop/qbittorrent.desktop
fi

# Cleanup for app layer
chown -R 1000:0 $HOME
find /usr/share/ -name "icon-theme.cache" -exec rm -f {} \; || true
if [ -z ${SKIP_CLEAN+x} ]; then
  if [ "$DISTRO" = "alpine" ]; then
    rm -rf /var/cache/apk/*
  else
    apt-get autoclean
    rm -rf \
      /var/lib/apt/lists/* \
      /var/tmp/* \
      /tmp/*
  fi
fi
