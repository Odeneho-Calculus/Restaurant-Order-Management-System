"""
Receipt generator for Restaurant Order Management System.

This module provides comprehensive receipt generation functionality
with professional formatting and multiple output options.
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

from ..models import Order


class ReceiptGenerator:
    """
    Generates professional receipts for restaurant orders.

    Supports multiple output formats and customizable restaurant information
    with comprehensive formatting options and error handling.
    """

    def __init__(self, restaurant_info: Optional[Dict[str, str]] = None):
        """
        Initialize the receipt generator with restaurant information.

        Args:
            restaurant_info (Dict[str, str], optional): Restaurant details
        """
        self.restaurant_info = restaurant_info or self._get_default_restaurant_info()
        self.logger = logging.getLogger(__name__)

        # Receipt formatting settings
        self.width = 48  # Character width for receipt
        self.separator_char = "-"
        self.double_separator_char = "="

        # Receipt counter for numbering
        self._receipt_counter = 1000

    def _get_default_restaurant_info(self) -> Dict[str, str]:
        """Get default restaurant information."""
        return {
            "name": "Restaurant Management System",
            "address_line1": "123 Main Street",
            "address_line2": "City, State 12345",
            "phone": "(555) 123-4567",
            "email": "info@restaurant.com",
            "website": "www.restaurant.com",
            "tax_id": "TAX ID: 123-456-789"
        }

    def set_restaurant_info(self, restaurant_info: Dict[str, str]) -> None:
        """
        Update restaurant information.

        Args:
            restaurant_info (Dict[str, str]): New restaurant details
        """
        self.restaurant_info.update(restaurant_info)

    def generate_receipt_text(self, order: Order, receipt_number: Optional[str] = None) -> str:
        """
        Generate a formatted text receipt for an order.

        Args:
            order (Order): The order to generate receipt for
            receipt_number (str, optional): Custom receipt number

        Returns:
            str: Formatted receipt text
        """
        try:
            receipt_data = order.get_receipt_data()
            receipt_num = receipt_number or self._generate_receipt_number()

            lines = []

            # Header section
            lines.extend(self._generate_header(receipt_num))
            lines.append("")

            # Order information
            lines.extend(self._generate_order_info(receipt_data))
            lines.append("")

            # Items section
            lines.extend(self._generate_items_section(receipt_data))
            lines.append("")

            # Totals section
            lines.extend(self._generate_totals_section(receipt_data))
            lines.append("")

            # Footer section
            lines.extend(self._generate_footer())

            return "\n".join(lines)

        except Exception as e:
            self.logger.error(f"Failed to generate receipt for order {order.order_id}: {e}")
            return f"Error generating receipt: {e}"

    def _generate_header(self, receipt_number: str) -> List[str]:
        """Generate the receipt header section."""
        lines = []

        # Restaurant name (centered)
        name = self.restaurant_info.get("name", "Restaurant")
        lines.append(self._center_text(name.upper()))

        # Address information (centered)
        if "address_line1" in self.restaurant_info:
            lines.append(self._center_text(self.restaurant_info["address_line1"]))
        if "address_line2" in self.restaurant_info:
            lines.append(self._center_text(self.restaurant_info["address_line2"]))

        # Contact information (centered)
        if "phone" in self.restaurant_info:
            lines.append(self._center_text(f"Phone: {self.restaurant_info['phone']}"))
        if "email" in self.restaurant_info:
            lines.append(self._center_text(self.restaurant_info["email"]))

        # Separator
        lines.append(self.double_separator_char * self.width)

        # Receipt information
        lines.append(f"Receipt #: {receipt_number}")
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return lines

    def _generate_order_info(self, receipt_data: Dict[str, Any]) -> List[str]:
        """Generate the order information section."""
        lines = []

        lines.append(f"Order ID: {receipt_data['order_id']}")
        lines.append(f"Order Time: {receipt_data['timestamp']}")

        if receipt_data.get('customer_name'):
            lines.append(f"Customer: {receipt_data['customer_name']}")

        if receipt_data.get('customer_phone'):
            lines.append(f"Phone: {receipt_data['customer_phone']}")

        if receipt_data.get('table_number'):
            lines.append(f"Table: {receipt_data['table_number']}")

        lines.append(f"Order Type: {receipt_data['order_type']}")

        return lines

    def _generate_items_section(self, receipt_data: Dict[str, Any]) -> List[str]:
        """Generate the items section of the receipt."""
        lines = []

        lines.append(self.separator_char * self.width)
        lines.append("ITEMS")
        lines.append(self.separator_char * self.width)

        # Column headers
        header = f"{'Item':<20} {'Qty':<4} {'Price':<8} {'Total':<8}"
        lines.append(header)
        lines.append("-" * len(header))

        # Items
        for item in receipt_data['items']:
            name = item['name']
            if len(name) > 20:
                name = name[:17] + "..."

            qty = str(item['quantity'])
            unit_price = f"${item['unit_price']:.2f}"
            subtotal = f"${item['subtotal']:.2f}"

            item_line = f"{name:<20} {qty:<4} {unit_price:<8} {subtotal:<8}"
            lines.append(item_line)

            # Add special instructions if present
            if item.get('special_instructions'):
                instructions = item['special_instructions']
                if len(instructions) > 40:
                    instructions = instructions[:37] + "..."
                lines.append(f"  * {instructions}")

        return lines

    def _generate_totals_section(self, receipt_data: Dict[str, Any]) -> List[str]:
        """Generate the totals section of the receipt."""
        lines = []

        lines.append(self.separator_char * self.width)

        # Subtotal
        subtotal_line = f"{'Subtotal:':<30} ${receipt_data['subtotal']:>10.2f}"
        lines.append(subtotal_line)

        # Tax
        tax_rate = receipt_data['tax_rate']
        tax_amount = receipt_data['tax_amount']
        tax_line = f"{'Tax (' + f'{tax_rate:.1f}%' + '):':<30} ${tax_amount:>10.2f}"
        lines.append(tax_line)

        # Total
        lines.append(self.separator_char * self.width)
        total_line = f"{'TOTAL:':<30} ${receipt_data['total_amount']:>10.2f}"
        lines.append(total_line)
        lines.append(self.double_separator_char * self.width)

        # Item count
        item_count = receipt_data['item_count']
        count_line = f"Total Items: {item_count}"
        lines.append(count_line)

        return lines

    def _generate_footer(self) -> List[str]:
        """Generate the receipt footer section."""
        lines = []

        # Thank you message
        lines.append("")
        lines.append(self._center_text("Thank you for your business!"))
        lines.append(self._center_text("Please come again!"))

        # Tax ID if available
        if "tax_id" in self.restaurant_info:
            lines.append("")
            lines.append(self._center_text(self.restaurant_info["tax_id"]))

        # Website if available
        if "website" in self.restaurant_info:
            lines.append(self._center_text(self.restaurant_info["website"]))

        return lines

    def _center_text(self, text: str) -> str:
        """Center text within the receipt width."""
        if len(text) >= self.width:
            return text

        padding = (self.width - len(text)) // 2
        return " " * padding + text

    def _generate_receipt_number(self) -> str:
        """Generate a unique receipt number."""
        self._receipt_counter += 1
        timestamp = datetime.now().strftime("%y%m%d")
        return f"R{timestamp}{self._receipt_counter:04d}"

    def save_receipt_to_file(self, order: Order, output_dir: str,
                           filename: Optional[str] = None) -> str:
        """
        Save receipt to a text file.

        Args:
            order (Order): The order to generate receipt for
            output_dir (str): Directory to save the receipt
            filename (str, optional): Custom filename

        Returns:
            str: Path to the saved receipt file

        Raises:
            IOError: If file cannot be saved
        """
        try:
            # Create output directory if it doesn't exist
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"receipt_{order.order_id}_{timestamp}.txt"

            # Ensure .txt extension
            if not filename.endswith('.txt'):
                filename += '.txt'

            file_path = output_path / filename

            # Generate and save receipt
            receipt_text = self.generate_receipt_text(order)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(receipt_text)

            self.logger.info(f"Receipt saved to: {file_path}")
            return str(file_path)

        except Exception as e:
            self.logger.error(f"Failed to save receipt to file: {e}")
            raise IOError(f"Could not save receipt: {e}")

    def print_receipt(self, order: Order, printer_name: Optional[str] = None) -> bool:
        """
        Print receipt to system printer (placeholder implementation).

        Args:
            order (Order): The order to print receipt for
            printer_name (str, optional): Specific printer to use

        Returns:
            bool: True if print was successful, False otherwise

        Note:
            This is a placeholder implementation. In a real system,
            this would integrate with actual printer drivers.
        """
        try:
            receipt_text = self.generate_receipt_text(order)

            # Placeholder for actual printing logic
            # In a real implementation, this would use printer drivers
            # or send to a network printer

            self.logger.info(f"Receipt for order {order.order_id} sent to printer")

            # For demonstration, we'll just log the receipt
            print("=== PRINTING RECEIPT ===")
            print(receipt_text)
            print("=== END RECEIPT ===")

            return True

        except Exception as e:
            self.logger.error(f"Failed to print receipt: {e}")
            return False

    def generate_receipt_html(self, order: Order, receipt_number: Optional[str] = None) -> str:
        """
        Generate an HTML version of the receipt for web display or PDF export.

        Args:
            order (Order): The order to generate receipt for
            receipt_number (str, optional): Custom receipt number

        Returns:
            str: HTML formatted receipt
        """
        try:
            receipt_data = order.get_receipt_data()
            receipt_num = receipt_number or self._generate_receipt_number()

            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Receipt - {receipt_num}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .receipt {{
            background-color: white;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        .restaurant-name {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .contact-info {{
            font-size: 12px;
            color: #666;
        }}
        .order-info {{
            margin-bottom: 15px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }}
        .items-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }}
        .items-table th, .items-table td {{
            text-align: left;
            padding: 5px;
            border-bottom: 1px solid #eee;
        }}
        .items-table th {{
            background-color: #f5f5f5;
            font-weight: bold;
        }}
        .totals {{
            border-top: 2px solid #333;
            padding-top: 10px;
        }}
        .total-line {{
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
        }}
        .grand-total {{
            font-weight: bold;
            border-top: 1px solid #333;
            padding-top: 5px;
            margin-top: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
            color: #666;
        }}
        .special-instructions {{
            font-style: italic;
            color: #666;
            font-size: 11px;
        }}
    </style>
</head>
<body>
    <div class="receipt">
        <!-- Header -->
        <div class="header">
            <div class="restaurant-name">{self.restaurant_info.get('name', 'Restaurant').upper()}</div>
            <div class="contact-info">
                {self.restaurant_info.get('address_line1', '')}<br>
                {self.restaurant_info.get('address_line2', '')}<br>
                Phone: {self.restaurant_info.get('phone', '')}<br>
                {self.restaurant_info.get('email', '')}
            </div>
        </div>

        <!-- Receipt Info -->
        <div>
            <strong>Receipt #:</strong> {receipt_num}<br>
            <strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>

        <!-- Order Info -->
        <div class="order-info">
            <strong>Order ID:</strong> {receipt_data['order_id']}<br>
            <strong>Order Time:</strong> {receipt_data['timestamp']}<br>
            {'<strong>Customer:</strong> ' + receipt_data['customer_name'] + '<br>' if receipt_data.get('customer_name') else ''}
            {'<strong>Phone:</strong> ' + receipt_data['customer_phone'] + '<br>' if receipt_data.get('customer_phone') else ''}
            {'<strong>Table:</strong> ' + receipt_data['table_number'] + '<br>' if receipt_data.get('table_number') else ''}
            <strong>Order Type:</strong> {receipt_data['order_type']}
        </div>

        <!-- Items -->
        <table class="items-table">
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
"""

            # Add items
            for item in receipt_data['items']:
                html += f"""
                <tr>
                    <td>{item['name']}</td>
                    <td>{item['quantity']}</td>
                    <td>${item['unit_price']:.2f}</td>
                    <td>${item['subtotal']:.2f}</td>
                </tr>
"""
                if item.get('special_instructions'):
                    html += f"""
                <tr>
                    <td colspan="4" class="special-instructions">
                        * {item['special_instructions']}
                    </td>
                </tr>
"""

            html += f"""
            </tbody>
        </table>

        <!-- Totals -->
        <div class="totals">
            <div class="total-line">
                <span>Subtotal:</span>
                <span>${receipt_data['subtotal']:.2f}</span>
            </div>
            <div class="total-line">
                <span>Tax ({receipt_data['tax_rate']:.1f}%):</span>
                <span>${receipt_data['tax_amount']:.2f}</span>
            </div>
            <div class="total-line grand-total">
                <span>TOTAL:</span>
                <span>${receipt_data['total_amount']:.2f}</span>
            </div>
            <div style="margin-top: 10px;">
                <strong>Total Items:</strong> {receipt_data['item_count']}
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <div>Thank you for your business!</div>
            <div>Please come again!</div>
            {'<div>' + self.restaurant_info.get('tax_id', '') + '</div>' if self.restaurant_info.get('tax_id') else ''}
            {'<div>' + self.restaurant_info.get('website', '') + '</div>' if self.restaurant_info.get('website') else ''}
        </div>
    </div>
</body>
</html>
"""
            return html

        except Exception as e:
            self.logger.error(f"Failed to generate HTML receipt: {e}")
            return f"<html><body><h1>Error generating receipt: {e}</h1></body></html>"