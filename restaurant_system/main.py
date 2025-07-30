#!/usr/bin/env python3
"""
Main entry point for Restaurant Order Management System.

This module serves as the primary entry point for the restaurant management
application, providing initialization, configuration, and startup procedures.
"""

import sys
import os
import logging
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from restaurant_system.gui import RestaurantMainWindow
except ImportError as e:
    print(f"Failed to import required modules: {e}")
    print("Please ensure all dependencies are installed and the project structure is correct.")
    sys.exit(1)


class RestaurantApplication:
    """
    Main application class for the Restaurant Order Management System.

    Handles application initialization, configuration management,
    error handling, and graceful shutdown procedures.
    """

    def __init__(self):
        """Initialize the restaurant application."""
        self.app_name = "Restaurant Order Management System"
        self.version = "1.0.0"
        self.main_window = None

        # Setup logging
        self.setup_logging()
        self.logger = logging.getLogger(__name__)

        # Setup application directories
        self.setup_directories()

        self.logger.info(f"Starting {self.app_name} v{self.version}")

    def setup_logging(self):
        """Setup application logging configuration."""
        # Create logs directory if it doesn't exist
        logs_dir = Path(__file__).parent / "logs"
        logs_dir.mkdir(exist_ok=True)

        # Configure logging
        log_file = logs_dir / "restaurant_system.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )

        # Set specific log levels for different modules
        logging.getLogger('tkinter').setLevel(logging.WARNING)
        logging.getLogger('PIL').setLevel(logging.WARNING)

    def setup_directories(self):
        """Setup required application directories."""
        try:
            # Data directory
            data_dir = Path(__file__).parent / "data"
            data_dir.mkdir(exist_ok=True)

            # Backup directory
            backup_dir = data_dir / "backups"
            backup_dir.mkdir(exist_ok=True)

            # Reports directory
            reports_dir = Path(__file__).parent / "reports"
            reports_dir.mkdir(exist_ok=True)

            # Receipts directory
            receipts_dir = Path(__file__).parent / "receipts"
            receipts_dir.mkdir(exist_ok=True)

            self.logger.info("Application directories setup completed")

        except Exception as e:
            self.logger.error(f"Failed to setup directories: {e}")
            raise

    def check_system_requirements(self):
        """Check system requirements and dependencies."""
        try:
            # Check Python version
            if sys.version_info < (3, 8):
                raise SystemError("Python 3.8 or higher is required")

            # Check required modules
            required_modules = [
                'tkinter',
                'csv',
                'json',
                'datetime',
                'decimal',
                'pathlib',
                'logging',
                'uuid'
            ]

            missing_modules = []
            for module in required_modules:
                try:
                    __import__(module)
                except ImportError:
                    missing_modules.append(module)

            if missing_modules:
                raise ImportError(f"Missing required modules: {', '.join(missing_modules)}")

            # Check tkinter availability
            try:
                root = tk.Tk()
                root.withdraw()  # Hide the window
                root.destroy()
            except tk.TclError as e:
                raise SystemError(f"Tkinter GUI framework not available: {e}")

            self.logger.info("System requirements check passed")
            return True

        except Exception as e:
            self.logger.error(f"System requirements check failed: {e}")
            return False

    def initialize_application(self):
        """Initialize the main application."""
        try:
            # Check system requirements
            if not self.check_system_requirements():
                messagebox.showerror(
                    "System Requirements",
                    "System requirements not met. Please check the logs for details."
                )
                return False

            # Initialize main window
            self.main_window = RestaurantMainWindow()

            self.logger.info("Application initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize application: {e}")
            messagebox.showerror(
                "Initialization Error",
                f"Failed to initialize application:\n{e}\n\nCheck the log file for details."
            )
            return False

    def run(self):
        """Run the main application."""
        try:
            if self.initialize_application():
                self.logger.info("Starting main application loop")
                self.main_window.run()
            else:
                self.logger.error("Failed to start application")
                return 1

        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
            return 0

        except Exception as e:
            self.logger.error(f"Unexpected application error: {e}")
            messagebox.showerror(
                "Application Error",
                f"An unexpected error occurred:\n{e}\n\nThe application will close."
            )
            return 1

        finally:
            self.cleanup()

        self.logger.info("Application shutdown completed")
        return 0

    def cleanup(self):
        """Cleanup resources before application shutdown."""
        try:
            if self.main_window:
                # Perform any necessary cleanup
                pass

            self.logger.info("Application cleanup completed")

        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


def show_startup_splash():
    """Show a startup splash screen."""
    try:
        splash = tk.Tk()
        splash.title("Restaurant Management System")
        splash.geometry("400x200")
        splash.resizable(False, False)
        splash.configure(bg='navy')

        # Center the splash screen
        splash.update_idletasks()
        x = (splash.winfo_screenwidth() // 2) - (400 // 2)
        y = (splash.winfo_screenheight() // 2) - (200 // 2)
        splash.geometry(f"400x200+{x}+{y}")

        # Remove window decorations
        splash.overrideredirect(True)

        # Splash content
        title_label = tk.Label(
            splash,
            text="Restaurant Order\nManagement System",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='navy'
        )
        title_label.pack(expand=True)

        version_label = tk.Label(
            splash,
            text="Version 1.0.0",
            font=('Arial', 10),
            fg='lightgray',
            bg='navy'
        )
        version_label.pack(side='bottom', pady=10)

        loading_label = tk.Label(
            splash,
            text="Loading...",
            font=('Arial', 10),
            fg='white',
            bg='navy'
        )
        loading_label.pack(side='bottom', pady=5)

        # Show splash for 2 seconds
        splash.after(2000, splash.destroy)
        splash.mainloop()

    except Exception:
        # If splash fails, continue without it
        pass


def main():
    """Main entry point function."""
    try:
        # Show startup splash
        show_startup_splash()

        # Create and run application
        app = RestaurantApplication()
        return app.run()

    except Exception as e:
        print(f"Fatal error: {e}")
        try:
            messagebox.showerror("Fatal Error", f"Fatal error occurred:\n{e}")
        except:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(main())