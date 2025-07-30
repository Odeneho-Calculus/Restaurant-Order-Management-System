"""
Sample data generation dialog for Restaurant Order Management System.

This module provides a dialog for generating sample menu items and orders
for testing and demonstration purposes.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from decimal import Decimal
from datetime import datetime, timedelta
import random
from typing import List, Callable

from ..models import MenuItem, Order, OrderType, OrderStatus
from ..utils import CSVHandler


class SampleDataDialog:
    """Dialog for generating sample data."""

    def __init__(self, parent: tk.Tk, csv_handler: CSVHandler, refresh_callback: Callable):
        """Initialize sample data dialog."""
        self.parent = parent
        self.csv_handler = csv_handler
        self.refresh_callback = refresh_callback
        self.logger = logging.getLogger(__name__)

        # Create dialog
        self.create_dialog()

    def create_dialog(self) -> None:
        """Create the sample data dialog."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Generate Sample Data")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        # Center the dialog
        self.center_dialog()

        # Create main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.dialog.grid_rowconfigure(0, weight=1)
        self.dialog.grid_columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Generate Sample Data",
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Create options
        self.create_options(main_frame)

        # Create buttons
        self.create_buttons(main_frame)

        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def center_dialog(self) -> None:
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()

        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        # Calculate center position
        dialog_width = 500
        dialog_height = 400
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    def create_options(self, parent: ttk.Frame) -> None:
        """Create sample data generation options."""
        # Menu items section
        menu_frame = ttk.LabelFrame(parent, text="Menu Items", padding="10")
        menu_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        parent.grid_columnconfigure(0, weight=1)

        self.generate_menu_var = tk.BooleanVar(value=True)
        menu_check = ttk.Checkbutton(menu_frame, text="Generate comprehensive menu items",
                                    variable=self.generate_menu_var)
        menu_check.grid(row=0, column=0, sticky="w")

        self.replace_menu_var = tk.BooleanVar(value=False)
        replace_check = ttk.Checkbutton(menu_frame, text="Replace existing menu items",
                                       variable=self.replace_menu_var)
        replace_check.grid(row=1, column=0, sticky="w", pady=(5, 0))

        menu_info = ttk.Label(menu_frame,
                             text="• Generates 25+ menu items across 5 categories\n• Includes appetizers, mains, desserts, soups, and beverages",
                             font=('Arial', 9), foreground='gray')
        menu_info.grid(row=2, column=0, sticky="w", pady=(5, 0))

        # Orders section
        orders_frame = ttk.LabelFrame(parent, text="Sample Orders", padding="10")
        orders_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        self.generate_orders_var = tk.BooleanVar(value=True)
        orders_check = ttk.Checkbutton(orders_frame, text="Generate sample orders",
                                      variable=self.generate_orders_var)
        orders_check.grid(row=0, column=0, sticky="w")

        # Number of orders
        ttk.Label(orders_frame, text="Number of orders:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.num_orders_var = tk.StringVar(value="10")
        orders_spinbox = ttk.Spinbox(orders_frame, from_=1, to=100, width=10,
                                    textvariable=self.num_orders_var)
        orders_spinbox.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(10, 0))

        # Order date range
        ttk.Label(orders_frame, text="Date range:").grid(row=2, column=0, sticky="w", pady=(5, 0))
        self.date_range_var = tk.StringVar(value="Last 7 days")
        date_combo = ttk.Combobox(orders_frame, textvariable=self.date_range_var,
                                 values=["Today", "Last 3 days", "Last 7 days", "Last 30 days"],
                                 width=15, state="readonly")
        date_combo.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=(5, 0))

        orders_info = ttk.Label(orders_frame,
                               text="• Creates realistic orders with multiple items\n• Includes various order types and statuses\n• Generates corresponding sales data",
                               font=('Arial', 9), foreground='gray')
        orders_info.grid(row=3, column=0, columnspan=2, sticky="w", pady=(5, 0))

        # Warning section
        warning_frame = ttk.Frame(parent)
        warning_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        warning_label = ttk.Label(warning_frame,
                                 text="⚠️ Warning: This will modify your data files. Consider backing up first.",
                                 font=('Arial', 9, 'bold'), foreground='red')
        warning_label.grid(row=0, column=0, sticky="w")

    def create_buttons(self, parent: ttk.Frame) -> None:
        """Create dialog buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, columnspan=2, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)

        # Button container (right-aligned)
        buttons = ttk.Frame(button_frame)
        buttons.grid(row=0, column=0, sticky="e")

        # Buttons
        ttk.Button(buttons, text="Cancel",
                  command=self.on_cancel).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(buttons, text="Generate",
                  command=self.generate_data).grid(row=0, column=1)

    def generate_comprehensive_menu(self) -> List[MenuItem]:
        """Generate comprehensive menu items."""
        menu_items = [
            # Appetizers
            MenuItem("Caesar Salad", "appetizers", Decimal("12.99"), "Fresh romaine with parmesan, croutons, and Caesar dressing"),
            MenuItem("Buffalo Wings", "appetizers", Decimal("14.99"), "Spicy buffalo chicken wings with blue cheese dip"),
            MenuItem("Mozzarella Sticks", "appetizers", Decimal("9.99"), "Crispy breaded mozzarella with marinara sauce"),
            MenuItem("Spinach Artichoke Dip", "appetizers", Decimal("11.99"), "Hot spinach and artichoke dip with tortilla chips"),
            MenuItem("Nachos Supreme", "appetizers", Decimal("13.99"), "Loaded nachos with cheese, jalapeños, and sour cream"),
            MenuItem("Calamari Rings", "appetizers", Decimal("12.99"), "Golden fried squid rings with spicy marinara"),
            MenuItem("Bruschetta", "appetizers", Decimal("8.99"), "Toasted bread with fresh tomatoes, basil, and garlic"),

            # Soups
            MenuItem("Tomato Basil Soup", "soups", Decimal("8.99"), "Classic tomato soup with fresh basil"),
            MenuItem("Chicken Noodle Soup", "soups", Decimal("9.99"), "Hearty chicken soup with egg noodles"),
            MenuItem("French Onion Soup", "soups", Decimal("10.99"), "Rich onion soup with melted cheese"),
            MenuItem("Clam Chowder", "soups", Decimal("11.99"), "New England style clam chowder"),

            # Main Courses
            MenuItem("Grilled Chicken Breast", "mains", Decimal("22.99"), "Herb-seasoned chicken breast with seasonal vegetables"),
            MenuItem("Ribeye Steak", "mains", Decimal("34.99"), "12oz ribeye steak cooked to perfection"),
            MenuItem("Pasta Alfredo", "mains", Decimal("18.99"), "Fettuccine pasta in creamy alfredo sauce"),
            MenuItem("Grilled Salmon", "mains", Decimal("26.99"), "Atlantic salmon with lemon butter and herbs"),
            MenuItem("BBQ Ribs", "mains", Decimal("28.99"), "Full rack of baby back ribs with BBQ sauce"),
            MenuItem("Vegetarian Burger", "mains", Decimal("16.99"), "Plant-based burger with avocado and sprouts"),
            MenuItem("Fish and Chips", "mains", Decimal("19.99"), "Beer-battered cod with crispy fries"),
            MenuItem("Chicken Parmesan", "mains", Decimal("24.99"), "Breaded chicken with marinara and mozzarella"),
            MenuItem("Beef Tacos", "mains", Decimal("15.99"), "Three soft tacos with seasoned beef and toppings"),
            MenuItem("Shrimp Scampi", "mains", Decimal("23.99"), "Garlic butter shrimp over linguine pasta"),

            # Desserts
            MenuItem("Chocolate Lava Cake", "desserts", Decimal("8.99"), "Warm chocolate cake with molten center"),
            MenuItem("Tiramisu", "desserts", Decimal("7.99"), "Classic Italian coffee-flavored dessert"),
            MenuItem("New York Cheesecake", "desserts", Decimal("6.99"), "Rich cheesecake with berry sauce"),
            MenuItem("Ice Cream Sundae", "desserts", Decimal("5.99"), "Vanilla ice cream with chocolate sauce and nuts"),
            MenuItem("Apple Pie", "desserts", Decimal("6.49"), "Homemade apple pie with vanilla ice cream"),
            MenuItem("Crème Brûlée", "desserts", Decimal("8.49"), "Classic French custard with caramelized sugar"),

            # Beverages
            MenuItem("Freshly Brewed Coffee", "beverages", Decimal("3.49"), "Colombian coffee, regular or decaf"),
            MenuItem("Fresh Orange Juice", "beverages", Decimal("4.99"), "100% fresh squeezed orange juice"),
            MenuItem("Craft Beer", "beverages", Decimal("5.99"), "Local craft beer selection"),
            MenuItem("House Wine", "beverages", Decimal("7.99"), "Red or white wine by the glass"),
            MenuItem("Soft Drinks", "beverages", Decimal("2.99"), "Coca-Cola, Pepsi, Sprite, and more"),
            MenuItem("Iced Tea", "beverages", Decimal("2.79"), "Sweet or unsweetened iced tea"),
            MenuItem("Hot Tea", "beverages", Decimal("3.29"), "Selection of premium teas"),
            MenuItem("Milkshake", "beverages", Decimal("5.49"), "Vanilla, chocolate, or strawberry")
        ]

        return menu_items

    def generate_sample_orders(self, menu_items: List[MenuItem], num_orders: int, date_range: str) -> List[Order]:
        """Generate sample orders."""
        if not menu_items:
            return []

        orders = []

        # Calculate date range
        end_date = datetime.now()
        if date_range == "Today":
            start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_range == "Last 3 days":
            start_date = end_date - timedelta(days=3)
        elif date_range == "Last 7 days":
            start_date = end_date - timedelta(days=7)
        elif date_range == "Last 30 days":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=7)

        # Sample customer names
        customer_names = [
            "John Smith", "Sarah Johnson", "Mike Davis", "Emily Brown", "David Wilson",
            "Lisa Anderson", "Chris Taylor", "Amanda Martinez", "Ryan Garcia", "Jessica Lee",
            "Kevin White", "Michelle Thompson", "Daniel Rodriguez", "Ashley Clark", "James Lewis"
        ]

        # Sample phone numbers
        phone_numbers = [
            "555-0101", "555-0102", "555-0103", "555-0104", "555-0105",
            "555-0106", "555-0107", "555-0108", "555-0109", "555-0110"
        ]

        order_types = [OrderType.DINE_IN, OrderType.TAKEOUT, OrderType.DELIVERY]
        order_statuses = [OrderStatus.PENDING, OrderStatus.PREPARING, OrderStatus.READY, OrderStatus.COMPLETED]

        for i in range(num_orders):
            # Create order
            order = Order()
            order.customer_name = random.choice(customer_names)
            order.customer_phone = random.choice(phone_numbers)
            order.table_number = f"Table {random.randint(1, 20)}" if random.choice([True, False]) else ""
            order.order_type = random.choice(order_types)
            order.status = random.choice(order_statuses)

            # Set random order time within date range
            time_diff = end_date - start_date
            random_seconds = random.randint(0, int(time_diff.total_seconds()))
            order.order_time = start_date + timedelta(seconds=random_seconds)

            # Add random items to order
            num_items = random.randint(1, 5)
            selected_items = random.sample(menu_items, min(num_items, len(menu_items)))

            for item in selected_items:
                quantity = random.randint(1, 3)
                special_instructions = ""

                # Sometimes add special instructions
                if random.random() < 0.3:  # 30% chance
                    instructions = [
                        "No onions", "Extra sauce", "Well done", "Medium rare",
                        "On the side", "Extra spicy", "No cheese", "Light salt"
                    ]
                    special_instructions = random.choice(instructions)

                order.add_item(item, quantity, special_instructions)

            orders.append(order)

        return orders

    def generate_data(self) -> None:
        """Generate the selected sample data."""
        try:
            generated_items = []

            # Generate menu items
            if self.generate_menu_var.get():
                self.logger.info("Generating sample menu items...")

                # Load existing menu items
                existing_items = self.csv_handler.load_menu_items()

                if self.replace_menu_var.get() or not existing_items:
                    # Replace or create new
                    menu_items = self.generate_comprehensive_menu()
                    self.csv_handler.save_menu_items(menu_items)
                    generated_items.append(f"Generated {len(menu_items)} menu items")
                else:
                    # Add to existing (avoid duplicates)
                    new_items = self.generate_comprehensive_menu()
                    existing_names = {item.name for item in existing_items}

                    unique_items = [item for item in new_items if item.name not in existing_names]
                    if unique_items:
                        all_items = existing_items + unique_items
                        self.csv_handler.save_menu_items(all_items)
                        generated_items.append(f"Added {len(unique_items)} new menu items")
                    else:
                        generated_items.append("No new menu items added (all already exist)")

            # Generate orders
            if self.generate_orders_var.get():
                self.logger.info("Generating sample orders...")

                # Load menu items for orders
                menu_items = self.csv_handler.load_menu_items()
                if not menu_items:
                    messagebox.showwarning("Warning", "No menu items available. Generate menu items first.")
                    return

                num_orders = int(self.num_orders_var.get())
                date_range = self.date_range_var.get()

                # Load existing orders
                menu_dict = {item.id: item for item in menu_items}
                existing_orders = self.csv_handler.load_orders(menu_dict)

                # Generate new orders
                new_orders = self.generate_sample_orders(menu_items, num_orders, date_range)

                # Save all orders
                all_orders = existing_orders + new_orders
                self.csv_handler.save_orders(all_orders)

                generated_items.append(f"Generated {len(new_orders)} sample orders")

            # Show success message
            if generated_items:
                message = "Sample data generated successfully!\n\n" + "\n".join(f"• {item}" for item in generated_items)
                messagebox.showinfo("Success", message)

                # Refresh the main application
                self.refresh_callback()

                self.dialog.destroy()
            else:
                messagebox.showwarning("Warning", "No data was generated. Please select at least one option.")

        except Exception as e:
            self.logger.error(f"Failed to generate sample data: {e}")
            messagebox.showerror("Error", f"Failed to generate sample data: {e}")

    def on_cancel(self) -> None:
        """Handle Cancel button click."""
        self.dialog.destroy()