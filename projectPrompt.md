# Restaurant Order Management System - AI Development Prompt

## Project Overview
Create a complete Restaurant Order Management System using Python with Tkinter GUI and CSV data persistence. The system should be professional, user-friendly, and suitable for real restaurant operations.

## Core Requirements

### 1. Data Models
Create robust classes for:
- **MenuItem**: Properties include id, name, category, price, description, availability status
- **Order**: Properties include order_id, timestamp, items list, customer info, status, total amount
- **OrderItem**: Properties include menu_item, quantity, special_instructions, subtotal

### 2. Menu Management Module
- **Add/Edit/Delete menu items** with validation
- **Categorize items** (appetizers, mains, desserts, beverages, etc.)
- **Set availability status** (available/out of stock)
- **Price management** with decimal precision
- **Menu persistence** using CSV files
- **Search and filter** functionality

### 3. Order Taking Interface
- **Intuitive GUI** with category tabs or dropdown menus
- **Item selection** with quantity spinboxes
- **Special instructions** text field for each item
- **Real-time order total** calculation
- **Customer information** input (name, phone, table number)
- **Order type selection** (dine-in, takeout, delivery)
- **Order review** before confirmation

### 4. Live Order Queue System
- **Visual order display** showing all pending orders
- **Status tracking**: Pending → Preparing → Ready → Completed
- **Time stamps** for each order and status change
- **Priority indicators** for urgent orders
- **Order completion** workflow
- **Auto-refresh** capabilities

### 5. Receipt Generation
- **Professional receipt format** with restaurant header
- **Itemized billing** with quantities and prices
- **Tax calculations** (configurable tax rate)
- **Order totals** with subtotal, tax, and grand total
- **Print functionality** or save as PDF
- **Receipt numbering** system

### 6. Daily Sales Reporting
- **Export to CSV** with comprehensive data
- **Daily sales summary** (total orders, revenue, popular items)
- **Time-based filtering** (by date range, specific dates)
- **Item-wise sales analysis**
- **Customer statistics** if applicable
- **Revenue tracking** with tax breakdown

## Technical Specifications

### GUI Framework
- Use **Tkinter** with modern styling (ttk widgets)
- Implement **responsive layout** using grid/pack managers
- Create **tabbed interface** for different modules
- Use **professional color scheme** and consistent fonts
- Include **icons and visual indicators** where appropriate

### Data Persistence
- **CSV files** for all data storage:
  - `menu_items.csv` - Menu database
  - `orders.csv` - Order history
  - `daily_sales.csv` - Sales reports
- Implement **data backup** and recovery mechanisms
- Handle **file I/O errors** gracefully
- Use **proper CSV formatting** with headers

### Error Handling & Validation
- **Input validation** for all user entries
- **Exception handling** for file operations
- **User-friendly error messages**
- **Data integrity checks**
- **Confirmation dialogs** for critical actions

### Performance & Usability
- **Fast loading** of menu items and orders
- **Keyboard shortcuts** for common actions
- **Auto-save** functionality
- **Undo/Redo** capabilities where relevant
- **Multi-threading** for non-blocking operations

## Advanced Features to Include

### User Interface Enhancements
- **Search functionality** across menus and orders
- **Drag-and-drop** for order management
- **Right-click context menus**
- **Status bar** with system information
- **Customizable themes** or color schemes

### Business Logic
- **Discount system** (percentage and fixed amount)
- **Tax calculation** with configurable rates
- **Combo deals** and special offers
- **Inventory tracking** (optional advanced feature)
- **Staff management** (basic user roles)

### Reporting & Analytics
- **Sales charts** using matplotlib integration
- **Peak hours analysis**
- **Customer preference tracking**
- **Monthly/weekly reports**
- **Export to multiple formats** (CSV, PDF, Excel)

## Code Structure Requirements

### File Organization
```
restaurant_system/
├── main.py                 # Entry point
├── models/
│   ├── menu_item.py       # MenuItem class
│   ├── order.py           # Order class
│   └── order_item.py      # OrderItem class
├── gui/
│   ├── main_window.py     # Main application window
│   ├── menu_manager.py    # Menu management interface
│   ├── order_interface.py # Order taking interface
│   ├── queue_display.py   # Order queue display
│   └── reports.py         # Reporting interface
├── utils/
│   ├── csv_handler.py     # CSV operations
│   ├── receipt_generator.py # Receipt creation
│   └── validators.py      # Input validation
└── data/
    ├── menu_items.csv
    ├── orders.csv
    └── sales_reports.csv
```

### Coding Standards
- Use **clear variable names** and comprehensive comments
- Implement **proper exception handling**
- Follow **PEP 8** Python style guidelines
- Create **modular, reusable code**
- Include **docstrings** for all classes and methods

## Sample Data to Include
Provide sample menu items across categories:
- Appetizers (3-5 items)
- Main courses (5-8 items)
- Desserts (3-4 items)
- Beverages (4-6 items)

## Testing Requirements
- Create **sample orders** for demonstration
- Test **edge cases** (empty orders, invalid inputs)
- Verify **CSV file handling** works correctly
- Ensure **GUI responsiveness** across different screen sizes
- Test **data persistence** between application sessions

## Documentation
Include:
- **User manual** with screenshots
- **Installation instructions**
- **Feature explanations**
- **Troubleshooting guide**
- **Code comments** explaining complex logic

## Deliverables Expected
1. Complete working Python application
2. All required CSV data files with sample data
3. User documentation
4. Code comments and docstrings
5. Error handling demonstrations
6. Sample receipts and reports

Make the system production-ready with professional appearance, robust error handling, and intuitive user experience suitable for actual restaurant use.