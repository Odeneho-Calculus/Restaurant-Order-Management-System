"""
Preferences dialog for Restaurant Order Management System.

This module provides a comprehensive preferences dialog for configuring
system settings, appearance, and operational parameters.
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog
import logging
from pathlib import Path
from decimal import Decimal
from typing import Dict, Any, Optional

from ..utils import CSVHandler, InputValidator, ValidationError
from .. import config


class PreferencesDialog:
    """Comprehensive preferences dialog for system configuration."""

    def __init__(self, parent: tk.Tk, csv_handler: CSVHandler):
        """Initialize preferences dialog."""
        self.parent = parent
        self.csv_handler = csv_handler
        self.logger = logging.getLogger(__name__)

        # Store original values for cancel functionality
        self.original_values = {}

        # Create dialog
        self.create_dialog()
        self.load_current_settings()

    def create_dialog(self) -> None:
        """Create the preferences dialog window."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Preferences - Restaurant Management System")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        # Center the dialog
        self.center_dialog()

        # Create main container
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.dialog.grid_rowconfigure(0, weight=1)
        self.dialog.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Create notebook for categories
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        # Create preference categories
        self.create_general_tab()
        self.create_restaurant_tab()
        self.create_display_tab()
        self.create_system_tab()

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
        dialog_width = 600
        dialog_height = 500
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    def create_general_tab(self) -> None:
        """Create general preferences tab."""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="General")

        # Tax settings
        tax_frame = ttk.LabelFrame(frame, text="Tax Configuration", padding="10")
        tax_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        frame.grid_columnconfigure(0, weight=1)

        ttk.Label(tax_frame, text="Tax Rate (%):").grid(row=0, column=0, sticky="w")
        self.tax_rate_var = tk.StringVar(value=str(float(config.DEFAULT_TAX_RATE) * 100))
        tax_entry = ttk.Entry(tax_frame, textvariable=self.tax_rate_var, width=10)
        tax_entry.grid(row=0, column=1, sticky="w", padx=(10, 0))

        ttk.Label(tax_frame, text="Tax Label:").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.tax_label_var = tk.StringVar(value=config.TAX_LABEL)
        tax_label_entry = ttk.Entry(tax_frame, textvariable=self.tax_label_var, width=20)
        tax_label_entry.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(5, 0))

        self.enable_tax_var = tk.BooleanVar(value=config.ENABLE_TAX_CALCULATION)
        tax_check = ttk.Checkbutton(tax_frame, text="Enable tax calculation",
                                   variable=self.enable_tax_var)
        tax_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 0))

        # Currency settings
        currency_frame = ttk.LabelFrame(frame, text="Currency Settings", padding="10")
        currency_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(currency_frame, text="Currency Symbol:").grid(row=0, column=0, sticky="w")
        self.currency_symbol_var = tk.StringVar(value=config.CURRENCY_SYMBOL)
        currency_entry = ttk.Entry(currency_frame, textvariable=self.currency_symbol_var, width=5)
        currency_entry.grid(row=0, column=1, sticky="w", padx=(10, 0))

        ttk.Label(currency_frame, text="Decimal Places:").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.decimal_places_var = tk.StringVar(value=str(config.CURRENCY_DECIMAL_PLACES))
        decimal_spinbox = ttk.Spinbox(currency_frame, from_=0, to=4, width=5,
                                     textvariable=self.decimal_places_var)
        decimal_spinbox.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(5, 0))

        # Auto-save settings
        autosave_frame = ttk.LabelFrame(frame, text="Auto-save Settings", padding="10")
        autosave_frame.grid(row=2, column=0, sticky="ew")

        self.autosave_enabled_var = tk.BooleanVar(value=config.AUTO_SAVE_ENABLED)
        autosave_check = ttk.Checkbutton(autosave_frame, text="Enable auto-save",
                                        variable=self.autosave_enabled_var)
        autosave_check.grid(row=0, column=0, columnspan=2, sticky="w")

        ttk.Label(autosave_frame, text="Auto-save interval (minutes):").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.autosave_interval_var = tk.StringVar(value=str(config.AUTO_SAVE_INTERVAL // 60000))
        interval_spinbox = ttk.Spinbox(autosave_frame, from_=1, to=60, width=5,
                                      textvariable=self.autosave_interval_var)
        interval_spinbox.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(5, 0))

    def create_restaurant_tab(self) -> None:
        """Create restaurant information tab."""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Restaurant Info")

        # Create scrollable frame
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Restaurant information fields
        info_frame = ttk.LabelFrame(scrollable_frame, text="Restaurant Information", padding="10")
        info_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # Store variables for restaurant info
        self.restaurant_vars = {}

        fields = [
            ("name", "Restaurant Name:"),
            ("address", "Address:"),
            ("city", "City:"),
            ("state", "State:"),
            ("zip_code", "ZIP Code:"),
            ("phone", "Phone:"),
            ("email", "Email:"),
            ("website", "Website:")
        ]

        for i, (key, label) in enumerate(fields):
            ttk.Label(info_frame, text=label).grid(row=i, column=0, sticky="w", pady=2)
            var = tk.StringVar(value=config.RESTAURANT_INFO.get(key, ""))
            self.restaurant_vars[key] = var
            entry = ttk.Entry(info_frame, textvariable=var, width=40)
            entry.grid(row=i, column=1, sticky="ew", padx=(10, 0), pady=2)

        info_frame.grid_columnconfigure(1, weight=1)

    def create_display_tab(self) -> None:
        """Create display preferences tab."""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Display")

        # Window settings
        window_frame = ttk.LabelFrame(frame, text="Window Settings", padding="10")
        window_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        frame.grid_columnconfigure(0, weight=1)

        ttk.Label(window_frame, text="Default Window Size:").grid(row=0, column=0, sticky="w")
        self.window_size_var = tk.StringVar(value=config.WINDOW_SIZE)
        size_combo = ttk.Combobox(window_frame, textvariable=self.window_size_var,
                                 values=["1024x768", "1200x800", "1366x768", "1440x900", "1920x1080"],
                                 width=15)
        size_combo.grid(row=0, column=1, sticky="w", padx=(10, 0))

        # Queue settings
        queue_frame = ttk.LabelFrame(frame, text="Queue Display", padding="10")
        queue_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        self.queue_auto_refresh_var = tk.BooleanVar(value=config.QUEUE_AUTO_REFRESH)
        refresh_check = ttk.Checkbutton(queue_frame, text="Enable auto-refresh",
                                       variable=self.queue_auto_refresh_var)
        refresh_check.grid(row=0, column=0, columnspan=2, sticky="w")

        ttk.Label(queue_frame, text="Refresh interval (seconds):").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.refresh_interval_var = tk.StringVar(value=str(config.QUEUE_REFRESH_INTERVAL // 1000))
        interval_spinbox = ttk.Spinbox(queue_frame, from_=5, to=300, width=5,
                                      textvariable=self.refresh_interval_var)
        interval_spinbox.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(5, 0))

        # Receipt settings
        receipt_frame = ttk.LabelFrame(frame, text="Receipt Settings", padding="10")
        receipt_frame.grid(row=2, column=0, sticky="ew")

        ttk.Label(receipt_frame, text="Receipt Width (characters):").grid(row=0, column=0, sticky="w")
        self.receipt_width_var = tk.StringVar(value=str(config.RECEIPT_WIDTH))
        width_spinbox = ttk.Spinbox(receipt_frame, from_=40, to=120, width=5,
                                   textvariable=self.receipt_width_var)
        width_spinbox.grid(row=0, column=1, sticky="w", padx=(10, 0))

        self.receipt_logo_var = tk.BooleanVar(value=config.RECEIPT_PRINT_LOGO)
        logo_check = ttk.Checkbutton(receipt_frame, text="Print restaurant logo on receipts",
                                    variable=self.receipt_logo_var)
        logo_check.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))

        ttk.Label(receipt_frame, text="Footer Message:").grid(row=2, column=0, sticky="w", pady=(5, 0))
        self.receipt_footer_var = tk.StringVar(value=config.RECEIPT_FOOTER_MESSAGE)
        footer_entry = ttk.Entry(receipt_frame, textvariable=self.receipt_footer_var, width=40)
        footer_entry.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(5, 0))

        receipt_frame.grid_columnconfigure(1, weight=1)

    def create_system_tab(self) -> None:
        """Create system preferences tab."""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="System")

        # Logging settings
        logging_frame = ttk.LabelFrame(frame, text="Logging Settings", padding="10")
        logging_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        frame.grid_columnconfigure(0, weight=1)

        ttk.Label(logging_frame, text="Log Level:").grid(row=0, column=0, sticky="w")
        self.log_level_var = tk.StringVar(value=config.LOG_LEVEL)
        log_combo = ttk.Combobox(logging_frame, textvariable=self.log_level_var,
                                values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                                width=10, state="readonly")
        log_combo.grid(row=0, column=1, sticky="w", padx=(10, 0))

        self.detailed_logging_var = tk.BooleanVar(value=config.ENABLE_DETAILED_LOGGING)
        detailed_check = ttk.Checkbutton(logging_frame, text="Enable detailed logging",
                                        variable=self.detailed_logging_var)
        detailed_check.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))

        # Backup settings
        backup_frame = ttk.LabelFrame(frame, text="Backup Settings", padding="10")
        backup_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(backup_frame, text="Backup frequency (hours):").grid(row=0, column=0, sticky="w")
        self.backup_frequency_var = tk.StringVar(value=str(config.BACKUP_FREQUENCY_HOURS))
        backup_spinbox = ttk.Spinbox(backup_frame, from_=1, to=168, width=5,
                                    textvariable=self.backup_frequency_var)
        backup_spinbox.grid(row=0, column=1, sticky="w", padx=(10, 0))

        ttk.Label(backup_frame, text="Max backup files:").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.max_backups_var = tk.StringVar(value=str(config.MAX_BACKUP_FILES))
        max_spinbox = ttk.Spinbox(backup_frame, from_=1, to=100, width=5,
                                 textvariable=self.max_backups_var)
        max_spinbox.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(5, 0))

        self.backup_compression_var = tk.BooleanVar(value=config.BACKUP_COMPRESSION)
        compression_check = ttk.Checkbutton(backup_frame, text="Enable backup compression",
                                           variable=self.backup_compression_var)
        compression_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 0))

        # Performance settings
        performance_frame = ttk.LabelFrame(frame, text="Performance Settings", padding="10")
        performance_frame.grid(row=2, column=0, sticky="ew")

        ttk.Label(performance_frame, text="Max orders in memory:").grid(row=0, column=0, sticky="w")
        self.max_orders_var = tk.StringVar(value=str(config.MAX_ORDERS_IN_MEMORY))
        orders_spinbox = ttk.Spinbox(performance_frame, from_=100, to=10000, width=8,
                                    textvariable=self.max_orders_var)
        orders_spinbox.grid(row=0, column=1, sticky="w", padx=(10, 0))

        ttk.Label(performance_frame, text="Search delay (ms):").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.search_delay_var = tk.StringVar(value=str(config.SEARCH_DELAY_MS))
        delay_spinbox = ttk.Spinbox(performance_frame, from_=100, to=2000, width=8,
                                   textvariable=self.search_delay_var)
        delay_spinbox.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(5, 0))

    def create_buttons(self, parent: ttk.Frame) -> None:
        """Create dialog buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=1, column=0, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)

        # Button container (right-aligned)
        buttons = ttk.Frame(button_frame)
        buttons.grid(row=0, column=0, sticky="e")

        # Buttons
        ttk.Button(buttons, text="Restore Defaults",
                  command=self.restore_defaults).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(buttons, text="Cancel",
                  command=self.on_cancel).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(buttons, text="Apply",
                  command=self.on_apply).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(buttons, text="OK",
                  command=self.on_ok).grid(row=0, column=3)

    def load_current_settings(self) -> None:
        """Load current settings into the dialog."""
        # Store original values for cancel functionality
        self.original_values = {
            'tax_rate': self.tax_rate_var.get(),
            'tax_label': self.tax_label_var.get(),
            'enable_tax': self.enable_tax_var.get(),
            'currency_symbol': self.currency_symbol_var.get(),
            'decimal_places': self.decimal_places_var.get(),
            'autosave_enabled': self.autosave_enabled_var.get(),
            'autosave_interval': self.autosave_interval_var.get(),
            'restaurant_info': {k: v.get() for k, v in self.restaurant_vars.items()},
            'window_size': self.window_size_var.get(),
            'queue_auto_refresh': self.queue_auto_refresh_var.get(),
            'refresh_interval': self.refresh_interval_var.get(),
            'receipt_width': self.receipt_width_var.get(),
            'receipt_logo': self.receipt_logo_var.get(),
            'receipt_footer': self.receipt_footer_var.get(),
            'log_level': self.log_level_var.get(),
            'detailed_logging': self.detailed_logging_var.get(),
            'backup_frequency': self.backup_frequency_var.get(),
            'max_backups': self.max_backups_var.get(),
            'backup_compression': self.backup_compression_var.get(),
            'max_orders': self.max_orders_var.get(),
            'search_delay': self.search_delay_var.get()
        }

    def restore_defaults(self) -> None:
        """Restore all settings to default values."""
        if messagebox.askyesno("Restore Defaults",
                              "Are you sure you want to restore all settings to their default values?"):
            # Restore default values
            self.tax_rate_var.set("8.0")
            self.tax_label_var.set("Sales Tax")
            self.enable_tax_var.set(True)
            self.currency_symbol_var.set("$")
            self.decimal_places_var.set("2")
            self.autosave_enabled_var.set(True)
            self.autosave_interval_var.set("5")

            # Restore default restaurant info
            default_info = {
                'name': 'Gourmet Kitchen',
                'address': '123 Main Street',
                'city': 'Anytown',
                'state': 'ST',
                'zip_code': '12345',
                'phone': '(555) 123-4567',
                'email': 'info@gourmetkitchen.com',
                'website': 'www.gourmetkitchen.com'
            }
            for key, value in default_info.items():
                if key in self.restaurant_vars:
                    self.restaurant_vars[key].set(value)

            self.window_size_var.set("1200x800")
            self.queue_auto_refresh_var.set(True)
            self.refresh_interval_var.set("30")
            self.receipt_width_var.set("80")
            self.receipt_logo_var.set(True)
            self.receipt_footer_var.set("Thank you for your business!")
            self.log_level_var.set("INFO")
            self.detailed_logging_var.set(True)
            self.backup_frequency_var.set("24")
            self.max_backups_var.set("30")
            self.backup_compression_var.set(True)
            self.max_orders_var.set("1000")
            self.search_delay_var.set("500")

    def validate_settings(self) -> bool:
        """Validate all settings before applying."""
        try:
            # Validate tax rate
            tax_rate = float(self.tax_rate_var.get())
            if tax_rate < 0 or tax_rate > 100:
                raise ValueError("Tax rate must be between 0 and 100")

            # Validate decimal places
            decimal_places = int(self.decimal_places_var.get())
            if decimal_places < 0 or decimal_places > 4:
                raise ValueError("Decimal places must be between 0 and 4")

            # Validate autosave interval
            if self.autosave_enabled_var.get():
                interval = int(self.autosave_interval_var.get())
                if interval < 1 or interval > 60:
                    raise ValueError("Auto-save interval must be between 1 and 60 minutes")

            # Validate email if provided
            email = self.restaurant_vars['email'].get().strip()
            if email:
                InputValidator.validate_email(email, required=False)

            # Validate phone if provided
            phone = self.restaurant_vars['phone'].get().strip()
            if phone:
                InputValidator.validate_phone_number(phone, required=False)

            # Validate refresh interval
            refresh_interval = int(self.refresh_interval_var.get())
            if refresh_interval < 5 or refresh_interval > 300:
                raise ValueError("Refresh interval must be between 5 and 300 seconds")

            # Validate receipt width
            receipt_width = int(self.receipt_width_var.get())
            if receipt_width < 40 or receipt_width > 120:
                raise ValueError("Receipt width must be between 40 and 120 characters")

            return True

        except (ValueError, ValidationError) as e:
            messagebox.showerror("Invalid Settings", str(e))
            return False

    def apply_settings(self) -> None:
        """Apply the current settings."""
        if not self.validate_settings():
            return

        try:
            # Update configuration values
            config.DEFAULT_TAX_RATE = Decimal(str(float(self.tax_rate_var.get()) / 100))
            config.TAX_LABEL = self.tax_label_var.get()
            config.ENABLE_TAX_CALCULATION = self.enable_tax_var.get()
            config.CURRENCY_SYMBOL = self.currency_symbol_var.get()
            config.CURRENCY_DECIMAL_PLACES = int(self.decimal_places_var.get())
            config.AUTO_SAVE_ENABLED = self.autosave_enabled_var.get()
            config.AUTO_SAVE_INTERVAL = int(self.autosave_interval_var.get()) * 60000

            # Update restaurant info
            for key, var in self.restaurant_vars.items():
                config.RESTAURANT_INFO[key] = var.get()

            config.WINDOW_SIZE = self.window_size_var.get()
            config.QUEUE_AUTO_REFRESH = self.queue_auto_refresh_var.get()
            config.QUEUE_REFRESH_INTERVAL = int(self.refresh_interval_var.get()) * 1000
            config.RECEIPT_WIDTH = int(self.receipt_width_var.get())
            config.RECEIPT_PRINT_LOGO = self.receipt_logo_var.get()
            config.RECEIPT_FOOTER_MESSAGE = self.receipt_footer_var.get()
            config.LOG_LEVEL = self.log_level_var.get()
            config.ENABLE_DETAILED_LOGGING = self.detailed_logging_var.get()
            config.BACKUP_FREQUENCY_HOURS = int(self.backup_frequency_var.get())
            config.MAX_BACKUP_FILES = int(self.max_backups_var.get())
            config.BACKUP_COMPRESSION = self.backup_compression_var.get()
            config.MAX_ORDERS_IN_MEMORY = int(self.max_orders_var.get())
            config.SEARCH_DELAY_MS = int(self.search_delay_var.get())

            # Update window title
            config.WINDOW_TITLE = f"{config.RESTAURANT_INFO['name']} - {config.APP_NAME}"

            self.logger.info("Preferences updated successfully")
            messagebox.showinfo("Success", "Preferences have been updated successfully.\n\nSome changes may require restarting the application to take effect.")

        except Exception as e:
            self.logger.error(f"Failed to apply preferences: {e}")
            messagebox.showerror("Error", f"Failed to apply preferences: {e}")

    def on_ok(self) -> None:
        """Handle OK button click."""
        self.apply_settings()
        self.dialog.destroy()

    def on_apply(self) -> None:
        """Handle Apply button click."""
        self.apply_settings()

    def on_cancel(self) -> None:
        """Handle Cancel button click."""
        # Restore original values
        self.tax_rate_var.set(self.original_values['tax_rate'])
        self.tax_label_var.set(self.original_values['tax_label'])
        self.enable_tax_var.set(self.original_values['enable_tax'])
        self.currency_symbol_var.set(self.original_values['currency_symbol'])
        self.decimal_places_var.set(self.original_values['decimal_places'])
        self.autosave_enabled_var.set(self.original_values['autosave_enabled'])
        self.autosave_interval_var.set(self.original_values['autosave_interval'])

        for key, value in self.original_values['restaurant_info'].items():
            if key in self.restaurant_vars:
                self.restaurant_vars[key].set(value)

        self.window_size_var.set(self.original_values['window_size'])
        self.queue_auto_refresh_var.set(self.original_values['queue_auto_refresh'])
        self.refresh_interval_var.set(self.original_values['refresh_interval'])
        self.receipt_width_var.set(self.original_values['receipt_width'])
        self.receipt_logo_var.set(self.original_values['receipt_logo'])
        self.receipt_footer_var.set(self.original_values['receipt_footer'])
        self.log_level_var.set(self.original_values['log_level'])
        self.detailed_logging_var.set(self.original_values['detailed_logging'])
        self.backup_frequency_var.set(self.original_values['backup_frequency'])
        self.max_backups_var.set(self.original_values['max_backups'])
        self.backup_compression_var.set(self.original_values['backup_compression'])
        self.max_orders_var.set(self.original_values['max_orders'])
        self.search_delay_var.set(self.original_values['search_delay'])

        self.dialog.destroy()