# Windcave Python Terminal POS

A Square-inspired POS interface for Windcave payment terminals running MicroPython + LVGL.

## Compatibility

| Component | Version |
|-----------|---------|
| MicroPython | 1.24.1 |
| LVGL | 9.3.0 |

## Terminal Models

| Model | Screen | Full LCD | Usable Area |
|-------|--------|----------|-------------|
| CHU200TxC | 3.5" | 320×480 | 320×452 |
| MTM300-C | 3.5" | 320×480 | 320×452 |
| CHU200TW | 8" widescreen | 800×480 | 800×452 |

*28px is reserved at the top for system status icons*

## Project Structure

```
windcave-python-terminal/
├── simulator/          # Web preview (run locally)
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── terminal/           # MicroPython + LVGL (deploy to device)
│   ├── main.py         # Entry point
│   ├── pos_ui.py       # UI components
│   └── config.py       # Configuration
├── serve.py            # Run simulator locally
└── README.md
```

## Quick Start

### Preview the Simulator

```bash
python3 serve.py
```

Opens http://localhost:8080 with the terminal simulator.

### Features

- **3.5" and 8" screen layouts** - Toggle between compact and widescreen
- **Dark/Light themes**
- **Demo data presets** - Coffee shop, restaurant, retail store
- **Interactive cart** - Add items, see totals, simulate payment

## Terminal Code

The `terminal/` folder contains MicroPython + LVGL 9.3 code ready for deployment.

### Configuration

Edit `terminal/config.py`:

```python
# Backend API URL
BACKEND_URL = "http://your-backend:5000"

# Screen size
# CHU200TxC / MTM300-C: 320x452
# CHU200TW: 800x452
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 452

# Tax rate
TAX_RATE = 0.15
```

### Loading Products

Products are loaded from your backend API. The terminal expects this format:

```json
{
  "products": [
    {
      "id": "prod-1",
      "name": "Flat White",
      "price": 5.50,
      "category_id": "cat-1",
      "color": "#D4A574"
    }
  ],
  "categories": [
    {
      "id": "cat-1",
      "name": "Coffee",
      "icon": "☕",
      "color": "#8B4513"
    }
  ]
}
```

### API Endpoints Expected

- `GET /api/sync` - Returns products, categories, settings
- `POST /api/transactions` - Records completed transactions

## LVGL 9.3 Notes

This code uses LVGL 9.3 API:
- `lv.button()` (not `lv.btn()`)
- `lv.screen_load()` (not `lv.scr_load()`)

Reference: https://docs.lvgl.io/9.3/

## Building Your Backend

The backend can be built with any technology (React/TypeScript, Python/Flask, Node.js, etc).

Required functionality:
1. **Product Management** - CRUD for products and categories
2. **Sync Endpoint** - Returns current products/categories for terminal
3. **Transaction Storage** - Records completed sales

## Deploying to Terminal

1. Configure `terminal/config.py` with your settings
2. Upload `terminal/` files to the Windcave terminal
3. The terminal auto-runs `main.py` on boot

## Theme Colors

```python
# Dark theme
BG_PRIMARY = 0x1A1A2E
BG_SECONDARY = 0x16213E
BG_CARD = 0x0F3460
ACCENT = 0x00D9FF
ACCENT_GREEN = 0x00C853
TEXT_PRIMARY = 0xFFFFFF
TEXT_SECONDARY = 0xA0A0A0
```
