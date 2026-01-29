#!/usr/bin/env python3
"""
LVGL Preview Runner for Windcave Terminal POS

This script runs the terminal code in the lv_micropython simulator.
Requires lv_micropython to be built at ~/Desktop/lv_micropython

Usage:
    ./run_lvgl.py [3.5|8]

    3.5 = 320x480 compact terminal (default)
    8   = 800x480 widescreen terminal
"""

import sys
import os

# Paths
MICROPYTHON = os.path.expanduser("~/Desktop/lv_micropython/ports/unix/build-lvgl/micropython")
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TERMINAL_DIR = os.path.join(PROJECT_DIR, "terminal")

# Screen sizes (full LCD, the code handles the 28px status bar internally)
SIZES = {
    "3.5": (320, 480),
    "8": (800, 480)
}

def main():
    # Get screen size from args
    size_arg = sys.argv[1] if len(sys.argv) > 1 else "3.5"
    if size_arg not in SIZES:
        print(f"Unknown size: {size_arg}")
        print("Usage: ./run_lvgl.py [3.5|8]")
        sys.exit(1)

    width, height = SIZES[size_arg]

    # Check if micropython exists
    if not os.path.exists(MICROPYTHON):
        print(f"Error: lv_micropython not found at {MICROPYTHON}")
        print("Run the setup first to build lv_micropython")
        sys.exit(1)

    # Create a launcher script that sets up the display
    launcher = f'''
import sys
sys.path.insert(0, "{TERMINAL_DIR}")

import lvgl as lv
import time

# Initialize LVGL
lv.init()

# Create SDL display
display = lv.sdl_window_create({width}, {height})
mouse = lv.sdl_mouse_create()

# Set window title
lv.sdl_window_set_title(display, b"Windcave Terminal POS")

print("LVGL Preview running - Close the window to exit")
print("Screen: {width}x{height}")

    # Now import and run the POS UI components
    try:
        from pos_ui import Theme, Styles, Header, CategoryBar, ProductGrid, CartPanel, CartPanelWide, Notification

        # Initialize styles
        Styles.init()

        # Create main screen
        screen = lv.obj()
        screen.set_style_bg_color(Theme.hex(Theme.BG_PRIMARY), 0)
        lv.screen_load(screen)

        is_wide = {width} > 600

        # Build UI
        if is_wide:
            header = Header(screen, {width}, 52)
            header.container.set_pos(0, 0)
            
            cat_bar = CategoryBar(screen, 520, 46, on_select=lambda x: print(f"Category: {{x}}"))
            cat_bar.container.set_pos(0, 52)
            
            product_area = lv.obj(screen)
            product_area.set_size(520, {height} - 52 - 46)
            product_area.set_pos(0, 52 + 46)
            
            btn_size = 115
        else:
            header = Header(screen, {width}, 44)
            header.container.set_pos(0, 0)
            
            cat_bar = CategoryBar(screen, {width}, 40, on_select=lambda x: print(f"Category: {{x}}"))
            cat_bar.container.set_pos(0, 44)
            
            product_area = lv.obj(screen)
            product_area.set_size({width}, {height} - 44 - 40 - 150)
            product_area.set_pos(0, 84)
            
            btn_size = 95

        # Demo categories
        categories = [
            {{"id": "cat-1", "name": "Coffee", "icon": "☕", "color": "#8B4513"}},
            {{"id": "cat-2", "name": "Food", "icon": "🍽", "color": "#228B22"}},
            {{"id": "cat-3", "name": "Drinks", "icon": "🥤", "color": "#4169E1"}},
        ]
        cat_bar.set_categories(categories)

        product_area.set_style_bg_opa(lv.OPA.TRANSP, 0)
        product_area.set_style_border_width(0, 0)
        product_area.set_style_pad_all(8, 0)

        cart_items = []

        def on_product_select(product):
            print(f"Selected: {{product['name']}}")
            # Add to cart
            for item in cart_items:
                if item['id'] == product['id']:
                    item['qty'] += 1
                    cart.update(cart_items, sum(i['price']*i['qty'] for i in cart_items) * 1.15)
                    grid.update_badges(cart_items)
                    return
            cart_items.append({{
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'qty': 1
            }})
            cart.update(cart_items, sum(i['price']*i['qty'] for i in cart_items) * 1.15)
            grid.update_badges(cart_items)
            Notification(screen, f"Added {{product['name']}}", style="success")

        grid = ProductGrid(product_area, btn_size=btn_size, on_select=on_product_select)
        
        # Demo products
        products = [
            {{"id": "p1", "name": "Flat White", "price": 5.50, "color": "#D4A574"}},
            {{"id": "p2", "name": "Cappuccino", "price": 5.50, "color": "#C4A484"}},
            {{"id": "p3", "name": "Long Black", "price": 5.00, "color": "#3C2415"}},
            {{"id": "p4", "name": "Latte", "price": 5.50, "color": "#E8D4B8"}},
            {{"id": "p5", "name": "Mocha", "price": 6.00, "color": "#5C4033"}},
            {{"id": "p6", "name": "Espresso", "price": 4.00, "color": "#2C1810"}},
        ]
        grid.set_products(products)

        # Cart panel
        def on_pay():
            if cart_items:
                print("Processing payment...")
                Notification(screen, "Payment initiated!", style="info")

        if is_wide:
            cart = CartPanelWide(screen, 280, {height} - 52, on_pay=on_pay)
            cart.container.set_pos(520, 52)
        else:
            cart = CartPanel(screen, {width}, 150, on_pay=on_pay)
            cart.container.set_pos(0, {height} - 150)

        print("UI loaded successfully!")    print("Click products to add to cart")

except Exception as e:
    print(f"Error loading UI: {{e}}")
    import sys
    sys.print_exception(e)

    # Show error on screen
    screen = lv.obj()
    screen.set_style_bg_color(lv.color_hex(0x1A1A2E), 0)
    lv.screen_load(screen)

    label = lv.label(screen)
    label.set_text(f"Error: {{str(e)[:50]}}")
    label.set_style_text_color(lv.color_hex(0xFF5252), 0)
    label.center()

# Main loop
while True:
    lv.task_handler()
    time.sleep_ms(5)
'''

    # Write temp launcher
    launcher_path = os.path.join(PROJECT_DIR, "_lvgl_launcher.py")
    with open(launcher_path, "w") as f:
        f.write(launcher)

    # Run micropython with the launcher
    print(f"Starting LVGL preview ({width}x{height})...")
    print("Close the window to exit.\n")

    exit_code = os.system(f'cd "{PROJECT_DIR}" && "{MICROPYTHON}" _lvgl_launcher.py')

    # Cleanup
    if os.path.exists(launcher_path):
        os.remove(launcher_path)

    return exit_code

if __name__ == "__main__":
    sys.exit(main() or 0)
