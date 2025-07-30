"""
OrderItem model for Restaurant Order Management System.

This module defines the OrderItem class that represents individual items
within an order with quantity, special instructions, and pricing calculations.
"""

from decimal import Decimal
from typing import Optional
from .menu_item import MenuItem


class OrderItem:
    """
    Represents an item within an order.

    This class links a MenuItem with quantity and special instructions,
    providing automatic subtotal calculations and comprehensive data management.
    """

    def __init__(self, menu_item: MenuItem, quantity: int = 1,
                 special_instructions: str = ""):
        """
        Initialize an OrderItem instance.

        Args:
            menu_item (MenuItem): The menu item being ordered
            quantity (int, optional): Quantity of the item (default 1)
            special_instructions (str, optional): Special preparation instructions

        Raises:
            ValueError: If quantity is not positive
            TypeError: If menu_item is not a MenuItem instance
        """
        if not isinstance(menu_item, MenuItem):
            raise TypeError("menu_item must be a MenuItem instance")

        self._menu_item = menu_item
        self.quantity = quantity
        self.special_instructions = special_instructions

    @property
    def menu_item(self) -> MenuItem:
        """Get the associated menu item."""
        return self._menu_item

    @property
    def quantity(self) -> int:
        """Get the quantity of this item."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """
        Set the quantity of this item.

        Args:
            value (int): The quantity to set

        Raises:
            ValueError: If quantity is not positive
            TypeError: If quantity is not an integer
        """
        if not isinstance(value, int):
            raise TypeError("Quantity must be an integer")
        if value <= 0:
            raise ValueError("Quantity must be positive")
        self._quantity = value

    @property
    def special_instructions(self) -> str:
        """Get the special instructions for this item."""
        return self._special_instructions

    @special_instructions.setter
    def special_instructions(self, value: str) -> None:
        """Set the special instructions for this item."""
        self._special_instructions = value.strip() if value else ""

    @property
    def unit_price(self) -> Decimal:
        """Get the unit price from the associated menu item."""
        return self.menu_item.price

    @property
    def subtotal(self) -> Decimal:
        """
        Calculate the subtotal for this order item.

        Returns:
            Decimal: Quantity multiplied by unit price
        """
        return self.unit_price * Decimal(str(self.quantity))

    @property
    def item_name(self) -> str:
        """Get the name of the associated menu item."""
        return self.menu_item.name

    @property
    def item_category(self) -> str:
        """Get the category of the associated menu item."""
        return self.menu_item.category

    @property
    def item_id(self) -> str:
        """Get the ID of the associated menu item."""
        return self.menu_item.id

    def update_quantity(self, new_quantity: int) -> None:
        """
        Update the quantity of this order item.

        Args:
            new_quantity (int): The new quantity to set

        Raises:
            ValueError: If new_quantity is not positive
        """
        self.quantity = new_quantity

    def add_special_instruction(self, instruction: str) -> None:
        """
        Add or append to special instructions.

        Args:
            instruction (str): Instruction to add
        """
        if self.special_instructions:
            self.special_instructions += f"; {instruction.strip()}"
        else:
            self.special_instructions = instruction.strip()

    def clear_special_instructions(self) -> None:
        """Clear all special instructions."""
        self.special_instructions = ""

    def to_dict(self) -> dict:
        """
        Convert the OrderItem to a dictionary representation.

        Returns:
            dict: Dictionary containing all order item properties
        """
        return {
            'menu_item_id': self.menu_item.id,
            'menu_item_name': self.menu_item.name,
            'menu_item_category': self.menu_item.category,
            'unit_price': float(self.unit_price),
            'quantity': self.quantity,
            'special_instructions': self.special_instructions,
            'subtotal': float(self.subtotal)
        }

    @classmethod
    def from_dict(cls, data: dict, menu_item: MenuItem) -> 'OrderItem':
        """
        Create an OrderItem instance from a dictionary and menu item.

        Args:
            data (dict): Dictionary containing order item data
            menu_item (MenuItem): The associated menu item

        Returns:
            OrderItem: New OrderItem instance

        Raises:
            KeyError: If required keys are missing
            ValueError: If data is invalid
        """
        order_item = cls(
            menu_item=menu_item,
            quantity=data['quantity'],
            special_instructions=data.get('special_instructions', '')
        )
        return order_item

    def get_display_text(self) -> str:
        """
        Get formatted display text for the order item.

        Returns:
            str: Formatted text showing quantity, name, and price
        """
        base_text = f"{self.quantity}x {self.item_name} - ${self.subtotal:.2f}"
        if self.special_instructions:
            base_text += f" (Special: {self.special_instructions})"
        return base_text

    def is_same_item(self, other_menu_item: MenuItem,
                     other_instructions: str = "") -> bool:
        """
        Check if this order item matches another menu item and instructions.

        Args:
            other_menu_item (MenuItem): Menu item to compare
            other_instructions (str, optional): Instructions to compare

        Returns:
            bool: True if menu item and instructions match
        """
        return (self.menu_item == other_menu_item and
                self.special_instructions.lower().strip() ==
                other_instructions.lower().strip())

    def __str__(self) -> str:
        """Return string representation of the order item."""
        return self.get_display_text()

    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return (f"OrderItem(menu_item={self.menu_item.name}, "
                f"quantity={self.quantity}, subtotal=${self.subtotal})")

    def __eq__(self, other) -> bool:
        """Check equality based on menu item and special instructions."""
        if not isinstance(other, OrderItem):
            return False
        return (self.menu_item == other.menu_item and
                self.special_instructions == other.special_instructions)

    def __hash__(self) -> int:
        """Return hash based on menu item ID and special instructions."""
        return hash((self.menu_item.id, self.special_instructions))