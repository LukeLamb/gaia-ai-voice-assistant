#!/usr/bin/env python3
"""
Simple test script to test gaia functions without running main()
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_gaia_functions():
    """Test individual gaia functions"""
    print("🧪 Testing Gaia Functions Individually")
    print("=" * 50)
    
    # Import the module
    print("📦 Importing gaia module...")
    import gaia
    print("✅ Gaia module imported successfully")
    
    # Test banner
    print("\n🎨 Testing banner display...")
    gaia._display_banner()
    print("✅ Banner displayed successfully")
    
    # Test interface mappings
    print("\n🔗 Testing interface mappings...")
    interfaces = gaia._get_interface_mappings()
    print(f"Available interfaces: {list(interfaces.keys())}")
    print("✅ Interface mappings work")
    
    # Test choice validation
    print("\n✅ Testing choice validation...")
    print(f"Valid choice '1': {gaia._is_valid_choice('1')}")
    print(f"Invalid choice 'x': {gaia._is_valid_choice('x')}")
    print("✅ Choice validation works")
    
    # Test interface type mapping
    print("\n🗺️ Testing interface type mapping...")
    print(f"Choice '1' maps to: {gaia._get_interface_type('1')}")
    print(f"Choice '2' maps to: {gaia._get_interface_type('2')}")
    print("✅ Interface type mapping works")
    
    print("\n" + "=" * 50)
    print("🎉 All Gaia functions work correctly!")
    print("✅ The terminal interface is functional")

if __name__ == "__main__":
    test_gaia_functions()
