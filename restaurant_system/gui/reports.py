"""
Reports Tab for Restaurant Order Management System.

This module provides comprehensive reporting functionality including
sales analytics, performance metrics, and data export capabilities.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import logging

from ..utils import CSVHandler, InputValidator, ValidationError


class ReportsTab:
    """
    Reports tab providing comprehensive analytics and reporting functionality.

    Features include sales reports, performance analytics, date filtering,
    data export, and visual charts integration.
    """

    def __init__(self, parent: ttk.Notebook, csv_handler: CSVHandler):
        """
        Initialize the reports tab.

        Args:
            parent (ttk.Notebook): Parent notebook widget
            csv_handler (CSVHandler): CSV data handler
        """
        self.parent = parent
        self.csv_handler = csv_handler
        self.logger = logging.getLogger(__name__)

        # Data storage
        self.sales_data: List[Dict[str, Any]] = []
        self.filtered_data: List[Dict[str, Any]] = []

        # Create the main frame
        self.frame = ttk.Frame(parent, padding="10")

        # Setup the interface
        self.setup_interface()

        # Load initial data
        self.load_sales_data()

    def setup_interface(self) -> None:
        """Setup the reports interface."""
        # Configure grid weights
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Top controls
        self.setup_controls()

        # Main content area
        self.setup_content_area()

    def setup_controls(self) -> None:
        """Setup the top control panel."""
        controls_frame = ttk.Frame(self.frame)
        controls_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        controls_frame.grid_columnconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(controls_frame, text="Sales Reports & Analytics", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        # Date filters
        date_frame = ttk.LabelFrame(controls_frame, text="Date Range", padding="10")
        date_frame.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        # Start date
        ttk.Label(date_frame, text="From:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.start_date_var = tk.StringVar()
        start_date_entry = ttk.Entry(date_frame, textvariable=self.start_date_var, width=12)
        start_date_entry.grid(row=0, column=1, padx=(0, 10))

        # End date
        ttk.Label(date_frame, text="To:").grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.end_date_var = tk.StringVar()
        end_date_entry = ttk.Entry(date_frame, textvariable=self.end_date_var, width=12)
        end_date_entry.grid(row=0, column=3, padx=(0, 10))

        # Quick date buttons
        quick_frame = ttk.Frame(date_frame)
        quick_frame.grid(row=1, column=0, columnspan=4, pady=(5, 0))

        ttk.Button(quick_frame, text="Today", command=self.set_today, width=8).pack(side="left", padx=2)
        ttk.Button(quick_frame, text="Yesterday", command=self.set_yesterday, width=10).pack(side="left", padx=2)
        ttk.Button(quick_frame, text="This Week", command=self.set_this_week, width=10).pack(side="left", padx=2)
        ttk.Button(quick_frame, text="This Month", command=self.set_this_month, width=10).pack(side="left", padx=2)

        # Action buttons
        action_frame = ttk.Frame(controls_frame)
        action_frame.grid(row=1, column=1, padx=10)

        ttk.Button(
            action_frame,
            text="Generate Report",
            command=self.generate_report,
            style='Action.TButton'
        ).pack(pady=2, fill="x")

        ttk.Button(
            action_frame,
            text="Export Data",
            command=self.export_data
        ).pack(pady=2, fill="x")

        ttk.Button(
            action_frame,
            text="Refresh Data",
            command=self.load_sales_data
        ).pack(pady=2, fill="x")

        # Report type selection
        type_frame = ttk.LabelFrame(controls_frame, text="Report Type", padding="10")
        type_frame.grid(row=1, column=2, sticky="ew", padx=(10, 0))

        self.report_type_var = tk.StringVar(value="summary")

        ttk.Radiobutton(
            type_frame,
            text="Sales Summary",
            variable=self.report_type_var,
            value="summary"
        ).pack(anchor="w")

        ttk.Radiobutton(
            type_frame,
            text="Detailed Sales",
            variable=self.report_type_var,
            value="detailed"
        ).pack(anchor="w")

        ttk.Radiobutton(
            type_frame,
            text="Performance Analytics",
            variable=self.report_type_var,
            value="analytics"
        ).pack(anchor="w")

    def setup_content_area(self) -> None:
        """Setup the main content area."""
        # Create notebook for different report views
        self.content_notebook = ttk.Notebook(self.frame)
        self.content_notebook.grid(row=1, column=0, sticky="nsew")

        # Summary tab
        self.setup_summary_tab()

        # Detailed data tab
        self.setup_detailed_tab()

        # Analytics tab
        self.setup_analytics_tab()

    def setup_summary_tab(self) -> None:
        """Setup the summary report tab."""
        summary_frame = ttk.Frame(self.content_notebook, padding="10")
        self.content_notebook.add(summary_frame, text="Summary")

        summary_frame.grid_rowconfigure(1, weight=1)
        summary_frame.grid_columnconfigure(0, weight=1)
        summary_frame.grid_columnconfigure(1, weight=1)

        # Key metrics section
        metrics_frame = ttk.LabelFrame(summary_frame, text="Key Metrics", padding="10")
        metrics_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_columnconfigure(3, weight=1)

        # Create metric labels
        self.metric_labels = {}

        metrics = [
            ("Total Orders:", "total_orders"),
            ("Total Revenue:", "total_revenue"),
            ("Average Order:", "avg_order"),
            ("Total Items:", "total_items")
        ]

        for i, (label_text, metric_name) in enumerate(metrics):
            row = i // 2
            col = (i % 2) * 2

            ttk.Label(metrics_frame, text=label_text, font=('Arial', 11, 'bold')).grid(
                row=row, column=col, sticky="w", padx=(0, 10), pady=5
            )

            self.metric_labels[metric_name] = ttk.Label(
                metrics_frame,
                text="$0.00",
                font=('Arial', 11),
                foreground="blue"
            )
            self.metric_labels[metric_name].grid(row=row, column=col + 1, sticky="e", padx=10, pady=5)

        # Daily summary section
        daily_frame = ttk.LabelFrame(summary_frame, text="Daily Breakdown", padding="10")
        daily_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        daily_frame.grid_rowconfigure(0, weight=1)
        daily_frame.grid_columnconfigure(0, weight=1)

        # Daily summary treeview
        daily_columns = ("date", "orders", "revenue", "avg_order")
        self.daily_tree = ttk.Treeview(
            daily_frame,
            columns=daily_columns,
            show="headings",
            height=12
        )

        self.daily_tree.heading("date", text="Date")
        self.daily_tree.heading("orders", text="Orders")
        self.daily_tree.heading("revenue", text="Revenue")
        self.daily_tree.heading("avg_order", text="Avg Order")

        self.daily_tree.column("date", width=100, minwidth=80)
        self.daily_tree.column("orders", width=80, minwidth=60)
        self.daily_tree.column("revenue", width=100, minwidth=80)
        self.daily_tree.column("avg_order", width=100, minwidth=80)

        self.daily_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar for daily tree
        daily_scrollbar = ttk.Scrollbar(daily_frame, orient="vertical", command=self.daily_tree.yview)
        daily_scrollbar.grid(row=0, column=1, sticky="ns")
        self.daily_tree.configure(yscrollcommand=daily_scrollbar.set)

        # Order type breakdown section
        type_frame = ttk.LabelFrame(summary_frame, text="Order Type Breakdown", padding="10")
        type_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        type_frame.grid_rowconfigure(0, weight=1)
        type_frame.grid_columnconfigure(0, weight=1)

        # Order types treeview
        type_columns = ("type", "count", "revenue", "percentage")
        self.type_tree = ttk.Treeview(
            type_frame,
            columns=type_columns,
            show="headings",
            height=12
        )

        self.type_tree.heading("type", text="Order Type")
        self.type_tree.heading("count", text="Count")
        self.type_tree.heading("revenue", text="Revenue")
        self.type_tree.heading("percentage", text="% of Total")

        self.type_tree.column("type", width=100, minwidth=80)
        self.type_tree.column("count", width=60, minwidth=50)
        self.type_tree.column("revenue", width=100, minwidth=80)
        self.type_tree.column("percentage", width=80, minwidth=60)

        self.type_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar for type tree
        type_scrollbar = ttk.Scrollbar(type_frame, orient="vertical", command=self.type_tree.yview)
        type_scrollbar.grid(row=0, column=1, sticky="ns")
        self.type_tree.configure(yscrollcommand=type_scrollbar.set)

    def setup_detailed_tab(self) -> None:
        """Setup the detailed data tab."""
        detailed_frame = ttk.Frame(self.content_notebook, padding="10")
        self.content_notebook.add(detailed_frame, text="Detailed Data")

        detailed_frame.grid_rowconfigure(1, weight=1)
        detailed_frame.grid_columnconfigure(0, weight=1)

        # Filter controls
        filter_frame = ttk.Frame(detailed_frame)
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(filter_frame, text="Filter by Order Type:", font=('Arial', 10, 'bold')).pack(side="left", padx=(0, 10))

        self.order_type_filter_var = tk.StringVar(value="All")
        type_filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.order_type_filter_var,
            values=["All", "dine_in", "takeout", "delivery"],
            state="readonly",
            width=15
        )
        type_filter_combo.pack(side="left", padx=(0, 20))
        type_filter_combo.bind('<<ComboboxSelected>>', self.apply_detailed_filter)

        ttk.Label(filter_frame, text="Status:", font=('Arial', 10, 'bold')).pack(side="left", padx=(0, 10))

        self.status_filter_var = tk.StringVar(value="All")
        status_filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.status_filter_var,
            values=["All", "completed", "cancelled"],
            state="readonly",
            width=15
        )
        status_filter_combo.pack(side="left")
        status_filter_combo.bind('<<ComboboxSelected>>', self.apply_detailed_filter)

        # Detailed data treeview
        detail_columns = ("date", "order_id", "customer", "type", "status", "items", "subtotal", "tax", "total")
        self.detail_tree = ttk.Treeview(
            detailed_frame,
            columns=detail_columns,
            show="headings",
            height=20
        )

        # Column headings and widths
        column_config = [
            ("date", "Date", 80),
            ("order_id", "Order ID", 120),
            ("customer", "Customer", 100),
            ("type", "Type", 80),
            ("status", "Status", 80),
            ("items", "Items", 60),
            ("subtotal", "Subtotal", 80),
            ("tax", "Tax", 60),
            ("total", "Total", 80)
        ]

        for col_id, heading, width in column_config:
            self.detail_tree.heading(col_id, text=heading)
            self.detail_tree.column(col_id, width=width, minwidth=width - 20)

        self.detail_tree.grid(row=1, column=0, sticky="nsew")

        # Scrollbars
        detail_v_scrollbar = ttk.Scrollbar(detailed_frame, orient="vertical", command=self.detail_tree.yview)
        detail_v_scrollbar.grid(row=1, column=1, sticky="ns")
        self.detail_tree.configure(yscrollcommand=detail_v_scrollbar.set)

        detail_h_scrollbar = ttk.Scrollbar(detailed_frame, orient="horizontal", command=self.detail_tree.xview)
        detail_h_scrollbar.grid(row=2, column=0, sticky="ew")
        self.detail_tree.configure(xscrollcommand=detail_h_scrollbar.set)

    def setup_analytics_tab(self) -> None:
        """Setup the analytics tab."""
        analytics_frame = ttk.Frame(self.content_notebook, padding="10")
        self.content_notebook.add(analytics_frame, text="Analytics")

        analytics_frame.grid_rowconfigure(1, weight=1)
        analytics_frame.grid_columnconfigure(0, weight=1)
        analytics_frame.grid_columnconfigure(1, weight=1)

        # Performance metrics
        perf_frame = ttk.LabelFrame(analytics_frame, text="Performance Metrics", padding="10")
        perf_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        perf_frame.grid_columnconfigure(1, weight=1)
        perf_frame.grid_columnconfigure(3, weight=1)

        # Performance labels
        self.perf_labels = {}

        perf_metrics = [
            ("Peak Day:", "peak_day"),
            ("Peak Revenue:", "peak_revenue"),
            ("Busiest Hour:", "busiest_hour"),
            ("Most Popular Item:", "popular_item")
        ]

        for i, (label_text, metric_name) in enumerate(perf_metrics):
            row = i // 2
            col = (i % 2) * 2

            ttk.Label(perf_frame, text=label_text, font=('Arial', 10, 'bold')).grid(
                row=row, column=col, sticky="w", padx=(0, 10), pady=5
            )

            self.perf_labels[metric_name] = ttk.Label(
                perf_frame,
                text="N/A",
                font=('Arial', 10),
                foreground="green"
            )
            self.perf_labels[metric_name].grid(row=row, column=col + 1, sticky="w", padx=10, pady=5)

        # Trend analysis (placeholder for charts)
        trend_frame = ttk.LabelFrame(analytics_frame, text="Sales Trends", padding="10")
        trend_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        trend_frame.grid_rowconfigure(0, weight=1)
        trend_frame.grid_columnconfigure(0, weight=1)

        # Placeholder for chart
        self.trend_text = tk.Text(trend_frame, height=15, wrap="word", state="disabled")
        self.trend_text.grid(row=0, column=0, sticky="nsew")

        trend_scrollbar = ttk.Scrollbar(trend_frame, orient="vertical", command=self.trend_text.yview)
        trend_scrollbar.grid(row=0, column=1, sticky="ns")
        self.trend_text.configure(yscrollcommand=trend_scrollbar.set)

        # Top customers (placeholder)
        customers_frame = ttk.LabelFrame(analytics_frame, text="Customer Analysis", padding="10")
        customers_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        customers_frame.grid_rowconfigure(0, weight=1)
        customers_frame.grid_columnconfigure(0, weight=1)

        # Customer analysis treeview
        customer_columns = ("customer", "orders", "total_spent", "avg_order")
        self.customer_tree = ttk.Treeview(
            customers_frame,
            columns=customer_columns,
            show="headings",
            height=15
        )

        self.customer_tree.heading("customer", text="Customer")
        self.customer_tree.heading("orders", text="Orders")
        self.customer_tree.heading("total_spent", text="Total Spent")
        self.customer_tree.heading("avg_order", text="Avg Order")

        self.customer_tree.column("customer", width=120, minwidth=100)
        self.customer_tree.column("orders", width=60, minwidth=50)
        self.customer_tree.column("total_spent", width=100, minwidth=80)
        self.customer_tree.column("avg_order", width=100, minwidth=80)

        self.customer_tree.grid(row=0, column=0, sticky="nsew")

        customer_scrollbar = ttk.Scrollbar(customers_frame, orient="vertical", command=self.customer_tree.yview)
        customer_scrollbar.grid(row=0, column=1, sticky="ns")
        self.customer_tree.configure(yscrollcommand=customer_scrollbar.set)

    def load_sales_data(self) -> None:
        """Load sales data from CSV."""
        try:
            self.sales_data = self.csv_handler.load_sales_data()
            self.filtered_data = self.sales_data.copy()

            # Apply current date filter if set
            start_date = self.start_date_var.get()
            end_date = self.end_date_var.get()

            if start_date or end_date:
                self.apply_date_filter()

            self.update_all_displays()
            self.logger.info(f"Loaded {len(self.sales_data)} sales records")

        except Exception as e:
            self.logger.error(f"Failed to load sales data: {e}")
            messagebox.showerror("Error", f"Failed to load sales data: {e}")

    def apply_date_filter(self) -> None:
        """Apply date range filter to sales data."""
        try:
            start_date = self.start_date_var.get()
            end_date = self.end_date_var.get()

            # Validate dates
            start_dt, end_dt = InputValidator.validate_date_range(start_date, end_date)

            # Filter data
            self.filtered_data = []
            for record in self.sales_data:
                record_date = datetime.strptime(record['date'], '%Y-%m-%d')

                if start_dt and record_date < start_dt:
                    continue
                if end_dt and record_date > end_dt:
                    continue

                self.filtered_data.append(record)

            self.logger.info(f"Applied date filter: {len(self.filtered_data)} records match")

        except ValidationError as e:
            messagebox.showerror("Invalid Date", str(e))
        except Exception as e:
            self.logger.error(f"Failed to apply date filter: {e}")
            messagebox.showerror("Error", f"Failed to apply date filter: {e}")

    def apply_detailed_filter(self, event=None) -> None:
        """Apply filters to detailed data view."""
        self.populate_detailed_data()

    def set_today(self) -> None:
        """Set date range to today."""
        today = datetime.now().strftime('%Y-%m-%d')
        self.start_date_var.set(today)
        self.end_date_var.set(today)

    def set_yesterday(self) -> None:
        """Set date range to yesterday."""
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.start_date_var.set(yesterday)
        self.end_date_var.set(yesterday)

    def set_this_week(self) -> None:
        """Set date range to this week."""
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())

        self.start_date_var.set(start_of_week.strftime('%Y-%m-%d'))
        self.end_date_var.set(today.strftime('%Y-%m-%d'))

    def set_this_month(self) -> None:
        """Set date range to this month."""
        today = datetime.now()
        start_of_month = today.replace(day=1)

        self.start_date_var.set(start_of_month.strftime('%Y-%m-%d'))
        self.end_date_var.set(today.strftime('%Y-%m-%d'))

    def generate_report(self) -> None:
        """Generate report based on current settings."""
        try:
            # Apply date filter
            if self.start_date_var.get() or self.end_date_var.get():
                self.apply_date_filter()
            else:
                self.filtered_data = self.sales_data.copy()

            # Update displays
            self.update_all_displays()

            messagebox.showinfo("Success", f"Report generated with {len(self.filtered_data)} records")

        except Exception as e:
            self.logger.error(f"Failed to generate report: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {e}")

    def update_all_displays(self) -> None:
        """Update all report displays with current data."""
        try:
            self.update_summary_metrics()
            self.populate_daily_summary()
            self.populate_order_type_breakdown()
            self.populate_detailed_data()
            self.update_analytics()

        except Exception as e:
            self.logger.error(f"Failed to update displays: {e}")

    def update_summary_metrics(self) -> None:
        """Update the summary metrics display."""
        if not self.filtered_data:
            # Clear metrics
            self.metric_labels["total_orders"].config(text="0")
            self.metric_labels["total_revenue"].config(text="$0.00")
            self.metric_labels["avg_order"].config(text="$0.00")
            self.metric_labels["total_items"].config(text="0")
            return

        # Calculate metrics
        total_orders = len(self.filtered_data)
        total_revenue = sum(Decimal(str(record['total_amount'])) for record in self.filtered_data)
        avg_order = total_revenue / total_orders if total_orders > 0 else Decimal('0')
        total_items = sum(record['items_count'] for record in self.filtered_data)

        # Update labels
        self.metric_labels["total_orders"].config(text=str(total_orders))
        self.metric_labels["total_revenue"].config(text=f"${total_revenue:.2f}")
        self.metric_labels["avg_order"].config(text=f"${avg_order:.2f}")
        self.metric_labels["total_items"].config(text=str(total_items))

    def populate_daily_summary(self) -> None:
        """Populate the daily summary treeview."""
        # Clear existing items
        for item in self.daily_tree.get_children():
            self.daily_tree.delete(item)

        if not self.filtered_data:
            return

        # Group by date
        daily_data = {}
        for record in self.filtered_data:
            date = record['date']
            if date not in daily_data:
                daily_data[date] = {'orders': 0, 'revenue': Decimal('0'), 'items': 0}

            daily_data[date]['orders'] += 1
            daily_data[date]['revenue'] += Decimal(str(record['total_amount']))
            daily_data[date]['items'] += record['items_count']

        # Sort by date
        sorted_dates = sorted(daily_data.keys(), reverse=True)

        # Populate treeview
        for date in sorted_dates:
            data = daily_data[date]
            avg_order = data['revenue'] / data['orders'] if data['orders'] > 0 else Decimal('0')

            values = (
                date,
                data['orders'],
                f"${data['revenue']:.2f}",
                f"${avg_order:.2f}"
            )

            self.daily_tree.insert("", "end", values=values)

    def populate_order_type_breakdown(self) -> None:
        """Populate the order type breakdown treeview."""
        # Clear existing items
        for item in self.type_tree.get_children():
            self.type_tree.delete(item)

        if not self.filtered_data:
            return

        # Group by order type
        type_data = {}
        total_revenue = Decimal('0')

        for record in self.filtered_data:
            order_type = record['order_type']
            if order_type not in type_data:
                type_data[order_type] = {'count': 0, 'revenue': Decimal('0')}

            type_data[order_type]['count'] += 1
            type_data[order_type]['revenue'] += Decimal(str(record['total_amount']))
            total_revenue += Decimal(str(record['total_amount']))

        # Populate treeview
        for order_type, data in type_data.items():
            percentage = (data['revenue'] / total_revenue * 100) if total_revenue > 0 else 0

            values = (
                order_type.replace('_', ' ').title(),
                data['count'],
                f"${data['revenue']:.2f}",
                f"{percentage:.1f}%"
            )

            self.type_tree.insert("", "end", values=values)

    def populate_detailed_data(self) -> None:
        """Populate the detailed data treeview."""
        # Clear existing items
        for item in self.detail_tree.get_children():
            self.detail_tree.delete(item)

        # Apply additional filters
        filtered_records = self.filtered_data.copy()

        # Order type filter
        type_filter = self.order_type_filter_var.get()
        if type_filter != "All":
            filtered_records = [r for r in filtered_records if r['order_type'] == type_filter]

        # Status filter
        status_filter = self.status_filter_var.get()
        if status_filter != "All":
            filtered_records = [r for r in filtered_records if r['status'] == status_filter]

        # Sort by date (newest first)
        filtered_records.sort(key=lambda x: x['date'], reverse=True)

        # Populate treeview
        for record in filtered_records:
            values = (
                record['date'],
                record['order_id'],
                record['customer_name'],
                record['order_type'].replace('_', ' ').title(),
                record['status'].title(),
                record['items_count'],
                f"${record['subtotal']:.2f}",
                f"${record['tax_amount']:.2f}",
                f"${record['total_amount']:.2f}"
            )

            self.detail_tree.insert("", "end", values=values)

    def update_analytics(self) -> None:
        """Update the analytics display."""
        if not self.filtered_data:
            # Clear analytics
            for label in self.perf_labels.values():
                label.config(text="N/A")

            self.trend_text.config(state="normal")
            self.trend_text.delete(1.0, tk.END)
            self.trend_text.insert(1.0, "No data available for analysis")
            self.trend_text.config(state="disabled")

            # Clear customer tree
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)

            return

        # Calculate performance metrics
        self.calculate_performance_metrics()

        # Update trend analysis
        self.update_trend_analysis()

        # Update customer analysis
        self.update_customer_analysis()

    def calculate_performance_metrics(self) -> None:
        """Calculate and display performance metrics."""
        try:
            # Peak day analysis
            daily_revenue = {}
            for record in self.filtered_data:
                date = record['date']
                if date not in daily_revenue:
                    daily_revenue[date] = Decimal('0')
                daily_revenue[date] += Decimal(str(record['total_amount']))

            if daily_revenue:
                peak_day = max(daily_revenue.keys(), key=lambda x: daily_revenue[x])
                peak_revenue = daily_revenue[peak_day]

                self.perf_labels["peak_day"].config(text=peak_day)
                self.perf_labels["peak_revenue"].config(text=f"${peak_revenue:.2f}")

            # Placeholder for other metrics
            self.perf_labels["busiest_hour"].config(text="12:00 PM")  # Placeholder
            self.perf_labels["popular_item"].config(text="N/A")  # Would need item-level data

        except Exception as e:
            self.logger.error(f"Failed to calculate performance metrics: {e}")

    def update_trend_analysis(self) -> None:
        """Update trend analysis text."""
        try:
            self.trend_text.config(state="normal")
            self.trend_text.delete(1.0, tk.END)

            # Generate trend report
            trend_report = "Sales Trend Analysis\n"
            trend_report += "=" * 50 + "\n\n"

            # Daily trends
            daily_revenue = {}
            for record in self.filtered_data:
                date = record['date']
                if date not in daily_revenue:
                    daily_revenue[date] = {'revenue': Decimal('0'), 'orders': 0}
                daily_revenue[date]['revenue'] += Decimal(str(record['total_amount']))
                daily_revenue[date]['orders'] += 1

            if len(daily_revenue) >= 2:
                sorted_dates = sorted(daily_revenue.keys())
                first_day = daily_revenue[sorted_dates[0]]
                last_day = daily_revenue[sorted_dates[-1]]

                revenue_change = last_day['revenue'] - first_day['revenue']
                revenue_change_pct = (revenue_change / first_day['revenue'] * 100) if first_day['revenue'] > 0 else 0

                trend_report += f"Revenue Trend:\n"
                trend_report += f"  First Day: ${first_day['revenue']:.2f}\n"
                trend_report += f"  Last Day: ${last_day['revenue']:.2f}\n"
                trend_report += f"  Change: ${revenue_change:.2f} ({revenue_change_pct:+.1f}%)\n\n"

            # Order volume trends
            total_orders = len(self.filtered_data)
            days_in_period = len(daily_revenue)
            avg_orders_per_day = total_orders / days_in_period if days_in_period > 0 else 0

            trend_report += f"Order Volume:\n"
            trend_report += f"  Total Orders: {total_orders}\n"
            trend_report += f"  Days in Period: {days_in_period}\n"
            trend_report += f"  Average Orders/Day: {avg_orders_per_day:.1f}\n\n"

            # Note about advanced analytics
            trend_report += "Note: Advanced chart visualization would be implemented\n"
            trend_report += "here using libraries like matplotlib or plotly for\n"
            trend_report += "production deployment."

            self.trend_text.insert(1.0, trend_report)
            self.trend_text.config(state="disabled")

        except Exception as e:
            self.logger.error(f"Failed to update trend analysis: {e}")

    def update_customer_analysis(self) -> None:
        """Update customer analysis treeview."""
        try:
            # Clear existing items
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)

            # Group by customer
            customer_data = {}
            for record in self.filtered_data:
                customer = record['customer_name'] or 'Guest'
                if customer not in customer_data:
                    customer_data[customer] = {'orders': 0, 'total_spent': Decimal('0')}

                customer_data[customer]['orders'] += 1
                customer_data[customer]['total_spent'] += Decimal(str(record['total_amount']))

            # Sort by total spent (descending)
            sorted_customers = sorted(
                customer_data.items(),
                key=lambda x: x[1]['total_spent'],
                reverse=True
            )

            # Populate treeview (top 20 customers)
            for customer, data in sorted_customers[:20]:
                avg_order = data['total_spent'] / data['orders'] if data['orders'] > 0 else Decimal('0')

                values = (
                    customer,
                    data['orders'],
                    f"${data['total_spent']:.2f}",
                    f"${avg_order:.2f}"
                )

                self.customer_tree.insert("", "end", values=values)

        except Exception as e:
            self.logger.error(f"Failed to update customer analysis: {e}")

    def export_data(self) -> None:
        """Export current filtered data to CSV."""
        try:
            if not self.filtered_data:
                messagebox.showwarning("Warning", "No data to export")
                return

            # Get export file path
            file_path = filedialog.asksaveasfilename(
                title="Export Sales Data",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialname=f"sales_report_{datetime.now().strftime('%Y%m%d')}.csv"
            )

            if not file_path:
                return

            # Export data
            import csv

            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                if self.filtered_data:
                    fieldnames = self.filtered_data[0].keys()
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.filtered_data)

            messagebox.showinfo("Success", f"Data exported to: {file_path}")
            self.logger.info(f"Exported {len(self.filtered_data)} records to {file_path}")

        except Exception as e:
            self.logger.error(f"Failed to export data: {e}")
            messagebox.showerror("Error", f"Failed to export data: {e}")