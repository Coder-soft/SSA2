"""
Installation script for Power Python IDE dependencies.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies using pip."""
    print("Installing Power Python IDE dependencies...")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(script_dir, "requirements.txt")
    
    # Check if requirements.txt exists
    if not os.path.exists(requirements_path):
        print(f"Error: requirements.txt not found at {requirements_path}")
        return False
    
    try:
        # Install dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Main function."""
    print("Power Python IDE Dependency Installer")
    print("=====================================")
    
    success = install_dependencies()
    
    if success:
        print("\nYou can now run the IDE with: python ide/desktop_ide.py")
    else:
        print("\nFailed to install dependencies. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
