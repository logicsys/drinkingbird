# Makefile for drinkingbird Debian package

PACKAGE_NAME = drinkingbird
VERSION = 1.0.0
ARCHITECTURE = all
DEB_FILE = $(PACKAGE_NAME)_$(VERSION)_$(ARCHITECTURE).deb

.PHONY: all build install uninstall clean test help

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
	@rm -rf build/
	@rm -f *.deb

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