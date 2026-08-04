#!/usr/bin/env bash
set -ex

# Install Deluge
if [ "$DISTRO" = "alpine" ]; then
  apk add --no-cache deluge
else
  apt-get update
  apt-get install -y deluge
fi

# Desktop Icon
cp /usr/share/applications/deluge*.desktop $HOME/Desktop/ || true
chmod +x $HOME/Desktop/deluge*.desktop || true

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
