"""
Queue Display Tab for Restaurant Order Management System.

This module provides real-time order queue monitoring with status updates,
priority management, and comprehensive order tracking functionality.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Callable, Optional
from datetime import datetime, timedelta
import logging

from ..models import Order, OrderStatus
from ..utils import ReceiptGenerator


class QueueDisplayTab:
    """
    Order queue display tab providing comprehensive order monitoring.

    Features include real-time order status tracking, priority management,
    order completion workflow, and integrated receipt generation.
    """

    def __init__(self, parent: ttk.Notebook, orders: List[Order],
                 status_callback: Callable[[Order], None],
                 receipt_generator: ReceiptGenerator):
        """
        Initialize the queue display tab.

        Args:
            parent (ttk.Notebook): Parent notebook widget
            orders (List[Order]): Reference to orders list
            status_callback (Callable): Callback when order status changes
            receipt_generator (ReceiptGenerator): Receipt generator instance
        """
        self.parent = parent
        self.orders = orders
        self.status_callback = status_callback
        self.receipt_generator = receipt_generator
        self.logger = logging.getLogger(__name__)

        # Selected order tracking
        self.selected_order: Optional[Order] = None

        # Auto-refresh settings
        self.auto_refresh_enabled = True
        self.refresh_interval = 30000  # 30 seconds

        # Create the main frame
        self.frame = ttk.Frame(parent, padding="10")

        # Setup the interface
        self.setup_interface()
        self.setup_bindings()

        # Start auto-refresh
        self.schedule_refresh()

        # Initial refresh
        self.refresh_orders(orders)

    def setup_interface(self) -> None:
        """Setup the queue display interface."""
        # Configure grid weights
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=2)
        self.frame.grid_columnconfigure(1, weight=1)

        # Top controls
        self.setup_controls()

        # Left panel - Orders queue
        self.setup_queue_panel()

        # Right panel - Order details and actions
        self.setup_details_panel()

    def setup_controls(self) -> None:
        """Setup the top control panel."""
        controls_frame = ttk.Frame(self.frame)
        controls_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        controls_frame.grid_columnconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(controls_frame, text="Order Queue", style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky="w")

        # Filter controls
        filter_frame = ttk.Frame(controls_frame)
        filter_frame.grid(row=0, column=1, padx=20)

        ttk.Label(filter_frame, text="Filter:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )

        self.filter_var = tk.StringVar(value="Active")
        filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All", "Active", "Pending", "Preparing", "Ready", "Completed"],
            state="readonly",
            width=12
        )
        filter_combo.grid(row=0, column=1)
        filter_combo.bind('<<ComboboxSelected>>', self.on_filter_changed)

        # Refresh controls
        refresh_frame = ttk.Frame(controls_frame)
        refresh_frame.grid(row=0, column=2, sticky="e")

        self.auto_refresh_var = tk.BooleanVar(value=True)
        auto_check = ttk.Checkbutton(
            refresh_frame,
            text="Auto-refresh",
            variable=self.auto_refresh_var,
            command=self.toggle_auto_refresh
        )
        auto_check.pack(side="left", padx=(0, 10))

        refresh_button = ttk.Button(
            refresh_frame,
            text="Refresh Now",
            command=self.manual_refresh,
            style='Action.TButton'
        )
        refresh_button.pack(side="left")

        # Last updated label
        self.last_updated_label = ttk.Label(
            controls_frame,
            text="",
            font=('Arial', 8),
            foreground="gray"
        )
        self.last_updated_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0))

    def setup_queue_panel(self) -> None:
        """Setup the orders queue panel."""
        queue_frame = ttk.LabelFrame(self.frame, text="Orders", padding="10")
        queue_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        queue_frame.grid_rowconfigure(0, weight=1)
        queue_frame.grid_columnconfigure(0, weight=1)

        # Orders treeview
        columns = ("order_id", "customer", "time", "status", "total", "items")
        self.queue_tree = ttk.Treeview(
            queue_frame,
            columns=columns,
            show="headings",
            height=20
        )

        # Column configurations
        self.queue_tree.heading("order_id", text="Order ID")
        self.queue_tree.heading("customer", text="Customer")
        self.queue_tree.heading("time", text="Order Time")
        self.queue_tree.heading("status", text="Status")
        self.queue_tree.heading("total", text="Total")
        self.queue_tree.heading("items", text="Items")

        self.queue_tree.column("order_id", width=120, minwidth=100)
        self.queue_tree.column("customer", width=120, minwidth=100)
        self.queue_tree.column("time", width=120, minwidth=100)
        self.queue_tree.column("status", width=100, minwidth=80)
        self.queue_tree.column("total", width=80, minwidth=60)
        self.queue_tree.column("items", width=60, minwidth=40)

        self.queue_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(queue_frame, orient="vertical", command=self.queue_tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.queue_tree.configure(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(queue_frame, orient="horizontal", command=self.queue_tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.queue_tree.configure(xscrollcommand=h_scrollbar.set)

    def setup_details_panel(self) -> None:
        """Setup the order details and actions panel."""
        details_frame = ttk.Frame(self.frame)
        details_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        details_frame.grid_rowconfigure(1, weight=1)

        # Order details section
        self.setup_order_details(details_frame)

        # Order items section
        self.setup_order_items(details_frame)

        # Action buttons section
        self.setup_action_buttons(details_frame)

    def setup_order_details(self, parent: ttk.Frame) -> None:
        """Setup order details display."""
        details_info_frame = ttk.LabelFrame(parent, text="Order Details", padding="10")
        details_info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        details_info_frame.grid_columnconfigure(1, weight=1)

        # Create detail labels
        self.detail_labels = {}

        fields = [
            ("Order ID:", "order_id"),
            ("Customer:", "customer"),
            ("Phone:", "phone"),
            ("Table:", "table"),
            ("Type:", "type"),
            ("Status:", "status"),
            ("Order Time:", "time"),
            ("Total:", "total")
        ]

        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(details_info_frame, text=label_text, font=('Arial', 9, 'bold')).grid(
                row=i, column=0, sticky="w", pady=2, padx=(0, 10)
            )

            self.detail_labels[field_name] = ttk.Label(
                details_info_frame,
                text="",
                font=('Arial', 9)
            )
            self.detail_labels[field_name].grid(row=i, column=1, sticky="w", pady=2)

        # Priority indicator
        self.priority_var = tk.BooleanVar()
        self.priority_check = ttk.Checkbutton(
            details_info_frame,
            text="Priority Order",
            variable=self.priority_var,
            command=self.toggle_priority,
            state="disabled"
        )
        self.priority_check.grid(row=len(fields), column=0, columnspan=2, sticky="w", pady=5)

        # Notes section
        ttk.Label(details_info_frame, text="Notes:", font=('Arial', 9, 'bold')).grid(
            row=len(fields) + 1, column=0, sticky="nw", pady=2, padx=(0, 10)
        )

        self.notes_text = tk.Text(details_info_frame, height=3, width=25, wrap="word")
        self.notes_text.grid(row=len(fields) + 1, column=1, sticky="ew", pady=2)
        self.notes_text.bind('<KeyRelease>', self.on_notes_changed)

    def setup_order_items(self, parent: ttk.Frame) -> None:
        """Setup order items display."""
        items_frame = ttk.LabelFrame(parent, text="Order Items", padding="10")
        items_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        items_frame.grid_rowconfigure(0, weight=1)
        items_frame.grid_columnconfigure(0, weight=1)

        # Items treeview
        columns = ("item", "qty", "price")
        self.items_tree = ttk.Treeview(
            items_frame,
            columns=columns,
            show="headings",
            height=8
        )

        self.items_tree.heading("item", text="Item")
        self.items_tree.heading("qty", text="Qty")
        self.items_tree.heading("price", text="Price")

        self.items_tree.column("item", width=150, minwidth=120)
        self.items_tree.column("qty", width=40, minwidth=30)
        self.items_tree.column("price", width=60, minwidth=50)

        self.items_tree.grid(row=0, column=0, sticky="nsew")

        # Items scrollbar
        items_scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=self.items_tree.yview)
        items_scrollbar.grid(row=0, column=1, sticky="ns")
        self.items_tree.configure(yscrollcommand=items_scrollbar.set)

    def setup_action_buttons(self, parent: ttk.Frame) -> None:
        """Setup action buttons."""
        actions_frame = ttk.LabelFrame(parent, text="Actions", padding="10")
        actions_frame.grid(row=2, column=0, sticky="ew")

        # Status update buttons
        status_frame = ttk.Frame(actions_frame)
        status_frame.pack(fill="x", pady=(0, 10))

        self.status_buttons = {}

        # Pending to Preparing
        self.status_buttons["preparing"] = ttk.Button(
            status_frame,
            text="Start Preparing",
            command=lambda: self.update_order_status(OrderStatus.PREPARING),
            state="disabled",
            style='Action.TButton'
        )
        self.status_buttons["preparing"].pack(fill="x", pady=1)

        # Preparing to Ready
        self.status_buttons["ready"] = ttk.Button(
            status_frame,
            text="Mark Ready",
            command=lambda: self.update_order_status(OrderStatus.READY),
            state="disabled",
            style='Warning.TButton'
        )
        self.status_buttons["ready"].pack(fill="x", pady=1)

        # Ready to Completed
        self.status_buttons["completed"] = ttk.Button(
            status_frame,
            text="Complete Order",
            command=lambda: self.update_order_status(OrderStatus.COMPLETED),
            state="disabled",
            style='Success.TButton'
        )
        self.status_buttons["completed"].pack(fill="x", pady=1)

        # Separator
        ttk.Separator(actions_frame, orient="horizontal").pack(fill="x", pady=10)

        # Other actions
        other_frame = ttk.Frame(actions_frame)
        other_frame.pack(fill="x")

        self.print_receipt_button = ttk.Button(
            other_frame,
            text="Print Receipt",
            command=self.print_receipt,
            state="disabled"
        )
        self.print_receipt_button.pack(fill="x", pady=1)

        self.view_receipt_button = ttk.Button(
            other_frame,
            text="View Receipt",
            command=self.view_receipt,
            state="disabled"
        )
        self.view_receipt_button.pack(fill="x", pady=1)

        self.cancel_order_button = ttk.Button(
            other_frame,
            text="Cancel Order",
            command=self.cancel_order,
            state="disabled",
            style='Danger.TButton'
        )
        self.cancel_order_button.pack(fill="x", pady=5)

    def setup_bindings(self) -> None:
        """Setup event bindings."""
        # Queue tree selection
        self.queue_tree.bind('<<TreeviewSelect>>', self.on_order_selected)

        # Double-click to view details
        self.queue_tree.bind('<Double-1>', self.view_order_details)

        # Right-click context menu
        self.queue_tree.bind('<Button-3>', self.show_context_menu)

        # Keyboard shortcuts
        self.frame.bind('<F5>', lambda e: self.manual_refresh())
        self.frame.bind('<Control-p>', lambda e: self.print_receipt())

    def refresh_orders(self, orders: List[Order]) -> None:
        """Refresh the orders display."""
        self.orders = orders
        self.populate_queue_tree()
        self.update_last_updated()

    def populate_queue_tree(self) -> None:
        """Populate the queue treeview with orders."""
        # Clear existing items
        for item in self.queue_tree.get_children():
            self.queue_tree.delete(item)

        # Apply filter
        filtered_orders = self.apply_filter()

        # Sort orders by timestamp (newest first)
        filtered_orders.sort(key=lambda x: x.timestamp, reverse=True)

        # Populate treeview
        for order in filtered_orders:
            customer = order.customer_name or "Guest"
            order_time = order.timestamp.strftime("%H:%M")
            status = order.status.value.title()
            total = f"${order.total_amount:.2f}"
            items_count = str(order.item_count)

            values = (order.order_id, customer, order_time, status, total, items_count)

            item_id = self.queue_tree.insert("", "end", values=values, tags=(order.order_id,))

            # Color coding based on status and priority
            self.apply_item_styling(item_id, order)

        self.logger.info(f"Queue refreshed with {len(filtered_orders)} orders")

    def apply_filter(self) -> List[Order]:
        """Apply filter to orders list."""
        filter_value = self.filter_var.get()

        if filter_value == "All":
            return self.orders
        elif filter_value == "Active":
            return [o for o in self.orders if o.status in [
                OrderStatus.PENDING, OrderStatus.PREPARING, OrderStatus.READY
            ]]
        else:
            status_filter = OrderStatus(filter_value.lower())
            return [o for o in self.orders if o.status == status_filter]

    def apply_item_styling(self, item_id: str, order: Order) -> None:
        """Apply styling to treeview item based on order properties."""
        tags = []

        # Status-based coloring
        if order.status == OrderStatus.PENDING:
            tags.append("pending")
        elif order.status == OrderStatus.PREPARING:
            tags.append("preparing")
        elif order.status == OrderStatus.READY:
            tags.append("ready")
        elif order.status == OrderStatus.COMPLETED:
            tags.append("completed")
        elif order.status == OrderStatus.CANCELLED:
            tags.append("cancelled")

        # Priority highlighting
        if order.is_priority:
            tags.append("priority")

        # Time-based urgency (orders older than 30 minutes)
        if datetime.now(order.timestamp.tzinfo) - order.timestamp > timedelta(minutes=30):
            tags.append("urgent")

        self.queue_tree.item(item_id, tags=tags)

        # Configure tag styles
        self.queue_tree.tag_configure("pending", background="#fff3cd")
        self.queue_tree.tag_configure("preparing", background="#d1ecf1")
        self.queue_tree.tag_configure("ready", background="#d4edda")
        self.queue_tree.tag_configure("completed", background="#f8f9fa")
        self.queue_tree.tag_configure("cancelled", background="#f8d7da")
        self.queue_tree.tag_configure("priority", foreground="#dc3545", font=('Arial', 9, 'bold'))
        self.queue_tree.tag_configure("urgent", background="#ffeaa7")

    def on_filter_changed(self, event) -> None:
        """Handle filter change."""
        self.populate_queue_tree()

    def on_order_selected(self, event) -> None:
        """Handle order selection."""
        selection = self.queue_tree.selection()

        if selection:
            # Get selected order
            order_id = self.queue_tree.item(selection[0])['tags'][0]
            self.selected_order = next((o for o in self.orders if o.order_id == order_id), None)

            if self.selected_order:
                self.display_order_details(self.selected_order)
                self.enable_action_buttons()
        else:
            self.clear_order_details()
            self.disable_action_buttons()
            self.selected_order = None

    def display_order_details(self, order: Order) -> None:
        """Display order details in the details panel."""
        self.detail_labels["order_id"].config(text=order.order_id)
        self.detail_labels["customer"].config(text=order.customer_name or "Guest")
        self.detail_labels["phone"].config(text=order.customer_phone or "N/A")
        self.detail_labels["table"].config(text=order.table_number or "N/A")
        self.detail_labels["type"].config(text=order.order_type.value.replace('_', ' ').title())
        self.detail_labels["status"].config(text=order.status.value.title())
        self.detail_labels["time"].config(text=order.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        self.detail_labels["total"].config(text=f"${order.total_amount:.2f}")

        # Priority checkbox
        self.priority_var.set(order.is_priority)
        self.priority_check.config(state="normal")

        # Notes
        self.notes_text.delete(1.0, tk.END)
        self.notes_text.insert(1.0, order.notes)

        # Display order items
        self.display_order_items(order)

    def display_order_items(self, order: Order) -> None:
        """Display order items in the items treeview."""
        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)

        # Add order items
        for order_item in order.items:
            values = (
                order_item.item_name,
                order_item.quantity,
                f"${order_item.subtotal:.2f}"
            )

            item_id = self.items_tree.insert("", "end", values=values)

            # Add special instructions as child if present
            if order_item.special_instructions:
                self.items_tree.insert(
                    item_id, "end",
                    values=("  * " + order_item.special_instructions, "", "")
                )

    def clear_order_details(self) -> None:
        """Clear the order details display."""
        for label in self.detail_labels.values():
            label.config(text="")

        self.priority_var.set(False)
        self.priority_check.config(state="disabled")

        self.notes_text.delete(1.0, tk.END)

        # Clear items tree
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)

    def enable_action_buttons(self) -> None:
        """Enable appropriate action buttons based on order status."""
        if not self.selected_order:
            return

        status = self.selected_order.status

        # Disable all status buttons first
        for button in self.status_buttons.values():
            button.config(state="disabled")

        # Enable appropriate buttons based on current status
        if status == OrderStatus.PENDING:
            self.status_buttons["preparing"].config(state="normal")
        elif status == OrderStatus.PREPARING:
            self.status_buttons["ready"].config(state="normal")
        elif status == OrderStatus.READY:
            self.status_buttons["completed"].config(state="normal")

        # Enable other buttons
        self.print_receipt_button.config(state="normal")
        self.view_receipt_button.config(state="normal")

        # Cancel button (only for non-completed orders)
        if status not in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            self.cancel_order_button.config(state="normal")
        else:
            self.cancel_order_button.config(state="disabled")

    def disable_action_buttons(self) -> None:
        """Disable all action buttons."""
        for button in self.status_buttons.values():
            button.config(state="disabled")

        self.print_receipt_button.config(state="disabled")
        self.view_receipt_button.config(state="disabled")
        self.cancel_order_button.config(state="disabled")

    def update_order_status(self, new_status: OrderStatus) -> None:
        """Update the status of the selected order."""
        if not self.selected_order:
            return

        try:
            old_status = self.selected_order.status
            self.selected_order.update_status(new_status)

            # Call status callback
            self.status_callback(self.selected_order)

            # Refresh display
            self.populate_queue_tree()
            self.display_order_details(self.selected_order)
            self.enable_action_buttons()

            messagebox.showinfo(
                "Status Updated",
                f"Order {self.selected_order.order_id} status updated from "
                f"{old_status.value} to {new_status.value}"
            )

            self.logger.info(f"Order {self.selected_order.order_id} status: {old_status.value} -> {new_status.value}")

        except Exception as e:
            self.logger.error(f"Failed to update order status: {e}")
            messagebox.showerror("Error", f"Failed to update order status: {e}")

    def toggle_priority(self) -> None:
        """Toggle the priority status of the selected order."""
        if not self.selected_order:
            return

        try:
            self.selected_order.is_priority = self.priority_var.get()
            self.status_callback(self.selected_order)
            self.populate_queue_tree()

            priority_text = "priority" if self.selected_order.is_priority else "normal priority"
            self.logger.info(f"Order {self.selected_order.order_id} marked as {priority_text}")

        except Exception as e:
            self.logger.error(f"Failed to toggle priority: {e}")
            messagebox.showerror("Error", f"Failed to toggle priority: {e}")

    def on_notes_changed(self, event) -> None:
        """Handle notes text changes."""
        if self.selected_order:
            # Update notes after a brief delay to avoid excessive updates
            self.frame.after(1000, self.update_notes)

    def update_notes(self) -> None:
        """Update the order notes."""
        if not self.selected_order:
            return

        try:
            notes = self.notes_text.get(1.0, tk.END).strip()
            self.selected_order.notes = notes
            self.status_callback(self.selected_order)

        except Exception as e:
            self.logger.error(f"Failed to update notes: {e}")

    def print_receipt(self) -> None:
        """Print receipt for the selected order."""
        if not self.selected_order:
            messagebox.showwarning("Warning", "Please select an order")
            return

        try:
            success = self.receipt_generator.print_receipt(self.selected_order)
            if success:
                messagebox.showinfo("Success", "Receipt sent to printer")
            else:
                messagebox.showerror("Error", "Failed to print receipt")

        except Exception as e:
            self.logger.error(f"Failed to print receipt: {e}")
            messagebox.showerror("Error", f"Failed to print receipt: {e}")

    def view_receipt(self) -> None:
        """View receipt for the selected order."""
        if not self.selected_order:
            messagebox.showwarning("Warning", "Please select an order")
            return

        try:
            # Generate receipt text
            receipt_text = self.receipt_generator.generate_receipt_text(self.selected_order)

            # Create receipt view dialog
            receipt_dialog = tk.Toplevel(self.frame)
            receipt_dialog.title(f"Receipt - {self.selected_order.order_id}")
            receipt_dialog.geometry("600x700")
            receipt_dialog.transient(self.frame.winfo_toplevel())
            receipt_dialog.grab_set()

            # Center dialog
            receipt_dialog.update_idletasks()
            x = (receipt_dialog.winfo_screenwidth() // 2) - (300)
            y = (receipt_dialog.winfo_screenheight() // 2) - (350)
            receipt_dialog.geometry(f"600x700+{x}+{y}")

            # Receipt content
            receipt_frame = ttk.Frame(receipt_dialog, padding="20")
            receipt_frame.pack(fill="both", expand=True)

            # Receipt text widget
            receipt_text_widget = tk.Text(
                receipt_frame,
                font=('Courier New', 10),
                wrap="none",
                state="disabled",
                bg="white"
            )

            # Scrollbars
            text_scrollbar_v = ttk.Scrollbar(receipt_frame, orient="vertical", command=receipt_text_widget.yview)
            text_scrollbar_h = ttk.Scrollbar(receipt_frame, orient="horizontal", command=receipt_text_widget.xview)

            receipt_text_widget.configure(yscrollcommand=text_scrollbar_v.set, xscrollcommand=text_scrollbar_h.set)

            receipt_text_widget.grid(row=0, column=0, sticky="nsew")
            text_scrollbar_v.grid(row=0, column=1, sticky="ns")
            text_scrollbar_h.grid(row=1, column=0, sticky="ew")

            receipt_frame.grid_rowconfigure(0, weight=1)
            receipt_frame.grid_columnconfigure(0, weight=1)

            # Insert receipt text
            receipt_text_widget.config(state="normal")
            receipt_text_widget.insert(1.0, receipt_text)
            receipt_text_widget.config(state="disabled")

            # Buttons
            button_frame = ttk.Frame(receipt_frame)
            button_frame.grid(row=2, column=0, columnspan=2, pady=10)

            ttk.Button(
                button_frame,
                text="Print",
                command=lambda: self.print_receipt()
            ).pack(side="left", padx=5)

            ttk.Button(
                button_frame,
                text="Save to File",
                command=lambda: self.save_receipt()
            ).pack(side="left", padx=5)

            ttk.Button(
                button_frame,
                text="Close",
                command=receipt_dialog.destroy
            ).pack(side="left", padx=5)

        except Exception as e:
            self.logger.error(f"Failed to view receipt: {e}")
            messagebox.showerror("Error", f"Failed to view receipt: {e}")

    def save_receipt(self) -> None:
        """Save receipt to file."""
        if not self.selected_order:
            return

        try:
            from tkinter import filedialog
            import os

            # Get save location
            file_path = filedialog.asksaveasfilename(
                title="Save Receipt",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialname=f"receipt_{self.selected_order.order_id}.txt"
            )

            if file_path:
                saved_path = self.receipt_generator.save_receipt_to_file(
                    self.selected_order,
                    os.path.dirname(file_path),
                    os.path.basename(file_path)
                )
                messagebox.showinfo("Success", f"Receipt saved to: {saved_path}")

        except Exception as e:
            self.logger.error(f"Failed to save receipt: {e}")
            messagebox.showerror("Error", f"Failed to save receipt: {e}")

    def cancel_order(self) -> None:
        """Cancel the selected order."""
        if not self.selected_order:
            return

        if self.selected_order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            messagebox.showwarning("Warning", "Cannot cancel completed or already cancelled orders")
            return

        # Get cancellation reason
        reason = tk.simpledialog.askstring(
            "Cancel Order",
            f"Enter reason for cancelling order {self.selected_order.order_id}:",
            initialvalue=""
        )

        if reason is not None:  # User didn't cancel the dialog
            try:
                self.selected_order.cancel_order(reason)
                self.status_callback(self.selected_order)

                self.populate_queue_tree()
                self.display_order_details(self.selected_order)
                self.enable_action_buttons()

                messagebox.showinfo("Order Cancelled", f"Order {self.selected_order.order_id} has been cancelled")
                self.logger.info(f"Order {self.selected_order.order_id} cancelled: {reason}")

            except Exception as e:
                self.logger.error(f"Failed to cancel order: {e}")
                messagebox.showerror("Error", f"Failed to cancel order: {e}")

    def view_order_details(self, event) -> None:
        """View detailed order information in a popup."""
        if not self.selected_order:
            return

        # Create details dialog
        details_dialog = tk.Toplevel(self.frame)
        details_dialog.title(f"Order Details - {self.selected_order.order_id}")
        details_dialog.geometry("500x600")
        details_dialog.transient(self.frame.winfo_toplevel())
        details_dialog.grab_set()

        # Center dialog
        details_dialog.update_idletasks()
        x = (details_dialog.winfo_screenwidth() // 2) - (250)
        y = (details_dialog.winfo_screenheight() // 2) - (300)
        details_dialog.geometry(f"500x600+{x}+{y}")

        # Details content (implementation would be similar to receipt view)
        ttk.Label(details_dialog, text="Order details view to be implemented").pack(pady=20)
        ttk.Button(details_dialog, text="Close", command=details_dialog.destroy).pack(pady=10)

    def show_context_menu(self, event) -> None:
        """Show context menu on right-click."""
        item = self.queue_tree.identify_row(event.y)
        if item:
            self.queue_tree.selection_set(item)
            self.on_order_selected(None)

            if self.selected_order:
                context_menu = tk.Menu(self.queue_tree, tearoff=0)

                # Status update options
                status = self.selected_order.status
                if status == OrderStatus.PENDING:
                    context_menu.add_command(
                        label="Start Preparing",
                        command=lambda: self.update_order_status(OrderStatus.PREPARING)
                    )
                elif status == OrderStatus.PREPARING:
                    context_menu.add_command(
                        label="Mark Ready",
                        command=lambda: self.update_order_status(OrderStatus.READY)
                    )
                elif status == OrderStatus.READY:
                    context_menu.add_command(
                        label="Complete Order",
                        command=lambda: self.update_order_status(OrderStatus.COMPLETED)
                    )

                context_menu.add_separator()
                context_menu.add_command(label="View Receipt", command=self.view_receipt)
                context_menu.add_command(label="Print Receipt", command=self.print_receipt)

                if status not in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
                    context_menu.add_separator()
                    context_menu.add_command(label="Cancel Order", command=self.cancel_order)

                try:
                    context_menu.tk_popup(event.x_root, event.y_root)
                finally:
                    context_menu.grab_release()

    def schedule_refresh(self) -> None:
        """Schedule the next auto-refresh."""
        if self.auto_refresh_enabled:
            self.frame.after(self.refresh_interval, self.auto_refresh)

    def auto_refresh(self) -> None:
        """Perform automatic refresh."""
        try:
            self.populate_queue_tree()
            self.update_last_updated()
            self.logger.debug("Auto-refresh completed")
        except Exception as e:
            self.logger.error(f"Auto-refresh failed: {e}")
        finally:
            self.schedule_refresh()

    def manual_refresh(self) -> None:
        """Perform manual refresh."""
        self.populate_queue_tree()
        self.update_last_updated()

    def toggle_auto_refresh(self) -> None:
        """Toggle auto-refresh on/off."""
        self.auto_refresh_enabled = self.auto_refresh_var.get()
        if self.auto_refresh_enabled:
            self.schedule_refresh()

    def update_last_updated(self) -> None:
        """Update the last updated timestamp."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_updated_label.config(text=f"Last updated: {current_time}")


# Import required for dialogs
import tkinter.simpledialog