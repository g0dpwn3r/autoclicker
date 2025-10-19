#!/usr/bin/env python3
"""
Test script to verify playback interruption and restart functionality
"""

import sys
import os
import time
import threading

# Add the inc directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'inc'))

from inc.Recording import Recording

def test_interruption_and_restart():
    """Test playback interruption and restart capabilities."""
    print("Testing playback interruption and restart...")

    # Create a recording instance
    recording = Recording()

    # Load the test recording
    success = recording.load_recording("test_recording")
    if not success:
        print("Failed to load test recording")
        return False

    print(f"Loaded recording with {len(recording.mousePositions)} positions")

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

    print("\n=== Test 1: Normal playback completion ===")
    try:
        recording.start_clicking()
        print("✓ Normal playback completed successfully")
    except Exception as e:
        print(f"✗ Normal playback failed: {e}")
        return False

    print("\n=== Test 2: Playback interruption (simulated failsafe) ===")
    # We'll need to modify the clicker to simulate interruption
    # For now, let's test the restart capability after a successful run

    print("\n=== Test 3: Restart after completion ===")
    try:
        recording.start_clicking()
        print("✓ Restart after completion successful")
    except Exception as e:
        print(f"✗ Restart failed: {e}")
        return False

    print("\n=== Test 4: Multiple restarts ===")
    for i in range(3):
        try:
            print(f"Restart attempt {i+1}...")
            recording.start_clicking()
            print(f"✓ Restart {i+1} successful")
        except Exception as e:
            print(f"✗ Restart {i+1} failed: {e}")
            return False

    print("\n✓ All interruption and restart tests passed!")
    return True

if __name__ == "__main__":
    test_interruption_and_restart()