# Restaurant Order Management System - Installation Guide

## Quick Start (5 Minutes)

### Option 1: Windows Users (Easiest)
1. **Download** all files to a folder (e.g., `restaurant_system`)
2. **Double-click** `start_restaurant_system.bat`
3. **Done!** The application will launch automatically

### Option 2: Python Users (All Platforms)
1. **Open terminal/command prompt**
2. **Navigate** to the project folder:
   ```bash
   cd path/to/restaurant_system
   ```
3. **Run the launcher**:
   ```bash
   python run_restaurant_system.py
   ```

### Option 3: Direct Launch
```bash
python restaurant_system/main.py
```

## System Requirements ✅

### Minimum Requirements
- **Python 3.8+** (Python 3.11 recommended)
- **Windows 10/11**, macOS 10.14+, or Linux Ubuntu 18.04+
- **4GB RAM** (2GB minimum)
- **100MB disk space**

### Built-in Components
- ✅ **tkinter** - GUI framework (included with Python)
- ✅ **csv** - Data storage (Python standard library)
- ✅ **All other dependencies** - Standard library only!

**No pip install required!** 🎉

## Pre-Installation Check

Run this command to verify your system:
```bash
python test_system.py
```

Expected output:
```
🎉 All tests passed! System is ready for use.
```

## File Structure Overview

```
restaurant_system/
├── 📂 restaurant_system/          # Main application code
│   ├── 📂 models/                 # Data models (MenuItem, Order, etc.)
│   ├── 📂 gui/                    # User interface components
│   ├── 📂 utils/                  # Utilities (CSV, validation, receipts)
│   ├── 📂 data/                   # Data storage (CSV files)
│   ├── 📂 logs/                   # Application logs
│   └── 📄 main.py                 # Application entry point
├── 📄 run_restaurant_system.py    # Easy launcher script
├── 📄 start_restaurant_system.bat # Windows batch file
├── 📄 test_system.py              # System verification
├── 📄 README.md                   # Main documentation
├── 📄 USER_MANUAL.md              # Detailed user guide
└── 📄 requirements.txt            # Dependencies info
```

## First Launch Experience

### What Happens Automatically
1. **Directory Creation**: Required folders are created
2. **Sample Data Loading**: 23 menu items across 4 categories
3. **Database Initialization**: Empty orders and sales reports
4. **Backup System Setup**: Automatic backup configuration

### Initial Sample Data
- **Appetizers**: Caesar Salad, Buffalo Wings, Mozzarella Sticks, etc.
- **Main Courses**: Grilled Chicken, Ribeye Steak, Pasta Alfredo, etc.
- **Desserts**: Chocolate Lava Cake, Tiramisu, Cheesecake, etc.
- **Beverages**: Coffee, Fresh Juice, Wine, Beer, etc.

## Configuration Options

### Restaurant Information
Edit `restaurant_system/config.py` to customize:
```python
RESTAURANT_INFO = {
    'name': 'Your Restaurant Name',
    'address': '123 Your Street',
    'city': 'Your City',
    'phone': '(555) YOUR-PHONE',
    # ... other details
}
```

### Tax Rate
```python
DEFAULT_TAX_RATE = Decimal('0.08')  # 8% (change as needed)
```

### Display Settings
```python
WINDOW_SIZE = "1200x800"  # Adjust window size
QUEUE_REFRESH_INTERVAL = 30000  # Queue refresh (milliseconds)
```

## Troubleshooting Installation

### Common Issues & Solutions

#### ❌ "Python not found"
**Solution**: Install Python 3.8+ from [python.org](https://python.org/downloads/)

#### ❌ "tkinter not available"
**Ubuntu/Debian**:
```bash
sudo apt-get install python3-tk
```

**CentOS/RHEL**:
```bash
sudo yum install tkinter
```

**macOS**: Usually included with Python

#### ❌ "Permission denied"
**Solution**: Run as administrator or check file permissions

#### ❌ "Module not found"
**Solution**: Ensure you're in the correct directory and all files are present

### Verification Steps

1. **Check Python version**:
   ```bash
   python --version
   ```
   Should show 3.8 or higher

2. **Test tkinter**:
   ```bash
   python -c "import tkinter; tkinter.Tk().destroy(); print('✓ tkinter works')"
   ```

3. **Test import**:
   ```bash
   python -c "import restaurant_system; print('✓ imports work')"
   ```

## Performance Optimization

### Recommended Settings
- **RAM**: 4GB+ for optimal performance
- **Display**: 1920x1080 resolution recommended
- **Storage**: SSD for faster CSV operations
- **Python**: Use Python 3.11 for best performance

### Large Restaurant Optimization
For restaurants with 100+ menu items:
- Increase auto-save interval to 10 minutes
- Use filtering in order interface
- Regular backup cleanup (keep last 30 days)

## Network Considerations

### Offline Operation
- ✅ **Fully offline** - no internet required
- ✅ **Local data storage** - all data stays on your computer
- ✅ **No cloud dependencies** - complete privacy

### Multi-Computer Setup
To use on multiple computers:
1. Install on each computer
2. Share the `data/` folder via network drive
3. Point each installation to shared data folder

## Security Notes

### Data Protection
- All data stored locally in CSV format
- No external network connections
- File permissions protect sensitive data
- Automatic backups prevent data loss

### Best Practices
- Regular backups of `data/` folder
- Secure your computer with password protection
- Limit access to authorized staff only
- Monitor log files for unusual activity

## Backup Strategy

### Automatic Backups
- **Frequency**: Every 24 hours
- **Location**: `data/backups/`
- **Retention**: 30 days
- **Compression**: Yes (saves space)

### Manual Backup
Copy the entire `data/` folder to external storage:
```bash
# Windows
xcopy /E /I data backup_YYYY-MM-DD

# Mac/Linux
cp -r data backup_$(date +%Y-%m-%d)
```

## Getting Support

### Self-Service Resources
1. **Log Files**: Check `logs/restaurant_system.log`
2. **User Manual**: Read `USER_MANUAL.md`
3. **Test System**: Run `python test_system.py`
4. **Sample Data**: Restore from `data/backups/`

### Common Solutions
- **Application freezes**: Restart the application
- **Data corruption**: Restore from backup
- **Performance issues**: Close other applications
- **Display problems**: Check screen resolution settings

## Upgrading

### Future Versions
- Backup your `data/` folder
- Replace application files
- Keep your configuration settings
- Test with `python test_system.py`

### Migration Path
The system is designed for easy migration to:
- Database backends (PostgreSQL, MySQL)
- Web-based interfaces
- Mobile applications
- Cloud deployments

## Success Checklist ✅

Before going live, verify:
- [ ] Application starts without errors
- [ ] Sample menu items display correctly
- [ ] Can create and submit test orders
- [ ] Order queue updates properly
- [ ] Reports generate successfully
- [ ] Receipts print correctly
- [ ] Backup system is working
- [ ] Staff training is complete

## Quick Reference

### Daily Startup
1. Double-click `start_restaurant_system.bat` (Windows)
2. Or run `python run_restaurant_system.py`
3. Verify auto-refresh is enabled in queue
4. Check system logs for any issues

### Daily Shutdown
1. Complete all pending orders
2. Generate end-of-day reports
3. Verify data is saved (automatic)
4. Close application normally

### Emergency Procedures
- **Data corruption**: Restore from `data/backups/`
- **System crash**: Restart application, data auto-recovers
- **Power outage**: Auto-save protects recent orders

---

**🎉 You're ready to start managing your restaurant efficiently!**

For detailed usage instructions, see [USER_MANUAL.md](USER_MANUAL.md)