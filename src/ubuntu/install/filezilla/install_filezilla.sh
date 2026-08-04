#!/usr/bin/env bash
set -ex

# Install Filezilla
if [ "$DISTRO" = "alpine" ]; then
  apk add --no-cache filezilla
else
  apt-get update
  apt-get install -y filezilla
  rm -rf \
    /var/lib/apt/lists/* \
    /var/tmp/*
fi

# Default settings and desktop icon
mkdir -p $HOME/.config/filezilla
cp /dockerstartup/install/filezilla/filezilla.xml $HOME/.config/filezilla
# Alpine might have it named org.filezillaproject.Filezilla.desktop or similar, or just filezilla.desktop
if [ "$DISTRO" = "alpine" ]; then
  cp /usr/share/applications/*.desktop $HOME/Desktop/ || true
else
  cp /usr/share/applications/filezilla.desktop $HOME/Desktop/
fi
chmod +x $HOME/Desktop/*.desktop || true

# Cleanup for app layer
chown -R 1000:0 $HOME
find /usr/share/ -name "icon-theme.cache" -exec rm -f {} \;
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
