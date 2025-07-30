"""
GUI package for Restaurant Order Management System.

This package contains all GUI components including the main window,
tabbed interfaces, and specialized widgets for restaurant operations.
"""

from .main_window import RestaurantMainWindow
from .menu_manager import MenuManagerTab
from .order_interface import OrderInterfaceTab
from .queue_display import QueueDisplayTab
from .reports import ReportsTab

__all__ = [
    'RestaurantMainWindow',
    'MenuManagerTab',
    'OrderInterfaceTab',
    'QueueDisplayTab',
    'ReportsTab'
]