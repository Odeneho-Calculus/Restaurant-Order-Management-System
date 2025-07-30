#!/usr/bin/env python3
"""
Test script for Restaurant Order Management System.

This script performs comprehensive testing of all system components
to ensure proper functionality and data integrity.
"""

import sys
import os
from pathlib import Path
from decimal import Decimal
import logging

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing module imports...")

    try:
        # Test model imports
        from restaurant_system.models import MenuItem, Order, OrderItem, OrderStatus, OrderType
        print("✓ Model classes imported successfully")

        # Test utility imports
        from restaurant_system.utils import CSVHandler, InputValidator, ReceiptGenerator
        print("✓ Utility classes imported successfully")

        # Test GUI imports
        from restaurant_system.gui import RestaurantMainWindow
        print("✓ GUI classes imported successfully")

        return True

    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_data_models():
    """Test data model functionality."""
    print("\nTesting data models...")

    try:
        from restaurant_system.models import MenuItem, Order, OrderItem, OrderStatus, OrderType

        # Test MenuItem creation
        item = MenuItem("Test Burger", "mains", Decimal("15.99"), "Delicious test burger")
        assert item.name == "Test Burger"
        assert item.price == Decimal("15.99")
        print("✓ MenuItem creation successful")

        # Test Order creation
        order = Order()
        assert order.status == OrderStatus.PENDING
        assert len(order.items) == 0
        print("✓ Order creation successful")

        # Test adding items to order
        order.add_item(item, 2)
        assert len(order.items) == 1
        assert order.items[0].quantity == 2
        print("✓ Order item addition successful")

        # Test order calculations
        assert order.subtotal == Decimal("31.98")  # 15.99 * 2
        assert order.total_amount > order.subtotal  # Should include tax
        print("✓ Order calculations successful")

        return True

    except Exception as e:
        print(f"✗ Data model test failed: {e}")
        return False

def test_csv_operations():
    """Test CSV file operations."""
    print("\nTesting CSV operations...")

    try:
        from restaurant_system.utils import CSVHandler
        from restaurant_system.models import MenuItem
        from restaurant_system.config import DATA_DIR

        # Initialize CSV handler with data directory
        csv_handler = CSVHandler(DATA_DIR)

        # Test menu item operations
        test_item = MenuItem("Test Item", "appetizers", Decimal("9.99"), "Test description")

        # Load existing menu items
        menu_items = csv_handler.load_menu_items()
        original_count = len(menu_items)
        print(f"✓ Loaded {original_count} menu items")

        # Add test item
        menu_items.append(test_item)
        csv_handler.save_menu_items(menu_items)
        print("✓ Menu item saved to CSV")

        # Reload and verify
        reloaded_items = csv_handler.load_menu_items()
        assert len(reloaded_items) == original_count + 1
        print("✓ Menu item successfully persisted")

        # Remove test item
        menu_items = [item for item in reloaded_items if item.name != "Test Item"]
        csv_handler.save_menu_items(menu_items)
        print("✓ Test data cleaned up")

        return True

    except Exception as e:
        print(f"✗ CSV operations test failed: {e}")
        return False

def test_validation():
    """Test input validation functionality."""
    print("\nTesting input validation...")

    try:
        from restaurant_system.utils import InputValidator, ValidationError

        # Test price validation
        valid_price = InputValidator.validate_price("15.99")
        assert valid_price == Decimal("15.99")
        print("✓ Price validation successful")

        try:
            InputValidator.validate_price("invalid")
            assert False, "Should have raised ValidationError"
        except ValidationError:
            print("✓ Invalid price correctly rejected")

        # Test phone validation
        valid_phone = InputValidator.validate_phone_number("555-123-4567", required=False)
        assert valid_phone == "555-123-4567"
        print("✓ Phone validation successful")

        # Test email validation
        valid_email = InputValidator.validate_email("test@example.com", required=False)
        assert valid_email == "test@example.com"
        print("✓ Email validation successful")

        return True

    except Exception as e:
        print(f"✗ Validation test failed: {e}")
        return False

def test_receipt_generation():
    """Test receipt generation functionality."""
    print("\nTesting receipt generation...")

    try:
        from restaurant_system.utils import ReceiptGenerator
        from restaurant_system.models import MenuItem, Order, OrderType

        # Create test order
        order = Order()
        order.customer_name = "Test Customer"
        order.customer_phone = "(555) 123-4567"
        order.table_number = "5"
        order.order_type = OrderType.DINE_IN

        # Add test items
        item1 = MenuItem("Test Burger", "mains", Decimal("15.99"), "Test burger")
        item2 = MenuItem("Test Fries", "sides", Decimal("5.99"), "Test fries")

        order.add_item(item1, 1)
        order.add_item(item2, 2)

        # Generate receipt
        receipt_gen = ReceiptGenerator()
        receipt_text = receipt_gen.generate_receipt_text(order)

        assert "Test Customer" in receipt_text
        assert "Test Burger" in receipt_text
        assert "Test Fries" in receipt_text
        print("✓ Receipt generation successful")

        return True

    except Exception as e:
        print(f"✗ Receipt generation test failed: {e}")
        return False

def test_data_files():
    """Test that required data files exist and are properly formatted."""
    print("\nTesting data files...")

    try:
        data_dir = Path(__file__).parent / "restaurant_system" / "data"

        # Check required files exist
        required_files = [
            "menu_items.csv",
            "orders.csv",
            "sales_reports.csv"
        ]

        for filename in required_files:
            file_path = data_dir / filename
            assert file_path.exists(), f"Missing required file: {filename}"
            print(f"✓ {filename} exists")

        # Check menu items file has data
        menu_file = data_dir / "menu_items.csv"
        with open(menu_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) > 1, "Menu items file should have data"
            print(f"✓ Menu items file contains {len(lines)-1} items")

        return True

    except Exception as e:
        print(f"✗ Data files test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")

    try:
        from restaurant_system import config

        # Test basic config values
        assert config.APP_NAME == "Restaurant Order Management System"
        assert config.DEFAULT_TAX_RATE > 0
        assert config.RESTAURANT_INFO['name'] is not None
        print("✓ Configuration loaded successfully")

        # Test config functions
        restaurant_info = config.get_restaurant_info()
        assert isinstance(restaurant_info, dict)
        print("✓ Configuration functions working")

        return True

    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def run_all_tests():
    """Run all test functions."""
    print("=" * 60)
    print("Restaurant Order Management System - Component Tests")
    print("=" * 60)

    tests = [
        test_imports,
        test_configuration,
        test_data_files,
        test_data_models,
        test_validation,
        test_csv_operations,
        test_receipt_generation
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            success = test_func()
            if success:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test_func.__name__} crashed: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("🎉 All tests passed! System is ready for use.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

def main():
    """Main test function."""
    try:
        # Setup logging for tests
        logging.basicConfig(level=logging.WARNING)

        # Run tests
        success = run_all_tests()

        if success:
            print("\nYou can now run the restaurant system with confidence!")
            print("Use: python run_restaurant_system.py")
        else:
            print("\nPlease fix the issues before running the main application.")

        return 0 if success else 1

    except KeyboardInterrupt:
        print("\nTests interrupted by user.")
        return 1
    except Exception as e:
        print(f"Test framework error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())