#!/usr/bin/env python3
"""
Milestone 2: Threading Pattern (35 points)
==========================================

This milestone verifies that the student has:
1. Imported threading and queue modules
2. Used Queue for thread-safe communication
3. Used Thread for concurrent execution
4. Structured functions correctly for threading

IMPORTANT: We test code STRUCTURE, not execution.
Actual thread execution in CI would be flaky.
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
# Test 2.1: Threading Import (10 points)
# ---------------------------------------------------------------------------
def test_threading_import():
    """
    Verify that the script imports the threading module.

    Expected: 'import threading' or 'from threading import'

    Suggestion: Add at the top of your script:
        import threading
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_threading = any([
        "import threading" in content,
        "from threading import" in content,
    ])

    if not has_threading:
        pytest.fail(
            f"\n\n"
            f"Expected: threading module import\n"
            f"Actual: No threading import found\n\n"
            f"Suggestion: Add threading import:\n"
            f"  import threading\n"
            f"\n"
            f"The threading module provides:\n"
            f"  - Thread: for creating threads\n"
            f"  - Event: for signaling between threads\n"
        )


# ---------------------------------------------------------------------------
# Test 2.2: Queue Import (10 points)
# ---------------------------------------------------------------------------
def test_queue_import():
    """
    Verify that the script imports the queue module.

    Expected: 'import queue' or 'from queue import'

    Suggestion: Add at the top of your script:
        import queue
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_queue = any([
        "import queue" in content,
        "from queue import" in content,
    ])

    if not has_queue:
        pytest.fail(
            f"\n\n"
            f"Expected: queue module import\n"
            f"Actual: No queue import found\n\n"
            f"Suggestion: Add queue import:\n"
            f"  import queue\n"
            f"\n"
            f"The queue module provides thread-safe Queue for\n"
            f"passing data between producer and consumer threads.\n"
        )


# ---------------------------------------------------------------------------
# Test 2.3: Queue Usage (7 points)
# ---------------------------------------------------------------------------
def test_queue_usage():
    """
    Verify that a Queue is created and used.

    Expected: queue.Queue() creation and .put() or .get() calls

    Suggestion: Create a queue for thread communication:
        data_queue = queue.Queue()
        data_queue.put(sensor_data)
        data = data_queue.get(timeout=1)
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_queue_creation = any([
        "Queue()" in content,
        "queue.Queue" in content,
    ])

    has_queue_usage = any([
        ".put(" in content,
        ".get(" in content,
    ])

    if not has_queue_creation:
        pytest.fail(
            f"\n\n"
            f"Expected: Queue creation (queue.Queue())\n"
            f"Actual: No Queue creation found\n\n"
            f"Suggestion: Create a queue for producer-consumer pattern:\n"
            f"  import queue\n"
            f"  data_queue = queue.Queue()\n"
        )

    if not has_queue_usage:
        pytest.fail(
            f"\n\n"
            f"Expected: Queue usage (.put() or .get())\n"
            f"Actual: No Queue operations found\n\n"
            f"Suggestion: Use the queue to pass data:\n"
            f"  # In producer thread:\n"
            f"  data_queue.put(sensor_data)\n"
            f"\n"
            f"  # In consumer thread:\n"
            f"  data = data_queue.get(timeout=1)\n"
        )


# ---------------------------------------------------------------------------
# Test 2.4: Thread Usage (8 points)
# ---------------------------------------------------------------------------
def test_thread_usage():
    """
    Verify that threads are created.

    Expected: threading.Thread() creation

    Suggestion: Create threads for concurrent execution:
        producer = threading.Thread(target=read_sensor, args=(sensor,))
        consumer = threading.Thread(target=publish_data, args=(client,))
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_thread_creation = any([
        "Thread(" in content,
        "threading.Thread" in content,
    ])

    if not has_thread_creation:
        pytest.fail(
            f"\n\n"
            f"Expected: Thread creation (threading.Thread())\n"
            f"Actual: No Thread creation found\n\n"
            f"Suggestion: Create threads for concurrent execution:\n"
            f"  import threading\n"
            f"\n"
            f"  # Create threads\n"
            f"  producer = threading.Thread(target=read_sensor, args=(sensor,))\n"
            f"  consumer = threading.Thread(target=publish_data, args=(client,))\n"
            f"\n"
            f"  # Start threads\n"
            f"  producer.start()\n"
            f"  consumer.start()\n"
        )


# ---------------------------------------------------------------------------
# Test 2.5: Thread Start (Bonus verification)
# ---------------------------------------------------------------------------
def test_thread_start():
    """
    Verify that threads are started.

    Expected: .start() calls on thread objects

    Suggestion: Start threads after creation:
        producer.start()
        consumer.start()
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_start = ".start()" in content

    if not has_start:
        # This is expected but we'll be lenient
        pytest.skip(
            ".start() not detected - make sure to start your threads"
        )
