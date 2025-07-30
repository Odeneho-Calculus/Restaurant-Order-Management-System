"""
CSV Handler for Restaurant Order Management System.

This module provides comprehensive CSV operations for data persistence
with robust error handling and data validation.
"""

import os
import csv
import shutil
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path
import logging

from ..models import MenuItem, Order, OrderItem, OrderStatus, OrderType


class CSVHandler:
    """
    Handles all CSV operations for the restaurant system.

    Provides methods for reading, writing, and managing CSV data files
    with comprehensive error handling and backup functionality.
    """

    def __init__(self, data_directory: str):
        """
        Initialize the CSV handler with data directory.

        Args:
            data_directory (str): Path to the data directory
        """
        self.data_dir = Path(data_directory)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Define file paths
        self.menu_file = self.data_dir / "menu_items.csv"
        self.orders_file = self.data_dir / "orders.csv"
        self.sales_file = self.data_dir / "sales_reports.csv"

        # Backup directory
        self.backup_dir = self.data_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)

        # Initialize logger
        self.logger = logging.getLogger(__name__)

        # Initialize CSV files if they don't exist
        self._initialize_csv_files()

    def _initialize_csv_files(self) -> None:
        """Initialize CSV files with headers if they don't exist."""
        # Menu items CSV headers
        menu_headers = [
            'id', 'name', 'category', 'price', 'description', 'is_available'
        ]

        # Orders CSV headers
        order_headers = [
            'order_id', 'timestamp', 'customer_name', 'customer_phone',
            'table_number', 'order_type', 'status', 'is_priority', 'notes',
            'tax_rate', 'subtotal', 'tax_amount', 'total_amount', 'items_json'
        ]

        # Sales reports CSV headers
        sales_headers = [
            'date', 'order_id', 'customer_name', 'order_type', 'status',
            'subtotal', 'tax_amount', 'total_amount', 'items_count'
        ]

        # Initialize files with headers
        self._create_csv_if_not_exists(self.menu_file, menu_headers)
        self._create_csv_if_not_exists(self.orders_file, order_headers)
        self._create_csv_if_not_exists(self.sales_file, sales_headers)

    def _create_csv_if_not_exists(self, file_path: Path, headers: List[str]) -> None:
        """Create CSV file with headers if it doesn't exist."""
        if not file_path.exists():
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                self.logger.info(f"Created CSV file: {file_path}")
            except Exception as e:
                self.logger.error(f"Failed to create CSV file {file_path}: {e}")
                raise

    def create_backup(self, file_path: Path) -> Optional[Path]:
        """
        Create a backup of the specified file.

        Args:
            file_path (Path): Path to the file to backup

        Returns:
            Optional[Path]: Path to the backup file, None if backup failed
        """
        if not file_path.exists():
            return None

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_{timestamp}.csv"
            backup_path = self.backup_dir / backup_name

            shutil.copy2(file_path, backup_path)
            self.logger.info(f"Created backup: {backup_path}")
            return backup_path
        except Exception as e:
            self.logger.error(f"Failed to create backup for {file_path}: {e}")
            return None

    def safe_write_csv(self, file_path: Path, data: List[Dict[str, Any]],
                      headers: List[str]) -> bool:
        """
        Safely write data to CSV file with backup and validation.

        Args:
            file_path (Path): Path to the CSV file
            data (List[Dict[str, Any]]): Data to write
            headers (List[str]): CSV headers

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create backup if file exists
            if file_path.exists():
                self.create_backup(file_path)

            # Write to temporary file first
            temp_file = file_path.with_suffix('.tmp')

            with open(temp_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)

            # Replace original file with temporary file
            shutil.move(temp_file, file_path)
            self.logger.info(f"Successfully wrote {len(data)} records to {file_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to write CSV file {file_path}: {e}")
            # Clean up temporary file if it exists
            temp_file = file_path.with_suffix('.tmp')
            if temp_file.exists():
                temp_file.unlink()
            return False

    def read_csv_safe(self, file_path: Path,
                     row_processor: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """
        Safely read CSV file with error handling.

        Args:
            file_path (Path): Path to the CSV file
            row_processor (Callable, optional): Function to process each row

        Returns:
            List[Dict[str, Any]]: List of CSV rows as dictionaries
        """
        data = []

        if not file_path.exists():
            self.logger.warning(f"CSV file does not exist: {file_path}")
            return data

        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                    try:
                        if row_processor:
                            processed_row = row_processor(row)
                            if processed_row is not None:
                                data.append(processed_row)
                        else:
                            data.append(row)
                    except Exception as e:
                        self.logger.warning(f"Error processing row {row_num} in {file_path}: {e}")
                        continue

            self.logger.info(f"Successfully read {len(data)} records from {file_path}")
            return data

        except Exception as e:
            self.logger.error(f"Failed to read CSV file {file_path}: {e}")
            return []

    def save_menu_items(self, menu_items: List[MenuItem]) -> bool:
        """
        Save menu items to CSV file.

        Args:
            menu_items (List[MenuItem]): List of menu items to save

        Returns:
            bool: True if successful, False otherwise
        """
        headers = ['id', 'name', 'category', 'price', 'description', 'is_available']
        data = [item.to_dict() for item in menu_items]
        return self.safe_write_csv(self.menu_file, data, headers)

    def load_menu_items(self) -> List[MenuItem]:
        """
        Load menu items from CSV file.

        Returns:
            List[MenuItem]: List of loaded menu items
        """
        def process_menu_row(row: Dict[str, str]) -> Optional[Dict[str, Any]]:
            try:
                return {
                    'id': row['id'],
                    'name': row['name'],
                    'category': row['category'],
                    'price': float(row['price']),
                    'description': row['description'],
                    'is_available': row['is_available'].lower() == 'true'
                }
            except (ValueError, KeyError) as e:
                self.logger.warning(f"Invalid menu item row: {e}")
                return None

        data = self.read_csv_safe(self.menu_file, process_menu_row)
        menu_items = []

        for item_data in data:
            try:
                menu_item = MenuItem.from_dict(item_data)
                menu_items.append(menu_item)
            except Exception as e:
                self.logger.warning(f"Failed to create MenuItem from data: {e}")
                continue

        return menu_items

    def save_orders(self, orders: List[Order]) -> bool:
        """
        Save orders to CSV file.

        Args:
            orders (List[Order]): List of orders to save

        Returns:
            bool: True if successful, False otherwise
        """
        import json

        headers = [
            'order_id', 'timestamp', 'customer_name', 'customer_phone',
            'table_number', 'order_type', 'status', 'is_priority', 'notes',
            'tax_rate', 'subtotal', 'tax_amount', 'total_amount', 'items_json'
        ]

        data = []
        for order in orders:
            order_dict = order.to_dict()
            # Convert items to JSON string for CSV storage
            order_dict['items_json'] = json.dumps(order_dict['items'])
            del order_dict['items']  # Remove the original items list
            del order_dict['status_history']  # Remove status history for CSV
            data.append(order_dict)

        return self.safe_write_csv(self.orders_file, data, headers)

    def load_orders(self, menu_items_dict: Dict[str, MenuItem]) -> List[Order]:
        """
        Load orders from CSV file.

        Args:
            menu_items_dict (Dict[str, MenuItem]): Dictionary of menu items by ID

        Returns:
            List[Order]: List of loaded orders
        """
        import json

        def process_order_row(row: Dict[str, str]) -> Optional[Dict[str, Any]]:
            try:
                return {
                    'order_id': row['order_id'],
                    'timestamp': row['timestamp'],
                    'customer_name': row['customer_name'],
                    'customer_phone': row['customer_phone'],
                    'table_number': row['table_number'],
                    'order_type': row['order_type'],
                    'status': row['status'],
                    'is_priority': row['is_priority'].lower() == 'true',
                    'notes': row['notes'],
                    'tax_rate': Decimal(row['tax_rate']),
                    'items_json': row['items_json']
                }
            except (ValueError, KeyError) as e:
                self.logger.warning(f"Invalid order row: {e}")
                return None

        data = self.read_csv_safe(self.orders_file, process_order_row)
        orders = []

        for order_data in data:
            try:
                # Create order instance
                order = Order(
                    customer_name=order_data['customer_name'],
                    customer_phone=order_data['customer_phone'],
                    table_number=order_data['table_number'],
                    order_type=OrderType(order_data['order_type']),
                    order_id=order_data['order_id']
                )

                # Set additional properties
                order.is_priority = order_data['is_priority']
                order.notes = order_data['notes']
                order.tax_rate = order_data['tax_rate']

                # Parse and add items
                items_data = json.loads(order_data['items_json'])
                for item_data in items_data:
                    menu_item_id = item_data['menu_item_id']
                    if menu_item_id in menu_items_dict:
                        menu_item = menu_items_dict[menu_item_id]
                        order.add_item(
                            menu_item,
                            item_data['quantity'],
                            item_data.get('special_instructions', '')
                        )

                # Set order status
                order.update_status(OrderStatus(order_data['status']))

                orders.append(order)

            except Exception as e:
                self.logger.warning(f"Failed to create Order from data: {e}")
                continue

        return orders

    def append_sales_record(self, order: Order) -> bool:
        """
        Append a sales record to the sales CSV file.

        Args:
            order (Order): Order to record as a sale

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            sales_data = {
                'date': order.timestamp.strftime('%Y-%m-%d'),
                'order_id': order.order_id,
                'customer_name': order.customer_name or 'Guest',
                'order_type': order.order_type.value,
                'status': order.status.value,
                'subtotal': float(order.subtotal),
                'tax_amount': float(order.tax_amount),
                'total_amount': float(order.total_amount),
                'items_count': order.item_count
            }

            # Append to sales file
            with open(self.sales_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=list(sales_data.keys()))
                writer.writerow(sales_data)

            self.logger.info(f"Added sales record for order {order.order_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to append sales record: {e}")
            return False

    def load_sales_data(self, start_date: Optional[str] = None,
                       end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load sales data with optional date filtering.

        Args:
            start_date (str, optional): Start date in YYYY-MM-DD format
            end_date (str, optional): End date in YYYY-MM-DD format

        Returns:
            List[Dict[str, Any]]: List of sales records
        """
        def process_sales_row(row: Dict[str, str]) -> Optional[Dict[str, Any]]:
            try:
                record_date = row['date']

                # Apply date filtering if specified
                if start_date and record_date < start_date:
                    return None
                if end_date and record_date > end_date:
                    return None

                return {
                    'date': record_date,
                    'order_id': row['order_id'],
                    'customer_name': row['customer_name'],
                    'order_type': row['order_type'],
                    'status': row['status'],
                    'subtotal': float(row['subtotal']),
                    'tax_amount': float(row['tax_amount']),
                    'total_amount': float(row['total_amount']),
                    'items_count': int(row['items_count'])
                }
            except (ValueError, KeyError) as e:
                self.logger.warning(f"Invalid sales row: {e}")
                return None

        return self.read_csv_safe(self.sales_file, process_sales_row)

    def cleanup_old_backups(self, max_backups: int = 10) -> None:
        """
        Clean up old backup files, keeping only the most recent ones.

        Args:
            max_backups (int): Maximum number of backups to keep per file type
        """
        try:
            backup_files = list(self.backup_dir.glob("*.csv"))

            # Group backups by file type
            backup_groups = {}
            for backup_file in backup_files:
                file_type = backup_file.name.split('_')[0]  # Get prefix before timestamp
                if file_type not in backup_groups:
                    backup_groups[file_type] = []
                backup_groups[file_type].append(backup_file)

            # Sort and remove old backups for each file type
            for file_type, files in backup_groups.items():
                files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

                if len(files) > max_backups:
                    for old_file in files[max_backups:]:
                        old_file.unlink()
                        self.logger.info(f"Removed old backup: {old_file}")

        except Exception as e:
            self.logger.error(f"Failed to cleanup old backups: {e}")