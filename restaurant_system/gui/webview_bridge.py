"""
WebView Bridge for Restaurant Order Management System.

This module provides a seamless bridge between the modern HTML/CSS/JavaScript
interface and the existing Python backend, maintaining all functionality
while upgrading the user interface.
"""

import webview
import json
import logging
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..models import MenuItem, Order, OrderItem, OrderStatus, OrderType
from ..utils import CSVHandler, InputValidator, ReceiptGenerator


class WebViewAPI:
    """
    API bridge between JavaScript frontend and Python backend.

    This class exposes Python functionality to the JavaScript interface
    through webview's API bridge system.
    """

    def __init__(self, data_dir: Path):
        """Initialize the WebView API bridge."""
        self.data_dir = data_dir
        self.csv_handler = CSVHandler(str(data_dir))
        self.receipt_generator = ReceiptGenerator()
        self.validator = InputValidator()
        self.logger = logging.getLogger(__name__)

        # Data storage
        self.menu_items: List[MenuItem] = []
        self.orders: List[Order] = []

        # Load initial data
        self.load_data()

        self.logger.info("WebView API bridge initialized")

    def load_data(self) -> None:
        """Load data from CSV files."""
        try:
            # Load menu items
            self.menu_items = self.csv_handler.load_menu_items()

            # Create menu items dictionary for order loading
            menu_items_dict = {item.id: item for item in self.menu_items}

            # Load orders
            self.orders = self.csv_handler.load_orders(menu_items_dict)

            # Create sample menu items if none exist
            if len(self.menu_items) == 0:
                self.create_sample_menu_items()

            self.logger.info(f"Loaded {len(self.menu_items)} menu items and {len(self.orders)} orders")

        except Exception as e:
            self.logger.error(f"Error loading data: {e}")

    def create_sample_menu_items(self) -> None:
        """Create sample menu items for demonstration."""
        try:
            sample_items = [
                # Appetizers
                MenuItem("Mozzarella Sticks", "appetizers", 9.99, "Crispy breaded mozzarella with marinara sauce"),
                MenuItem("Buffalo Wings", "appetizers", 12.99, "Spicy chicken wings with blue cheese dip"),
                MenuItem("Onion Rings", "appetizers", 7.99, "Golden fried onion rings with ranch dressing"),
                MenuItem("Spinach Artichoke Dip", "appetizers", 10.99, "Creamy dip served with tortilla chips"),

                # Main Course
                MenuItem("Grilled Salmon", "mains", 24.99, "Fresh Atlantic salmon with lemon herb butter"),
                MenuItem("Ribeye Steak", "mains", 32.99, "12oz prime ribeye with garlic mashed potatoes"),
                MenuItem("Chicken Parmesan", "mains", 19.99, "Breaded chicken breast with marinara and mozzarella"),
                MenuItem("Fish and Chips", "mains", 16.99, "Beer-battered cod with crispy fries"),
                MenuItem("Vegetarian Pasta", "mains", 15.99, "Penne with seasonal vegetables in garlic olive oil"),

                # Desserts
                MenuItem("Chocolate Cake", "desserts", 8.99, "Rich chocolate layer cake with vanilla ice cream"),
                MenuItem("Cheesecake", "desserts", 7.99, "New York style cheesecake with berry compote"),
                MenuItem("Apple Pie", "desserts", 6.99, "Homemade apple pie with cinnamon ice cream"),
                MenuItem("Tiramisu", "desserts", 9.99, "Classic Italian dessert with espresso and mascarpone"),

                # Beverages
                MenuItem("Craft Beer", "beverages", 5.99, "Local craft beer selection"),
                MenuItem("House Wine", "beverages", 7.99, "Red or white wine by the glass"),
                MenuItem("Fresh Lemonade", "beverages", 3.99, "Freshly squeezed lemonade"),
                MenuItem("Coffee", "beverages", 2.99, "Freshly brewed coffee"),
                MenuItem("Soft Drinks", "beverages", 2.49, "Coke, Pepsi, Sprite, and more")
            ]

            self.menu_items.extend(sample_items)
            self.save_data()
            self.logger.info(f"Created {len(sample_items)} sample menu items")

        except Exception as e:
            self.logger.error(f"Error creating sample menu items: {e}")

    def save_data(self) -> None:
        """Save data to CSV files."""
        try:
            # Save menu items
            self.csv_handler.save_menu_items(self.menu_items)

            # Save orders
            self.csv_handler.save_orders(self.orders)

            self.logger.info("Data saved successfully")

        except Exception as e:
            self.logger.error(f"Error saving data: {e}")
            raise

    def handleRequest(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle API requests from JavaScript frontend.

        Args:
            request_data: Request data containing method and parameters

        Returns:
            Response data with success/error status
        """
        try:
            method = request_data.get('method')
            data = request_data.get('data', {})
            request_id = request_data.get('id')

            self.logger.debug(f"Handling request: {method}")

            # Route to appropriate method
            if method == 'getMenuItems':
                result = self.get_menu_items()
            elif method == 'addMenuItem':
                result = self.add_menu_item(data)
            elif method == 'updateMenuItem':
                result = self.update_menu_item(data)
            elif method == 'deleteMenuItem':
                result = self.delete_menu_item(data)
            elif method == 'submitOrder':
                result = self.submit_order(data)
            elif method == 'getOrders':
                result = self.get_orders(data)
            elif method == 'updateOrderStatus':
                result = self.update_order_status(data)
            elif method == 'getSalesData':
                result = self.get_sales_data(data)
            elif method == 'exportData':
                result = self.export_data(data)
            elif method == 'getSettings':
                result = self.get_settings()
            elif method == 'updateSettings':
                result = self.update_settings(data)
            elif method == 'backupData':
                result = self.backup_data(data)
            elif method == 'restoreData':
                result = self.restore_data(data)
            elif method == 'generateReceipt':
                result = self.generate_receipt(data)
            else:
                raise ValueError(f"Unknown method: {method}")

            # Send response back to JavaScript
            response = {
                'id': request_id,
                'success': True,
                'data': result
            }

            # Use webview to send response to frontend
            webview.windows[0].evaluate_js(
                f"window.dispatchEvent(new CustomEvent('python-response', {{detail: {json.dumps(response)}}}));"
            )

            return response

        except Exception as e:
            self.logger.error(f"Error handling request {method}: {e}")

            error_response = {
                'id': request_data.get('id'),
                'success': False,
                'error': str(e)
            }

            # Send error response to frontend
            webview.windows[0].evaluate_js(
                f"window.dispatchEvent(new CustomEvent('python-response', {{detail: {json.dumps(error_response)}}}));"
            )

            return error_response

    def get_menu_items(self) -> List[Dict[str, Any]]:
        """Get all menu items."""
        self.logger.info(f"🍽️ API: get_menu_items called - returning {len(self.menu_items)} items")
        result = [item.to_dict() for item in self.menu_items]
        self.logger.info(f"✅ API: Successfully serialized {len(result)} menu items")
        return result

    def add_menu_item(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new menu item."""
        # Validate input
        required_fields = ['name', 'category', 'price']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"Missing required field: {field}")

        # Create menu item
        menu_item = MenuItem(
            name=data['name'],
            category=data['category'],
            price=float(data['price']),
            description=data.get('description', ''),
            is_available=data.get('is_available', True)
        )

        self.menu_items.append(menu_item)
        self.save_data()

        return menu_item.to_dict()

    def update_menu_item(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing menu item."""
        item_id = data.get('id')
        if not item_id:
            raise ValueError("Missing item ID")

        # Find item
        item = next((item for item in self.menu_items if item.id == item_id), None)
        if not item:
            raise ValueError("Menu item not found")

        # Update fields
        if 'name' in data:
            item.name = data['name']
        if 'category' in data:
            item.category = data['category']
        if 'price' in data:
            item.price = float(data['price'])
        if 'description' in data:
            item.description = data['description']
        if 'is_available' in data:
            item.is_available = data['is_available']

        self.save_data()
        return item.to_dict()

    def delete_menu_item(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Delete a menu item."""
        item_id = data.get('id')
        if not item_id:
            raise ValueError("Missing item ID")

        # Find and remove item
        original_count = len(self.menu_items)
        self.menu_items = [item for item in self.menu_items if item.id != item_id]

        if len(self.menu_items) == original_count:
            raise ValueError("Menu item not found")

        self.save_data()
        return {'success': True}

    def submit_order(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a new order."""
        # Validate required fields
        if not data.get('items'):
            raise ValueError("Order must contain items")

        # Create order items
        order_items = []
        for item_data in data['items']:
            # Find menu item
            menu_item = next((item for item in self.menu_items if item.id == item_data['id']), None)
            if not menu_item:
                raise ValueError(f"Menu item not found: {item_data['id']}")

            order_item = OrderItem(
                menu_item=menu_item,
                quantity=item_data['quantity'],
                special_instructions=item_data.get('instructions', '')
            )
            order_items.append(order_item)

        # Create order
        order = Order(
            customer_name=data.get('customer_name', ''),
            customer_phone=data.get('customer_phone', ''),
            table_number=data.get('table_number', ''),
            order_type=OrderType(data.get('order_type', 'dine_in'))
        )

        # Add items to the order
        for order_item in order_items:
            order._items.append(order_item)

        self.orders.append(order)
        self.save_data()

        return {
            'success': True,
            'order_id': order.order_id,
            'order': order.to_dict()
        }

    def get_orders(self, data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get all orders with optional filtering."""
        self.logger.info(f"📋 API: get_orders called with data: {data}")

        orders = self.orders
        self.logger.info(f"📊 API: Found {len(orders)} total orders")

        # Apply filters if provided
        if data:
            status_filter = data.get('status')
            if status_filter:
                orders = [order for order in orders if order.status.value == status_filter]
                self.logger.info(f"🏷️ API: Filtered to {len(orders)} orders by status: {status_filter}")

            date_filter = data.get('date')
            if date_filter:
                # Filter by date (implement as needed)
                self.logger.info(f"📅 API: Date filter requested: {date_filter} (not implemented)")
                pass

        try:
            result = [order.to_dict() for order in orders]
            self.logger.info(f"✅ API: Successfully serialized {len(result)} orders")
            return result
        except Exception as e:
            self.logger.error(f"❌ API: Error serializing orders: {e}")
            raise

    def update_order_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update order status."""
        order_id = data.get('orderId')
        new_status = data.get('status')

        if not order_id or not new_status:
            raise ValueError("Missing order ID or status")

        # Find order
        order = next((order for order in self.orders if order.order_id == order_id), None)
        if not order:
            raise ValueError("Order not found")

        # Update status using the proper method
        try:
            status_enum = OrderStatus(new_status)
            order.update_status(status_enum)
            self.save_data()
        except ValueError as e:
            # Provide better error message for invalid status values
            valid_statuses = [status.value for status in OrderStatus]
            raise ValueError(f"'{new_status}' is not a valid OrderStatus. Valid options are: {valid_statuses}")

        return order.to_dict()

    def get_sales_data(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get sales data and reports with comprehensive filtering and calculations."""
        from datetime import datetime, timedelta

        # Get filter period and custom dates
        period = data.get('period', 'today') if data else 'today'

        # Calculate date range based on period
        now = datetime.now()

        if period == 'custom' and data:
            # Handle custom date range
            try:
                start_date_str = data.get('startDate')
                end_date_str = data.get('endDate')

                if start_date_str and end_date_str:
                    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
                    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=999999)
                else:
                    # Fallback to today if custom dates are invalid
                    start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
                    end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
                    period = 'today'
            except ValueError:
                # Fallback to today if date parsing fails
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
                period = 'today'
        elif period == 'today':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif period == 'week':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now
        elif period == 'month':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = now
        else:  # default to today
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Filter orders by status and date range
        filtered_orders = []
        for order in self.orders:
            # Check if order is completed
            if order.status == OrderStatus.COMPLETED:
                # Check date range (orders have timezone-aware timestamps)
                order_date = order.timestamp.replace(tzinfo=None)  # Convert to naive datetime for comparison
                if start_date <= order_date <= end_date:
                    filtered_orders.append(order)

        # Calculate financial metrics
        total_sales = sum(order.total_amount for order in filtered_orders)
        orders_count = len(filtered_orders)
        avg_order_value = total_sales / orders_count if orders_count > 0 else 0

        # Calculate popular items with proper access to order items
        item_counts = {}
        total_items_sold = 0

        for order in filtered_orders:
            for item in order.items:  # This accesses the _items list through the property
                item_name = item.menu_item.name if hasattr(item, 'menu_item') else item.item_name
                item_quantity = item.quantity

                if item_name in item_counts:
                    item_counts[item_name] += item_quantity
                else:
                    item_counts[item_name] = item_quantity

                total_items_sold += item_quantity

        # Sort and format popular items
        popular_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        popular_items = [
            {
                'name': name,
                'count': count,
                'percentage': round((count / total_items_sold * 100), 1) if total_items_sold > 0 else 0
            }
            for name, count in popular_items
        ]

        # Calculate additional metrics
        if len(filtered_orders) > 0:
            # Revenue by time (hourly breakdown for today, daily for week/month)
            time_breakdown = {}
            for order in filtered_orders:
                if period == 'today':
                    time_key = order.timestamp.strftime('%H:00')
                elif period == 'week':
                    time_key = order.timestamp.strftime('%a')
                else:  # month
                    time_key = order.timestamp.strftime('%d')

                if time_key not in time_breakdown:
                    time_breakdown[time_key] = {'sales': 0, 'orders': 0}

                time_breakdown[time_key]['sales'] += float(order.total_amount)
                time_breakdown[time_key]['orders'] += 1

            # Sort time breakdown
            sorted_time_breakdown = sorted(time_breakdown.items())
        else:
            sorted_time_breakdown = []

        self.logger.info(f"📊 Sales data calculated for period '{period}': ${total_sales:.2f} from {orders_count} orders")

        return {
            'totalSales': float(total_sales),
            'ordersCount': orders_count,
            'avgOrderValue': float(avg_order_value),
            'popularItems': popular_items,
            'period': period,
            'dateRange': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'timeBreakdown': sorted_time_breakdown,
            'totalItemsSold': total_items_sold
        }

    def export_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Export data to file with enhanced reporting."""
        import csv
        from pathlib import Path

        export_type = data.get('type', 'csv')
        options = data.get('options', {})
        period = options.get('period', 'today')

        if export_type == 'csv':
            try:
                # Prepare sales data request with all options
                sales_request = {'period': period}

                # Handle custom date range
                if period == 'custom':
                    if 'startDate' in options:
                        sales_request['startDate'] = options['startDate']
                    if 'endDate' in options:
                        sales_request['endDate'] = options['endDate']

                # Get sales data for the specified period
                sales_data = self.get_sales_data(sales_request)

                # Create reports directory if it doesn't exist
                reports_dir = self.data_dir.parent / 'reports'
                reports_dir.mkdir(exist_ok=True)

                # Generate filename with timestamp
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'sales_report_{period}_{timestamp}.csv'
                file_path = reports_dir / filename

                # Write sales report to CSV
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)

                    # Write header information
                    writer.writerow(['Restaurant Sales Report'])
                    writer.writerow(['Period:', period.title()])
                    writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                    writer.writerow([])  # Empty row

                    # Write summary
                    writer.writerow(['SUMMARY'])
                    writer.writerow(['Total Sales:', f"${sales_data['totalSales']:.2f}"])
                    writer.writerow(['Orders Count:', sales_data['ordersCount']])
                    writer.writerow(['Average Order Value:', f"${sales_data['avgOrderValue']:.2f}"])
                    writer.writerow(['Total Items Sold:', sales_data['totalItemsSold']])
                    writer.writerow([])  # Empty row

                    # Write popular items
                    writer.writerow(['POPULAR ITEMS'])
                    writer.writerow(['Rank', 'Item Name', 'Quantity Sold', 'Percentage'])
                    for i, item in enumerate(sales_data['popularItems'], 1):
                        writer.writerow([i, item['name'], item['count'], f"{item['percentage']}%"])
                    writer.writerow([])  # Empty row

                    # Write time breakdown
                    if sales_data['timeBreakdown']:
                        writer.writerow(['TIME BREAKDOWN'])
                        if period == 'today':
                            writer.writerow(['Hour', 'Sales', 'Orders'])
                        elif period == 'week':
                            writer.writerow(['Day', 'Sales', 'Orders'])
                        else:
                            writer.writerow(['Date', 'Sales', 'Orders'])

                        for time_key, data in sales_data['timeBreakdown']:
                            writer.writerow([time_key, f"${data['sales']:.2f}", data['orders']])

                self.logger.info(f"📄 Sales report exported to: {file_path}")

                return {
                    'success': True,
                    'message': f'Sales report exported successfully',
                    'filename': filename,
                    'path': str(file_path)
                }

            except Exception as e:
                self.logger.error(f"Error exporting sales report: {e}")
                raise ValueError(f"Failed to export sales report: {str(e)}")
        else:
            raise ValueError(f"Unsupported export type: {export_type}")

    def get_settings(self) -> Dict[str, Any]:
        """Get application settings."""
        # Return default settings (can be extended to load from file)
        return {
            'restaurant_name': 'My Restaurant',
            'restaurant_address': '123 Main St, City, State 12345',
            'restaurant_phone': '(555) 123-4567',
            'tax_rate': 0.08,
            'enable_sounds': True,
            'auto_refresh': True
        }

    def update_settings(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update application settings."""
        # In a real implementation, save settings to file
        return {'success': True, 'message': 'Settings updated'}

    def backup_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create data backup."""
        try:
            backup_dir = self.data_dir / "backups"
            backup_dir.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"backup_{timestamp}.json"

            backup_data = {
                'menu_items': [item.to_dict() for item in self.menu_items],
                'orders': [order.to_dict() for order in self.orders],
                'created_at': datetime.now().isoformat()
            }

            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)

            return {'success': True, 'message': f'Backup created: {backup_file.name}'}

        except Exception as e:
            raise ValueError(f"Backup failed: {e}")

    def restore_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Restore data from backup."""
        backup_file = data.get('backupFile')
        if not backup_file:
            raise ValueError("No backup file specified")

        try:
            backup_path = self.data_dir / "backups" / backup_file

            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)

            # Restore menu items
            self.menu_items = [MenuItem.from_dict(item) for item in backup_data['menu_items']]

            # Restore orders
            self.orders = []
            for order_dict in backup_data['orders']:
                order_items = [OrderItem.from_dict(item) for item in order_dict['items']]
                order = Order(
                    customer_name=order_dict['customer_name'],
                    customer_phone=order_dict['customer_phone'],
                    table_number=order_dict['table_number'],
                    order_type=OrderType(order_dict['order_type']),
                    order_id=order_dict['id']  # Pass order_id to constructor
                )

                # Add items to the order
                for item in order_items:
                    order.add_item(item.menu_item, item.quantity, item.special_instructions)

                # Update status using the proper method
                order.update_status(OrderStatus(order_dict['status']))

                # Set timestamp directly (no public setter available)
                order._timestamp = datetime.fromisoformat(order_dict['created_at'])

                self.orders.append(order)

            # Save restored data
            self.save_data()

            return {'success': True, 'message': 'Data restored successfully'}

        except Exception as e:
            raise ValueError(f"Restore failed: {e}")

    def generate_receipt(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate receipt for an order."""
        order_id = data.get('orderId')
        if not order_id:
            raise ValueError("Missing order ID")

        # Find order
        order = next((order for order in self.orders if order.order_id == order_id), None)
        if not order:
            raise ValueError("Order not found")

        try:
            receipt_path = self.receipt_generator.generate_receipt(order)
            return {
                'success': True,
                'receipt_path': str(receipt_path),
                'message': 'Receipt generated successfully'
            }
        except Exception as e:
            raise ValueError(f"Receipt generation failed: {e}")


class ModernRestaurantWindow:
    """
    Modern Restaurant Management Window using WebView.

    This class replaces the tkinter-based interface with a modern
    HTML/CSS/JavaScript interface while maintaining full compatibility
    with the existing backend.
    """

    def __init__(self):
        """Initialize the modern restaurant window."""
        self.logger = logging.getLogger(__name__)

        # Setup data directory
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)

        # Create API bridge
        self.api = WebViewAPI(self.data_dir)

        # WebView window
        self.window = None

        self.logger.info("Modern Restaurant Window initialized")

    def run(self):
        """Run the modern restaurant application."""
        try:
            # Get the HTML file path
            html_file = Path(__file__).parent / "index.html"

            self.logger.info(f"Looking for HTML file at: {html_file}")

            if not html_file.exists():
                raise FileNotFoundError(f"HTML file not found: {html_file}")

            self.logger.info("HTML file found, creating webview window...")

            # Create webview window
            self.logger.info(f"🔧 Creating webview window with API bridge: {type(self.api)}")
            self.logger.info(f"🔍 API methods: {[method for method in dir(self.api) if not method.startswith('_')]}")

            self.window = webview.create_window(
                title="Restaurant Order Management System",
                url=str(html_file),
                width=1920,
                height=1080,
                min_size=(1000, 600),
                js_api=self.api,
                resizable=True,
                fullscreen=False,
                minimized=False
            )

            self.logger.info("Webview window created, starting webview...")

            # Add window event handlers
            def on_window_loaded():
                """Maximize window when loaded."""
                try:
                    # Try to maximize the window
                    if hasattr(self.window, 'maximize'):
                        self.window.maximize()
                        self.logger.info("Window maximized successfully")
                    else:
                        # Fallback: try to resize to screen dimensions
                        self.window.resize(1920, 1080)
                        self.logger.info("Window resized to fullscreen dimensions")
                except Exception as e:
                    self.logger.warning(f"Could not maximize window: {e}")

            # Set window loaded event
            self.window.events.loaded += on_window_loaded

            # Start webview
            self.logger.info("🌐 Starting webview with HTTP server...")
            webview.start(
                debug=True,  # Enable debug mode to see browser console
                http_server=True  # Enable local HTTP server for assets
            )

            self.logger.info("Webview started successfully")

        except Exception as e:
            self.logger.error(f"Failed to start modern interface: {e}")
            raise

    def cleanup(self):
        """Cleanup resources."""
        try:
            if self.api:
                self.api.save_data()
            self.logger.info("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


# Export the main window class for compatibility
RestaurantMainWindow = ModernRestaurantWindow