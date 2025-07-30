"""
Configuration settings for Restaurant Order Management System.

This module contains all configurable settings for the restaurant
management system, including business rules, display preferences,
and operational parameters.
"""

from decimal import Decimal
from pathlib import Path

# Application Information
APP_NAME = "Restaurant Order Management System"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Professional restaurant order management solution"

# Restaurant Information (can be customized)
RESTAURANT_INFO = {
    'name': 'Gourmet Kitchen',
    'address': '123 Main Street',
    'city': 'Anytown',
    'state': 'ST',
    'zip_code': '12345',
    'phone': '(555) 123-4567',
    'email': 'info@gourmetkitchen.com',
    'website': 'www.gourmetkitchen.com'
}

# Tax Configuration
DEFAULT_TAX_RATE = Decimal('0.08')  # 8% default tax rate
TAX_LABEL = "Sales Tax"
ENABLE_TAX_CALCULATION = True

# Currency Settings
CURRENCY_SYMBOL = "$"
CURRENCY_DECIMAL_PLACES = 2

# File Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"
RECEIPTS_DIR = BASE_DIR / "receipts"
BACKUP_DIR = DATA_DIR / "backups"

# Data Files
MENU_ITEMS_FILE = DATA_DIR / "menu_items.csv"
ORDERS_FILE = DATA_DIR / "orders.csv"
SALES_REPORTS_FILE = DATA_DIR / "sales_reports.csv"

# Auto-save Settings
AUTO_SAVE_ENABLED = True
AUTO_SAVE_INTERVAL = 300000  # 5 minutes in milliseconds
BACKUP_RETENTION_HOURS = 168  # 1 week

# Order Settings
ORDER_ID_PREFIX = "ORD"
ORDER_ID_LENGTH = 8
MAX_SPECIAL_INSTRUCTIONS_LENGTH = 500

# Menu Settings
MENU_ID_PREFIX = "menu"
MENU_ID_LENGTH = 6
MAX_MENU_ITEM_NAME_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500

# Display Settings
WINDOW_TITLE = f"{RESTAURANT_INFO['name']} - {APP_NAME}"
WINDOW_SIZE = "1200x800"
WINDOW_MIN_SIZE = (1000, 700)

# GUI Theme Colors
THEME_COLORS = {
    'primary': '#2c3e50',      # Dark blue-gray
    'secondary': '#3498db',    # Blue
    'success': '#27ae60',      # Green
    'warning': '#f39c12',      # Orange
    'danger': '#e74c3c',       # Red
    'info': '#3498db',         # Light blue
    'light': '#ecf0f1',        # Light gray
    'dark': '#2c3e50'          # Dark gray
}

# Order Status Colors
STATUS_COLORS = {
    'pending': '#fff3cd',      # Light yellow
    'preparing': '#d1ecf1',    # Light blue
    'ready': '#d4edda',        # Light green
    'completed': '#f8f9fa',    # Light gray
    'cancelled': '#f8d7da'     # Light red
}

# Queue Refresh Settings
QUEUE_AUTO_REFRESH = True
QUEUE_REFRESH_INTERVAL = 30000  # 30 seconds

# Receipt Settings
RECEIPT_WIDTH = 80  # Characters
RECEIPT_PRINT_LOGO = True
RECEIPT_FOOTER_MESSAGE = "Thank you for your business!"

# Validation Settings
PHONE_REGEX = r'^[\+]?[1-9]?[\d\s\-\(\)]{10,15}$'
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PRICE_MIN = Decimal('0.01')
PRICE_MAX = Decimal('999.99')

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Performance Settings
MAX_ORDERS_IN_MEMORY = 1000
MAX_MENU_ITEMS = 500
SEARCH_DELAY_MS = 500  # Delay for search to avoid excessive filtering

# Development Settings
DEBUG_MODE = False
ENABLE_DETAILED_LOGGING = True
SHOW_SQL_QUERIES = False  # For future database integration

# Feature Flags
ENABLE_CUSTOMER_MANAGEMENT = True
ENABLE_INVENTORY_TRACKING = False  # Future feature
ENABLE_STAFF_MANAGEMENT = False    # Future feature
ENABLE_LOYALTY_PROGRAM = False     # Future feature
ENABLE_ONLINE_ORDERING = False     # Future feature

# Business Rules
MIN_ORDER_AMOUNT = Decimal('0.01')
MAX_ORDER_AMOUNT = Decimal('9999.99')
MAX_ITEMS_PER_ORDER = 99
MAX_QUANTITY_PER_ITEM = 99

# Report Settings
DEFAULT_REPORT_PERIOD_DAYS = 30
MAX_REPORT_RECORDS = 10000
ENABLE_CHART_GENERATION = False  # Future feature with matplotlib

# Printer Settings (for future implementation)
DEFAULT_PRINTER = "Default"
RECEIPT_PRINTER_DPI = 203
KITCHEN_PRINTER_ENABLED = False

# Database Settings (for future migration)
DATABASE_TYPE = "csv"  # csv, sqlite, postgresql, mysql
DATABASE_URL = None
CONNECTION_POOL_SIZE = 5

# API Settings (for future web integration)
API_ENABLED = False
API_PORT = 8000
API_HOST = "localhost"

# Security Settings
ENABLE_PASSWORD_PROTECTION = False  # Future feature
SESSION_TIMEOUT_MINUTES = 480  # 8 hours
ENABLE_AUDIT_LOG = True

# Backup Settings
BACKUP_FREQUENCY_HOURS = 24
MAX_BACKUP_FILES = 30
BACKUP_COMPRESSION = True

# Email Settings (for future notifications)
SMTP_SERVER = None
SMTP_PORT = 587
SMTP_USERNAME = None
SMTP_PASSWORD = None
ENABLE_EMAIL_NOTIFICATIONS = False

# Integration Settings (for future POS integration)
POS_INTEGRATION_ENABLED = False
POS_SYSTEM_TYPE = None
POS_API_KEY = None

def get_config(key: str, default=None):
    """Get configuration value by key."""
    return globals().get(key, default)

def update_config(key: str, value):
    """Update configuration value (for runtime changes)."""
    if key in globals():
        globals()[key] = value
        return True
    return False

def get_restaurant_info():
    """Get restaurant information for receipts and displays."""
    return RESTAURANT_INFO.copy()

def get_theme_colors():
    """Get theme color configuration."""
    return THEME_COLORS.copy()

def get_status_colors():
    """Get order status color configuration."""
    return STATUS_COLORS.copy()