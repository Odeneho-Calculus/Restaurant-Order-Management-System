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
import webview
from tkinter import messagebox

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from restaurant_system.gui.webview_bridge import RestaurantMainWindow
except ImportError as e:
    print(f"Failed to import required modules: {e}")
    print("Please ensure all dependencies are installed and the project structure is correct.")
    print("Run: pip install webview")
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
        logging.getLogger('webview').setLevel(logging.WARNING)
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
                'webview',
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

            # Check webview availability
            try:
                # Test webview import and basic functionality
                test_window = webview.create_window("Test", "about:blank", width=1, height=1)
                # Clear the test window from memory
                webview.windows.clear()
            except Exception as e:
                raise SystemError(f"WebView framework not available: {e}")

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
                try:
                    import tkinter
                    from tkinter import messagebox
                    root = tkinter.Tk()
                    root.withdraw()
                    messagebox.showerror(
                        "System Requirements",
                        "System requirements not met. Please check the logs for details.\n\n"
                        "Required: pip install webview"
                    )
                    root.destroy()
                except:
                    print("System requirements not met. Please install webview: pip install webview")
                return False

            # Initialize main window
            self.main_window = RestaurantMainWindow()

            self.logger.info("Application initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize application: {e}")
            try:
                import tkinter
                from tkinter import messagebox
                root = tkinter.Tk()
                root.withdraw()
                messagebox.showerror(
                    "Initialization Error",
                    f"Failed to initialize application:\n{e}\n\nCheck the log file for details."
                )
                root.destroy()
            except:
                print(f"Failed to initialize application: {e}")
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
            try:
                import tkinter
                from tkinter import messagebox
                root = tkinter.Tk()
                root.withdraw()
                messagebox.showerror(
                    "Application Error",
                    f"An unexpected error occurred:\n{e}\n\nThe application will close."
                )
                root.destroy()
            except:
                print(f"An unexpected error occurred: {e}")
            return 1

        finally:
            self.cleanup()

        self.logger.info("Application shutdown completed")
        return 0

    def cleanup(self):
        """Cleanup resources before application shutdown."""
        try:
            if self.main_window:
                self.main_window.cleanup()

            self.logger.info("Application cleanup completed")

        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


def show_startup_splash():
    """Show a startup splash screen with modern styling."""
    try:
        # Create a simple splash using webview
        splash_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    text-align: center;
                }
                .logo {
                    font-size: 3rem;
                    margin-bottom: 1rem;
                }
                .title {
                    font-size: 1.8rem;
                    font-weight: 300;
                    margin-bottom: 0.5rem;
                }
                .subtitle {
                    font-size: 1rem;
                    opacity: 0.8;
                    margin-bottom: 2rem;
                }
                .loading {
                    font-size: 0.9rem;
                    opacity: 0.7;
                }
                .spinner {
                    width: 40px;
                    height: 40px;
                    border: 3px solid rgba(255,255,255,0.3);
                    border-radius: 50%;
                    border-top-color: white;
                    animation: spin 1s ease-in-out infinite;
                    margin: 1rem auto;
                }
                @keyframes spin {
                    to { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <div class="logo">🍽️</div>
            <div class="title">Restaurant Management System</div>
            <div class="subtitle">Modern Order Management Solution</div>
            <div class="spinner"></div>
            <div class="loading">Loading...</div>
            <script>
                setTimeout(() => {
                    if (typeof pywebview !== 'undefined') {
                        pywebview.api.closeSplash();
                    }
                }, 2000);
            </script>
        </body>
        </html>
        """

        class SplashAPI:
            def closeSplash(self):
                webview.windows[0].destroy()

        webview.create_window(
            "Loading",
            html=splash_html,
            width=400,
            height=300,
            resizable=False,
            js_api=SplashAPI()
        )

        webview.start(debug=False)

    except Exception:
        # If splash fails, continue without it
        pass


def main():
    """Main entry point function."""
    try:
        # Show startup splash
        # show_startup_splash()  # Commented out to avoid blocking

        # Create and run application
        app = RestaurantApplication()
        return app.run()

    except Exception as e:
        print(f"Fatal error: {e}")
        try:
            import tkinter
            from tkinter import messagebox
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showerror("Fatal Error", f"Fatal error occurred:\n{e}")
            root.destroy()
        except:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(main())