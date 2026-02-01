#!/usr/bin/env python3
"""
Milestone 3: Callbacks and Cleanup (40 points)
===============================================

This milestone verifies that the student has:
1. Used gpiozero for button callbacks
2. Implemented clean shutdown with Event
3. Proper error handling in callbacks
4. KeyboardInterrupt handling for Ctrl+C

These tests verify code STRUCTURE for callbacks and cleanup patterns.
"""

import os
import ast
import re
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helper: Get repository root
# ---------------------------------------------------------------------------
def get_repo_root():
    """Find the repository root by looking for .github folder."""
    current = Path(__file__).parent.parent
    if (current / ".github").exists():
        return current
    return current


REPO_ROOT = get_repo_root()


# ---------------------------------------------------------------------------
# Test 3.1: gpiozero Import (10 points)
# ---------------------------------------------------------------------------
def test_gpiozero_import():
    """
    Verify that the script imports gpiozero.

    Expected: 'from gpiozero import' Button or similar

    Suggestion: Add gpiozero import for button handling:
        from gpiozero import Button
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_gpiozero = any([
        "gpiozero" in content,
        "from gpiozero" in content,
    ])

    if not has_gpiozero:
        pytest.fail(
            f"\n\n"
            f"Expected: gpiozero import for button callbacks\n"
            f"Actual: No gpiozero import found\n\n"
            f"Suggestion: Add gpiozero import:\n"
            f"  from gpiozero import Button\n"
            f"\n"
            f"gpiozero provides simple button handling with callbacks\n"
            f"that work on Raspberry Pi 5.\n"
        )


# ---------------------------------------------------------------------------
# Test 3.2: Callback Pattern (10 points)
# ---------------------------------------------------------------------------
def test_callback_pattern():
    """
    Verify that button callbacks are defined.

    Expected: when_pressed or when_released assignment

    Suggestion: Set up button callbacks:
        button.when_pressed = on_button_press
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_callback = any([
        "when_pressed" in content,
        "when_released" in content,
        "when_held" in content,
    ])

    if not has_callback:
        pytest.fail(
            f"\n\n"
            f"Expected: Button callback assignment (when_pressed, etc.)\n"
            f"Actual: No callback pattern found\n\n"
            f"Suggestion: Set up button callbacks:\n"
            f"  from gpiozero import Button\n"
            f"\n"
            f"  button = Button(17, bounce_time=0.1)\n"
            f"\n"
            f"  def on_button_press():\n"
            f"      print(\"Bouton appuye!\")\n"
            f"\n"
            f"  button.when_pressed = on_button_press\n"
        )


# ---------------------------------------------------------------------------
# Test 3.3: Event for Stop Signal (10 points)
# ---------------------------------------------------------------------------
def test_stop_event():
    """
    Verify that threading.Event is used for clean shutdown.

    Expected: Event() creation for stop signaling

    Suggestion: Use Event for thread coordination:
        stop_event = threading.Event()
        stop_event.set()  # Signal threads to stop
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_event = any([
        "Event()" in content,
        "threading.Event" in content,
        "stop_event" in content.lower(),
        "stop_flag" in content.lower(),
    ])

    if not has_event:
        pytest.fail(
            f"\n\n"
            f"Expected: threading.Event for clean shutdown\n"
            f"Actual: No Event or stop signal found\n\n"
            f"Suggestion: Use Event for thread coordination:\n"
            f"  import threading\n"
            f"\n"
            f"  stop_event = threading.Event()\n"
            f"\n"
            f"  def read_sensor():\n"
            f"      while not stop_event.is_set():\n"
            f"          # Read sensor\n"
            f"          ...\n"
            f"\n"
            f"  # To stop all threads:\n"
            f"  stop_event.set()\n"
        )


# ---------------------------------------------------------------------------
# Test 3.4: Try/Except in Callbacks (5 points)
# ---------------------------------------------------------------------------
def test_callback_error_handling():
    """
    Verify that callbacks include error handling.

    Expected: try/except in callback functions

    WHY THIS MATTERS:
    gpiozero runs callbacks in background threads.
    Exceptions in callbacks are SILENTLY IGNORED!
    Always wrap callback code in try/except.

    Suggestion: Add error handling in callbacks:
        def on_button_press():
            try:
                # Your code
            except Exception as e:
                print(f"Callback error: {e}")
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    # Count try/except blocks - should have at least 2
    try_count = content.count("try:")
    except_count = content.count("except")

    if try_count < 2 or except_count < 2:
        pytest.fail(
            f"\n\n"
            f"Expected: Multiple try/except blocks (at least 2)\n"
            f"Actual: Found {try_count} try blocks, {except_count} except blocks\n\n"
            f"WHY THIS MATTERS:\n"
            f"  gpiozero runs callbacks in background threads.\n"
            f"  Exceptions in callbacks are SILENTLY IGNORED!\n"
            f"  Your button may appear to stop working with no error message.\n\n"
            f"Suggestion: ALWAYS wrap callback code in try/except:\n"
            f"  def on_button_press():\n"
            f"      try:\n"
            f"          data = sensor.read()\n"
            f"          print(f\"Temperature: {{data}}\")\n"
            f"      except Exception as e:\n"
            f"          print(f\"Erreur dans callback: {{e}}\")\n"
        )


# ---------------------------------------------------------------------------
# Test 3.5: KeyboardInterrupt Handling (5 points)
# ---------------------------------------------------------------------------
def test_keyboard_interrupt():
    """
    Verify that KeyboardInterrupt is handled for clean Ctrl+C exit.

    Expected: except KeyboardInterrupt pattern

    Suggestion: Handle Ctrl+C gracefully:
        try:
            main()
        except KeyboardInterrupt:
            print("Arret demande...")
            stop_event.set()
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_keyboard_interrupt = "KeyboardInterrupt" in content

    if not has_keyboard_interrupt:
        pytest.fail(
            f"\n\n"
            f"Expected: KeyboardInterrupt handling\n"
            f"Actual: No KeyboardInterrupt handler found\n\n"
            f"Suggestion: Handle Ctrl+C for clean exit:\n"
            f"  if __name__ == \"__main__\":\n"
            f"      try:\n"
            f"          main()\n"
            f"      except KeyboardInterrupt:\n"
            f"          print(\"Arret demande...\")\n"
            f"          stop_event.set()\n"
            f"\n"
            f"This ensures threads stop cleanly when user presses Ctrl+C.\n"
        )
