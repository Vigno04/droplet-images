#!/usr/bin/env bash
set -ex

# Configure Openbox to run in single-application mode:
# - Remove all window decorations (title bars) to prevent dragging
# - Force all windows to open maximized
# - This is the equivalent of the old XFCE single-application config for Ubuntu Noble (24.04+)

OPENBOX_RC="/etc/xdg/openbox/rc.xml"

if [ -f "$OPENBOX_RC" ]; then
    # Inject an <application> rule that matches all windows (class="*")
    # and forces no decorations + maximized state
    sed -i 's|</applications>|    <application class="*">\n        <decor>no</decor>\n        <maximized>yes</maximized>\n    </application>\n</applications>|' "$OPENBOX_RC"
    echo "Openbox single-application rules applied to $OPENBOX_RC"
else
    echo "WARNING: Openbox rc.xml not found at $OPENBOX_RC, skipping."
fi

cat >/usr/bin/desktop_ready <<'EOL'
#!/usr/bin/env bash
if [ -z ${START_DE+x} ]; then
  START_DE="xfce4-session"
fi
until pids=$(pidof ${START_DE}); do sleep .5; done
EOL
chmod +x /usr/bin/desktop_ready
