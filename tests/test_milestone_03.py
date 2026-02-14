"""
Milestone 3: Bouton Polling et Cleanup (40 points)
===================================================

This milestone verifies that the student has:
1. Used CircuitPython digitalio for button polling
2. Implemented clean shutdown with Event
3. Proper error handling in polling thread
4. KeyboardInterrupt handling for Ctrl+C

These tests verify code STRUCTURE for polling and cleanup patterns.
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
# Test 3.1: digitalio + board Import (10 points)
# ---------------------------------------------------------------------------
def test_digitalio_button_import():
    """
    Verify that the script imports digitalio and board (not gpiozero).

    Expected: 'import digitalio' and 'import board'

    Suggestion: Add digitalio and board imports for button handling:
        import board
        import digitalio
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    # Check for digitalio import
    has_digitalio = any([
        "import digitalio" in content,
        "from digitalio" in content,
    ])

    # Check for board import
    has_board = any([
        "import board" in content,
        "from board" in content,
    ])

    # Check for gpiozero (should NOT be present)
    has_gpiozero = any([
        "gpiozero" in content,
        "from gpiozero" in content,
    ])

    if has_gpiozero:
        pytest.fail(
            f"\n\n"
            f"Votre code utilise gpiozero.\n"
            f"Utilisez digitalio pour lire le bouton par polling,\n"
            f"comme montre dans la theorie semaine 4.\n\n"
            f"Suggestion: Remplacez gpiozero par digitalio:\n"
            f"  import board\n"
            f"  import digitalio\n"
        )

    if not has_digitalio or not has_board:
        missing = []
        if not has_digitalio:
            missing.append("digitalio")
        if not has_board:
            missing.append("board")
        pytest.fail(
            f"\n\n"
            f"Votre code n'importe pas {' et '.join(missing)}.\n"
            f"Ajoutez 'import board' et 'import digitalio' en haut\n"
            f"de votre script pour lire le bouton.\n\n"
            f"Suggestion:\n"
            f"  import board\n"
            f"  import digitalio\n"
        )


# ---------------------------------------------------------------------------
# Test 3.2: Button Polling Pattern (10 points)
# ---------------------------------------------------------------------------
def test_button_polling_pattern():
    """
    Verify that button polling with digitalio is used.

    Expected: digitalio configuration and button.value reading

    Suggestion: Configure and poll the button:
        button = digitalio.DigitalInOut(board.GP17)
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP
        # In a loop:
        if not button.value:
            print("Bouton appuye!")
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    # Check for gpiozero callback patterns (should NOT be present)
    has_gpiozero_callback = any([
        "when_pressed" in content,
        "when_released" in content,
        "when_held" in content,
    ])

    if has_gpiozero_callback:
        pytest.fail(
            f"\n\n"
            f"Votre code utilise des callbacks gpiozero (when_pressed).\n"
            f"Utilisez plutot digitalio polling (button.value dans une boucle)\n"
            f"comme montre dans la theorie.\n\n"
            f"Suggestion: Remplacez le callback par du polling:\n"
            f"  button = digitalio.DigitalInOut(board.GP17)\n"
            f"  button.direction = digitalio.Direction.INPUT\n"
            f"  button.pull = digitalio.Pull.UP\n"
            f"\n"
            f"  while not stop_event.is_set():\n"
            f"      if not button.value:\n"
            f"          print(\"Bouton appuye!\")\n"
            f"      time.sleep(0.05)\n"
        )

    # Check for digitalio polling patterns
    has_polling = any([
        "button.value" in content,
        ".value" in content and "digitalio" in content,
        "DigitalInOut" in content,
        "digitalio.DigitalInOut" in content,
        "Direction.INPUT" in content,
        "digitalio.Direction.INPUT" in content,
        "Pull.UP" in content,
        "digitalio.Pull.UP" in content,
    ])

    if not has_polling:
        pytest.fail(
            f"\n\n"
            f"Votre code doit lire le bouton par polling avec digitalio.\n"
            f"Configurez avec:\n"
            f"  button = digitalio.DigitalInOut(board.GP17)\n"
            f"  button.direction = digitalio.Direction.INPUT\n"
            f"  button.pull = digitalio.Pull.UP\n\n"
            f"Puis lisez button.value dans une boucle:\n"
            f"  while not stop_event.is_set():\n"
            f"      if not button.value:\n"
            f"          print(\"Bouton appuye!\")\n"
            f"      time.sleep(0.05)\n"
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
# Test 3.4: Try/Except in Polling Thread (5 points)
# ---------------------------------------------------------------------------
def test_callback_error_handling():
    """
    Verify that the polling thread includes error handling.

    Expected: try/except in polling and thread functions

    WHY THIS MATTERS:
    Le thread de polling du bouton s'execute en arriere-plan.
    Les exceptions dans un thread ne sont PAS affichees dans le
    terminal principal! Toujours entourer le code du thread
    avec try/except.

    Suggestion: Add error handling in polling thread:
        def button_polling_thread():
            while not stop_event.is_set():
                try:
                    current = button.value
                    if not current:
                        print("Bouton appuye!")
                except Exception as e:
                    print(f"Erreur polling: {e}")
                time.sleep(0.05)
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
            f"  Le thread de polling du bouton s'execute en arriere-plan.\n"
            f"  Les exceptions dans un thread ne sont PAS affichees\n"
            f"  dans le terminal principal!\n"
            f"  Votre bouton peut sembler \"arreter de fonctionner\"\n"
            f"  sans message d'erreur.\n\n"
            f"Suggestion: TOUJOURS entourer le code du thread\n"
            f"de polling avec try/except:\n"
            f"  def button_polling_thread():\n"
            f"      while not stop_event.is_set():\n"
            f"          try:\n"
            f"              current = button.value\n"
            f"              if not current:\n"
            f"                  print(\"Bouton appuye!\")\n"
            f"          except Exception as e:\n"
            f"              print(f\"Erreur polling: {{e}}\")\n"
            f"          time.sleep(0.05)\n"
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
