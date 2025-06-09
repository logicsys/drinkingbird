#!/bin/bash

# Build script for creating a Debian package for drinkingbird
# This script creates a .deb package that installs drinkingbird as a system command

set -e

# Package information
PACKAGE_NAME="drinkingbird"
VERSION="1.0.2"
ARCHITECTURE="all"
MAINTAINER="User <user@example.com>"
DESCRIPTION="System activity monitor that prevents idle status by moving mouse"

# Directories
BUILD_DIR="build"
PACKAGE_DIR="${BUILD_DIR}/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}"
DEBIAN_DIR="${PACKAGE_DIR}/DEBIAN"
BIN_DIR="${PACKAGE_DIR}/usr/bin"
DOC_DIR="${PACKAGE_DIR}/usr/share/doc/${PACKAGE_NAME}"

echo "Building Debian package for ${PACKAGE_NAME} v${VERSION}..."

# Clean previous build
if [ -d "$BUILD_DIR" ]; then
    echo "Cleaning previous build..."
    rm -rf "$BUILD_DIR"
fi

# Create directory structure
echo "Creating package directory structure..."
mkdir -p "$DEBIAN_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DOC_DIR"

# Copy the main script to /usr/bin/
echo "Copying drinkingbird script..."
cp drinkingbird.py "$BIN_DIR/drinkingbird"
chmod +x "$BIN_DIR/drinkingbird"

# Create control file
echo "Creating control file..."
cat > "$DEBIAN_DIR/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Architecture: $ARCHITECTURE
Maintainer: $MAINTAINER
Depends: python3, python3-pip, python3-pynput
Description: $DESCRIPTION
 Drinkingbird is a system activity monitor that tracks keyboard and mouse
 activity. When the system is idle for more than 3 minutes, it automatically
 moves the mouse slightly to prevent idle status in applications like Teams,
 Slack, etc. The movement is minimal and barely noticeable.
 .
 Features:
  - Real-time activity monitoring
  - Configurable idle threshold (default: 3 minutes)
  - Subtle mouse movement to prevent idle
  - Live status display
  - Clean shutdown with Ctrl+C
EOF

# Create postinst script (runs after package installation)
echo "Creating post-installation script..."
cat > "$DEBIAN_DIR/postinst" << 'EOF'
#!/bin/bash
set -e

echo "Installing Python dependencies for drinkingbird..."
pip3 install pynput >/dev/null 2>&1 || {
    echo "Warning: Could not install pynput automatically."
    echo "Please run: pip3 install pynput"
}

echo "Drinkingbird installed successfully!"
echo "Run 'drinkingbird' to start the activity monitor."
echo "Use Ctrl+C to stop the monitor."

exit 0
EOF

chmod +x "$DEBIAN_DIR/postinst"

# Create prerm script (runs before package removal)
echo "Creating pre-removal script..."
cat > "$DEBIAN_DIR/prerm" << 'EOF'
#!/bin/bash
set -e

echo "Removing drinkingbird..."
# Kill any running drinkingbird processes
pkill -f "python.*drinkingbird" 2>/dev/null || true

exit 0
EOF

chmod +x "$DEBIAN_DIR/prerm"

# Create copyright file
echo "Creating copyright file..."
cat > "$DOC_DIR/copyright" << EOF
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: drinkingbird
Source: https://github.com/user/drinkingbird

Files: *
Copyright: $(date +%Y) User
License: MIT
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 .
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 .
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
EOF

# Create changelog
echo "Creating changelog..."
cat > "$DOC_DIR/changelog" << EOF
drinkingbird (${VERSION}) unstable; urgency=low

  * Initial release
  * System activity monitoring
  * Automatic mouse movement to prevent idle
  * Configurable idle threshold
  * Real-time status display

 -- $MAINTAINER  $(date -R)
EOF

# Compress changelog
gzip -9 "$DOC_DIR/changelog"

# Create README
echo "Creating README..."
cat > "$DOC_DIR/README" << 'EOF'
Drinkingbird - System Activity Monitor
======================================

Drinkingbird monitors your system activity and prevents it from going idle
by making subtle mouse movements when no activity is detected for a specified
period (default: 3 minutes).

Usage:
    drinkingbird                    # Start with 3-minute threshold
    
The program will display real-time status showing:
- Current time
- Last activity time
- Idle duration
- Threshold setting

Press Ctrl+C to stop the monitor.

Requirements:
- Python 3
- pynput library (automatically installed)

The mouse movements are minimal (1 pixel) and return to the original position,
making them virtually unnoticeable while effectively preventing idle status.
EOF

# Build the package
echo "Building Debian package..."
dpkg-deb --build "$PACKAGE_DIR"

# Move the package to current directory
mv "${PACKAGE_DIR}.deb" "./${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb"

echo ""
echo "✅ Package built successfully!"
echo "📦 Package: ${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb"
echo ""
echo "To install:"
echo "  sudo dpkg -i ${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb"
echo ""
echo "To uninstall:"
echo "  sudo dpkg -r ${PACKAGE_NAME}"
echo ""
echo "To run after installation:"
echo "  drinkingbird" 