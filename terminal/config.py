"""
Windcave Terminal Configuration
Edit these values before deploying to terminal

Tested with:
- MicroPython 1.24.1
- LVGL 9.3.0
"""

# Backend API configuration
# Set this to your backend server URL
BACKEND_URL = "http://192.168.1.100:5000"

# Sync interval in milliseconds
SYNC_INTERVAL_MS = 30000

# Screen configuration (LVGL usable area - 28px reserved for system status icons)
#
# CHU200TxC / MTM300-C (3.5" terminals):
#   Full LCD: 320x480
#   Usable:   320x452
#
# CHU200TW (8" widescreen):
#   Full LCD: 800x480
#   Usable:   800x452
#
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 452

# Tax rate (0.15 = 15% GST)
TAX_RATE = 0.15

# Currency symbol
CURRENCY = "$"

# Business name shown in header
BUSINESS_NAME = "WINDCAVE POS"

# WiFi configuration (for Windcave terminals)
WIFI_SSID = "your_network"
WIFI_PASSWORD = "your_password"
