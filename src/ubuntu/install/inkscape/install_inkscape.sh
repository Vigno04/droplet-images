#!/usr/bin/env bash
set -ex

# Install Inkscape
if [ "$DISTRO" = "alpine" ]; then
  apk add --no-cache inkscape
else
  apt-get update
  apt-get install -y software-properties-common
  add-apt-repository -y ppa:inkscape.dev/stable
  apt-get update
  apt-get install -y inkscape
fi

# Default settings and desktop icon
if [ -f /usr/share/applications/org.inkscape.Inkscape.desktop ]; then
  cp /usr/share/applications/org.inkscape.Inkscape.desktop $HOME/Desktop/
  chmod +x $HOME/Desktop/org.inkscape.Inkscape.desktop
elif [ -f /usr/share/applications/inkscape.desktop ]; then
  cp /usr/share/applications/inkscape.desktop $HOME/Desktop/
  chmod +x $HOME/Desktop/inkscape.desktop
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
