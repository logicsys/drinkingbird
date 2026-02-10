# Makefile for drinkingbird Debian package

PACKAGE_NAME = drinkingbird
VERSION = 1.0.3
ARCHITECTURE = all
DEB_FILE = $(PACKAGE_NAME)_$(VERSION)_$(ARCHITECTURE).deb

.PHONY: all build install uninstall clean test help windows windows-clean

all: build

build:
	@echo "Building Debian package..."
	@chmod +x build-deb.sh
	@./build-deb.sh

install: build
	@echo "Installing $(DEB_FILE)..."
	@sudo dpkg -i $(DEB_FILE) || (echo "Installation failed. Trying to fix dependencies..." && sudo apt-get install -f)

uninstall:
	@echo "Uninstalling $(PACKAGE_NAME)..."
	@sudo dpkg -r $(PACKAGE_NAME)

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build/ dist/ __pycache__/ venv-build/
	@rm -f *.deb *.spec.bak

test:
	@echo "Testing drinkingbird installation..."
	@which drinkingbird >/dev/null && echo "✅ drinkingbird command found" || echo "❌ drinkingbird command not found"

help:
	@echo "Drinkingbird Package Builder"
	@echo ""
	@echo "Available targets:"
	@echo "  build     - Build the Debian package"
	@echo "  install   - Build and install the package"
	@echo "  uninstall - Remove the installed package"
	@echo "  clean     - Remove build artifacts"
	@echo "  test      - Test if drinkingbird is installed"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Usage examples:"
	@echo "  make build    # Build the .deb package"
	@echo "  make install  # Build and install"
	@echo "  make clean    # Clean up build files"
	@echo ""
	@echo "Windows targets:"
	@echo "  make windows       # Build Windows executable (requires PyInstaller)"
	@echo "  make windows-clean # Clean Windows build artifacts"

# Windows build targets
windows:
	@echo "Building Windows executable..."
	@python3 build-windows.py --spec

windows-clean:
	@echo "Cleaning Windows build artifacts..."
	@rm -rf build/ dist/ __pycache__/ venv-build/
	@rm -f *.spec.bak 
