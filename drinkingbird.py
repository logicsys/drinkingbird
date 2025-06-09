#!/usr/bin/env python3
"""
System Activity Monitor and Keep-Alive Script

This script monitors keyboard and mouse activity, displays when the user was last active,
and automatically moves the mouse slightly if there's no activity for 3 minutes.
"""

import time
import threading
from datetime import datetime, timedelta
from pynput import mouse, keyboard
from pynput.mouse import Button, Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import sys
import os
import argparse

class ActivityMonitor:
    def __init__(self, idle_threshold_minutes=3, start_time=None, end_time=None):
        self.last_activity = datetime.now()
        self.idle_threshold = timedelta(minutes=idle_threshold_minutes)
        self.running = True
        self.mouse_controller = mouse.Controller()
        self.ignore_next_mouse_move = False
        self.last_mouse_pos = self.mouse_controller.position
        self.mouse_move_threshold = 3  # Minimum pixels to consider as intentional movement
        self.last_auto_move = None  # Track when we last moved the mouse automatically
        self.auto_move_cooldown = timedelta(seconds=30)  # Wait 30 seconds between auto moves
        self.start_time = start_time  # Working hours start time
        self.end_time = end_time      # Working hours end time
        
    def on_mouse_move(self, x, y):
        """Called when mouse moves"""
        # Ignore if this is our automated mouse movement
        if self.ignore_next_mouse_move:
            self.ignore_next_mouse_move = False
            self.last_mouse_pos = (x, y)
            return
            
        # Calculate distance moved from last position
        last_x, last_y = self.last_mouse_pos
        distance = ((x - last_x) ** 2 + (y - last_y) ** 2) ** 0.5
        
        # Only count as activity if movement is above threshold
        if distance >= self.mouse_move_threshold:
            self.update_activity()
            self.last_mouse_pos = (x, y)
        
    def on_mouse_click(self, x, y, button, pressed):
        """Called when mouse is clicked"""
        if pressed:
            self.update_activity()
            
    def on_mouse_scroll(self, x, y, dx, dy):
        """Called when mouse is scrolled"""
        self.update_activity()
        
    def on_key_press(self, key):
        """Called when a key is pressed"""
        self.update_activity()
        
    def update_activity(self):
        """Update the last activity timestamp"""
        self.last_activity = datetime.now()
        
    def get_idle_time(self):
        """Get how long the system has been idle"""
        return datetime.now() - self.last_activity
        
    def is_idle(self):
        """Check if system has been idle for longer than threshold"""
        return self.get_idle_time() > self.idle_threshold
    
    def is_within_working_hours(self):
        """Check if current time is within specified working hours"""
        if self.start_time is None or self.end_time is None:
            return True  # No working hours specified, always active
            
        current_time = datetime.now().time()
        
        # Handle case where end time is next day (e.g., 22:00 to 06:00)
        if self.start_time <= self.end_time:
            return self.start_time <= current_time <= self.end_time
        else:
            return current_time >= self.start_time or current_time <= self.end_time
    
    def should_auto_move(self):
        """Check if we should move mouse automatically (includes cooldown and working hours check)"""
        if not self.is_idle():
            return False
            
        # Check if we're within working hours
        if not self.is_within_working_hours():
            return False
            
        # If we've never moved automatically, or enough time has passed since last auto move
        if self.last_auto_move is None:
            return True
            
        time_since_last_move = datetime.now() - self.last_auto_move
        return time_since_last_move >= self.auto_move_cooldown
        
    def move_mouse_slightly(self):
        """Move mouse by 1 pixel and back to simulate activity"""
        current_pos = self.mouse_controller.position
        
        # Set flag to ignore our automated movements
        self.ignore_next_mouse_move = True
        
        # Move mouse 1 pixel right and down
        self.mouse_controller.position = (current_pos[0] + 1, current_pos[1] + 1)
        time.sleep(0.1)
        
        # Set flag again for the return movement
        self.ignore_next_mouse_move = True
        
        # Move mouse back to original position
        self.mouse_controller.position = current_pos
        
        # Update the last auto move time
        self.last_auto_move = datetime.now()
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Mouse moved to prevent idle (next auto-move in {self.auto_move_cooldown.seconds}s)")
        
    def display_status(self):
        """Display current activity status"""
        while self.running:
            try:
                current_time = datetime.now()
                idle_time = self.get_idle_time()
                
                # Build status message
                status_parts = [
                    f"[{current_time.strftime('%H:%M:%S')}]",
                    f"Last active: {self.last_activity.strftime('%H:%M:%S')}",
                    f"(idle for {int(idle_time.total_seconds())}s)",
                    f"Threshold: {int(self.idle_threshold.total_seconds())}s"
                ]
                
                # Add working hours status if configured
                if self.start_time is not None and self.end_time is not None:
                    working_status = "ACTIVE" if self.is_within_working_hours() else "OUTSIDE HOURS"
                    status_parts.append(f"Status: {working_status}")
                
                # Clear the line and print status
                print(f"\r{' '.join(status_parts)}", end="", flush=True)
                
                # Check if we need to move mouse (with cooldown)
                if self.should_auto_move():
                    print()  # New line before the action message
                    self.move_mouse_slightly()
                    
                time.sleep(1)  # Update every second
                
            except KeyboardInterrupt:
                break
                
    def start_monitoring(self):
        """Start monitoring keyboard and mouse activity"""
        print("Starting activity monitor...")
        print(f"Idle threshold: {self.idle_threshold.total_seconds()/60:.1f} minutes")
        
        if self.start_time is not None and self.end_time is not None:
            print(f"Working hours: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}")
            if not self.is_within_working_hours():
                print("⚠️  Currently outside working hours - mouse movement disabled")
            else:
                print("✅ Currently within working hours - monitoring active")
        else:
            print("Working hours: Not configured (24/7 monitoring)")
            
        print("Press Ctrl+C to stop\n")
        
        # Start mouse listener
        mouse_listener = MouseListener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )
        
        # Start keyboard listener
        keyboard_listener = KeyboardListener(
            on_press=self.on_key_press
        )
        
        # Start listeners in background threads
        mouse_listener.start()
        keyboard_listener.start()
        
        # Start status display in main thread
        try:
            self.display_status()
        except KeyboardInterrupt:
            print("\n\nShutting down activity monitor...")
            self.running = False
            
        # Stop listeners
        mouse_listener.stop()
        keyboard_listener.stop()
        
        print("Activity monitor stopped.")

def parse_time_string(time_str):
    """Parse time string in various formats (HH:MM, H:MM, HH, H)"""
    try:
        # Try HH:MM format first
        if ':' in time_str:
            time_obj = datetime.strptime(time_str, '%H:%M').time()
        else:
            # Try hour only format
            hour = int(time_str)
            if 0 <= hour <= 23:
                time_obj = datetime.strptime(f'{hour:02d}:00', '%H:%M').time()
            else:
                raise ValueError("Hour must be between 0 and 23")
        return time_obj
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid time format '{time_str}'. Use HH:MM or H format (e.g., '09:00', '9', '17:30')")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Drinkingbird - System Activity Monitor & Keep-Alive Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
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
        """
    )
    
    parser.add_argument(
        '-t', '--threshold',
        type=float,
        default=3.0,
        metavar='MINUTES',
        help='Idle threshold in minutes before mouse movement (default: 3.0)'
    )
    
    parser.add_argument(
        '--start', '--start-time',
        type=parse_time_string,
        metavar='TIME',
        help='Working hours start time (e.g., "9", "09:00", "09:30")'
    )
    
    parser.add_argument(
        '--end', '--end-time',
        type=parse_time_string,
        metavar='TIME',
        help='Working hours end time (e.g., "17", "17:00", "17:30")'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='Drinkingbird 1.0.0'
    )
    
    return parser.parse_args()

def main():
    """Main function"""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Validate threshold
        if args.threshold <= 0:
            print("Error: Threshold must be greater than 0")
            sys.exit(1)
        if args.threshold < 0.1:
            print("Warning: Very low threshold may cause excessive mouse movement")
        
        # Validate working hours
        if (args.start is None) != (args.end is None):
            print("Error: Both --start and --end times must be specified together")
            sys.exit(1)
        
        # Check if running with appropriate permissions
        if os.name == 'posix' and os.geteuid() != 0:
            print("Note: You may need to run with appropriate permissions if mouse control doesn't work.")
            
        # Create and start activity monitor
        monitor = ActivityMonitor(
            idle_threshold_minutes=args.threshold,
            start_time=args.start,
            end_time=args.end
        )
        monitor.start_monitoring()
        
    except ImportError as e:
        print(f"Error: Missing required library. Please install with:")
        print("pip install pynput")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
