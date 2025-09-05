#!/usr/bin/env python3
"""
CoreWar Visualization File Inspector
Analyzes .viz files to verify format and display battle information
"""

import struct
import sys
import os

# Event type mapping for better readability (matches visualizer.h)
EVENT_TYPES = {
    0: "EXEC",      # Instruction execution
    1: "READ",      # Memory read
    2: "WRITE",     # Memory write
    3: "DEC",       # Memory decrement
    4: "INC",       # Memory increment
    5: "SPL",       # Process spawn
    6: "DAT",       # Process death
    7: "DIE",       # Warrior death
    8: "CYCLE",     # Cycle start
    9: "PUSH"       # Task queue push
}

def format_bytes(num_bytes):
    """Format byte count with appropriate units"""
    if num_bytes < 1024:
        return f"{num_bytes} bytes"
    elif num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KB"
    else:
        return f"{num_bytes / (1024 * 1024):.1f} MB"

def analyze_events(events):
    """Analyze event patterns and provide statistics"""
    if not events:
        return {}
    
    # Count events by type
    type_counts = {}
    warrior_activity = {0: 0, 1: 0}
    cycle_range = [float('inf'), 0]
    
    for cycle, address, warrior_id, event_type, data in events:
        # Event type statistics
        event_name = EVENT_TYPES.get(event_type, f"UNKNOWN_{event_type}")
        type_counts[event_name] = type_counts.get(event_name, 0) + 1
        
        # Warrior activity
        if warrior_id in warrior_activity:
            warrior_activity[warrior_id] += 1
        
        # Cycle range
        cycle_range[0] = min(cycle_range[0], cycle)
        cycle_range[1] = max(cycle_range[1], cycle)
    
    return {
        'type_counts': type_counts,
        'warrior_activity': warrior_activity,
        'cycle_range': cycle_range,
        'total_events': len(events)
    }

def test_viz_file(filename):
    """Test reading and analyze a .viz file"""
    print(f"=== CoreWar Visualization File Inspector ===")
    print(f"Analyzing: {filename}")
    
    # Check file existence and size
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found")
        return False
    
    file_size = os.path.getsize(filename)
    print(f"File size: {format_bytes(file_size)}")
    
    try:
        with open(filename, 'rb') as f:
            # Read and validate header (168 bytes total with reserved fields)
            header_data = f.read(168)
            if len(header_data) < 168:
                print(f"Error: Invalid header size {len(header_data)} bytes (expected 168)")
                return False
            
            print(f"\n--- Header Analysis ---")
            
            # Parse magic number
            magic = header_data[0:8].decode('ascii').rstrip('\x00')
            print(f"Magic Number: '{magic}'")
            
            if magic != "PMARSREC":
                print(f"Warning: Unexpected magic number (expected 'PMARSREC')")
            
            # Parse header fields
            try:
                (version, core_size, total_cycles, total_events) = struct.unpack('<IIII', header_data[8:24])
                
                # Extract warrior names (64 bytes each)
                warrior1_name = header_data[24:88].decode('ascii').rstrip('\x00')
                warrior2_name = header_data[88:152].decode('ascii').rstrip('\x00')
                
                # Extract starting positions
                (warrior1_start, warrior2_start) = struct.unpack('<II', header_data[152:160])
                
                print(f"Format Version: {version}")
                print(f"Core Size: {core_size:,} locations")
                print(f"Total Cycles: {total_cycles:,}")
                print(f"Expected Events: {total_events:,}")
                
                print(f"\n--- Warrior Information ---")
                print(f"Warrior 1: '{warrior1_name}' (length: {len(warrior1_name)})")
                print(f"  Starting Position: {warrior1_start}")
                
                print(f"Warrior 2: '{warrior2_name}' (length: {len(warrior2_name)})")
                print(f"  Starting Position: {warrior2_start}")
                
                # Validation checks
                if len(warrior1_name) > 64 or len(warrior2_name) > 64:
                    print("Warning: Warrior name exceeds 64 character limit")
                
                if warrior1_start >= core_size or warrior2_start >= core_size:
                    print("Warning: Starting position outside core bounds")
                
            except struct.error as e:
                print(f"Error parsing header: {e}")
                return False
            
            # Read and analyze events
            print(f"\n--- Event Analysis ---")
            events = []
            event_count = 0
            invalid_events = 0
            
            while True:
                event_data = f.read(16)  # Updated for 16-byte events
                if len(event_data) < 16:
                    break
                
                try:
                    cycle, address, event_type, warrior_id, padding1, padding2, padding3, data = struct.unpack('<IHHBBBBI', event_data)
                    
                    # Basic validation
                    if address >= core_size:
                        invalid_events += 1
                        continue
                    
                    if warrior_id > 1:
                        invalid_events += 1
                        continue
                    
                    events.append((cycle, address, warrior_id, event_type, data))
                    event_count += 1
                    
                except struct.error:
                    invalid_events += 1
                    break
            
            print(f"Events Read: {event_count:,}")
            print(f"Invalid Events: {invalid_events}")
            
            if event_count != total_events:
                print(f"Warning: Event count mismatch (header: {total_events}, actual: {event_count})")
            
            # Display sample events
            if events:
                print(f"\n--- Sample Events (first 10) ---")
                for i, (cycle, address, warrior_id, event_type, data) in enumerate(events[:10]):
                    event_name = EVENT_TYPES.get(event_type, f"UNK_{event_type}")
                    print(f"  {i+1:2d}: Cycle {cycle:5d} | Addr {address:4d} | W{warrior_id} | {event_name:5s} | Data {data}")
                
                if len(events) > 10:
                    print(f"       ... and {len(events) - 10:,} more events")
            
            # Event statistics
            if events:
                stats = analyze_events(events)
                print(f"\n--- Event Statistics ---")
                print(f"Cycle Range: {stats['cycle_range'][0]} - {stats['cycle_range'][1]}")
                print(f"Total Events: {stats['total_events']:,}")
                
                print(f"\nEvent Types:")
                for event_type, count in sorted(stats['type_counts'].items()):
                    percentage = (count / stats['total_events']) * 100
                    print(f"  {event_type:8s}: {count:6,} ({percentage:5.1f}%)")
                
                print(f"\nWarrior Activity:")
                for warrior_id, count in stats['warrior_activity'].items():
                    warrior_name = warrior1_name if warrior_id == 0 else warrior2_name
                    percentage = (count / stats['total_events']) * 100
                    print(f"  Warrior {warrior_id} ({warrior_name[:20]}...): {count:6,} events ({percentage:5.1f}%)")
            
            # File integrity summary
            print(f"\n--- File Integrity Summary ---")
            expected_size = 168 + (total_events * 16)  # 168-byte header + 16-byte events
            print(f"Expected Size: {format_bytes(expected_size)}")
            print(f"Actual Size: {format_bytes(file_size)}")
            
            if file_size == expected_size:
                print("OK File size matches expected format")
            else:
                print("WARNING File size mismatch - possible corruption")
            
            if invalid_events == 0 and event_count == total_events:
                print("OK All events valid and complete")
                return True
            else:
                print("WARNING File contains invalid or missing events")
                return False
                
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("CoreWar Visualization File Inspector")
        print("Usage: python test_viz.py <file.viz>")
        print("\nThis tool analyzes .viz files created by pmars with -T option")
        print("and provides detailed information about the battle recording.")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    if not filename.endswith('.viz'):
        print("Warning: File doesn't have .viz extension")
    
    success = test_viz_file(filename)
    
    print(f"\n{'='*50}")
    if success:
        print("✓ File analysis completed successfully")
        sys.exit(0)
    else:
        print("⚠ File analysis completed with warnings/errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
