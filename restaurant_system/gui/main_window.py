"""
Main window for Restaurant Order Management System.

This module provides the main application window with tabbed interface
for all restaurant management functionality.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
from pathlib import Path
from typing import Dict, List, Optional

from ..models import MenuItem, Order, OrderStatus
from ..utils import CSVHandler, InputValidator, ReceiptGenerator
from .menu_manager import MenuManagerTab
from .order_interface import OrderInterfaceTab
from .queue_display import QueueDisplayTab
from .reports import ReportsTab


class RestaurantMainWindow:
    """
    Main application window for the Restaurant Order Management System.

    Provides a comprehensive tabbed interface for all restaurant operations
    including menu management, order taking, queue monitoring, and reporting.
    """

    def __init__(self):
        """Initialize the main application window."""
        self.root = tk.Tk()
        self.setup_logging()
        self.logger = logging.getLogger(__name__)

        # Initialize data handlers
        self.data_dir = Path(__file__).parent.parent / "data"
        self.csv_handler = CSVHandler(str(self.data_dir))
        self.receipt_generator = ReceiptGenerator()

        # Data storage
        self.menu_items: List[MenuItem] = []
        self.orders: List[Order] = []
        self.current_order: Optional[Order] = None

        # GUI setup
        self.setup_window()
        self.setup_styles()
        self.create_menu_bar()
        self.create_main_interface()
        self.setup_status_bar()

        # Load initial data
        self.load_data()

        # Setup auto-save
        self.setup_auto_save()

        self.logger.info("Restaurant Management System initialized successfully")

    def setup_logging(self) -> None:
        """Setup application logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('restaurant_system.log'),
                logging.StreamHandler()
            ]
        )

    def setup_window(self) -> None:
        """Setup the main window properties."""
        self.root.title("Restaurant Order Management System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)

        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")

        # Configure window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def setup_styles(self) -> None:
        """Setup custom styles for the application."""
        self.style = ttk.Style()

        # Configure theme
        self.style.theme_use('clam')

        # Custom styles
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Status.TLabel', font=('Arial', 10))

        # Button styles
        self.style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        self.style.configure('Success.TButton', background='#28a745')
        self.style.configure('Danger.TButton', background='#dc3545')
        self.style.configure('Warning.TButton', background='#ffc107')

        # Notebook styles
        self.style.configure('TNotebook.Tab', padding=[20, 10])

    def create_menu_bar(self) -> None:
        """Create the application menu bar."""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Order", command=self.new_order, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Import Menu", command=self.import_menu)
        file_menu.add_command(label="Export Menu", command=self.export_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Backup Data", command=self.backup_data)
        file_menu.add_command(label="Restore Data", command=self.restore_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")

        # Edit menu
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Preferences", command=self.show_preferences)
        edit_menu.add_command(label="Restaurant Info", command=self.edit_restaurant_info)

        # View menu
        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh All", command=self.refresh_all, accelerator="F5")
        view_menu.add_command(label="Toggle Fullscreen", command=self.toggle_fullscreen, accelerator="F11")

        # Tools menu
        tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Generate Sample Data", command=self.generate_sample_data)
        tools_menu.add_command(label="Clear All Orders", command=self.clear_all_orders)
        tools_menu.add_command(label="Database Maintenance", command=self.database_maintenance)

        # Help menu
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Manual", command=self.show_user_manual)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_command(label="About", command=self.show_about)

        # Bind keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_order())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<F5>', lambda e: self.refresh_all())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())

    def create_main_interface(self) -> None:
        """Create the main tabbed interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=1, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # Initialize tab instances
        self.menu_manager_tab = MenuManagerTab(
            self.notebook,
            self.menu_items,
            self.csv_handler,
            self.refresh_menu_data
        )

        self.order_interface_tab = OrderInterfaceTab(
            self.notebook,
            self.menu_items,
            self.on_order_created
        )

        self.queue_display_tab = QueueDisplayTab(
            self.notebook,
            self.orders,
            self.on_order_status_changed,
            self.receipt_generator
        )

        self.reports_tab = ReportsTab(
            self.notebook,
            self.csv_handler
        )

        # Add tabs to notebook
        self.notebook.add(self.menu_manager_tab.frame, text="Menu Management")
        self.notebook.add(self.order_interface_tab.frame, text="Take Order")
        self.notebook.add(self.queue_display_tab.frame, text="Order Queue")
        self.notebook.add(self.reports_tab.frame, text="Reports")

        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def setup_status_bar(self) -> None:
        """Create the status bar."""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=2)

        # Status labels
        self.status_label = ttk.Label(
            self.status_frame,
            text="Ready",
            style='Status.TLabel'
        )
        self.status_label.pack(side="left")

        # Separator
        ttk.Separator(self.status_frame, orient="vertical").pack(side="left", fill="y", padx=10)

        # Statistics labels
        self.menu_count_label = ttk.Label(
            self.status_frame,
            text="Menu Items: 0",
            style='Status.TLabel'
        )
        self.menu_count_label.pack(side="left", padx=10)

        self.orders_count_label = ttk.Label(
            self.status_frame,
            text="Active Orders: 0",
            style='Status.TLabel'
        )
        self.orders_count_label.pack(side="left", padx=10)

        # Time display
        self.time_label = ttk.Label(
            self.status_frame,
            text="",
            style='Status.TLabel'
        )
        self.time_label.pack(side="right", padx=10)

        # Update time every second
        self.update_time()

    def setup_auto_save(self) -> None:
        """Setup automatic data saving."""
        self.auto_save_enabled = True
        self.auto_save_interval = 300000  # 5 minutes in milliseconds
        self.schedule_auto_save()

    def schedule_auto_save(self) -> None:
        """Schedule the next auto-save operation."""
        if self.auto_save_enabled:
            self.root.after(self.auto_save_interval, self.auto_save)

    def auto_save(self) -> None:
        """Perform automatic data saving."""
        try:
            self.save_all_data()
            self.update_status("Auto-saved data")
            self.logger.info("Auto-save completed successfully")
        except Exception as e:
            self.logger.error(f"Auto-save failed: {e}")
        finally:
            self.schedule_auto_save()

    def load_data(self) -> None:
        """Load all data from CSV files."""
        try:
            # Load menu items
            self.menu_items = self.csv_handler.load_menu_items()
            self.menu_manager_tab.refresh_menu_list()
            self.order_interface_tab.refresh_menu_items(self.menu_items)

            # Load orders
            menu_items_dict = {item.id: item for item in self.menu_items}
            self.orders = self.csv_handler.load_orders(menu_items_dict)
            self.queue_display_tab.refresh_orders(self.orders)

            self.update_status_counts()
            self.update_status("Data loaded successfully")
            self.logger.info(f"Loaded {len(self.menu_items)} menu items and {len(self.orders)} orders")

        except Exception as e:
            self.logger.error(f"Failed to load data: {e}")
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def save_all_data(self) -> None:
        """Save all data to CSV files."""
        try:
            # Save menu items
            if not self.csv_handler.save_menu_items(self.menu_items):
                raise Exception("Failed to save menu items")

            # Save orders
            if not self.csv_handler.save_orders(self.orders):
                raise Exception("Failed to save orders")

            self.update_status("All data saved successfully")

        except Exception as e:
            self.logger.error(f"Failed to save data: {e}")
            raise

    def refresh_menu_data(self) -> None:
        """Refresh menu data across all tabs."""
        self.order_interface_tab.refresh_menu_items(self.menu_items)
        self.update_status_counts()

    def on_order_created(self, order: Order) -> None:
        """Handle when a new order is created."""
        try:
            self.orders.append(order)
            self.queue_display_tab.refresh_orders(self.orders)
            self.save_all_data()
            self.update_status_counts()
            self.update_status(f"Order {order.order_id} created successfully")
            self.logger.info(f"New order created: {order.order_id}")

            # Switch to queue tab
            self.notebook.select(2)  # Queue tab index

        except Exception as e:
            self.logger.error(f"Failed to process new order: {e}")
            messagebox.showerror("Error", f"Failed to save order: {e}")

    def on_order_status_changed(self, order: Order) -> None:
        """Handle when an order status changes."""
        try:
            # Record sales data if order is completed
            if order.status == OrderStatus.COMPLETED:
                self.csv_handler.append_sales_record(order)

            self.save_all_data()
            self.update_status_counts()
            self.update_status(f"Order {order.order_id} status updated to {order.status.value}")

        except Exception as e:
            self.logger.error(f"Failed to update order status: {e}")
            messagebox.showerror("Error", f"Failed to update order: {e}")

    def on_tab_changed(self, event) -> None:
        """Handle tab change events."""
        selected_tab = self.notebook.index(self.notebook.select())
        tab_names = ["Menu Management", "Take Order", "Order Queue", "Reports"]

        if selected_tab < len(tab_names):
            self.update_status(f"Switched to {tab_names[selected_tab]} tab")

    def update_status_counts(self) -> None:
        """Update the status bar counts."""
        menu_count = len(self.menu_items)
        active_orders = len([o for o in self.orders if o.status in [OrderStatus.PENDING, OrderStatus.PREPARING, OrderStatus.READY]])

        self.menu_count_label.config(text=f"Menu Items: {menu_count}")
        self.orders_count_label.config(text=f"Active Orders: {active_orders}")

    def update_status(self, message: str) -> None:
        """Update the status bar message."""
        self.status_label.config(text=message)
        # Clear status after 5 seconds
        self.root.after(5000, lambda: self.status_label.config(text="Ready"))

    def update_time(self) -> None:
        """Update the time display."""
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    # Menu bar command methods
    def new_order(self) -> None:
        """Create a new order."""
        self.notebook.select(1)  # Switch to order tab
        self.order_interface_tab.new_order()

    def import_menu(self) -> None:
        """Import menu from CSV file."""
        try:
            file_path = filedialog.askopenfilename(
                title="Import Menu Items",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if file_path:
                # Implementation would go here
                messagebox.showinfo("Info", "Menu import functionality to be implemented")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to import menu: {e}")

    def export_menu(self) -> None:
        """Export menu to CSV file."""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export Menu Items",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if file_path:
                # Implementation would go here
                messagebox.showinfo("Info", "Menu export functionality to be implemented")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export menu: {e}")

    def backup_data(self) -> None:
        """Create a backup of all data."""
        try:
            backup_dir = filedialog.askdirectory(title="Select Backup Directory")
            if backup_dir:
                # Create backups of all CSV files
                for file_path in [self.csv_handler.menu_file, self.csv_handler.orders_file, self.csv_handler.sales_file]:
                    self.csv_handler.create_backup(file_path)

                messagebox.showinfo("Success", "Data backup created successfully")
                self.update_status("Data backup completed")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {e}")

    def restore_data(self) -> None:
        """Restore data from backup."""
        messagebox.showinfo("Info", "Data restore functionality to be implemented")

    def show_preferences(self) -> None:
        """Show preferences dialog."""
        messagebox.showinfo("Info", "Preferences dialog to be implemented")

    def edit_restaurant_info(self) -> None:
        """Edit restaurant information for receipts."""
        messagebox.showinfo("Info", "Restaurant info editor to be implemented")

    def refresh_all(self) -> None:
        """Refresh all data and tabs."""
        self.load_data()
        self.update_status("All data refreshed")

    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode."""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)

    def generate_sample_data(self) -> None:
        """Generate sample orders for testing."""
        messagebox.showinfo("Info", "Sample data generation to be implemented")

    def clear_all_orders(self) -> None:
        """Clear all orders (with confirmation)."""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all orders? This cannot be undone."):
            self.orders.clear()
            self.queue_display_tab.refresh_orders(self.orders)
            self.save_all_data()
            self.update_status_counts()
            self.update_status("All orders cleared")

    def database_maintenance(self) -> None:
        """Perform database maintenance tasks."""
        try:
            # Clean up old backups
            self.csv_handler.cleanup_old_backups()
            messagebox.showinfo("Success", "Database maintenance completed")
            self.update_status("Database maintenance completed")

        except Exception as e:
            messagebox.showerror("Error", f"Database maintenance failed: {e}")

    def show_user_manual(self) -> None:
        """Show user manual."""
        messagebox.showinfo("User Manual",
                          "Restaurant Order Management System\n\n"
                          "Tabs:\n"
                          "• Menu Management: Add, edit, and manage menu items\n"
                          "• Take Order: Create new customer orders\n"
                          "• Order Queue: Monitor and update order status\n"
                          "• Reports: View sales reports and analytics\n\n"
                          "Use keyboard shortcuts for faster operation:\n"
                          "• Ctrl+N: New Order\n"
                          "• F5: Refresh All\n"
                          "• F11: Toggle Fullscreen")

    def show_shortcuts(self) -> None:
        """Show keyboard shortcuts."""
        shortcuts = """Keyboard Shortcuts:

File Operations:
• Ctrl+N: New Order
• Ctrl+Q: Exit Application

View:
• F5: Refresh All Data
• F11: Toggle Fullscreen

Navigation:
• Tab: Move between fields
• Enter: Confirm action
• Escape: Cancel action"""

        messagebox.showinfo("Keyboard Shortcuts", shortcuts)

    def show_about(self) -> None:
        """Show about dialog."""
        about_text = """Restaurant Order Management System
Version 1.0

A comprehensive restaurant management solution built with Python and Tkinter.

Features:
• Menu Management
• Order Processing
• Queue Monitoring
• Sales Reporting
• Receipt Generation

Developed with professional-grade architecture and error handling."""

        messagebox.showinfo("About", about_text)

    def on_closing(self) -> None:
        """Handle application closing."""
        try:
            # Ask for confirmation if there are unsaved changes
            if messagebox.askokcancel("Quit", "Do you want to quit? Any unsaved changes will be lost."):
                # Save data before closing
                self.save_all_data()
                self.auto_save_enabled = False
                self.logger.info("Application closing")
                self.root.destroy()

        except Exception as e:
            self.logger.error(f"Error during application shutdown: {e}")
            self.root.destroy()

    def run(self) -> None:
        """Start the application main loop."""
        try:
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")


def main():
    """Main entry point for the application."""
    app = RestaurantMainWindow()
    app.run()


if __name__ == "__main__":
    main()