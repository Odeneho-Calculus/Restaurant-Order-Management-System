# Restaurant Order Management System - User Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [Menu Management](#menu-management)
3. [Taking Orders](#taking-orders)
4. [Queue Monitoring](#queue-monitoring)
5. [Reports and Analytics](#reports-and-analytics)
6. [System Settings](#system-settings)
7. [Troubleshooting](#troubleshooting)

## Getting Started

### System Requirements
- Windows 10/11, macOS 10.14+, or Linux Ubuntu 18.04+
- Python 3.8 or higher
- 4GB RAM minimum
- 100MB available disk space

### Installation
1. Download the system files to your computer
2. Double-click `start_restaurant_system.bat` (Windows) or run `python run_restaurant_system.py`
3. The system will automatically create necessary folders and sample data

### First Launch
When you first start the system:
- The application window will open with four main tabs
- Sample menu items will be loaded automatically
- Empty order queue and sales reports will be initialized

## Menu Management

### Overview
The Menu Management tab allows you to add, edit, and organize your restaurant's menu items.

### Adding New Menu Items

1. **Click "Add Item" Button**
   - The "Add/Edit Item" form will appear
   - All fields will be empty and ready for input

2. **Fill in Item Details**:
   - **Name**: Enter the menu item name (required)
   - **Category**: Select from dropdown (appetizers, mains, desserts, beverages, soups)
   - **Price**: Enter price with decimal (e.g., 12.99)
   - **Description**: Add a detailed description (optional)
   - **Available**: Check if item is currently available

3. **Save the Item**
   - Click "Save Changes"
   - The item will appear in the menu list
   - Data is automatically saved to the CSV file

### Editing Existing Items

1. **Select an Item**
   - Click on any item in the menu list
   - The item details will appear in the edit form

2. **Modify Details**
   - Change any field as needed
   - Use "Clear Form" to reset changes

3. **Save Changes**
   - Click "Save Changes" to confirm
   - Click "Cancel" to discard changes

### Managing Availability

- **Toggle Single Item**: Select item and click "Toggle Availability"
- **Bulk Operations**: Select multiple items using Ctrl+click, then use bulk actions
- **Unavailable items** appear grayed out in the order interface

### Menu Categories

The system supports these categories:
- **Appetizers**: Starters and small plates
- **Mains**: Main course dishes
- **Desserts**: Sweet endings
- **Beverages**: Drinks (alcoholic and non-alcoholic)
- **Soups**: Soup dishes

### Search and Filter

- **Search Box**: Type to find items by name or description
- **Category Filter**: Use dropdown to show only specific categories
- **Availability Filter**: Toggle to show only available or all items

## Taking Orders

### Customer Information

1. **Enter Customer Details**:
   - **Name**: Customer's name (optional, defaults to "Guest")
   - **Phone**: Contact number (optional, but recommended)
   - **Table**: Table number for dine-in orders
   - **Type**: Select order type (Dine-in, Takeout, Delivery)

### Browsing the Menu

1. **Category Selection**
   - Use the dropdown to browse by category
   - Select "All" to see all available items

2. **Search Function**
   - Type in the search box to find specific items
   - Search works on both names and descriptions

3. **Menu Display**
   - Items are grouped by category
   - Each item shows name, price, and description
   - Quantity controls and "Add to Order" button

### Adding Items to Order

1. **Set Quantity**
   - Use the spin box to select quantity (1-99)
   - Default is 1

2. **Regular Addition**
   - Click "Add to Order" to add with current quantity

3. **Special Instructions**
   - Click "Special" button to add custom instructions
   - A dialog will appear for entering special requests
   - Examples: "No onions", "Extra spicy", "Sauce on side"

### Managing the Current Order

1. **Order Summary**
   - Shows all items, quantities, and prices
   - Displays subtotal, tax, and total

2. **Editing Order Items**
   - **Change Quantity**: Double-click on an item
   - **Remove Item**: Select item and click "Remove Item"
   - **Special Instructions**: Shown below each item

3. **Order Actions**
   - **Clear Order**: Remove all items (confirmation required)
   - **Preview Order**: See formatted order summary
   - **Submit Order**: Send order to kitchen

### Order Totals

- **Subtotal**: Sum of all item prices
- **Tax**: Calculated at 8% (configurable)
- **Total**: Final amount including tax

### Submitting Orders

1. **Review Order**
   - Click "Preview Order" to see final summary
   - Check customer information and items

2. **Submit to Kitchen**
   - Click "Submit Order"
   - Confirmation dialog will appear
   - Order moves to kitchen queue
   - New order form is started automatically

## Queue Monitoring

### Overview
The Queue Display tab shows all orders in various stages of preparation.

### Order Status Flow

Orders progress through these stages:
1. **Pending**: Just received, waiting to start
2. **Preparing**: Kitchen is working on the order
3. **Ready**: Order is complete, ready for pickup/serving
4. **Completed**: Order has been delivered to customer

### Queue Interface

1. **Filter Controls**
   - **Filter Dropdown**: All, Active, Pending, Preparing, Ready, Completed
   - **Auto-refresh**: Toggle automatic updates every 30 seconds
   - **Refresh Now**: Manual refresh button

2. **Order List**
   - Shows order ID, customer, time, status, total, and item count
   - Color-coded by status for quick identification
   - Click to select and view details

### Order Details Panel

When an order is selected:
- **Order Information**: ID, customer, phone, table, type, status
- **Order Items**: List of all items with quantities and prices
- **Priority Toggle**: Mark urgent orders
- **Notes Field**: Add internal notes

### Updating Order Status

1. **Status Buttons**
   - **Start Preparing**: Move from Pending to Preparing
   - **Mark Ready**: Move from Preparing to Ready
   - **Complete Order**: Move from Ready to Completed

2. **Priority Management**
   - Check "Priority Order" for urgent orders
   - Priority orders are highlighted in red

3. **Adding Notes**
   - Type in the notes field
   - Notes are saved automatically
   - Useful for special instructions or issues

### Receipt Functions

1. **View Receipt**
   - Click "View Receipt" to see formatted receipt
   - Shows itemized bill with totals

2. **Print Receipt**
   - Click "Print Receipt" to send to printer
   - System will use default printer

3. **Save Receipt**
   - Save receipts as text files
   - Useful for record keeping

### Order Management

1. **Cancel Order**
   - Available for non-completed orders
   - Requires cancellation reason
   - Order status changes to "Cancelled"

2. **Context Menu**
   - Right-click orders for quick actions
   - Access common functions easily

## Reports and Analytics

### Date Range Selection

1. **Manual Date Entry**
   - Enter start and end dates in YYYY-MM-DD format
   - Use "From" and "To" fields

2. **Quick Date Buttons**
   - **Today**: Current day only
   - **Yesterday**: Previous day
   - **This Week**: Monday to today
   - **This Month**: First of month to today

### Report Types

#### Sales Summary
- **Key Metrics**: Total orders, revenue, average order, total items
- **Daily Breakdown**: Sales by date with order counts
- **Order Type Analysis**: Breakdown by dine-in, takeout, delivery

#### Detailed Data
- **Complete Transaction List**: All orders with full details
- **Filtering Options**: By order type and status
- **Sortable Columns**: Click headers to sort data

#### Performance Analytics
- **Peak Performance**: Best day, highest revenue
- **Customer Analysis**: Top customers by spending
- **Trend Analysis**: Sales patterns and insights

### Generating Reports

1. **Set Date Range**
   - Choose desired time period
   - Use quick buttons or manual entry

2. **Select Report Type**
   - Choose from radio button options
   - Each type shows different information

3. **Generate Report**
   - Click "Generate Report" button
   - Data will update automatically

### Exporting Data

1. **Export Function**
   - Click "Export Data" button
   - Choose file location and name
   - Data saved as CSV format

2. **Uses for Exported Data**
   - Import into Excel or other spreadsheet software
   - Create custom reports
   - Share with accountants or managers

## System Settings

### Restaurant Information
Configure your restaurant details for receipts:
- Name, address, phone number
- Email and website
- Tax rate settings

### Display Preferences
- Window size and layout
- Color themes
- Auto-refresh intervals

### Data Management
- Backup settings
- Auto-save frequency
- Data retention policies

## Troubleshooting

### Common Issues

#### Application Won't Start
**Problem**: Error message when launching
**Solutions**:
1. Check Python version (must be 3.8+)
2. Verify tkinter is installed
3. Run as administrator if needed
4. Check log files for specific errors

#### Menu Items Not Showing
**Problem**: Menu appears empty
**Solutions**:
1. Check if menu_items.csv exists in data folder
2. Verify file permissions
3. Look for data corruption in CSV
4. Restore from backup if available

#### Orders Not Saving
**Problem**: Orders disappear after restart
**Solutions**:
1. Check write permissions in data folder
2. Ensure sufficient disk space
3. Verify CSV file integrity
4. Check auto-save settings

#### Print Function Not Working
**Problem**: Receipts won't print
**Solutions**:
1. Check default printer settings
2. Verify printer is online and connected
3. Test printing from other applications
4. Use "Save to File" as alternative

### Error Messages

#### "Validation Error"
- Check input format (prices, phone numbers)
- Ensure required fields are filled
- Verify data ranges are correct

#### "File Permission Error"
- Run application as administrator
- Check folder permissions
- Ensure files aren't open in other programs

#### "Data Corruption Detected"
- Restore from automatic backup
- Check CSV file format
- Re-enter affected data manually

### Getting Help

1. **Log Files**
   - Check restaurant_system/logs/ folder
   - Look for recent error messages
   - Note timestamp of issues

2. **Data Recovery**
   - Automatic backups in data/backups/
   - Restore previous version if needed
   - CSV files can be edited manually

3. **Performance Issues**
   - Close other applications
   - Restart the system
   - Check available memory and disk space

### Best Practices

1. **Regular Backups**
   - System creates automatic backups
   - Consider manual backups of data folder
   - Store backups in separate location

2. **Data Entry**
   - Use consistent naming for menu items
   - Include detailed descriptions
   - Keep customer information up to date

3. **System Maintenance**
   - Restart application daily
   - Monitor log files for errors
   - Keep system updated

4. **Staff Training**
   - Train all users on basic functions
   - Create workflow procedures
   - Document custom settings and preferences

---

**For technical support or additional questions, refer to the system logs and documentation files included with the application.**