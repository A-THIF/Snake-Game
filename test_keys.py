import os
import sys
import time
import msvcrt
import threading

def clear_screen():
    """Clear the console screen"""
    os.system('cls')

def main():
    """Main function to test key detection"""
    clear_screen()
    print("Keyboard Test Utility")
    print("=====================")
    print("\nPress any keys to see their key codes")
    print("This test will run for 10 seconds or until you press 'q'")
    print("\nDetected keys will appear below:")
    print("-" * 50)
    
    # Setup variables
    start_time = time.time()
    end_time = start_time + 10  # Run for 10 seconds
    keys_detected = []
    
    # Create a flag for when to stop
    stop_flag = threading.Event()
    
    # Function to show countdown
    def show_countdown():
        while not stop_flag.is_set() and time.time() < end_time:
            remaining = int(end_time - time.time())
            sys.stdout.write(f"\rTime remaining: {remaining} seconds ")
            sys.stdout.flush()
            time.sleep(0.1)
    
    # Start countdown thread
    countdown_thread = threading.Thread(target=show_countdown)
    countdown_thread.daemon = True
    countdown_thread.start()
    
    # Main key detection loop
    try:
        while time.time() < end_time:
            # Method 1: msvcrt.kbhit() and msvcrt.getch()
            if msvcrt.kbhit():
                key = ord(msvcrt.getch())
                
                # Print the key code
                print(f"\nDetected key: {key} (0x{key:02x})")
                keys_detected.append(key)
                
                # Check if it's a special key that needs another byte
                if key in [0, 224, 0xE0]:
                    try:
                        key2 = ord(msvcrt.getch())
                        print(f"  Extended key, second byte: {key2} (0x{key2:02x})")
                        keys_detected.append(key2)
                        
                        # Try to identify some common keys
                        if key2 == 72:
                            print("  Identified as: UP ARROW")
                        elif key2 == 80:
                            print("  Identified as: DOWN ARROW")
                        elif key2 == 75:
                            print("  Identified as: LEFT ARROW")
                        elif key2 == 77:
                            print("  Identified as: RIGHT ARROW")
                    except Exception as e:
                        print(f"  Error reading second byte: {e}")
                
                # Try to identify common keys
                elif key == 13:
                    print("  Identified as: ENTER")
                elif key == 27:
                    print("  Identified as: ESC")
                elif key == 32:
                    print("  Identified as: SPACE")
                elif key == 113 or key == 81:
                    print("  Identified as: Q (quit)")
                    break
                elif 97 <= key <= 122:
                    print(f"  Identified as: {chr(key)}")
                
                # Force display update
                sys.stdout.flush()
            
            # Brief pause to prevent CPU hogging
            time.sleep(0.01)
    
    except Exception as e:
        print(f"\nError during key detection: {e}")
    
    finally:
        # Stop the countdown thread
        stop_flag.set()
        countdown_thread.join(0.5)
        
        # Show summary
        print("\n" + "-" * 50)
        print(f"Test completed. Detected {len(keys_detected)} key presses:")
        print(f"Key codes: {keys_detected}")
        
        print("\nPress any key to exit...")
        msvcrt.getch()

if __name__ == "__main__":
    main()

