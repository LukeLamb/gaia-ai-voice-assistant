"""
Gaia AI Voice Assistant - Main Entry Point
Professional modular architecture with PyQt5 GUI
"""
import sys
import os
import signal

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from gui.main_window import GaiaMainWindow
from core.agent.gaia_agent import GaiaAgent


class GaiaWorkerThread(QThread):
    """Worker thread for running Gaia agent"""
    
    # Signals
    message_logged = pyqtSignal(str)
    status_changed = pyqtSignal(str)
    user_identified = pyqtSignal(str)
    chat_message = pyqtSignal(str, str)  # speaker, message
    
    def __init__(self):
        super().__init__()
        self.gaia_agent = None
        self.running = False
        
    def initialize_agent(self):
        """Initialize the Gaia agent"""
        try:
            self.gaia_agent = GaiaAgent(log_callback=self.handle_log)
            return True
        except Exception as e:
            self.message_logged.emit(f"Error initializing Gaia: {e}")
            return False
            
    def handle_log(self, message):
        """Handle log messages from Gaia agent"""
        self.message_logged.emit(message)
        
        # Parse different types of messages
        if message.startswith("Luke:"):
            user_msg = message[5:].strip()
            self.chat_message.emit("user", user_msg)
        elif message.startswith("Gaia:"):
            gaia_msg = message[5:].strip()
            self.chat_message.emit("gaia", gaia_msg)
        elif message.startswith("System:"):
            system_msg = message[7:].strip()
            self.chat_message.emit("system", system_msg)
            self.status_changed.emit(system_msg)
            
    def start_gaia(self):
        """Start the Gaia agent"""
        if self.gaia_agent:
            self.gaia_agent.start()
            self.status_changed.emit("Listening")
            
    def pause_gaia(self):
        """Pause/resume the Gaia agent"""
        if self.gaia_agent:
            if self.gaia_agent.paused:
                self.gaia_agent.resume()
                self.status_changed.emit("Listening")
            else:
                self.gaia_agent.pause()
                self.status_changed.emit("Paused")
                
    def stop_gaia(self):
        """Stop the Gaia agent"""
        if self.gaia_agent:
            self.gaia_agent.stop()
            self.status_changed.emit("Stopped")
            
    def run(self):
        """Main thread execution"""
        # Keep thread alive but don't do heavy processing here
        # The actual work is done by the agent in its own thread
        self.exec_()


class GaiaApplication:
    """Main application class"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Gaia AI Assistant")
        self.app.setApplicationVersion("2.0")
        self.app.setOrganizationName("Gaia AI")
        
        # Create main window
        self.main_window = GaiaMainWindow()
        
        # Create worker thread
        self.worker_thread = GaiaWorkerThread()
        
        # Connect signals
        self.setup_connections()
        
        # Connect cleanup to window close
        self.app.aboutToQuit.connect(self.cleanup)
        
        # Initialize
        self.initialize()
        
    def setup_connections(self):
        """Setup signal connections between components"""
        # Control panel signals
        self.main_window.control_panel.start_clicked.connect(self.start_gaia)
        self.main_window.control_panel.pause_clicked.connect(self.pause_gaia)
        self.main_window.control_panel.stop_clicked.connect(self.stop_gaia)
        
        # Worker thread signals
        self.worker_thread.message_logged.connect(self.main_window.log_message)
        self.worker_thread.status_changed.connect(self.main_window.update_status)
        self.worker_thread.user_identified.connect(self.main_window.update_user)
        self.worker_thread.chat_message.connect(self.handle_chat_message)
        
    def handle_chat_message(self, speaker, message):
        """Handle chat messages from different speakers"""
        if speaker == "user":
            self.main_window.chat_widget.add_user_message(message)
        elif speaker == "gaia":
            self.main_window.chat_widget.add_gaia_message(message)
        elif speaker == "system":
            self.main_window.chat_widget.add_system_message(message)
            
    def initialize(self):
        """Initialize the application"""
        self.main_window.log_message("Initializing Gaia AI Assistant...")
        
        # Start worker thread
        self.worker_thread.start()
        
        # Initialize Gaia agent
        if self.worker_thread.initialize_agent():
            self.main_window.log_message("Gaia agent initialized successfully")
            self.main_window.update_status("Ready")
        else:
            self.main_window.log_message("Failed to initialize Gaia agent")
            self.main_window.update_status("Error")
            
    def start_gaia(self):
        """Start Gaia"""
        self.main_window.log_message("Starting Gaia...")
        self.worker_thread.start_gaia()
        
    def pause_gaia(self):
        """Pause/Resume Gaia"""
        self.worker_thread.pause_gaia()
        
    def stop_gaia(self):
        """Stop Gaia"""
        self.main_window.log_message("Stopping Gaia...")
        self.worker_thread.stop_gaia()
        
    def run(self):
        """Run the application"""
        self.main_window.show()
        return self.app.exec_()
        
    def cleanup(self):
        """Cleanup before exit"""
        print("Cleaning up Gaia...")
        
        # Stop the agent first
        if self.worker_thread and hasattr(self.worker_thread, 'gaia_agent') and self.worker_thread.gaia_agent:
            print("Stopping Gaia agent...")
            self.worker_thread.gaia_agent.stop()
            
        # Then stop the worker thread
        if self.worker_thread and self.worker_thread.isRunning():
            print("Stopping worker thread...")
            self.worker_thread.quit()
            if not self.worker_thread.wait(5000):  # Wait up to 5 seconds
                print("Force terminating worker thread...")
                self.worker_thread.terminate()
                self.worker_thread.wait(2000)  # Wait 2 more seconds
            
        print("Cleanup complete.")
        
        # Quit the application
        if self.app:
            self.app.quit()


def main():
    """Main function"""
    
    # Global reference for signal handler
    app_instance = None
    
    def signal_handler(signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\nReceived interrupt signal, shutting down...")
        if app_instance:
            app_instance.cleanup()
        sys.exit(0)
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        app_instance = GaiaApplication()
        exit_code = app_instance.run()
        app_instance.cleanup()
        return exit_code
    except Exception as e:
        print(f"Fatal error: {e}")
        if app_instance:
            app_instance.cleanup()
        return 1


if __name__ == "__main__":
    sys.exit(main())
