#!/usr/bin/env python3
"""Test script to verify long polling fixes work locally"""

import sys
sys.path.insert(0, '/Users/cyf/Desktop/CYF/SDC/React-chat-app/Backend')

from datetime import datetime, timedelta
from message_model import Message, Timestamp
from repository_inmemory import InMemoryMessageRepository
from service import MessageService
from long_polling.poller import LongPoller

def test_timestamp_comparison():
    """Test that Timestamp can be compared with datetime"""
    print("\n=== Testing Timestamp Comparison ===")
    ts = Timestamp()
    dt = datetime.now()
    
    try:
        result = ts > dt
        print(f"✓ Timestamp > datetime works: {result}")
    except Exception as e:
        print(f"✗ Timestamp comparison failed: {e}")
        return False
    
    return True

def test_get_messages_after():
    """Test that get_messages_after works correctly"""
    print("\n=== Testing get_messages_after ===")
    
    repo = InMemoryMessageRepository()
    service = MessageService(repo)
    
    msg1 = service.create_message("user1", "First message")
    print(f"Created message 1 at: {msg1.timestamp.value.isoformat()}")
    
    import time
    time.sleep(0.1)
    
    checkpoint = datetime.now()
    print(f"Checkpoint time: {checkpoint.isoformat()}")
    
    time.sleep(0.1)
    
    msg2 = service.create_message("user2", "Second message")
    print(f"Created message 2 at: {msg2.timestamp.value.isoformat()}")
    
    try:
        new_messages = service.get_messages_after(checkpoint)
        print(f"✓ Found {len(new_messages)} messages after checkpoint")
        
        if len(new_messages) == 1 and new_messages[0].id == msg2.id:
            print("✓ Correctly returned only the second message")
            return True
        else:
            print(f"✗ Expected 1 message (msg2), got {len(new_messages)}")
            return False
    except Exception as e:
        print(f"✗ get_messages_after failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_long_poller():
    """Test that LongPoller works without errors"""
    print("\n=== Testing LongPoller ===")
    
    repo = InMemoryMessageRepository()
    service = MessageService(repo)
    poller = LongPoller(service, timeout=2, interval=0.2)
    
    msg = service.create_message("test", "Test message")
    
    before_time = datetime.now() - timedelta(seconds=5)
    
    try:
        messages = poller.wait_for_new_messages(before_time)
        print(f"✓ LongPoller returned {len(messages)} messages")
        
        if len(messages) == 1 and messages[0].id == msg.id:
            print("✓ LongPoller correctly found the message")
            return True
        else:
            print(f"✗ Expected to find the test message")
            return False
    except Exception as e:
        print(f"✗ LongPoller failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Long Polling Fixes")
    print("=" * 60)
    
    results = []
    
    results.append(("Timestamp Comparison", test_timestamp_comparison()))
    results.append(("Get Messages After", test_get_messages_after()))
    results.append(("Long Poller", test_long_poller()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed! The fixes are working correctly.")
        print("Once you redeploy, the 500 errors should be resolved.")
    else:
        print("✗ Some tests failed. Review the errors above.")
    print("=" * 60)
    
    sys.exit(0 if all_passed else 1)
