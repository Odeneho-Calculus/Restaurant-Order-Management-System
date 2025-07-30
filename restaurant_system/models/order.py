"""
Order model for Restaurant Order Management System.

This module defines the Order class that represents complete customer orders
with comprehensive status tracking, customer information, and financial calculations.
"""

from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid

from .order_item import OrderItem
from .menu_item import MenuItem


class OrderStatus(Enum):
    """Enumeration of possible order statuses."""
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderType(Enum):
    """Enumeration of order types."""
    DINE_IN = "dine_in"
    TAKEOUT = "takeout"
    DELIVERY = "delivery"


class Order:
    """
    Represents a complete customer order.

    This class encompasses all aspects of an order including items, customer
    information, status tracking, and comprehensive financial calculations.
    """

    # Default tax rate (configurable)
    DEFAULT_TAX_RATE = Decimal('0.08')  # 8%

    def __init__(self, customer_name: str = "", customer_phone: str = "",
                 table_number: str = "", order_type: OrderType = OrderType.DINE_IN,
                 order_id: Optional[str] = None, tax_rate: Optional[Decimal] = None):
        """
        Initialize an Order instance.

        Args:
            customer_name (str, optional): Name of the customer
            customer_phone (str, optional): Customer's phone number
            table_number (str, optional): Table number for dine-in orders
            order_type (OrderType, optional): Type of order (default DINE_IN)
            order_id (str, optional): Unique identifier (auto-generated if not provided)
            tax_rate (Decimal, optional): Tax rate to apply (default DEFAULT_TAX_RATE)
        """
        self._order_id = order_id or self._generate_order_id()
        self._timestamp = datetime.now(timezone.utc)
        self._items: List[OrderItem] = []
        self._status = OrderStatus.PENDING
        self._status_history: List[Dict[str, Any]] = []

        # Customer information
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.table_number = table_number
        self.order_type = order_type

        # Financial settings
        self._tax_rate = tax_rate or self.DEFAULT_TAX_RATE

        # Priority and notes
        self._is_priority = False
        self._notes = ""

        # Track status change
        self._add_status_change(OrderStatus.PENDING)

    @staticmethod
    def _generate_order_id() -> str:
        """Generate a unique order ID with timestamp prefix."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        unique_suffix = str(uuid.uuid4())[:8].upper()
        return f"ORD-{timestamp}-{unique_suffix}"

    @property
    def order_id(self) -> str:
        """Get the unique order identifier."""
        return self._order_id

    @property
    def timestamp(self) -> datetime:
        """Get the order creation timestamp."""
        return self._timestamp

    @property
    def items(self) -> List[OrderItem]:
        """Get a copy of the order items list."""
        return self._items.copy()

    @property
    def status(self) -> OrderStatus:
        """Get the current order status."""
        return self._status

    @property
    def status_history(self) -> List[Dict[str, Any]]:
        """Get the complete status change history."""
        return self._status_history.copy()

    @property
    def tax_rate(self) -> Decimal:
        """Get the tax rate for this order."""
        return self._tax_rate

    @tax_rate.setter
    def tax_rate(self, value: Decimal) -> None:
        """
        Set the tax rate for this order.

        Args:
            value (Decimal): Tax rate to set (between 0 and 1)

        Raises:
            ValueError: If tax rate is negative or greater than 1
        """
        if value < 0 or value > 1:
            raise ValueError("Tax rate must be between 0 and 1")
        self._tax_rate = value

    @property
    def is_priority(self) -> bool:
        """Get the priority status of this order."""
        return self._is_priority

    @is_priority.setter
    def is_priority(self, value: bool) -> None:
        """Set the priority status of this order."""
        self._is_priority = bool(value)

    @property
    def notes(self) -> str:
        """Get the order notes."""
        return self._notes

    @notes.setter
    def notes(self, value: str) -> None:
        """Set the order notes."""
        self._notes = value.strip() if value else ""

    def add_item(self, menu_item: MenuItem, quantity: int = 1,
                 special_instructions: str = "") -> OrderItem:
        """
        Add an item to the order.

        Args:
            menu_item (MenuItem): The menu item to add
            quantity (int, optional): Quantity to add (default 1)
            special_instructions (str, optional): Special instructions

        Returns:
            OrderItem: The added order item

        Raises:
            ValueError: If menu item is not available or quantity is invalid
        """
        if not menu_item.is_available:
            raise ValueError(f"Menu item '{menu_item.name}' is not available")

        # Check if same item with same instructions already exists
        existing_item = self._find_matching_item(menu_item, special_instructions)
        if existing_item:
            existing_item.quantity += quantity
            return existing_item
        else:
            new_item = OrderItem(menu_item, quantity, special_instructions)
            self._items.append(new_item)
            return new_item

    def remove_item(self, order_item: OrderItem) -> bool:
        """
        Remove an item from the order.

        Args:
            order_item (OrderItem): The order item to remove

        Returns:
            bool: True if item was removed, False if not found
        """
        try:
            self._items.remove(order_item)
            return True
        except ValueError:
            return False

    def update_item_quantity(self, order_item: OrderItem, new_quantity: int) -> bool:
        """
        Update the quantity of an existing order item.

        Args:
            order_item (OrderItem): The order item to update
            new_quantity (int): The new quantity

        Returns:
            bool: True if updated successfully, False if item not found

        Raises:
            ValueError: If new_quantity is not positive
        """
        if order_item in self._items:
            if new_quantity <= 0:
                return self.remove_item(order_item)
            else:
                order_item.quantity = new_quantity
                return True
        return False

    def clear_items(self) -> None:
        """Remove all items from the order."""
        self._items.clear()

    def update_status(self, new_status: OrderStatus) -> None:
        """
        Update the order status and record the change.

        Args:
            new_status (OrderStatus): The new status to set

        Raises:
            ValueError: If status transition is invalid
        """
        if new_status == self._status:
            return  # No change needed

        # Validate status transition (basic validation)
        if self._status == OrderStatus.CANCELLED and new_status != OrderStatus.CANCELLED:
            raise ValueError("Cannot change status of a cancelled order")

        old_status = self._status
        self._status = new_status
        self._add_status_change(new_status, old_status)

    def cancel_order(self, reason: str = "") -> None:
        """
        Cancel the order with optional reason.

        Args:
            reason (str, optional): Reason for cancellation
        """
        old_status = self._status
        self._status = OrderStatus.CANCELLED
        self._add_status_change(OrderStatus.CANCELLED, old_status, {"reason": reason})

    def _add_status_change(self, new_status: OrderStatus,
                          old_status: Optional[OrderStatus] = None,
                          metadata: Optional[Dict[str, Any]] = None) -> None:
        """Record a status change in the history."""
        change_record = {
            "timestamp": datetime.now(timezone.utc),
            "old_status": old_status.value if old_status else None,
            "new_status": new_status.value,
            "metadata": metadata or {}
        }
        self._status_history.append(change_record)

    def _find_matching_item(self, menu_item: MenuItem,
                           special_instructions: str = "") -> Optional[OrderItem]:
        """Find an existing order item that matches the menu item and instructions."""
        for item in self._items:
            if item.is_same_item(menu_item, special_instructions):
                return item
        return None

    @property
    def subtotal(self) -> Decimal:
        """Calculate the subtotal of all items in the order."""
        return sum(item.subtotal for item in self._items)

    @property
    def tax_amount(self) -> Decimal:
        """Calculate the tax amount for the order."""
        return (self.subtotal * self._tax_rate).quantize(Decimal('0.01'))

    @property
    def total_amount(self) -> Decimal:
        """Calculate the total amount including tax."""
        return self.subtotal + self.tax_amount

    @property
    def item_count(self) -> int:
        """Get the total number of items in the order."""
        return sum(item.quantity for item in self._items)

    @property
    def is_empty(self) -> bool:
        """Check if the order has no items."""
        return len(self._items) == 0

    def get_items_by_category(self) -> Dict[str, List[OrderItem]]:
        """
        Group order items by category.

        Returns:
            Dict[str, List[OrderItem]]: Items grouped by category
        """
        categories = {}
        for item in self._items:
            category = item.item_category
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        return categories

    def get_preparation_time_estimate(self) -> int:
        """
        Estimate preparation time in minutes based on items.

        Returns:
            int: Estimated preparation time in minutes
        """
        # Basic estimation logic (can be enhanced based on item types)
        base_time = 5  # Base preparation time
        item_time = len(self._items) * 2  # 2 minutes per unique item
        quantity_time = self.item_count * 0.5  # 30 seconds per item quantity

        total_time = base_time + item_time + quantity_time

        # Add priority adjustment
        if self.is_priority:
            total_time *= 0.8  # Reduce time for priority orders

        return max(5, int(total_time))  # Minimum 5 minutes

    def to_dict(self) -> dict:
        """
        Convert the Order to a dictionary representation.

        Returns:
            dict: Dictionary containing all order properties
        """
        return {
            'order_id': self.order_id,
            'timestamp': self.timestamp.isoformat(),
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'table_number': self.table_number,
            'order_type': self.order_type.value,
            'status': self.status.value,
            'is_priority': self.is_priority,
            'notes': self.notes,
            'tax_rate': float(self.tax_rate),
            'items': [item.to_dict() for item in self._items],
            'subtotal': float(self.subtotal),
            'tax_amount': float(self.tax_amount),
            'total_amount': float(self.total_amount),
            'status_history': self.status_history
        }

    def get_receipt_data(self) -> dict:
        """
        Get formatted data for receipt generation.

        Returns:
            dict: Receipt-ready data
        """
        return {
            'order_id': self.order_id,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'customer_name': self.customer_name or "Guest",
            'customer_phone': self.customer_phone,
            'table_number': self.table_number,
            'order_type': self.order_type.value.replace('_', ' ').title(),
            'items': [
                {
                    'name': item.item_name,
                    'quantity': item.quantity,
                    'unit_price': float(item.unit_price),
                    'subtotal': float(item.subtotal),
                    'special_instructions': item.special_instructions
                }
                for item in self._items
            ],
            'subtotal': float(self.subtotal),
            'tax_rate': float(self.tax_rate * 100),  # Convert to percentage
            'tax_amount': float(self.tax_amount),
            'total_amount': float(self.total_amount),
            'item_count': self.item_count
        }

    def __str__(self) -> str:
        """Return string representation of the order."""
        status_display = self.status.value.title()
        customer_info = self.customer_name or "Guest"
        return f"Order {self.order_id} - {customer_info} - {status_display} - ${self.total_amount:.2f}"

    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return (f"Order(order_id='{self.order_id}', status={self.status.value}, "
                f"items={len(self._items)}, total=${self.total_amount})")

    def __len__(self) -> int:
        """Return the number of items in the order."""
        return len(self._items)