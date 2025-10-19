#!/usr/bin/env python3
"""
Test script to verify mouse movement and clicking functionality
without relying on the GUI.
"""

import sys
import os
import time

# Add the inc directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'inc'))

from inc.Recording import Recording

def test_mouse_functionality():
    """Test mouse movement and clicking with a loaded recording."""
    print("Testing mouse functionality...")

    # Create a recording instance
    recording = Recording()

    # Load the test recording
    success = recording.load_recording("test_recording")
    if not success:
        print("Failed to load test recording")
        return False

    print(f"Loaded recording with {len(recording.mousePositions)} positions:")
    for i, pos in enumerate(recording.mousePositions):
        print(f"  Position {i+1}: ({pos[0]}, {pos[1]})")

    # Set parameters for testing (fast to avoid long waits)
    recording.start = 0.5  # Fast movement
    recording.end = 1.0
    recording.startc = 0.1  # Fast clicking
    recording.endc = 0.2
    recording.radius = 5
    recording.angle = 360
    recording.timeout = 0.5

    # Parse config to create Clicker instance
    recording.parse_config()

    print("\nStarting continuous playback test...")
    print("WARNING: Mouse will move and click continuously! Move mouse to corner to stop if needed.")
    print("This will loop through the positions multiple times until interrupted.")

    try:
        # Start the continuous clicking process
        recording.start_clicking(continuous=True)
        print("Continuous playback completed successfully!")
        return True
    except Exception as e:
        print(f"Error during continuous playback: {e}")
        return False

if __name__ == "__main__":
    test_mouse_functionality()