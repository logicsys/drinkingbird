![Drinkingbird](drinkingbird.jpeg)

# 🐦 Drinkingbird

**System Activity Monitor & Keep-Alive Tool**

Drinkingbird is a lightweight Python application that monitors your system activity and prevents it from going idle by making subtle mouse movements when no user activity is detected. Perfect for keeping your status active in Teams, Slack, or other applications without manual intervention.

## ✨ Features

- 🖱️ **Real-time Activity Monitoring** - Tracks keyboard and mouse activity
- ⏰ **Configurable Idle Threshold** - Default 3 minutes, customizable
- 🎯 **Subtle Mouse Movement** - Barely noticeable 1-pixel movements
- 📊 **Live Status Display** - Shows current activity status and idle time
- 🛡️ **Smart Detection** - Filters out system noise and micro-movements
- 🔄 **Cooldown System** - Prevents excessive mouse movements
- ⏰ **Working Hours** - Restrict activity to specific time periods
- 🚫 **Clean Shutdown** - Graceful exit with Ctrl+C

## 🚀 Quick Start

### Install from Package

```bash
# Build and install the Debian package
make install

# Or build manually
make build
sudo dpkg -i drinkingbird_1.0.0_all.deb
```

### Run

```bash
drinkingbird
```

### Stop

Press `Ctrl+C` to stop the monitor.

## 📋 Requirements

- **Python 3** - Core runtime
- **pynput** - Input monitoring and control (auto-installed)
- **Linux** - Developed and tested on Linux systems

## 🛠️ Installation Methods

### Method 1: Debian Package (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd drinkingbird

# Build and install
make install
```

### Method 2: Direct Python Execution

```bash
# Install dependencies
pip3 install pynput

# Run directly
python3 drinkingbird.py
```

## 📖 Usage

### Basic Usage

```bash
# Use default 3-minute threshold
drinkingbird

# Set custom threshold (5 minutes)
drinkingbird -t 5

# Set threshold with decimal (1.5 minutes)
drinkingbird --threshold 1.5

# Set working hours (9 AM to 5 PM)
drinkingbird --start 9 --end 17

# Set precise working hours with minutes
drinkingbird --start 09:30 --end 17:30

# Combine threshold and working hours
drinkingbird -t 2 --start 8 --end 18

# Show help
drinkingbird --help

# Show version
drinkingbird --version
```

### Sample Output

```
Starting activity monitor...
Idle threshold: 5.0 minutes
Working hours: 09:00 - 17:00
✅ Currently within working hours - monitoring active
Press Ctrl+C to stop

[14:32:15] Last active: 14:32:15 (idle for 45s) Threshold: 300s Status: ACTIVE
[14:37:16] Mouse moved to prevent idle (next auto-move in 30s)
```

### Working Hours Examples

```bash
# Standard business hours
drinkingbird --start 9 --end 17

# Early bird schedule  
drinkingbird --start 7 --end 15

# Night shift (22:00 to 06:00 next day)
drinkingbird --start 22 --end 6

# Precise timing with minutes
drinkingbird --start 08:30 --end 17:45
```

### Command Line Options

```bash
drinkingbird --help
```

```
usage: drinkingbird [-h] [-t MINUTES] [-v]

Drinkingbird - System Activity Monitor & Keep-Alive Tool

options:
  -h, --help            show this help message and exit
  -t MINUTES, --threshold MINUTES
                        Idle threshold in minutes before mouse movement (default: 3.0)
  --start TIME          Working hours start time (e.g., "9", "09:00", "09:30")
  --end TIME            Working hours end time (e.g., "17", "17:00", "17:30")
  -v, --version         show program's version number and exit

Examples:
  drinkingbird                              # Default settings
  drinkingbird -t 5                        # 5-minute idle threshold
  drinkingbird --threshold 1.5             # 1.5-minute threshold
  drinkingbird --start 9 --end 17          # Work 9 AM to 5 PM
  drinkingbird --start 09:30 --end 17:30   # Work 9:30 AM to 5:30 PM
  drinkingbird -t 2 --start 8 --end 18     # 2-minute threshold, 8 AM to 6 PM

The program monitors keyboard and mouse activity and moves the mouse
slightly when idle for the specified duration to prevent system idle status.
Working hours restrict when mouse movement occurs.
Press Ctrl+C to stop the monitor.
```

### How It Works

1. **Monitors Activity**: Tracks mouse movements, clicks, scrolling, and key presses
2. **Calculates Idle Time**: Determines how long since last user activity
3. **Smart Movement**: After 3 minutes of inactivity, moves mouse 1 pixel and back
4. **Cooldown Period**: Waits 30 seconds between automatic movements
5. **Status Updates**: Shows real-time status every second

## 🔧 Building from Source

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get install dpkg-dev python3 python3-pip

# Fedora/RHEL
sudo dnf install dpkg-devel python3 python3-pip
```

### Build Commands

```bash
# Show available targets
make help

# Build package
make build

# Build and install
make install

# Clean build files
make clean

# Test installation
make test

# Uninstall
make uninstall
```

### Manual Build

```bash
# Make script executable
chmod +x build-deb.sh

# Build package
./build-deb.sh

# Install
sudo dpkg -i drinkingbird_1.0.0_all.deb
```

## ⚙️ Configuration

### Command Line Configuration

The idle threshold can be configured via command line arguments:

```bash
# Set different thresholds
drinkingbird -t 1     # 1 minute
drinkingbird -t 5     # 5 minutes  
drinkingbird -t 0.5   # 30 seconds
drinkingbird -t 10    # 10 minutes

# Working hours examples
drinkingbird --start 9 --end 17           # 9 AM to 5 PM
drinkingbird --start 08:30 --end 16:30    # 8:30 AM to 4:30 PM
drinkingbird --start 22 --end 6           # Night shift: 10 PM to 6 AM
```

### Advanced Configuration

For other settings, you can modify the source code:

- **Cooldown period**: Edit `auto_move_cooldown` in `ActivityMonitor.__init__()`
- **Mouse movement distance**: Modify the pixel offset in `move_mouse_slightly()`
- **Movement threshold**: Adjust `mouse_move_threshold` for activity detection

## 🔍 Technical Details

### Activity Detection

- **Mouse Movement**: Minimum 3-pixel threshold to filter system noise
- **Mouse Clicks**: All button presses (left, right, middle)
- **Mouse Scrolling**: Wheel scrolling in any direction
- **Keyboard**: Any key press

### Mouse Movement

- **Distance**: 1 pixel right and down, then back to original position
- **Duration**: 100ms total movement time
- **Frequency**: Maximum once every 30 seconds when idle
- **Detection**: Own movements are ignored to prevent feedback loops

### System Integration

- **Installation Path**: `/usr/bin/drinkingbird`
- **Documentation**: `/usr/share/doc/drinkingbird/`
- **Dependencies**: Automatically managed via package system
- **Process Management**: Clean shutdown and process cleanup

## 🐛 Troubleshooting

### Permission Issues

If mouse control doesn't work:

```bash
# Check if running with appropriate permissions
# Some systems may require additional setup for input control
```

### Dependencies

If `pynput` fails to install:

```bash
# Manual installation
pip3 install pynput

# Or system package (if available)
sudo apt-get install python3-pynput
```

### Process Management

To stop all running instances:

```bash
pkill -f "python.*drinkingbird"
```

## 📝 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

- **Issues**: Report bugs and feature requests via GitHub issues
- **Documentation**: Check this README and `/usr/share/doc/drinkingbird/`
- **Code**: Well-documented Python code for easy understanding

## 🎯 Use Cases

- **Remote Work**: Keep Teams/Slack status active during breaks
- **Presentations**: Prevent screen lock during long presentations  
- **Monitoring**: Avoid idle timeouts on monitoring systems
- **Development**: Prevent IDE timeouts during long compile times

---

**Note**: Use responsibly and in accordance with your organization's policies regarding activity monitoring and system automation.
