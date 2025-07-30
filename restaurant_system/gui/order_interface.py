"""
Order Interface Tab for Restaurant Order Management System.

This module provides comprehensive order taking functionality with
intuitive menu browsing, item selection, and order management.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Callable, Dict
from decimal import Decimal
import logging

from ..models import MenuItem, Order, OrderItem, OrderType
from ..utils import InputValidator, ValidationError


class OrderInterfaceTab:
    """
    Order interface tab providing comprehensive order taking functionality.

    Features include menu browsing by category, item selection with quantities,
    special instructions, customer information collection, and order totals.
    """

    def __init__(self, parent: ttk.Notebook, menu_items: List[MenuItem],
                 order_callback: Callable[[Order], None]):
        """
        Initialize the order interface tab.

        Args:
            parent (ttk.Notebook): Parent notebook widget
            menu_items (List[MenuItem]): List of available menu items
            order_callback (Callable): Callback when order is created
        """
        self.parent = parent
        self.menu_items = menu_items
        self.order_callback = order_callback
        self.logger = logging.getLogger(__name__)

        # Current order
        self.current_order: Optional[Order] = None

        # Menu items by category
        self.menu_by_category: Dict[str, List[MenuItem]] = {}

        # Create the main frame
        self.frame = ttk.Frame(parent, padding="10")

        # Setup the interface
        self.setup_interface()
        self.setup_bindings()

        # Initialize data
        self.refresh_menu_items(menu_items)
        self.new_order()

    def setup_interface(self) -> None:
        """Setup the order interface layout."""
        # Configure grid weights
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # Left panel - Menu browsing
        self.setup_menu_panel()

        # Right panel - Order details and customer info
        self.setup_order_panel()

    def setup_menu_panel(self) -> None:
        """Setup the menu browsing panel."""
        menu_frame = ttk.LabelFrame(self.frame, text="Menu", padding="10")
        menu_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        menu_frame.grid_rowconfigure(1, weight=1)
        menu_frame.grid_columnconfigure(0, weight=1)

        # Category selection
        category_frame = ttk.Frame(menu_frame)
        category_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        category_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(category_frame, text="Category:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )

        self.category_var = tk.StringVar()
        self.category_var.trace('w', self.on_category_changed)
        self.category_combo = ttk.Combobox(
            category_frame,
            textvariable=self.category_var,
            values=[],
            state="readonly",
            width=20
        )
        self.category_combo.grid(row=0, column=1, sticky="ew")

        # Search functionality
        search_frame = ttk.Frame(category_frame)
        search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        search_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_changed)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew")

        # Menu items display
        self.setup_menu_display(menu_frame)

    def setup_menu_display(self, parent: ttk.Frame) -> None:
        """Setup the menu items display area."""
        # Create scrollable frame
        canvas_frame = ttk.Frame(parent)
        canvas_frame.grid(row=1, column=0, sticky="nsew")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        # Canvas and scrollbar
        self.menu_canvas = tk.Canvas(canvas_frame, bg="white")
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.menu_canvas.yview)

        self.menu_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.menu_canvas.configure(yscrollcommand=scrollbar.set)

        # Scrollable frame inside canvas
        self.menu_scrollable_frame = ttk.Frame(self.menu_canvas)
        self.canvas_window = self.menu_canvas.create_window(
            (0, 0), window=self.menu_scrollable_frame, anchor="nw"
        )

        # Bind canvas resize
        self.menu_canvas.bind('<Configure>', self.on_canvas_configure)
        self.menu_scrollable_frame.bind('<Configure>', self.on_frame_configure)

        # Mouse wheel scrolling
        self.menu_canvas.bind("<MouseWheel>", self.on_mousewheel)

    def setup_order_panel(self) -> None:
        """Setup the order details and customer information panel."""
        order_frame = ttk.Frame(self.frame)
        order_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        order_frame.grid_rowconfigure(1, weight=1)

        # Customer information section
        self.setup_customer_info(order_frame)

        # Current order section
        self.setup_current_order(order_frame)

        # Order actions section
        self.setup_order_actions(order_frame)

    def setup_customer_info(self, parent: ttk.Frame) -> None:
        """Setup customer information input section."""
        customer_frame = ttk.LabelFrame(parent, text="Customer Information", padding="10")
        customer_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        customer_frame.grid_columnconfigure(1, weight=1)

        # Customer name
        ttk.Label(customer_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=2)
        self.customer_name_var = tk.StringVar()
        name_entry = ttk.Entry(customer_frame, textvariable=self.customer_name_var, width=25)
        name_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=2)

        # Customer phone
        ttk.Label(customer_frame, text="Phone:").grid(row=1, column=0, sticky="w", pady=2)
        self.customer_phone_var = tk.StringVar()
        phone_entry = ttk.Entry(customer_frame, textvariable=self.customer_phone_var, width=25)
        phone_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=2)

        # Table number
        ttk.Label(customer_frame, text="Table:").grid(row=2, column=0, sticky="w", pady=2)
        self.table_number_var = tk.StringVar()
        table_entry = ttk.Entry(customer_frame, textvariable=self.table_number_var, width=25)
        table_entry.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=2)

        # Order type
        ttk.Label(customer_frame, text="Type:").grid(row=3, column=0, sticky="w", pady=2)
        self.order_type_var = tk.StringVar(value="dine_in")
        type_combo = ttk.Combobox(
            customer_frame,
            textvariable=self.order_type_var,
            values=["dine_in", "takeout", "delivery"],
            state="readonly",
            width=22
        )
        type_combo.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=2)

    def setup_current_order(self, parent: ttk.Frame) -> None:
        """Setup current order display section."""
        order_frame = ttk.LabelFrame(parent, text="Current Order", padding="10")
        order_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        order_frame.grid_rowconfigure(0, weight=1)
        order_frame.grid_columnconfigure(0, weight=1)

        # Order items treeview
        columns = ("item", "qty", "price", "total")
        self.order_tree = ttk.Treeview(
            order_frame,
            columns=columns,
            show="headings",
            height=10
        )

        # Column configurations
        self.order_tree.heading("item", text="Item")
        self.order_tree.heading("qty", text="Qty")
        self.order_tree.heading("price", text="Unit Price")
        self.order_tree.heading("total", text="Total")

        self.order_tree.column("item", width=200, minwidth=150)
        self.order_tree.column("qty", width=50, minwidth=40)
        self.order_tree.column("price", width=80, minwidth=60)
        self.order_tree.column("total", width=80, minwidth=60)

        self.order_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar for order tree
        order_scrollbar = ttk.Scrollbar(order_frame, orient="vertical", command=self.order_tree.yview)
        order_scrollbar.grid(row=0, column=1, sticky="ns")
        self.order_tree.configure(yscrollcommand=order_scrollbar.set)

        # Order totals
        totals_frame = ttk.Frame(order_frame)
        totals_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        totals_frame.grid_columnconfigure(1, weight=1)

        # Subtotal
        ttk.Label(totals_frame, text="Subtotal:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky="w"
        )
        self.subtotal_label = ttk.Label(totals_frame, text="$0.00", font=('Arial', 10))
        self.subtotal_label.grid(row=0, column=1, sticky="e")

        # Tax
        ttk.Label(totals_frame, text="Tax (8%):", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky="w"
        )
        self.tax_label = ttk.Label(totals_frame, text="$0.00", font=('Arial', 10))
        self.tax_label.grid(row=1, column=1, sticky="e")

        # Total
        ttk.Separator(totals_frame, orient="horizontal").grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=5
        )
        ttk.Label(totals_frame, text="Total:", font=('Arial', 12, 'bold')).grid(
            row=3, column=0, sticky="w"
        )
        self.total_label = ttk.Label(totals_frame, text="$0.00", font=('Arial', 12, 'bold'))
        self.total_label.grid(row=3, column=1, sticky="e")

    def setup_order_actions(self, parent: ttk.Frame) -> None:
        """Setup order action buttons."""
        actions_frame = ttk.Frame(parent)
        actions_frame.grid(row=2, column=0, sticky="ew")

        # Button layout
        button1_frame = ttk.Frame(actions_frame)
        button1_frame.pack(fill="x", pady=(0, 5))

        button2_frame = ttk.Frame(actions_frame)
        button2_frame.pack(fill="x")

        # Order management buttons
        self.clear_order_button = ttk.Button(
            button1_frame,
            text="Clear Order",
            command=self.clear_order,
            style='Warning.TButton'
        )
        self.clear_order_button.pack(side="left", padx=(0, 5))

        self.remove_item_button = ttk.Button(
            button1_frame,
            text="Remove Item",
            command=self.remove_selected_item,
            state="disabled"
        )
        self.remove_item_button.pack(side="left")

        # Order completion buttons
        self.preview_button = ttk.Button(
            button2_frame,
            text="Preview Order",
            command=self.preview_order
        )
        self.preview_button.pack(side="left", padx=(0, 5))

        self.submit_button = ttk.Button(
            button2_frame,
            text="Submit Order",
            command=self.submit_order,
            style='Success.TButton'
        )
        self.submit_button.pack(side="right")

    def setup_bindings(self) -> None:
        """Setup event bindings."""
        # Order tree selection
        self.order_tree.bind('<<TreeviewSelect>>', self.on_order_item_selected)

        # Double-click to edit quantity
        self.order_tree.bind('<Double-1>', self.edit_item_quantity)

        # Right-click context menu
        self.order_tree.bind('<Button-3>', self.show_order_context_menu)

        # Keyboard shortcuts
        self.frame.bind('<Control-Return>', lambda e: self.submit_order())
        self.frame.bind('<Control-Delete>', lambda e: self.clear_order())
        self.frame.bind('<Delete>', lambda e: self.remove_selected_item())

    def refresh_menu_items(self, menu_items: List[MenuItem]) -> None:
        """Refresh the menu items display."""
        self.menu_items = menu_items
        self.organize_menu_by_category()
        self.populate_category_dropdown()
        self.display_menu_items()

    def organize_menu_by_category(self) -> None:
        """Organize menu items by category."""
        self.menu_by_category.clear()

        for item in self.menu_items:
            if item.is_available:  # Only show available items
                category = item.category
                if category not in self.menu_by_category:
                    self.menu_by_category[category] = []
                self.menu_by_category[category].append(item)

        # Sort items within each category by name
        for category in self.menu_by_category:
            self.menu_by_category[category].sort(key=lambda x: x.name)

    def populate_category_dropdown(self) -> None:
        """Populate the category dropdown."""
        categories = ["All"] + sorted(self.menu_by_category.keys())
        self.category_combo['values'] = categories

        if categories:
            self.category_var.set("All")

    def display_menu_items(self) -> None:
        """Display menu items in the scrollable area."""
        # Clear existing items
        for widget in self.menu_scrollable_frame.winfo_children():
            widget.destroy()

        # Get items to display
        items_to_show = self.get_filtered_menu_items()

        if not items_to_show:
            # No items message
            no_items_label = ttk.Label(
                self.menu_scrollable_frame,
                text="No items available",
                font=('Arial', 12),
                foreground="gray"
            )
            no_items_label.pack(pady=20)
            return

        # Group items by category for display
        current_category = None
        row = 0

        for item in items_to_show:
            if item.category != current_category:
                # Category header
                if current_category is not None:
                    # Add spacing between categories
                    spacer = ttk.Frame(self.menu_scrollable_frame, height=10)
                    spacer.grid(row=row, column=0, columnspan=3, sticky="ew")
                    row += 1

                current_category = item.category
                category_label = ttk.Label(
                    self.menu_scrollable_frame,
                    text=item.category.title(),
                    font=('Arial', 14, 'bold'),
                    foreground="navy"
                )
                category_label.grid(row=row, column=0, columnspan=3, sticky="w", pady=(10, 5))
                row += 1

                # Separator line
                separator = ttk.Separator(self.menu_scrollable_frame, orient="horizontal")
                separator.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(0, 10))
                row += 1

            # Create menu item widget
            self.create_menu_item_widget(item, row)
            row += 2  # Leave space between items

        # Update scroll region
        self.menu_scrollable_frame.update_idletasks()
        self.menu_canvas.configure(scrollregion=self.menu_canvas.bbox("all"))

    def create_menu_item_widget(self, item: MenuItem, row: int) -> None:
        """Create a widget for a menu item."""
        # Main item frame
        item_frame = ttk.Frame(self.menu_scrollable_frame, relief="solid", borderwidth=1)
        item_frame.grid(row=row, column=0, columnspan=3, sticky="ew", padx=5, pady=2)
        item_frame.grid_columnconfigure(0, weight=1)

        # Item information
        info_frame = ttk.Frame(item_frame)
        info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        info_frame.grid_columnconfigure(0, weight=1)

        # Item name and price
        name_price_frame = ttk.Frame(info_frame)
        name_price_frame.grid(row=0, column=0, sticky="ew")
        name_price_frame.grid_columnconfigure(0, weight=1)

        name_label = ttk.Label(
            name_price_frame,
            text=item.name,
            font=('Arial', 11, 'bold')
        )
        name_label.grid(row=0, column=0, sticky="w")

        price_label = ttk.Label(
            name_price_frame,
            text=f"${item.price:.2f}",
            font=('Arial', 11, 'bold'),
            foreground="green"
        )
        price_label.grid(row=0, column=1, sticky="e")

        # Description
        if item.description:
            desc_label = ttk.Label(
                info_frame,
                text=item.description,
                font=('Arial', 9),
                foreground="gray",
                wraplength=300
            )
            desc_label.grid(row=1, column=0, sticky="ew", pady=(2, 0))

        # Add to order controls
        controls_frame = ttk.Frame(item_frame)
        controls_frame.grid(row=0, column=1, padx=10, pady=5)

        # Quantity spinner
        qty_frame = ttk.Frame(controls_frame)
        qty_frame.pack(side="left", padx=(0, 10))

        ttk.Label(qty_frame, text="Qty:", font=('Arial', 9)).pack(side="left")

        qty_var = tk.StringVar(value="1")
        qty_spinbox = ttk.Spinbox(
            qty_frame,
            from_=1,
            to=99,
            width=5,
            textvariable=qty_var
        )
        qty_spinbox.pack(side="left", padx=(5, 0))

        # Add button
        add_button = ttk.Button(
            controls_frame,
            text="Add to Order",
            command=lambda: self.add_item_to_order(item, qty_var.get()),
            style='Action.TButton'
        )
        add_button.pack(side="left")

        # Special instructions button (optional)
        special_button = ttk.Button(
            controls_frame,
            text="Special",
            command=lambda: self.add_item_with_instructions(item, qty_var.get()),
            width=8
        )
        special_button.pack(side="left", padx=(5, 0))

    def get_filtered_menu_items(self) -> List[MenuItem]:
        """Get menu items based on current filters."""
        items = []

        # Category filter
        selected_category = self.category_var.get()
        if selected_category == "All":
            for category_items in self.menu_by_category.values():
                items.extend(category_items)
        else:
            items = self.menu_by_category.get(selected_category, [])

        # Search filter
        search_text = self.search_var.get().lower().strip()
        if search_text:
            items = [
                item for item in items
                if (search_text in item.name.lower() or
                    search_text in item.description.lower())
            ]

        # Sort by category first, then by name
        items.sort(key=lambda x: (x.category, x.name))

        return items

    def on_category_changed(self, *args) -> None:
        """Handle category selection change."""
        self.display_menu_items()

    def on_search_changed(self, *args) -> None:
        """Handle search text change."""
        self.display_menu_items()

    def on_canvas_configure(self, event) -> None:
        """Handle canvas resize."""
        # Update the canvas window width
        canvas_width = event.width
        self.menu_canvas.itemconfig(self.canvas_window, width=canvas_width)

    def on_frame_configure(self, event) -> None:
        """Handle frame resize."""
        # Update scroll region
        self.menu_canvas.configure(scrollregion=self.menu_canvas.bbox("all"))

    def on_mousewheel(self, event) -> None:
        """Handle mouse wheel scrolling."""
        self.menu_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_item_to_order(self, item: MenuItem, qty_str: str) -> None:
        """Add an item to the current order."""
        try:
            quantity = InputValidator.validate_quantity(qty_str)

            if self.current_order is not None:
                self.current_order.add_item(item, quantity)
                self.refresh_order_display()
                self.logger.info(f"Added {quantity}x {item.name} to order")

        except ValidationError as e:
            messagebox.showerror("Invalid Quantity", str(e))
        except Exception as e:
            self.logger.error(f"Failed to add item to order: {e}")
            messagebox.showerror("Error", f"Failed to add item: {e}")

    def add_item_with_instructions(self, item: MenuItem, qty_str: str) -> None:
        """Add an item to order with special instructions."""
        try:
            quantity = InputValidator.validate_quantity(qty_str)

            # Get special instructions
            instructions = self.get_special_instructions()

            if self.current_order is not None:
                self.current_order.add_item(item, quantity, instructions)
                self.refresh_order_display()
                self.logger.info(f"Added {quantity}x {item.name} with instructions to order")

        except ValidationError as e:
            messagebox.showerror("Invalid Quantity", str(e))
        except Exception as e:
            self.logger.error(f"Failed to add item to order: {e}")
            messagebox.showerror("Error", f"Failed to add item: {e}")

    def get_special_instructions(self) -> str:
        """Get special instructions from user."""
        dialog = tk.Toplevel(self.frame)
        dialog.title("Special Instructions")
        dialog.geometry("400x200")
        dialog.transient(self.frame.winfo_toplevel())
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")

        instructions = ""

        # Dialog content
        ttk.Label(dialog, text="Enter special instructions:", font=('Arial', 10, 'bold')).pack(pady=10)

        text_widget = tk.Text(dialog, height=6, width=45, wrap="word")
        text_widget.pack(pady=10, padx=20, fill="both", expand=True)
        text_widget.focus()

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def on_ok():
            nonlocal instructions
            instructions = text_widget.get(1.0, tk.END).strip()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        ttk.Button(button_frame, text="OK", command=on_ok).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side="left", padx=5)

        # Wait for dialog to close
        dialog.wait_window()

        return instructions

    def refresh_order_display(self) -> None:
        """Refresh the current order display."""
        # Clear order tree
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)

        if not self.current_order or self.current_order.is_empty:
            self.update_order_totals(Decimal('0'), Decimal('0'), Decimal('0'))
            return

        # Populate order items
        for order_item in self.current_order.items:
            values = (
                order_item.item_name,
                order_item.quantity,
                f"${order_item.unit_price:.2f}",
                f"${order_item.subtotal:.2f}"
            )

            item_id = self.order_tree.insert("", "end", values=values)

            # Add special instructions as child if present
            if order_item.special_instructions:
                self.order_tree.insert(
                    item_id, "end",
                    values=("  * " + order_item.special_instructions, "", "", "")
                )

        # Update totals
        self.update_order_totals(
            self.current_order.subtotal,
            self.current_order.tax_amount,
            self.current_order.total_amount
        )

    def update_order_totals(self, subtotal: Decimal, tax: Decimal, total: Decimal) -> None:
        """Update the order totals display."""
        self.subtotal_label.config(text=f"${subtotal:.2f}")
        self.tax_label.config(text=f"${tax:.2f}")
        self.total_label.config(text=f"${total:.2f}")

    def on_order_item_selected(self, event) -> None:
        """Handle order item selection."""
        selection = self.order_tree.selection()
        self.remove_item_button.config(state="normal" if selection else "disabled")

    def remove_selected_item(self) -> None:
        """Remove the selected item from the order."""
        selection = self.order_tree.selection()
        if not selection or not self.current_order:
            return

        try:
            # Get selected item index
            item_index = self.order_tree.index(selection[0])

            # Remove from order
            if 0 <= item_index < len(self.current_order.items):
                removed_item = self.current_order.items[item_index]
                self.current_order.remove_item(removed_item)
                self.refresh_order_display()
                self.logger.info(f"Removed {removed_item.item_name} from order")

        except Exception as e:
            self.logger.error(f"Failed to remove item: {e}")
            messagebox.showerror("Error", f"Failed to remove item: {e}")

    def edit_item_quantity(self, event) -> None:
        """Edit the quantity of the selected order item."""
        selection = self.order_tree.selection()
        if not selection or not self.current_order:
            return

        try:
            item_index = self.order_tree.index(selection[0])
            if 0 <= item_index < len(self.current_order.items):
                order_item = self.current_order.items[item_index]

                # Get new quantity
                new_qty = tk.simpledialog.askinteger(
                    "Edit Quantity",
                    f"Enter new quantity for {order_item.item_name}:",
                    initialvalue=order_item.quantity,
                    minvalue=1,
                    maxvalue=99
                )

                if new_qty:
                    self.current_order.update_item_quantity(order_item, new_qty)
                    self.refresh_order_display()
                    self.logger.info(f"Updated quantity for {order_item.item_name} to {new_qty}")

        except Exception as e:
            self.logger.error(f"Failed to edit quantity: {e}")
            messagebox.showerror("Error", f"Failed to edit quantity: {e}")

    def show_order_context_menu(self, event) -> None:
        """Show context menu for order items."""
        item = self.order_tree.identify_row(event.y)
        if item:
            self.order_tree.selection_set(item)

            context_menu = tk.Menu(self.order_tree, tearoff=0)
            context_menu.add_command(label="Edit Quantity", command=lambda: self.edit_item_quantity(None))
            context_menu.add_command(label="Remove Item", command=self.remove_selected_item)

            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()

    def new_order(self) -> None:
        """Start a new order."""
        self.current_order = Order()
        self.refresh_order_display()

        # Clear customer information
        self.customer_name_var.set("")
        self.customer_phone_var.set("")
        self.table_number_var.set("")
        self.order_type_var.set("dine_in")

        self.logger.info("Started new order")

    def clear_order(self) -> None:
        """Clear the current order."""
        if self.current_order and not self.current_order.is_empty:
            if messagebox.askyesno("Confirm", "Are you sure you want to clear the current order?"):
                self.current_order.clear_items()
                self.refresh_order_display()
                self.logger.info("Cleared current order")

    def preview_order(self) -> None:
        """Preview the order before submission."""
        if not self.current_order or self.current_order.is_empty:
            messagebox.showwarning("Warning", "No items in order")
            return

        # Create preview dialog
        preview_dialog = tk.Toplevel(self.frame)
        preview_dialog.title("Order Preview")
        preview_dialog.geometry("500x600")
        preview_dialog.transient(self.frame.winfo_toplevel())
        preview_dialog.grab_set()

        # Center dialog
        preview_dialog.update_idletasks()
        x = (preview_dialog.winfo_screenwidth() // 2) - (250)
        y = (preview_dialog.winfo_screenheight() // 2) - (300)
        preview_dialog.geometry(f"500x600+{x}+{y}")

        # Preview content
        preview_frame = ttk.Frame(preview_dialog, padding="20")
        preview_frame.pack(fill="both", expand=True)

        # Order summary
        ttk.Label(preview_frame, text="Order Summary", font=('Arial', 16, 'bold')).pack(pady=(0, 10))

        # Customer info
        customer_frame = ttk.LabelFrame(preview_frame, text="Customer Information", padding="10")
        customer_frame.pack(fill="x", pady=(0, 10))

        customer_info = f"""Name: {self.customer_name_var.get() or 'Guest'}
Phone: {self.customer_phone_var.get() or 'N/A'}
Table: {self.table_number_var.get() or 'N/A'}
Type: {self.order_type_var.get().replace('_', ' ').title()}"""

        ttk.Label(customer_frame, text=customer_info, justify="left").pack(anchor="w")

        # Order items
        items_frame = ttk.LabelFrame(preview_frame, text="Order Items", padding="10")
        items_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Items text widget
        items_text = tk.Text(items_frame, height=15, wrap="word", state="disabled")
        items_scrollbar = ttk.Scrollbar(items_frame, command=items_text.yview)
        items_text.configure(yscrollcommand=items_scrollbar.set)

        items_text.pack(side="left", fill="both", expand=True)
        items_scrollbar.pack(side="right", fill="y")

        # Populate items
        items_text.config(state="normal")
        for order_item in self.current_order.items:
            item_text = f"{order_item.quantity}x {order_item.item_name} - ${order_item.subtotal:.2f}\n"
            if order_item.special_instructions:
                item_text += f"   Special: {order_item.special_instructions}\n"
            item_text += "\n"
            items_text.insert(tk.END, item_text)
        items_text.config(state="disabled")

        # Totals
        totals_frame = ttk.LabelFrame(preview_frame, text="Order Total", padding="10")
        totals_frame.pack(fill="x", pady=(0, 10))

        totals_text = f"""Subtotal: ${self.current_order.subtotal:.2f}
Tax: ${self.current_order.tax_amount:.2f}
Total: ${self.current_order.total_amount:.2f}"""

        ttk.Label(totals_frame, text=totals_text, font=('Arial', 11), justify="left").pack(anchor="w")

        # Close button
        ttk.Button(preview_frame, text="Close", command=preview_dialog.destroy).pack(pady=10)

    def submit_order(self) -> None:
        """Submit the current order."""
        if not self.current_order or self.current_order.is_empty:
            messagebox.showwarning("Warning", "No items in order")
            return

        try:
            # Validate and set customer information
            customer_name = self.customer_name_var.get().strip()
            customer_phone = InputValidator.validate_phone_number(
                self.customer_phone_var.get(), required=False
            )
            table_number = InputValidator.validate_table_number(
                self.table_number_var.get()
            )

            # Update order with customer information
            self.current_order.customer_name = customer_name
            self.current_order.customer_phone = customer_phone
            self.current_order.table_number = table_number
            self.current_order.order_type = OrderType(self.order_type_var.get())

            # Confirm submission
            if messagebox.askyesno(
                "Confirm Order",
                f"Submit order for ${self.current_order.total_amount:.2f}?\n\n"
                f"Customer: {customer_name or 'Guest'}\n"
                f"Items: {self.current_order.item_count}\n"
                f"Total: ${self.current_order.total_amount:.2f}"
            ):
                # Submit order
                self.order_callback(self.current_order)

                # Start new order
                self.new_order()

                messagebox.showinfo("Success", "Order submitted successfully!")
                self.logger.info(f"Order submitted: {self.current_order.order_id}")

        except ValidationError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            self.logger.error(f"Failed to submit order: {e}")
            messagebox.showerror("Error", f"Failed to submit order: {e}")


# Import required for dialog
import tkinter.simpledialog