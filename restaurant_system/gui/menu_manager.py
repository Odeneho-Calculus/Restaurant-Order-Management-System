"""
Menu Manager Tab for Restaurant Order Management System.

This module provides comprehensive menu management functionality including
adding, editing, deleting, and organizing menu items with validation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Callable
import logging

from ..models import MenuItem
from ..utils import InputValidator, ValidationError, CSVHandler


class MenuManagerTab:
    """
    Menu management tab providing comprehensive menu item operations.

    Features include adding, editing, deleting menu items, category management,
    availability toggling, and comprehensive search and filtering capabilities.
    """

    def __init__(self, parent: ttk.Notebook, menu_items: List[MenuItem],
                 csv_handler: CSVHandler, refresh_callback: Callable):
        """
        Initialize the menu manager tab.

        Args:
            parent (ttk.Notebook): Parent notebook widget
            menu_items (List[MenuItem]): Reference to menu items list
            csv_handler (CSVHandler): CSV data handler
            refresh_callback (Callable): Callback to refresh other tabs
        """
        self.parent = parent
        self.menu_items = menu_items
        self.csv_handler = csv_handler
        self.refresh_callback = refresh_callback
        self.logger = logging.getLogger(__name__)

        # Selected item tracking
        self.selected_item: Optional[MenuItem] = None

        # Create the main frame
        self.frame = ttk.Frame(parent, padding="10")

        # Setup the interface
        self.setup_interface()
        self.setup_bindings()

        # Initial refresh
        self.refresh_menu_list()

    def setup_interface(self) -> None:
        """Setup the menu manager interface."""
        # Configure grid weights
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # Left panel - Menu list and controls
        self.setup_left_panel()

        # Right panel - Item details and editing
        self.setup_right_panel()

    def setup_left_panel(self) -> None:
        """Setup the left panel with menu list and controls."""
        left_frame = ttk.Frame(self.frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_frame.grid_rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(left_frame, text="Menu Items", style='Heading.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Search and filter controls
        search_frame = ttk.Frame(left_frame)
        search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        search_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky="w", padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_changed)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 5))

        # Category filter
        ttk.Label(search_frame, text="Category:").grid(row=1, column=0, sticky="w", padx=(0, 5), pady=(5, 0))

        self.category_filter_var = tk.StringVar(value="All")
        self.category_filter_var.trace('w', self.on_filter_changed)
        category_combo = ttk.Combobox(
            search_frame,
            textvariable=self.category_filter_var,
            values=["All"] + list(MenuItem.VALID_CATEGORIES),
            state="readonly",
            width=15
        )
        category_combo.grid(row=1, column=1, sticky="ew", pady=(5, 0))

        # Availability filter
        self.availability_filter_var = tk.StringVar(value="All")
        self.availability_filter_var.trace('w', self.on_filter_changed)
        availability_combo = ttk.Combobox(
            search_frame,
            textvariable=self.availability_filter_var,
            values=["All", "Available", "Out of Stock"],
            state="readonly",
            width=15
        )
        availability_combo.grid(row=2, column=1, sticky="ew", pady=(5, 0))

        ttk.Label(search_frame, text="Status:").grid(row=2, column=0, sticky="w", padx=(0, 5), pady=(5, 0))

        # Menu items treeview
        self.setup_menu_treeview(left_frame)

        # Control buttons
        self.setup_control_buttons(left_frame)

    def setup_menu_treeview(self, parent: ttk.Frame) -> None:
        """Setup the menu items treeview."""
        # Treeview with scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Treeview
        columns = ("name", "category", "price", "status")
        self.menu_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=15
        )

        # Column configurations
        self.menu_tree.heading("name", text="Name")
        self.menu_tree.heading("category", text="Category")
        self.menu_tree.heading("price", text="Price")
        self.menu_tree.heading("status", text="Status")

        self.menu_tree.column("name", width=200, minwidth=150)
        self.menu_tree.column("category", width=100, minwidth=80)
        self.menu_tree.column("price", width=80, minwidth=60)
        self.menu_tree.column("status", width=100, minwidth=80)

        self.menu_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.menu_tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.menu_tree.configure(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.menu_tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.menu_tree.configure(xscrollcommand=h_scrollbar.set)

    def setup_control_buttons(self, parent: ttk.Frame) -> None:
        """Setup control buttons for menu operations."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

        # Create buttons
        self.add_button = ttk.Button(
            button_frame,
            text="Add Item",
            command=self.add_menu_item,
            style='Action.TButton'
        )
        self.add_button.pack(side="left", padx=(0, 5))

        self.edit_button = ttk.Button(
            button_frame,
            text="Edit Item",
            command=self.edit_menu_item,
            state="disabled"
        )
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = ttk.Button(
            button_frame,
            text="Delete Item",
            command=self.delete_menu_item,
            state="disabled",
            style='Danger.TButton'
        )
        self.delete_button.pack(side="left", padx=5)

        self.toggle_button = ttk.Button(
            button_frame,
            text="Toggle Availability",
            command=self.toggle_availability,
            state="disabled",
            style='Warning.TButton'
        )
        self.toggle_button.pack(side="left", padx=5)

    def setup_right_panel(self) -> None:
        """Setup the right panel for item details and editing."""
        right_frame = ttk.Frame(self.frame)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(right_frame, text="Item Details", style='Heading.TLabel')
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Details notebook
        self.details_notebook = ttk.Notebook(right_frame)
        self.details_notebook.grid(row=1, column=0, sticky="nsew")

        # Item details tab
        self.setup_details_tab()

        # Edit item tab
        self.setup_edit_tab()

    def setup_details_tab(self) -> None:
        """Setup the item details display tab."""
        details_frame = ttk.Frame(self.details_notebook, padding="10")
        self.details_notebook.add(details_frame, text="View Details")

        # Create labels for displaying item information
        self.detail_labels = {}

        fields = [
            ("ID:", "id"),
            ("Name:", "name"),
            ("Category:", "category"),
            ("Price:", "price"),
            ("Description:", "description"),
            ("Availability:", "availability")
        ]

        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(details_frame, text=label_text, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky="nw", padx=(0, 10), pady=5
            )

            if field_name == "description":
                # Multi-line text widget for description
                self.detail_labels[field_name] = tk.Text(
                    details_frame,
                    height=4,
                    width=40,
                    wrap="word",
                    state="disabled",
                    bg="#f0f0f0"
                )
                self.detail_labels[field_name].grid(
                    row=i, column=1, sticky="ew", pady=5
                )
            else:
                self.detail_labels[field_name] = ttk.Label(
                    details_frame,
                    text="",
                    font=('Arial', 10)
                )
                self.detail_labels[field_name].grid(
                    row=i, column=1, sticky="w", pady=5
                )

        details_frame.grid_columnconfigure(1, weight=1)

    def setup_edit_tab(self) -> None:
        """Setup the item editing tab."""
        edit_frame = ttk.Frame(self.details_notebook, padding="10")
        self.details_notebook.add(edit_frame, text="Edit Item")

        # Form fields
        self.form_vars = {}

        # Name field
        ttk.Label(edit_frame, text="Name:*").grid(row=0, column=0, sticky="w", pady=5)
        self.form_vars['name'] = tk.StringVar()
        name_entry = ttk.Entry(edit_frame, textvariable=self.form_vars['name'], width=30)
        name_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))

        # Category field
        ttk.Label(edit_frame, text="Category:*").grid(row=1, column=0, sticky="w", pady=5)
        self.form_vars['category'] = tk.StringVar()
        category_combo = ttk.Combobox(
            edit_frame,
            textvariable=self.form_vars['category'],
            values=list(MenuItem.VALID_CATEGORIES),
            state="readonly",
            width=27
        )
        category_combo.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))

        # Price field
        ttk.Label(edit_frame, text="Price:*").grid(row=2, column=0, sticky="w", pady=5)
        self.form_vars['price'] = tk.StringVar()
        price_entry = ttk.Entry(edit_frame, textvariable=self.form_vars['price'], width=30)
        price_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))

        # Description field
        ttk.Label(edit_frame, text="Description:").grid(row=3, column=0, sticky="nw", pady=5)
        self.description_text = tk.Text(edit_frame, height=4, width=30, wrap="word")
        self.description_text.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))

        # Availability checkbox
        self.form_vars['is_available'] = tk.BooleanVar(value=True)
        availability_check = ttk.Checkbutton(
            edit_frame,
            text="Available",
            variable=self.form_vars['is_available']
        )
        availability_check.grid(row=4, column=1, sticky="w", pady=10, padx=(10, 0))

        # Form buttons
        button_frame = ttk.Frame(edit_frame)
        button_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)

        self.save_button = ttk.Button(
            button_frame,
            text="Save Changes",
            command=self.save_item_changes,
            style='Success.TButton'
        )
        self.save_button.pack(side="left", padx=(0, 10))

        self.cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel_edit
        )
        self.cancel_button.pack(side="left")

        # Clear form button
        self.clear_button = ttk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form
        )
        self.clear_button.pack(side="right")

        edit_frame.grid_columnconfigure(1, weight=1)

    def setup_bindings(self) -> None:
        """Setup event bindings."""
        # Treeview selection
        self.menu_tree.bind('<<TreeviewSelect>>', self.on_item_selected)

        # Double-click to edit
        self.menu_tree.bind('<Double-1>', lambda e: self.edit_menu_item())

        # Right-click context menu
        self.menu_tree.bind('<Button-3>', self.show_context_menu)

        # Keyboard shortcuts
        self.frame.bind('<Control-n>', lambda e: self.add_menu_item())
        self.frame.bind('<Delete>', lambda e: self.delete_menu_item())
        self.frame.bind('<F2>', lambda e: self.edit_menu_item())

    def update_menu_items(self, menu_items: List[MenuItem]) -> None:
        """Update the menu items reference and refresh display."""
        self.menu_items = menu_items
        self.refresh_menu_list()

    def refresh_menu_list(self) -> None:
        """Refresh the menu items list display."""
        try:
            # Clear current items
            for item in self.menu_tree.get_children():
                self.menu_tree.delete(item)

            # Apply filters
            filtered_items = self.apply_filters()

            # Populate treeview
            for item in filtered_items:
                status = "Available" if item.is_available else "Out of Stock"
                values = (item.name, item.category.title(), f"${item.price:.2f}", status)

                item_id = self.menu_tree.insert("", "end", values=values, tags=(item.id,))

                # Color coding based on availability
                if not item.is_available:
                    self.menu_tree.set(item_id, "status", "Out of Stock")
                    self.menu_tree.item(item_id, tags=("unavailable",))

            # Configure tags
            self.menu_tree.tag_configure("unavailable", foreground="red")

            self.logger.info(f"Menu list refreshed with {len(filtered_items)} items")

        except Exception as e:
            self.logger.error(f"Failed to refresh menu list: {e}")
            messagebox.showerror("Error", f"Failed to refresh menu list: {e}")

    def apply_filters(self) -> List[MenuItem]:
        """Apply search and filter criteria to menu items."""
        filtered_items = self.menu_items.copy()

        # Search filter
        search_text = self.search_var.get().lower().strip()
        if search_text:
            filtered_items = [
                item for item in filtered_items
                if (search_text in item.name.lower() or
                    search_text in item.description.lower() or
                    search_text in item.category.lower())
            ]

        # Category filter
        category_filter = self.category_filter_var.get()
        if category_filter != "All":
            filtered_items = [
                item for item in filtered_items
                if item.category.lower() == category_filter.lower()
            ]

        # Availability filter
        availability_filter = self.availability_filter_var.get()
        if availability_filter == "Available":
            filtered_items = [item for item in filtered_items if item.is_available]
        elif availability_filter == "Out of Stock":
            filtered_items = [item for item in filtered_items if not item.is_available]

        return filtered_items

    def on_search_changed(self, *args) -> None:
        """Handle search text changes."""
        self.refresh_menu_list()

    def on_filter_changed(self, *args) -> None:
        """Handle filter changes."""
        self.refresh_menu_list()

    def on_item_selected(self, event) -> None:
        """Handle menu item selection."""
        selection = self.menu_tree.selection()

        if selection:
            # Get selected item
            item_id = self.menu_tree.item(selection[0])['tags'][0]
            self.selected_item = next((item for item in self.menu_items if item.id == item_id), None)

            if self.selected_item:
                self.display_item_details(self.selected_item)
                self.populate_edit_form(self.selected_item)

                # Enable buttons
                self.edit_button.config(state="normal")
                self.delete_button.config(state="normal")
                self.toggle_button.config(state="normal")
        else:
            self.clear_item_details()
            self.clear_form()
            self.selected_item = None

            # Disable buttons
            self.edit_button.config(state="disabled")
            self.delete_button.config(state="disabled")
            self.toggle_button.config(state="disabled")

    def display_item_details(self, item: MenuItem) -> None:
        """Display item details in the details tab."""
        self.detail_labels['id'].config(text=item.id)
        self.detail_labels['name'].config(text=item.name)
        self.detail_labels['category'].config(text=item.category.title())
        self.detail_labels['price'].config(text=f"${item.price:.2f}")
        self.detail_labels['availability'].config(
            text="Available" if item.is_available else "Out of Stock"
        )

        # Update description text
        desc_widget = self.detail_labels['description']
        desc_widget.config(state="normal")
        desc_widget.delete(1.0, tk.END)
        desc_widget.insert(1.0, item.description)
        desc_widget.config(state="disabled")

    def clear_item_details(self) -> None:
        """Clear the item details display."""
        for field_name, widget in self.detail_labels.items():
            if field_name == "description":
                widget.config(state="normal")
                widget.delete(1.0, tk.END)
                widget.config(state="disabled")
            else:
                widget.config(text="")

    def populate_edit_form(self, item: MenuItem) -> None:
        """Populate the edit form with item data."""
        self.form_vars['name'].set(item.name)
        self.form_vars['category'].set(item.category)
        self.form_vars['price'].set(str(item.price))
        self.form_vars['is_available'].set(item.is_available)

        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(1.0, item.description)

    def clear_form(self) -> None:
        """Clear the edit form."""
        for var in self.form_vars.values():
            if isinstance(var, tk.BooleanVar):
                var.set(True)
            else:
                var.set("")

        self.description_text.delete(1.0, tk.END)

    def add_menu_item(self) -> None:
        """Add a new menu item."""
        self.clear_form()
        self.selected_item = None
        self.details_notebook.select(1)  # Switch to edit tab

        # Focus on name field
        name_entry = self.form_vars['name']
        # Find the name entry widget and focus it
        for widget in self.details_notebook.nametowidget(self.details_notebook.select()).winfo_children():
            if isinstance(widget, ttk.Entry) and widget['textvariable'] == str(name_entry):
                widget.focus()
                break

    def edit_menu_item(self) -> None:
        """Edit the selected menu item."""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select an item to edit")
            return

        self.details_notebook.select(1)  # Switch to edit tab

    def save_item_changes(self) -> None:
        """Save changes to the menu item."""
        try:
            # Validate form data
            name = InputValidator.validate_required_string(
                self.form_vars['name'].get(), "Name"
            )
            category = InputValidator.validate_category(
                self.form_vars['category'].get(), list(MenuItem.VALID_CATEGORIES)
            )
            price = InputValidator.validate_price(self.form_vars['price'].get())
            description = self.description_text.get(1.0, tk.END).strip()
            is_available = self.form_vars['is_available'].get()

            if self.selected_item:
                # Update existing item
                self.selected_item.name = name
                self.selected_item.category = category
                self.selected_item.price = float(price)
                self.selected_item.description = description
                self.selected_item.is_available = is_available

                message = f"Menu item '{name}' updated successfully"
            else:
                # Create new item
                new_item = MenuItem(
                    name=name,
                    category=category,
                    price=float(price),
                    description=description,
                    is_available=is_available
                )
                self.menu_items.append(new_item)
                self.selected_item = new_item

                message = f"Menu item '{name}' added successfully"

            # Save to CSV
            if not self.csv_handler.save_menu_items(self.menu_items):
                raise Exception("Failed to save menu items to file")

            # Refresh displays
            self.refresh_menu_list()
            self.refresh_callback()

            # Show success message
            messagebox.showinfo("Success", message)

            # Switch back to details tab
            self.details_notebook.select(0)

            self.logger.info(message)

        except ValidationError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            self.logger.error(f"Failed to save menu item: {e}")
            messagebox.showerror("Error", f"Failed to save menu item: {e}")

    def cancel_edit(self) -> None:
        """Cancel editing and return to details view."""
        if self.selected_item:
            self.populate_edit_form(self.selected_item)
        else:
            self.clear_form()

        self.details_notebook.select(0)  # Switch to details tab

    def delete_menu_item(self) -> None:
        """Delete the selected menu item."""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return

        # Confirm deletion
        if messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete '{self.selected_item.name}'?\n\n"
            "This action cannot be undone."
        ):
            try:
                # Remove from list
                self.menu_items.remove(self.selected_item)

                # Save to CSV
                if not self.csv_handler.save_menu_items(self.menu_items):
                    raise Exception("Failed to save menu items to file")

                # Clear selection and refresh
                self.selected_item = None
                self.refresh_menu_list()
                self.refresh_callback()
                self.clear_item_details()
                self.clear_form()

                messagebox.showinfo("Success", "Menu item deleted successfully")
                self.logger.info(f"Menu item deleted: {self.selected_item.name}")

            except Exception as e:
                self.logger.error(f"Failed to delete menu item: {e}")
                messagebox.showerror("Error", f"Failed to delete menu item: {e}")

    def toggle_availability(self) -> None:
        """Toggle the availability of the selected menu item."""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select an item to toggle availability")
            return

        try:
            # Toggle availability
            self.selected_item.is_available = not self.selected_item.is_available

            # Save to CSV
            if not self.csv_handler.save_menu_items(self.menu_items):
                raise Exception("Failed to save menu items to file")

            # Refresh displays
            self.refresh_menu_list()
            self.refresh_callback()
            self.display_item_details(self.selected_item)
            self.populate_edit_form(self.selected_item)

            status = "available" if self.selected_item.is_available else "out of stock"
            messagebox.showinfo("Success", f"'{self.selected_item.name}' is now {status}")

            self.logger.info(f"Toggled availability for {self.selected_item.name}: {status}")

        except Exception as e:
            self.logger.error(f"Failed to toggle availability: {e}")
            messagebox.showerror("Error", f"Failed to toggle availability: {e}")

    def show_context_menu(self, event) -> None:
        """Show context menu on right-click."""
        # Select item under cursor
        item = self.menu_tree.identify_row(event.y)
        if item:
            self.menu_tree.selection_set(item)
            self.on_item_selected(None)

            # Create context menu
            context_menu = tk.Menu(self.menu_tree, tearoff=0)
            context_menu.add_command(label="Edit Item", command=self.edit_menu_item)
            context_menu.add_command(label="Toggle Availability", command=self.toggle_availability)
            context_menu.add_separator()
            context_menu.add_command(label="Delete Item", command=self.delete_menu_item)

            # Show menu
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()