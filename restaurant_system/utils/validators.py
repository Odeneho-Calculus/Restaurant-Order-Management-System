"""
Input validation utilities for Restaurant Order Management System.

This module provides comprehensive validation functions for all user inputs
and data integrity checks throughout the application.
"""

import re
from decimal import Decimal, InvalidOperation
from typing import Optional, Union, List, Tuple
from datetime import datetime


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class InputValidator:
    """
    Comprehensive input validation class for restaurant system.

    Provides static methods for validating various types of input data
    with detailed error messages and flexible validation rules.
    """

    # Regular expression patterns
    PHONE_PATTERN = re.compile(r'^[\+]?[1-9][\d\s\-\(\)]{7,15}$')
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    ALPHANUMERIC_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-\_]+$')

    @staticmethod
    def validate_required_string(value: str, field_name: str,
                               min_length: int = 1, max_length: int = 255) -> str:
        """
        Validate a required string field.

        Args:
            value (str): The string to validate
            field_name (str): Name of the field for error messages
            min_length (int): Minimum allowed length
            max_length (int): Maximum allowed length

        Returns:
            str: The validated and trimmed string

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")

        trimmed_value = value.strip()

        if len(trimmed_value) < min_length:
            raise ValidationError(f"{field_name} must be at least {min_length} characters long")

        if len(trimmed_value) > max_length:
            raise ValidationError(f"{field_name} must not exceed {max_length} characters")

        return trimmed_value

    @staticmethod
    def validate_optional_string(value: Optional[str], field_name: str,
                               max_length: int = 255) -> str:
        """
        Validate an optional string field.

        Args:
            value (Optional[str]): The string to validate
            field_name (str): Name of the field for error messages
            max_length (int): Maximum allowed length

        Returns:
            str: The validated and trimmed string (empty if None)

        Raises:
            ValidationError: If validation fails
        """
        if value is None:
            return ""

        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")

        trimmed_value = value.strip()

        if len(trimmed_value) > max_length:
            raise ValidationError(f"{field_name} must not exceed {max_length} characters")

        return trimmed_value

    @staticmethod
    def validate_price(value: Union[str, float, Decimal], field_name: str = "Price") -> Decimal:
        """
        Validate a price value.

        Args:
            value (Union[str, float, Decimal]): The price to validate
            field_name (str): Name of the field for error messages

        Returns:
            Decimal: The validated price with proper precision

        Raises:
            ValidationError: If validation fails
        """
        try:
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    raise ValidationError(f"{field_name} cannot be empty")

                # Remove currency symbols if present
                value = value.replace('$', '').replace(',', '')

            decimal_price = Decimal(str(value))

            if decimal_price < 0:
                raise ValidationError(f"{field_name} cannot be negative")

            if decimal_price > Decimal('9999.99'):
                raise ValidationError(f"{field_name} cannot exceed $9999.99")

            # Round to 2 decimal places
            return decimal_price.quantize(Decimal('0.01'))

        except (InvalidOperation, ValueError, TypeError):
            raise ValidationError(f"Invalid {field_name.lower()} format")

    @staticmethod
    def validate_quantity(value: Union[str, int], field_name: str = "Quantity") -> int:
        """
        Validate a quantity value.

        Args:
            value (Union[str, int]): The quantity to validate
            field_name (str): Name of the field for error messages

        Returns:
            int: The validated quantity

        Raises:
            ValidationError: If validation fails
        """
        try:
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    raise ValidationError(f"{field_name} cannot be empty")

            quantity = int(value)

            if quantity <= 0:
                raise ValidationError(f"{field_name} must be positive")

            if quantity > 999:
                raise ValidationError(f"{field_name} cannot exceed 999")

            return quantity

        except (ValueError, TypeError):
            raise ValidationError(f"Invalid {field_name.lower()} format")

    @staticmethod
    def validate_phone_number(value: Optional[str], required: bool = False) -> str:
        """
        Validate a phone number.

        Args:
            value (Optional[str]): The phone number to validate
            required (bool): Whether the phone number is required

        Returns:
            str: The validated phone number

        Raises:
            ValidationError: If validation fails
        """
        if not value or not value.strip():
            if required:
                raise ValidationError("Phone number is required")
            return ""

        phone = value.strip()

        # Remove common formatting characters for validation
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone)

        if not InputValidator.PHONE_PATTERN.match(phone):
            raise ValidationError("Invalid phone number format")

        if len(clean_phone) < 7 or len(clean_phone) > 15:
            raise ValidationError("Phone number must be between 7 and 15 digits")

        return phone

    @staticmethod
    def validate_email(value: Optional[str], required: bool = False) -> str:
        """
        Validate an email address.

        Args:
            value (Optional[str]): The email to validate
            required (bool): Whether the email is required

        Returns:
            str: The validated email address

        Raises:
            ValidationError: If validation fails
        """
        if not value or not value.strip():
            if required:
                raise ValidationError("Email address is required")
            return ""

        email = value.strip().lower()

        if not InputValidator.EMAIL_PATTERN.match(email):
            raise ValidationError("Invalid email address format")

        if len(email) > 254:  # RFC 5321 limit
            raise ValidationError("Email address is too long")

        return email

    @staticmethod
    def validate_table_number(value: Optional[str]) -> str:
        """
        Validate a table number.

        Args:
            value (Optional[str]): The table number to validate

        Returns:
            str: The validated table number

        Raises:
            ValidationError: If validation fails
        """
        if not value or not value.strip():
            return ""

        table_num = value.strip().upper()

        if not InputValidator.ALPHANUMERIC_PATTERN.match(table_num):
            raise ValidationError("Table number can only contain letters, numbers, spaces, hyphens, and underscores")

        if len(table_num) > 10:
            raise ValidationError("Table number cannot exceed 10 characters")

        return table_num

    @staticmethod
    def validate_category(value: str, valid_categories: List[str]) -> str:
        """
        Validate a category selection.

        Args:
            value (str): The category to validate
            valid_categories (List[str]): List of valid categories

        Returns:
            str: The validated category

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, str):
            raise ValidationError("Category must be a string")

        category = value.strip().lower()

        if not category:
            raise ValidationError("Category cannot be empty")

        valid_categories_lower = [cat.lower() for cat in valid_categories]

        if category not in valid_categories_lower:
            raise ValidationError(f"Category must be one of: {', '.join(valid_categories)}")

        return category

    @staticmethod
    def validate_tax_rate(value: Union[str, float, Decimal]) -> Decimal:
        """
        Validate a tax rate.

        Args:
            value (Union[str, float, Decimal]): The tax rate to validate

        Returns:
            Decimal: The validated tax rate

        Raises:
            ValidationError: If validation fails
        """
        try:
            if isinstance(value, str):
                value = value.strip().replace('%', '')
                if not value:
                    raise ValidationError("Tax rate cannot be empty")

            tax_rate = Decimal(str(value))

            # If the value is greater than 1, assume it's a percentage
            if tax_rate > 1:
                tax_rate = tax_rate / 100

            if tax_rate < 0:
                raise ValidationError("Tax rate cannot be negative")

            if tax_rate > 1:
                raise ValidationError("Tax rate cannot exceed 100%")

            return tax_rate.quantize(Decimal('0.0001'))  # 4 decimal places for precision

        except (InvalidOperation, ValueError, TypeError):
            raise ValidationError("Invalid tax rate format")

    @staticmethod
    def validate_date_string(value: str, date_format: str = "%Y-%m-%d") -> datetime:
        """
        Validate a date string.

        Args:
            value (str): The date string to validate
            date_format (str): Expected date format

        Returns:
            datetime: The validated date

        Raises:
            ValidationError: If validation fails
        """
        if not value or not value.strip():
            raise ValidationError("Date cannot be empty")

        try:
            return datetime.strptime(value.strip(), date_format)
        except ValueError:
            raise ValidationError(f"Invalid date format. Expected format: {date_format}")

    @staticmethod
    def validate_date_range(start_date: Optional[str], end_date: Optional[str],
                          date_format: str = "%Y-%m-%d") -> Tuple[Optional[datetime], Optional[datetime]]:
        """
        Validate a date range.

        Args:
            start_date (Optional[str]): Start date string
            end_date (Optional[str]): End date string
            date_format (str): Expected date format

        Returns:
            Tuple[Optional[datetime], Optional[datetime]]: Validated date range

        Raises:
            ValidationError: If validation fails
        """
        start_dt = None
        end_dt = None

        if start_date:
            start_dt = InputValidator.validate_date_string(start_date, date_format)

        if end_date:
            end_dt = InputValidator.validate_date_string(end_date, date_format)

        if start_dt and end_dt and start_dt > end_dt:
            raise ValidationError("Start date cannot be after end date")

        return start_dt, end_dt

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename for safe file system operations.

        Args:
            filename (str): The filename to sanitize

        Returns:
            str: The sanitized filename
        """
        if not filename:
            return "untitled"

        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        sanitized = filename

        for char in invalid_chars:
            sanitized = sanitized.replace(char, '_')

        # Remove leading/trailing dots and spaces
        sanitized = sanitized.strip('. ')

        # Limit length
        if len(sanitized) > 100:
            sanitized = sanitized[:100]

        # Ensure it's not empty after sanitization
        if not sanitized:
            sanitized = "untitled"

        return sanitized

    @staticmethod
    def validate_search_query(query: Optional[str], min_length: int = 1) -> str:
        """
        Validate a search query.

        Args:
            query (Optional[str]): The search query to validate
            min_length (int): Minimum query length

        Returns:
            str: The validated search query

        Raises:
            ValidationError: If validation fails
        """
        if not query or not query.strip():
            if min_length > 0:
                raise ValidationError(f"Search query must be at least {min_length} characters long")
            return ""

        query = query.strip()

        if len(query) < min_length:
            raise ValidationError(f"Search query must be at least {min_length} characters long")

        if len(query) > 100:
            raise ValidationError("Search query cannot exceed 100 characters")

        # Check for potential injection attempts (basic protection)
        dangerous_patterns = ['<script', 'javascript:', 'on(load|error|click)=']
        query_lower = query.lower()

        for pattern in dangerous_patterns:
            if pattern in query_lower:
                raise ValidationError("Invalid characters in search query")

        return query


class DataIntegrityValidator:
    """
    Validates data integrity and business rules.

    Provides methods for validating complex business logic and
    ensuring data consistency across the application.
    """

    @staticmethod
    def validate_order_consistency(order_data: dict) -> List[str]:
        """
        Validate order data consistency.

        Args:
            order_data (dict): Order data to validate

        Returns:
            List[str]: List of validation errors (empty if valid)
        """
        errors = []

        # Check required fields
        required_fields = ['order_id', 'timestamp', 'items']
        for field in required_fields:
            if field not in order_data or not order_data[field]:
                errors.append(f"Missing required field: {field}")

        # Validate order totals if present
        if 'items' in order_data and isinstance(order_data['items'], list):
            calculated_subtotal = sum(
                item.get('subtotal', 0) for item in order_data['items']
            )

            if 'subtotal' in order_data:
                reported_subtotal = order_data['subtotal']
                if abs(calculated_subtotal - reported_subtotal) > 0.01:
                    errors.append("Order subtotal does not match item totals")

        return errors

    @staticmethod
    def validate_menu_item_uniqueness(menu_items: List[dict]) -> List[str]:
        """
        Validate menu item uniqueness.

        Args:
            menu_items (List[dict]): List of menu item data

        Returns:
            List[str]: List of validation errors (empty if valid)
        """
        errors = []
        seen_ids = set()
        seen_names = set()

        for i, item in enumerate(menu_items):
            item_id = item.get('id')
            item_name = item.get('name', '').lower().strip()

            if item_id in seen_ids:
                errors.append(f"Duplicate menu item ID at position {i}: {item_id}")
            else:
                seen_ids.add(item_id)

            if item_name in seen_names:
                errors.append(f"Duplicate menu item name at position {i}: {item.get('name')}")
            else:
                seen_names.add(item_name)

        return errors