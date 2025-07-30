"""
Restaurant Order Management System

A comprehensive restaurant management solution built with Python and Tkinter.

This package provides a complete restaurant order management system with
the following key features:

- Menu Management: Add, edit, and organize menu items
- Order Processing: Intuitive order taking interface
- Queue Monitoring: Real-time order status tracking
- Sales Reporting: Comprehensive analytics and reporting
- Receipt Generation: Professional receipt printing
- Data Persistence: CSV-based data storage with backup

The system is designed for real restaurant operations with professional
error handling, data validation, and user-friendly interfaces.

Usage:
    from restaurant_system.main import main
    main()

Or run directly:
    python -m restaurant_system.main
"""

__version__ = "1.0.0"
__author__ = "Restaurant Management System Development Team"
__email__ = "support@restaurant-system.com"
__license__ = "MIT"

# Package metadata
__title__ = "Restaurant Order Management System"
__description__ = "A comprehensive restaurant management solution"
__url__ = "https://github.com/restaurant-system/restaurant-management"

# Version info tuple
VERSION_INFO = tuple(int(part) for part in __version__.split('.'))

# Import main components for easier access
try:
    from .models import MenuItem, Order, OrderItem, OrderStatus, OrderType
    from .utils import CSVHandler, InputValidator, ReceiptGenerator
    from .gui import RestaurantMainWindow

    __all__ = [
        'MenuItem',
        'Order',
        'OrderItem',
        'OrderStatus',
        'OrderType',
        'CSVHandler',
        'InputValidator',
        'ReceiptGenerator',
        'RestaurantMainWindow'
    ]

except ImportError:
    # Handle import errors gracefully during setup
    __all__ = []


def get_version():
    """Return the version string."""
    return __version__


def get_version_info():
    """Return version info as a tuple."""
    return VERSION_INFO


def print_system_info():
    """Print system information."""
    import sys
    import platform

    print(f"{__title__} v{__version__}")
    print(f"Python: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()[0]}")


# System requirements check
def check_requirements():
    """Check if system requirements are met."""
    import sys

    requirements = {
        'python_version': (3, 8),
        'required_modules': [
            'tkinter',
            'csv',
            'json',
            'datetime',
            'decimal',
            'pathlib',
            'logging',
            'uuid',
            'shutil',
            're'
        ]
    }

    # Check Python version
    if sys.version_info < requirements['python_version']:
        return False, f"Python {'.'.join(map(str, requirements['python_version']))} or higher required"

    # Check required modules
    missing_modules = []
    for module in requirements['required_modules']:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        return False, f"Missing required modules: {', '.join(missing_modules)}"

    return True, "All requirements met"


# Development and debugging utilities
def enable_debug_logging():
    """Enable debug-level logging for development."""
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_sample_data():
    """Create sample data for testing and demonstration."""
    try:
        from .models import MenuItem

        # Sample menu items
        sample_items = [
            MenuItem("Caesar Salad", "appetizers", 12.99, "Fresh romaine with parmesan"),
            MenuItem("Grilled Chicken", "mains", 22.99, "Herb-seasoned chicken breast"),
            MenuItem("Chocolate Cake", "desserts", 8.99, "Rich chocolate layer cake"),
            MenuItem("Coffee", "beverages", 3.49, "Freshly brewed coffee")
        ]

        return sample_items

    except ImportError:
        return []


# Entry point for command-line usage
def cli_main():
    """Command-line interface main function."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        prog='restaurant-system',
        description=__description__
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'{__title__} {__version__}'
    )

    parser.add_argument(
        '--info',
        action='store_true',
        help='Show system information'
    )

    parser.add_argument(
        '--check-requirements',
        action='store_true',
        help='Check system requirements'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )

    args = parser.parse_args()

    if args.info:
        print_system_info()
        return

    if args.check_requirements:
        success, message = check_requirements()
        print(f"Requirements check: {message}")
        sys.exit(0 if success else 1)

    if args.debug:
        enable_debug_logging()

    # Import and run main application
    try:
        from .main import main
        sys.exit(main())
    except ImportError as e:
        print(f"Failed to import main application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli_main()