"""
Restaurant information dialog for Restaurant Order Management System.

This module provides a dialog for editing restaurant information
that appears on receipts and reports.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Dict

from ..utils import InputValidator, ValidationError
from .. import config


class RestaurantInfoDialog:
    """Dialog for editing restaurant information."""

    def __init__(self, parent: tk.Tk):
        """Initialize restaurant info dialog."""
        self.parent = parent
        self.logger = logging.getLogger(__name__)

        # Store original values
        self.original_values = config.RESTAURANT_INFO.copy()

        # Create dialog
        self.create_dialog()
        self.load_current_info()

    def create_dialog(self) -> None:
        """Create the restaurant info dialog."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Restaurant Information")
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
        title_label = ttk.Label(main_frame, text="Restaurant Information",
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Create form fields
        self.create_form_fields(main_frame)

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

    def create_form_fields(self, parent: ttk.Frame) -> None:
        """Create form fields for restaurant information."""
        # Create scrollable frame for form
        canvas = tk.Canvas(parent, height=250)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 20))
        scrollbar.grid(row=1, column=2, sticky="ns", pady=(0, 20))

        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Form fields
        self.info_vars = {}

        fields = [
            ("name", "Restaurant Name:", True, "The name of your restaurant"),
            ("address", "Street Address:", False, "Street address for receipts"),
            ("city", "City:", False, "City name"),
            ("state", "State/Province:", False, "State or province"),
            ("zip_code", "ZIP/Postal Code:", False, "ZIP or postal code"),
            ("phone", "Phone Number:", False, "Contact phone number"),
            ("email", "Email Address:", False, "Contact email address"),
            ("website", "Website:", False, "Restaurant website URL")
        ]

        for i, (key, label, required, tooltip) in enumerate(fields):
            # Label with required indicator
            label_text = label
            if required:
                label_text += " *"

            label_widget = ttk.Label(scrollable_frame, text=label_text)
            label_widget.grid(row=i*2, column=0, sticky="w", pady=(5, 2))

            # Entry field
            var = tk.StringVar()
            self.info_vars[key] = var

            entry = ttk.Entry(scrollable_frame, textvariable=var, width=50)
            entry.grid(row=i*2, column=1, sticky="ew", padx=(10, 0), pady=(5, 2))

            # Tooltip/help text
            help_label = ttk.Label(scrollable_frame, text=tooltip,
                                  font=('Arial', 8), foreground='gray')
            help_label.grid(row=i*2+1, column=1, sticky="w", padx=(10, 0), pady=(0, 5))

        scrollable_frame.grid_columnconfigure(1, weight=1)

        # Required fields note
        note_label = ttk.Label(parent, text="* Required fields",
                              font=('Arial', 8), foreground='gray')
        note_label.grid(row=2, column=0, sticky="w")

    def create_buttons(self, parent: ttk.Frame) -> None:
        """Create dialog buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        button_frame.grid_columnconfigure(0, weight=1)

        # Button container (right-aligned)
        buttons = ttk.Frame(button_frame)
        buttons.grid(row=0, column=0, sticky="e")

        # Buttons
        ttk.Button(buttons, text="Preview Receipt",
                  command=self.preview_receipt).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(buttons, text="Cancel",
                  command=self.on_cancel).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(buttons, text="Save",
                  command=self.on_save).grid(row=0, column=2)

    def load_current_info(self) -> None:
        """Load current restaurant information into the form."""
        for key, var in self.info_vars.items():
            value = config.RESTAURANT_INFO.get(key, "")
            var.set(value)

    def validate_info(self) -> bool:
        """Validate the restaurant information."""
        try:
            # Check required fields
            name = self.info_vars['name'].get().strip()
            if not name:
                raise ValidationError("Restaurant name is required")

            # Validate email if provided
            email = self.info_vars['email'].get().strip()
            if email:
                InputValidator.validate_email(email, required=False)

            # Validate phone if provided
            phone = self.info_vars['phone'].get().strip()
            if phone:
                InputValidator.validate_phone_number(phone, required=False)

            # Validate website if provided
            website = self.info_vars['website'].get().strip()
            if website and not website.startswith(('http://', 'https://', 'www.')):
                if '.' in website:  # Looks like a domain
                    self.info_vars['website'].set(f"www.{website}")

            return True

        except ValidationError as e:
            messagebox.showerror("Validation Error", str(e))
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Validation failed: {e}")
            return False

    def preview_receipt(self) -> None:
        """Preview how the restaurant info will look on a receipt."""
        if not self.validate_info():
            return

        # Create preview window
        preview = tk.Toplevel(self.dialog)
        preview.title("Receipt Preview")
        preview.geometry("400x300")
        preview.transient(self.dialog)

        # Create text widget for preview
        text_frame = ttk.Frame(preview, padding="10")
        text_frame.grid(row=0, column=0, sticky="nsew")

        preview.grid_rowconfigure(0, weight=1)
        preview.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Courier', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Generate preview content
        preview_text = self.generate_receipt_preview()
        text_widget.insert(tk.END, preview_text)
        text_widget.config(state=tk.DISABLED)

        # Close button
        close_button = ttk.Button(preview, text="Close", command=preview.destroy)
        close_button.grid(row=1, column=0, pady=10)

    def generate_receipt_preview(self) -> str:
        """Generate a preview of how the restaurant info will appear on receipts."""
        info = {key: var.get().strip() for key, var in self.info_vars.items()}

        lines = []
        lines.append("=" * 40)
        lines.append("RECEIPT PREVIEW")
        lines.append("=" * 40)
        lines.append("")

        # Restaurant name (centered)
        if info['name']:
            lines.append(info['name'].center(40))
            lines.append("")

        # Address information
        if info['address']:
            lines.append(info['address'].center(40))

        city_state_zip = []
        if info['city']:
            city_state_zip.append(info['city'])
        if info['state']:
            city_state_zip.append(info['state'])
        if info['zip_code']:
            city_state_zip.append(info['zip_code'])

        if city_state_zip:
            city_line = ", ".join(city_state_zip[:2])  # City, State
            if len(city_state_zip) > 2:
                city_line += f" {city_state_zip[2]}"  # ZIP
            lines.append(city_line.center(40))

        if info['phone']:
            lines.append(info['phone'].center(40))

        if info['email']:
            lines.append(info['email'].center(40))

        if info['website']:
            lines.append(info['website'].center(40))

        lines.append("")
        lines.append("-" * 40)
        lines.append("Order #12345")
        lines.append("Date: 2025-07-30 19:30:00")
        lines.append("Table: 5")
        lines.append("-" * 40)
        lines.append("1x Sample Burger          $15.99")
        lines.append("2x Sample Fries           $11.98")
        lines.append("-" * 40)
        lines.append("Subtotal:                 $27.97")
        lines.append("Tax (8%):                  $2.24")
        lines.append("Total:                    $30.21")
        lines.append("-" * 40)
        lines.append("")
        lines.append("Thank you for your business!")
        lines.append("=" * 40)

        return "\n".join(lines)

    def save_info(self) -> None:
        """Save the restaurant information."""
        if not self.validate_info():
            return

        try:
            # Update configuration
            for key, var in self.info_vars.items():
                config.RESTAURANT_INFO[key] = var.get().strip()

            # Update window title
            config.WINDOW_TITLE = f"{config.RESTAURANT_INFO['name']} - {config.APP_NAME}"

            self.logger.info("Restaurant information updated successfully")
            messagebox.showinfo("Success", "Restaurant information has been saved successfully!")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save restaurant info: {e}")
            messagebox.showerror("Error", f"Failed to save restaurant information: {e}")
            return False

    def on_save(self) -> None:
        """Handle Save button click."""
        if self.save_info():
            self.dialog.destroy()

    def on_cancel(self) -> None:
        """Handle Cancel button click."""
        # Check if changes were made
        changes_made = False
        for key, var in self.info_vars.items():
            if var.get().strip() != self.original_values.get(key, ""):
                changes_made = True
                break

        if changes_made:
            if messagebox.askyesno("Unsaved Changes",
                                  "You have unsaved changes. Are you sure you want to cancel?"):
                self.dialog.destroy()
        else:
            self.dialog.destroy()