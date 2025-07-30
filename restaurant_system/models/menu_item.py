"""
MenuItem model for Restaurant Order Management System.

This module defines the MenuItem class that represents individual menu items
with comprehensive properties and validation.
"""

from decimal import Decimal, InvalidOperation
from typing import Optional
import uuid


class MenuItem:
    """
    Represents a menu item in the restaurant system.

    This class encapsulates all properties of a menu item including
    identification, categorization, pricing, and availability status.
    """

    # Valid categories for menu items
    VALID_CATEGORIES = {
        'appetizers', 'mains', 'desserts', 'beverages',
        'salads', 'soups', 'sides', 'specials'
    }

    def __init__(self, name: str, category: str, price: float,
                 description: str = "", item_id: Optional[str] = None,
                 is_available: bool = True):
        """
        Initialize a MenuItem instance.

        Args:
            name (str): The name of the menu item
            category (str): Category of the item (must be in VALID_CATEGORIES)
            price (float): Price of the item (must be positive)
            description (str, optional): Description of the item
            item_id (str, optional): Unique identifier (auto-generated if not provided)
            is_available (bool, optional): Availability status (default True)

        Raises:
            ValueError: If invalid parameters are provided
        """
        self._id = item_id or str(uuid.uuid4())
        self.name = name
        self.category = category
        self.price = price
        self.description = description
        self.is_available = is_available

    @property
    def id(self) -> str:
        """Get the unique identifier of the menu item."""
        return self._id

    @property
    def name(self) -> str:
        """Get the name of the menu item."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the menu item.

        Args:
            value (str): The name to set

        Raises:
            ValueError: If name is empty or contains only whitespace
        """
        if not value or not value.strip():
            raise ValueError("Menu item name cannot be empty")
        self._name = value.strip()

    @property
    def category(self) -> str:
        """Get the category of the menu item."""
        return self._category

    @category.setter
    def category(self, value: str) -> None:
        """
        Set the category of the menu item.

        Args:
            value (str): The category to set

        Raises:
            ValueError: If category is not in VALID_CATEGORIES
        """
        if value.lower() not in self.VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(self.VALID_CATEGORIES)}")
        self._category = value.lower()

    @property
    def price(self) -> Decimal:
        """Get the price of the menu item as Decimal for precision."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """
        Set the price of the menu item.

        Args:
            value (float): The price to set

        Raises:
            ValueError: If price is negative or invalid
        """
        try:
            decimal_price = Decimal(str(value))
            if decimal_price < 0:
                raise ValueError("Price cannot be negative")
            self._price = decimal_price.quantize(Decimal('0.01'))
        except (InvalidOperation, TypeError):
            raise ValueError("Invalid price format")

    @property
    def description(self) -> str:
        """Get the description of the menu item."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set the description of the menu item."""
        self._description = value.strip() if value else ""

    @property
    def is_available(self) -> bool:
        """Get the availability status of the menu item."""
        return self._is_available

    @is_available.setter
    def is_available(self, value: bool) -> None:
        """Set the availability status of the menu item."""
        self._is_available = bool(value)

    def to_dict(self) -> dict:
        """
        Convert the MenuItem to a dictionary representation.

        Returns:
            dict: Dictionary containing all menu item properties
        """
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': float(self.price),
            'description': self.description,
            'is_available': self.is_available
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'MenuItem':
        """
        Create a MenuItem instance from a dictionary.

        Args:
            data (dict): Dictionary containing menu item data

        Returns:
            MenuItem: New MenuItem instance

        Raises:
            KeyError: If required keys are missing
            ValueError: If data is invalid
        """
        return cls(
            item_id=data['id'],
            name=data['name'],
            category=data['category'],
            price=data['price'],
            description=data.get('description', ''),
            is_available=data.get('is_available', True)
        )

    def __str__(self) -> str:
        """Return string representation of the menu item."""
        status = "Available" if self.is_available else "Out of Stock"
        return f"{self.name} ({self.category.title()}) - ${self.price} [{status}]"

    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return (f"MenuItem(id='{self.id}', name='{self.name}', "
                f"category='{self.category}', price={self.price}, "
                f"is_available={self.is_available})")

    def __eq__(self, other) -> bool:
        """Check equality based on item ID."""
        if not isinstance(other, MenuItem):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Return hash based on item ID."""
        return hash(self.id)