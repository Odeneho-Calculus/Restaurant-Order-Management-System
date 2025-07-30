"""
Data restore dialog for Restaurant Order Management System.

This module provides a dialog for restoring data from backup files
or importing data from external sources.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import Callable, List, Dict, Any
import zipfile
import json

from ..utils import CSVHandler


class DataRestoreDialog:
    """Dialog for restoring data from backups."""

    def __init__(self, parent: tk.Tk, csv_handler: CSVHandler, refresh_callback: Callable):
        """Initialize data restore dialog."""
        self.parent = parent
        self.csv_handler = csv_handler
        self.refresh_callback = refresh_callback
        self.logger = logging.getLogger(__name__)

        # Create dialog
        self.create_dialog()

    def create_dialog(self) -> None:
        """Create the data restore dialog."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Restore Data")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        # Center the dialog
        self.center_dialog()

        # Create main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.dialog.grid_rowconfigure(0, weight=1)
        self.dialog.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Restore Data",
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))

        # Create notebook for restore options
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky="nsew", pady=(0, 20))

        # Create tabs
        self.create_backup_restore_tab()
        self.create_file_restore_tab()
        self.create_emergency_restore_tab()

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

    def create_backup_restore_tab(self) -> None:
        """Create backup restore tab."""
        frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(frame, text="From Backup")

        # Instructions
        instructions = ttk.Label(frame,
                                text="Restore data from a previously created backup file.",
                                font=('Arial', 10))
        instructions.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # Backup file selection
        file_frame = ttk.LabelFrame(frame, text="Select Backup File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        frame.grid_columnconfigure(0, weight=1)

        self.backup_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.backup_file_var, width=50)
        file_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        file_frame.grid_columnconfigure(0, weight=1)

        browse_button = ttk.Button(file_frame, text="Browse...",
                                  command=self.browse_backup_file)
        browse_button.grid(row=0, column=1)

        # Backup info display
        info_frame = ttk.LabelFrame(frame, text="Backup Information", padding="10")
        info_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        self.backup_info_text = tk.Text(info_frame, height=8, width=60, wrap=tk.WORD)
        info_scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.backup_info_text.yview)
        self.backup_info_text.configure(yscrollcommand=info_scrollbar.set)

        self.backup_info_text.grid(row=0, column=0, sticky="nsew")
        info_scrollbar.grid(row=0, column=1, sticky="ns")
        info_frame.grid_rowconfigure(0, weight=1)
        info_frame.grid_columnconfigure(0, weight=1)

        # Restore options
        options_frame = ttk.LabelFrame(frame, text="Restore Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.restore_menu_var = tk.BooleanVar(value=True)
        menu_check = ttk.Checkbutton(options_frame, text="Restore menu items",
                                    variable=self.restore_menu_var)
        menu_check.grid(row=0, column=0, sticky="w")

        self.restore_orders_var = tk.BooleanVar(value=True)
        orders_check = ttk.Checkbutton(options_frame, text="Restore orders",
                                      variable=self.restore_orders_var)
        orders_check.grid(row=1, column=0, sticky="w", pady=(5, 0))

        self.restore_reports_var = tk.BooleanVar(value=True)
        reports_check = ttk.Checkbutton(options_frame, text="Restore sales reports",
                                       variable=self.restore_reports_var)
        reports_check.grid(row=2, column=0, sticky="w", pady=(5, 0))

        self.backup_current_var = tk.BooleanVar(value=True)
        backup_check = ttk.Checkbutton(options_frame, text="Backup current data before restore",
                                      variable=self.backup_current_var)
        backup_check.grid(row=3, column=0, sticky="w", pady=(10, 0))

    def create_file_restore_tab(self) -> None:
        """Create individual file restore tab."""
        frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(frame, text="Individual Files")

        # Instructions
        instructions = ttk.Label(frame,
                                text="Restore individual CSV files (menu items, orders, or reports).",
                                font=('Arial', 10))
        instructions.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # File type selection
        type_frame = ttk.LabelFrame(frame, text="Data Type", padding="10")
        type_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        frame.grid_columnconfigure(0, weight=1)

        self.file_type_var = tk.StringVar(value="menu_items")

        ttk.Radiobutton(type_frame, text="Menu Items", variable=self.file_type_var,
                       value="menu_items").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(type_frame, text="Orders", variable=self.file_type_var,
                       value="orders").grid(row=0, column=1, sticky="w", padx=(20, 0))
        ttk.Radiobutton(type_frame, text="Sales Reports", variable=self.file_type_var,
                       value="sales_reports").grid(row=0, column=2, sticky="w", padx=(20, 0))

        # File selection
        file_frame = ttk.LabelFrame(frame, text="Select File", padding="10")
        file_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        self.restore_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.restore_file_var, width=50)
        file_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        file_frame.grid_columnconfigure(0, weight=1)

        browse_button = ttk.Button(file_frame, text="Browse...",
                                  command=self.browse_restore_file)
        browse_button.grid(row=0, column=1)

        # Preview area
        preview_frame = ttk.LabelFrame(frame, text="File Preview", padding="10")
        preview_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(0, 15))
        frame.grid_rowconfigure(3, weight=1)

        self.preview_text = tk.Text(preview_frame, height=10, width=60, wrap=tk.NONE)
        preview_h_scroll = ttk.Scrollbar(preview_frame, orient="horizontal", command=self.preview_text.xview)
        preview_v_scroll = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview_text.yview)
        self.preview_text.configure(xscrollcommand=preview_h_scroll.set, yscrollcommand=preview_v_scroll.set)

        self.preview_text.grid(row=0, column=0, sticky="nsew")
        preview_h_scroll.grid(row=1, column=0, sticky="ew")
        preview_v_scroll.grid(row=0, column=1, sticky="ns")
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)

        # Restore options
        options_frame = ttk.LabelFrame(frame, text="Import Options", padding="10")
        options_frame.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.replace_data_var = tk.BooleanVar(value=False)
        replace_check = ttk.Checkbutton(options_frame, text="Replace existing data",
                                       variable=self.replace_data_var)
        replace_check.grid(row=0, column=0, sticky="w")

        help_label = ttk.Label(options_frame,
                              text="If unchecked, data will be merged with existing records",
                              font=('Arial', 8), foreground='gray')
        help_label.grid(row=1, column=0, sticky="w", pady=(2, 0))

    def create_emergency_restore_tab(self) -> None:
        """Create emergency restore tab."""
        frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(frame, text="Emergency")

        # Warning
        warning_frame = ttk.Frame(frame)
        warning_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        frame.grid_columnconfigure(0, weight=1)

        warning_label = ttk.Label(warning_frame,
                                 text="⚠️ Emergency Data Recovery",
                                 font=('Arial', 12, 'bold'), foreground='red')
        warning_label.grid(row=0, column=0, sticky="w")

        warning_desc = ttk.Label(warning_frame,
                                text="Use these options only if your data files are corrupted or missing.",
                                font=('Arial', 10))
        warning_desc.grid(row=1, column=0, sticky="w", pady=(5, 0))

        # Recovery options
        recovery_frame = ttk.LabelFrame(frame, text="Recovery Options", padding="15")
        recovery_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))

        # Reset to defaults
        reset_button = ttk.Button(recovery_frame, text="Reset to Default Data",
                                 command=self.reset_to_defaults)
        reset_button.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        reset_desc = ttk.Label(recovery_frame,
                              text="• Restores sample menu items\n• Clears all orders and reports\n• Resets configuration to defaults",
                              font=('Arial', 9), foreground='gray')
        reset_desc.grid(row=1, column=0, sticky="w", pady=(0, 15))

        # Recreate data structure
        recreate_button = ttk.Button(recovery_frame, text="Recreate Data Files",
                                    command=self.recreate_data_files)
        recreate_button.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        recreate_desc = ttk.Label(recovery_frame,
                                 text="• Creates empty data files with proper structure\n• Preserves any existing data that can be read\n• Fixes file corruption issues",
                                 font=('Arial', 9), foreground='gray')
        recreate_desc.grid(row=3, column=0, sticky="w", pady=(0, 15))

        recovery_frame.grid_columnconfigure(0, weight=1)

        # Status area
        status_frame = ttk.LabelFrame(frame, text="Recovery Status", padding="10")
        status_frame.grid(row=2, column=0, sticky="nsew")
        frame.grid_rowconfigure(2, weight=1)

        self.status_text = tk.Text(status_frame, height=8, width=60, wrap=tk.WORD)
        status_scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)

        self.status_text.grid(row=0, column=0, sticky="nsew")
        status_scrollbar.grid(row=0, column=1, sticky="ns")
        status_frame.grid_rowconfigure(0, weight=1)
        status_frame.grid_columnconfigure(0, weight=1)

    def create_buttons(self, parent: ttk.Frame) -> None:
        """Create dialog buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)

        # Button container (right-aligned)
        buttons = ttk.Frame(button_frame)
        buttons.grid(row=0, column=0, sticky="e")

        # Buttons
        ttk.Button(buttons, text="Cancel",
                  command=self.on_cancel).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(buttons, text="Restore",
                  command=self.perform_restore).grid(row=0, column=1)

    def browse_backup_file(self) -> None:
        """Browse for backup file."""
        file_path = filedialog.askopenfilename(
            title="Select Backup File",
            filetypes=[
                ("Backup files", "*.zip"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.backup_file_var.set(file_path)
            self.analyze_backup_file(file_path)

    def browse_restore_file(self) -> None:
        """Browse for individual restore file."""
        file_path = filedialog.askopenfilename(
            title="Select File to Restore",
            filetypes=[
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.restore_file_var.set(file_path)
            self.preview_restore_file(file_path)

    def analyze_backup_file(self, file_path: str) -> None:
        """Analyze backup file and display information."""
        try:
            self.backup_info_text.delete(1.0, tk.END)

            if file_path.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_file:
                    file_list = zip_file.namelist()

                    info_lines = [
                        f"Backup File: {Path(file_path).name}",
                        f"File Size: {Path(file_path).stat().st_size / 1024:.1f} KB",
                        f"Created: {datetime.fromtimestamp(Path(file_path).stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}",
                        "",
                        "Contents:"
                    ]

                    for file_name in sorted(file_list):
                        if file_name.endswith('.csv'):
                            try:
                                with zip_file.open(file_name) as csv_file:
                                    lines = csv_file.read().decode('utf-8').split('\n')
                                    record_count = len([line for line in lines if line.strip()]) - 1  # Subtract header
                                    info_lines.append(f"  • {file_name}: {max(0, record_count)} records")
                            except:
                                info_lines.append(f"  • {file_name}: Unable to read")
                        else:
                            info_lines.append(f"  • {file_name}")

                    self.backup_info_text.insert(tk.END, "\n".join(info_lines))
            else:
                self.backup_info_text.insert(tk.END, "Selected file is not a recognized backup format.")

        except Exception as e:
            self.backup_info_text.insert(tk.END, f"Error analyzing backup file: {e}")

    def preview_restore_file(self, file_path: str) -> None:
        """Preview the contents of a restore file."""
        try:
            self.preview_text.delete(1.0, tk.END)

            with open(file_path, 'r', encoding='utf-8') as file:
                # Read first 20 lines for preview
                lines = []
                for i, line in enumerate(file):
                    if i >= 20:
                        lines.append("... (file continues)")
                        break
                    lines.append(line.rstrip())

                self.preview_text.insert(tk.END, "\n".join(lines))

        except Exception as e:
            self.preview_text.insert(tk.END, f"Error reading file: {e}")

    def reset_to_defaults(self) -> None:
        """Reset system to default data."""
        if not messagebox.askyesno("Confirm Reset",
                                  "This will replace ALL current data with default sample data.\n\n"
                                  "This action cannot be undone. Continue?"):
            return

        try:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, "Starting reset to defaults...\n")
            self.status_text.update()

            # Import sample data dialog functionality
            from .sample_data_dialog import SampleDataDialog

            # Create sample menu items
            sample_dialog = SampleDataDialog(self.dialog, self.csv_handler, self.refresh_callback)
            menu_items = sample_dialog.generate_comprehensive_menu()

            self.csv_handler.save_menu_items(menu_items)
            self.status_text.insert(tk.END, f"✓ Created {len(menu_items)} sample menu items\n")

            # Clear orders and reports
            self.csv_handler.save_orders([])
            self.status_text.insert(tk.END, "✓ Cleared all orders\n")

            # Clear sales reports
            from ..config import DATA_DIR
            sales_file = DATA_DIR / "sales_reports.csv"
            if sales_file.exists():
                sales_file.write_text("order_id,customer_name,order_time,total_amount,payment_method\n")
            self.status_text.insert(tk.END, "✓ Cleared sales reports\n")

            self.status_text.insert(tk.END, "\n✅ Reset completed successfully!")

            # Refresh the application
            self.refresh_callback()

            messagebox.showinfo("Reset Complete", "System has been reset to default data successfully!")

        except Exception as e:
            self.logger.error(f"Failed to reset to defaults: {e}")
            self.status_text.insert(tk.END, f"\n❌ Error: {e}")
            messagebox.showerror("Reset Failed", f"Failed to reset system: {e}")

    def recreate_data_files(self) -> None:
        """Recreate data files with proper structure."""
        if not messagebox.askyesno("Confirm Recreation",
                                  "This will recreate all data files with proper structure.\n\n"
                                  "Existing data will be preserved where possible. Continue?"):
            return

        try:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, "Recreating data files...\n")
            self.status_text.update()

            from ..config import DATA_DIR

            # Ensure data directory exists
            DATA_DIR.mkdir(exist_ok=True)
            self.status_text.insert(tk.END, f"✓ Data directory: {DATA_DIR}\n")

            # Recreate menu items file
            menu_file = DATA_DIR / "menu_items.csv"
            try:
                existing_items = self.csv_handler.load_menu_items()
                self.csv_handler.save_menu_items(existing_items)
                self.status_text.insert(tk.END, f"✓ Menu items file: {len(existing_items)} items preserved\n")
            except:
                menu_file.write_text("id,name,category,price,description,is_available\n")
                self.status_text.insert(tk.END, "✓ Menu items file: Created empty structure\n")

            # Recreate orders file
            orders_file = DATA_DIR / "orders.csv"
            try:
                menu_dict = {item.id: item for item in self.csv_handler.load_menu_items()}
                existing_orders = self.csv_handler.load_orders(menu_dict)
                self.csv_handler.save_orders(existing_orders)
                self.status_text.insert(tk.END, f"✓ Orders file: {len(existing_orders)} orders preserved\n")
            except:
                orders_file.write_text("order_id,customer_name,customer_phone,table_number,order_type,status,order_time,items\n")
                self.status_text.insert(tk.END, "✓ Orders file: Created empty structure\n")

            # Recreate sales reports file
            sales_file = DATA_DIR / "sales_reports.csv"
            if not sales_file.exists():
                sales_file.write_text("order_id,customer_name,order_time,total_amount,payment_method\n")
                self.status_text.insert(tk.END, "✓ Sales reports file: Created empty structure\n")
            else:
                self.status_text.insert(tk.END, "✓ Sales reports file: Already exists\n")

            self.status_text.insert(tk.END, "\n✅ Data files recreation completed!")

            # Refresh the application
            self.refresh_callback()

            messagebox.showinfo("Recreation Complete", "Data files have been recreated successfully!")

        except Exception as e:
            self.logger.error(f"Failed to recreate data files: {e}")
            self.status_text.insert(tk.END, f"\n❌ Error: {e}")
            messagebox.showerror("Recreation Failed", f"Failed to recreate data files: {e}")

    def perform_restore(self) -> None:
        """Perform the selected restore operation."""
        current_tab = self.notebook.tab(self.notebook.select(), "text")

        if current_tab == "From Backup":
            self.restore_from_backup()
        elif current_tab == "Individual Files":
            self.restore_individual_file()
        else:
            messagebox.showinfo("Info", "Use the buttons in the Emergency tab for recovery operations.")

    def restore_from_backup(self) -> None:
        """Restore data from backup file."""
        backup_file = self.backup_file_var.get().strip()
        if not backup_file:
            messagebox.showwarning("No File Selected", "Please select a backup file to restore.")
            return

        if not Path(backup_file).exists():
            messagebox.showerror("File Not Found", "The selected backup file does not exist.")
            return

        try:
            # Implementation for backup restore would go here
            messagebox.showinfo("Restore", "Backup restore functionality is ready for implementation.")

        except Exception as e:
            self.logger.error(f"Failed to restore from backup: {e}")
            messagebox.showerror("Restore Failed", f"Failed to restore from backup: {e}")

    def restore_individual_file(self) -> None:
        """Restore individual file."""
        file_path = self.restore_file_var.get().strip()
        if not file_path:
            messagebox.showwarning("No File Selected", "Please select a file to restore.")
            return

        if not Path(file_path).exists():
            messagebox.showerror("File Not Found", "The selected file does not exist.")
            return

        try:
            file_type = self.file_type_var.get()
            replace_data = self.replace_data_var.get()

            if file_type == "menu_items":
                # Use the existing import functionality
                from ..gui.main_window import RestaurantMainWindow
                main_window = RestaurantMainWindow()
                main_window.csv_handler = self.csv_handler
                main_window.import_menu_from_file(file_path)

                messagebox.showinfo("Restore Complete", "Menu items have been restored successfully!")
                self.refresh_callback()
                self.dialog.destroy()
            else:
                messagebox.showinfo("Info", f"Restore functionality for {file_type} is ready for implementation.")

        except Exception as e:
            self.logger.error(f"Failed to restore file: {e}")
            messagebox.showerror("Restore Failed", f"Failed to restore file: {e}")

    def on_cancel(self) -> None:
        """Handle Cancel button click."""
        self.dialog.destroy()