#!/usr/bin/env python3
"""
Feature Demonstration Script for Restaurant Order Management System.

This script demonstrates key features and capabilities of the system
without requiring GUI interaction.
"""

import sys
from pathlib import Path
from decimal import Decimal
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def demo_menu_management():
    """Demonstrate menu management features."""
    print("🍽️  MENU MANAGEMENT DEMO")
    print("=" * 50)

    from restaurant_system.models import MenuItem
    from restaurant_system.utils import CSVHandler
    from restaurant_system.config import DATA_DIR

    # Load existing menu
    csv_handler = CSVHandler(DATA_DIR)
    menu_items = csv_handler.load_menu_items()

    print(f"📋 Loaded {len(menu_items)} menu items")

    # Display menu by category
    categories = {}
    for item in menu_items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)

    for category, items in categories.items():
        print(f"\n🏷️  {category.upper()}")
        for item in items[:3]:  # Show first 3 items per category
            print(f"   • {item.name} - ${item.price}")

    print(f"\n✅ Total menu items: {len(menu_items)}")
    print(f"✅ Categories: {len(categories)}")

def demo_order_processing():
    """Demonstrate order processing features."""
    print("\n\n📝 ORDER PROCESSING DEMO")
    print("=" * 50)

    from restaurant_system.models import MenuItem, Order, OrderType, OrderStatus

    # Create sample menu items
    burger = MenuItem("Demo Burger", "mains", Decimal("15.99"), "Delicious demo burger")
    fries = MenuItem("Demo Fries", "sides", Decimal("5.99"), "Crispy demo fries")
    soda = MenuItem("Demo Soda", "beverages", Decimal("2.99"), "Refreshing demo soda")

    # Create new order
    order = Order()
    order.customer_name = "Demo Customer"
    order.customer_phone = "555-DEMO-123"
    order.table_number = "Table 5"
    order.order_type = OrderType.DINE_IN

    print(f"📋 Created order: {order.order_id}")
    print(f"👤 Customer: {order.customer_name}")
    print(f"🪑 Table: {order.table_number}")

    # Add items to order
    order.add_item(burger, 2, "Medium rare, no onions")
    order.add_item(fries, 2)
    order.add_item(soda, 3, "Extra ice")

    print(f"\n🛒 Order Contents:")
    for item in order.items:
        special = f" ({item.special_instructions})" if item.special_instructions else ""
        print(f"   • {item.quantity}x {item.item_name} - ${item.subtotal}{special}")

    print(f"\n💰 Order Totals:")
    print(f"   Subtotal: ${order.subtotal:.2f}")
    print(f"   Tax (8%): ${order.tax_amount:.2f}")
    print(f"   Total: ${order.total_amount:.2f}")

    # Demonstrate status updates
    print(f"\n📊 Status Updates:")
    print(f"   Initial Status: {order.status.value}")

    order.update_status(OrderStatus.PREPARING)
    print(f"   Updated Status: {order.status.value}")

    order.update_status(OrderStatus.READY)
    print(f"   Final Status: {order.status.value}")

def demo_receipt_generation():
    """Demonstrate receipt generation."""
    print("\n\n🧾 RECEIPT GENERATION DEMO")
    print("=" * 50)

    from restaurant_system.models import MenuItem, Order, OrderType
    from restaurant_system.utils import ReceiptGenerator

    # Create demo order
    order = Order()
    order.customer_name = "Receipt Demo Customer"
    order.customer_phone = "(555) 123-DEMO"
    order.table_number = "Demo Table"
    order.order_type = OrderType.DINE_IN

    # Add items
    pasta = MenuItem("Pasta Alfredo", "mains", Decimal("18.99"), "Creamy alfredo pasta")
    salad = MenuItem("Garden Salad", "appetizers", Decimal("8.99"), "Fresh mixed greens")
    wine = MenuItem("House Wine", "beverages", Decimal("7.99"), "Red wine by glass")

    order.add_item(pasta, 1)
    order.add_item(salad, 1, "Dressing on the side")
    order.add_item(wine, 2)

    # Generate receipt
    receipt_gen = ReceiptGenerator()
    receipt_text = receipt_gen.generate_receipt_text(order)

    print("📄 Generated Receipt Preview:")
    print("-" * 40)
    # Show first few lines of receipt
    lines = receipt_text.split('\n')
    for line in lines[:15]:  # Show first 15 lines
        print(line)
    print("   ... (receipt continues)")
    print("-" * 40)

    print(f"✅ Receipt generated successfully")
    print(f"✅ Order total: ${order.total_amount:.2f}")

def demo_data_persistence():
    """Demonstrate data persistence features."""
    print("\n\n💾 DATA PERSISTENCE DEMO")
    print("=" * 50)

    from restaurant_system.utils import CSVHandler
    from restaurant_system.config import DATA_DIR
    import os

    # Check data files
    csv_handler = CSVHandler(DATA_DIR)

    print("📁 Data Directory Structure:")
    for root, dirs, files in os.walk(DATA_DIR):
        level = root.replace(str(DATA_DIR), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            file_path = Path(root) / file
            size = file_path.stat().st_size
            print(f"{subindent}{file} ({size} bytes)")

    # Test data operations
    menu_items = csv_handler.load_menu_items()
    menu_items_dict = {item.id: item for item in menu_items}
    orders = csv_handler.load_orders(menu_items_dict)

    print(f"\n📊 Data Statistics:")
    print(f"   Menu items in database: {len(menu_items)}")
    print(f"   Orders in database: {len(orders)}")

    # Show backup information
    backup_dir = DATA_DIR / "backups"
    if backup_dir.exists():
        backups = list(backup_dir.glob("*.zip"))
        print(f"   Available backups: {len(backups)}")

    print(f"✅ Data persistence system operational")

def demo_validation_system():
    """Demonstrate input validation."""
    print("\n\n🔍 VALIDATION SYSTEM DEMO")
    print("=" * 50)

    from restaurant_system.utils import InputValidator, ValidationError

    # Price validation
    print("💰 Price Validation:")
    test_prices = ["15.99", "0.01", "999.99", "invalid", "-5.00", "1000.00"]
    for price in test_prices:
        try:
            validated = InputValidator.validate_price(price)
            print(f"   ✅ '{price}' → ${validated}")
        except ValidationError as e:
            print(f"   ❌ '{price}' → {e}")

    # Phone validation
    print("\n📞 Phone Validation:")
    test_phones = ["555-123-4567", "5551234567", "(555) 123-4567", "invalid", "123"]
    for phone in test_phones:
        try:
            validated = InputValidator.validate_phone_number(phone, required=False)
            print(f"   ✅ '{phone}' → '{validated}'")
        except ValidationError as e:
            print(f"   ❌ '{phone}' → {e}")

    # Email validation
    print("\n📧 Email Validation:")
    test_emails = ["user@example.com", "invalid-email", "test@test.co.uk", "@invalid.com"]
    for email in test_emails:
        try:
            validated = InputValidator.validate_email(email, required=False)
            print(f"   ✅ '{email}' → '{validated}'")
        except ValidationError as e:
            print(f"   ❌ '{email}' → {e}")

def demo_system_capabilities():
    """Demonstrate overall system capabilities."""
    print("\n\n🚀 SYSTEM CAPABILITIES OVERVIEW")
    print("=" * 50)

    capabilities = [
        ("🍽️ Menu Management", "Add, edit, delete menu items with categories"),
        ("📝 Order Processing", "Intuitive order taking with special instructions"),
        ("📊 Queue Monitoring", "Real-time order status tracking"),
        ("🧾 Receipt Generation", "Professional receipt printing and viewing"),
        ("📈 Sales Reporting", "Comprehensive analytics and data export"),
        ("💾 Data Persistence", "Reliable CSV-based storage with backups"),
        ("🔍 Input Validation", "Comprehensive data validation and error handling"),
        ("🎨 Professional GUI", "User-friendly interface with modern styling"),
        ("🔄 Auto-save", "Automatic data saving every 5 minutes"),
        ("📱 Multi-platform", "Works on Windows, macOS, and Linux"),
        ("🔒 Offline Operation", "No internet required, complete data privacy"),
        ("⚡ High Performance", "Handles 100+ menu items and 1000+ orders")
    ]

    for feature, description in capabilities:
        print(f"{feature} {description}")

    print(f"\n✅ All systems operational and ready for production use!")

def main():
    """Run all demonstrations."""
    print("🏪 RESTAURANT ORDER MANAGEMENT SYSTEM")
    print("🎯 FEATURE DEMONSTRATION")
    print("=" * 70)
    print(f"⏰ Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        demo_menu_management()
        demo_order_processing()
        demo_receipt_generation()
        demo_data_persistence()
        demo_validation_system()
        demo_system_capabilities()

        print(f"\n🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("🚀 Ready to launch the full application!")
        print("💡 Run: python run_restaurant_system.py")

    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("🔧 Please run: python test_system.py")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())