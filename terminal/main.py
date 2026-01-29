"""
Windcave Terminal POS - Main Application
MicroPython + LVGL Entry Point

Deploy this to your Windcave terminal. The UI mimics the
web simulator at 1:1 pixel accuracy.
"""

import lvgl as lv
import time

# Import configuration
from config import (
    BACKEND_URL, SYNC_INTERVAL_MS,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    TAX_RATE, CURRENCY, BUSINESS_NAME
)

# Import UI components
from pos_ui import (
    Theme, Styles,
    Header, CategoryBar, ProductGrid,
    CartPanel, PaymentScreen
)

# Try to import Windcave-specific modules
try:
    from windcave import display_driver, wifi, payment
    SIMULATOR = False
except ImportError:
    SIMULATOR = True
    print("[POS] Running without Windcave hardware")

# Try to import networking
try:
    import urequests as requests
    HAS_NETWORK = True
except ImportError:
    try:
        import requests
        HAS_NETWORK = True
    except ImportError:
        HAS_NETWORK = False
        print("[POS] No network library available")


class POSApp:
    """Main POS Application"""

    def __init__(self):
        self.products = []
        self.categories = []
        self.cart = []
        self.settings = {}
        self.active_category = None
        self.last_sync = 0

        # Initialize display and styles
        self._init_display()
        Styles.init()

        # Build UI
        self._build_ui()

        # Load initial data
        self._load_data()

    def _init_display(self):
        """Initialize LVGL display"""
        if not SIMULATOR:
            display_driver.init(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.screen = lv.obj()
        self.screen.set_style_bg_color(Theme.hex(Theme.BG_PRIMARY), 0)
        lv.screen_load(self.screen)

    def _build_ui(self):
        """Build the main UI"""
        is_widescreen = SCREEN_WIDTH > 600

        if is_widescreen:
            self._build_widescreen()
        else:
            self._build_compact()

    def _build_compact(self):
        """Build UI for 3.5" display (320x452 usable area)"""
        # Header (with settings button)
        self.header = Header(self.screen, 320, 44, on_settings=self._on_settings)
        self.header.container.set_pos(0, 0)

        # Category bar
        self.category_bar = CategoryBar(
            self.screen, 320, 40,
            on_select=self._on_category_select
        )
        self.category_bar.container.set_pos(0, 44)

        # Product area (320x452 - 44 header - 40 categories - 150 cart = 218)
        product_container = lv.obj(self.screen)
        product_container.set_size(320, 218)
        product_container.set_pos(0, 84)
        product_container.set_style_bg_opa(lv.OPA.TRANSP, 0)
        product_container.set_style_border_width(0, 0)
        product_container.set_style_pad_all(8, 0)
        product_container.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)

        self.product_grid = ProductGrid(
            product_container,
            btn_size=95,
            on_select=self._on_product_select
        )

        # Cart panel
        self.cart_panel = CartPanel(
            self.screen, 320, 150,
            on_pay=self._on_pay,
            on_item_click=self._on_cart_item_click
        )
        self.cart_panel.container.set_pos(0, 302)

    def _build_widescreen(self):
        """Build UI for 8" display (800x452 usable area)"""
        # Header (with settings button)
        self.header = Header(self.screen, 800, 52, on_settings=self._on_settings)
        self.header.container.set_pos(0, 0)

        # Left panel (products)
        left_panel = lv.obj(self.screen)
        left_panel.set_size(520, 400)
        left_panel.set_pos(0, 52)
        left_panel.set_style_bg_opa(lv.OPA.TRANSP, 0)
        left_panel.set_style_border_width(0, 0)
        left_panel.set_style_pad_all(0, 0)

        # Category bar
        self.category_bar = CategoryBar(
            left_panel, 520, 46,
            on_select=self._on_category_select
        )
        self.category_bar.container.set_pos(0, 0)

        # Product area (400 - 46 categories = 354)
        product_container = lv.obj(left_panel)
        product_container.set_size(520, 354)
        product_container.set_pos(0, 46)
        product_container.set_style_bg_opa(lv.OPA.TRANSP, 0)
        product_container.set_style_border_width(0, 0)
        product_container.set_style_pad_all(12, 0)
        product_container.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)

        self.product_grid = ProductGrid(
            product_container,
            btn_size=115,
            on_select=self._on_product_select
        )

        # Cart panel (right side)
        self.cart_panel = CartPanel(
            self.screen, 280, 400,
            on_pay=self._on_pay,
            on_item_click=self._on_cart_item_click
        )
        self.cart_panel.container.set_pos(520, 52)
        self.cart_panel.container.set_style_radius(0, 0)
        self.cart_panel.container.set_style_border_width(1, 0)
        self.cart_panel.container.set_style_border_side(lv.BORDER_SIDE.LEFT, 0)
        self.cart_panel.container.set_style_border_color(Theme.hex(Theme.DIVIDER), 0)

    def _load_data(self):
        """Load products from backend or demo data"""
        if HAS_NETWORK and BACKEND_URL:
            try:
                self._sync_with_backend()
            except Exception as e:
                print(f"[POS] Sync failed: {e}")
                self._load_demo_data()
        else:
            self._load_demo_data()

        self._update_display()

    def _sync_with_backend(self):
        """Fetch data from backend API"""
        response = requests.get(f"{BACKEND_URL}/api/sync")
        if response.status_code == 200:
            data = response.json()
            self.products = data.get('products', [])
            self.categories = data.get('categories', [])
            self.settings = data.get('settings', {})
            self.last_sync = time.ticks_ms()
            print(f"[POS] Synced {len(self.products)} products")
        response.close()

    def _load_demo_data(self):
        """Load demo data for testing"""
        self.categories = [
            {"id": "cat-1", "name": "Coffee", "icon": "☕", "color": "#8B4513"},
            {"id": "cat-2", "name": "Food", "icon": "🍽", "color": "#228B22"},
            {"id": "cat-3", "name": "Drinks", "icon": "🥤", "color": "#4169E1"},
            {"id": "cat-4", "name": "Desserts", "icon": "🍰", "color": "#FF69B4"},
        ]

        self.products = [
            {"id": "p1", "name": "Flat White", "price": 5.50, "category_id": "cat-1", "color": "#D4A574"},
            {"id": "p2", "name": "Cappuccino", "price": 5.50, "category_id": "cat-1", "color": "#C4A484"},
            {"id": "p3", "name": "Long Black", "price": 5.00, "category_id": "cat-1", "color": "#3C2415"},
            {"id": "p4", "name": "Latte", "price": 5.50, "category_id": "cat-1", "color": "#E8D4B8"},
            {"id": "p5", "name": "Mocha", "price": 6.00, "category_id": "cat-1", "color": "#5C4033"},
            {"id": "p6", "name": "Espresso", "price": 4.00, "category_id": "cat-1", "color": "#2C1810"},
            {"id": "p7", "name": "Avo Toast", "price": 16.00, "category_id": "cat-2", "color": "#568203"},
            {"id": "p8", "name": "Eggs Bene", "price": 22.00, "category_id": "cat-2", "color": "#FFD700"},
            {"id": "p9", "name": "Bacon Eggs", "price": 18.00, "category_id": "cat-2", "color": "#CD853F"},
            {"id": "p10", "name": "Croissant", "price": 6.50, "category_id": "cat-2", "color": "#DEB887"},
            {"id": "p11", "name": "OJ Fresh", "price": 6.00, "category_id": "cat-3", "color": "#FFA500"},
            {"id": "p12", "name": "Smoothie", "price": 8.00, "category_id": "cat-3", "color": "#FF6B6B"},
            {"id": "p13", "name": "Choc Cake", "price": 9.00, "category_id": "cat-4", "color": "#4A2C2A"},
            {"id": "p14", "name": "Cheesecake", "price": 10.00, "category_id": "cat-4", "color": "#FFFACD"},
            {"id": "p15", "name": "Brownie", "price": 7.00, "category_id": "cat-4", "color": "#3D2314"},
        ]

        print(f"[POS] Loaded {len(self.products)} demo products")

    def _update_display(self):
        """Refresh UI with current data"""
        self.category_bar.set_categories(self.categories)
        self._filter_products()
        self._update_cart()

    def _filter_products(self):
        """Filter products by active category"""
        if self.active_category:
            filtered = [p for p in self.products if p.get('category_id') == self.active_category]
        else:
            filtered = self.products

        self.product_grid.set_products(filtered)

    def _update_cart(self):
        """Update cart display"""
        subtotal = sum(item['price'] * item['qty'] for item in self.cart)
        total = subtotal * (1 + TAX_RATE)
        self.cart_panel.update(self.cart, total)

    # Event handlers
    def _on_settings(self):
        """Handle settings button press"""
        # TODO: Show settings screen
        print("[POS] Settings button pressed")
        # You can implement a settings overlay here

    def _on_category_select(self, category_id):
        """Handle category button press"""
        self.active_category = category_id
        self._filter_products()

    def _on_product_select(self, product):
        """Handle product tap - add to cart"""
        # Check if already in cart
        for item in self.cart:
            if item['id'] == product['id']:
                item['qty'] += 1
                self._update_cart()
                return

        # Add new item
        self.cart.append({
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'qty': 1
        })
        self._update_cart()

    def _on_cart_item_click(self, item):
        """Handle cart item tap - remove one"""
        for cart_item in self.cart:
            if cart_item['id'] == item['id']:
                cart_item['qty'] -= 1
                if cart_item['qty'] <= 0:
                    self.cart.remove(cart_item)
                break
        self._update_cart()

    def _on_pay(self):
        """Handle pay button press"""
        if not self.cart:
            return

        subtotal = sum(item['price'] * item['qty'] for item in self.cart)
        total = subtotal * (1 + TAX_RATE)

        self.payment_screen = PaymentScreen(
            self.screen,
            SCREEN_WIDTH, SCREEN_HEIGHT,
            total,
            on_cancel=self._on_payment_cancel,
            on_complete=self._on_payment_complete
        )

        # In production, trigger Windcave payment here
        if not SIMULATOR:
            self._process_payment(total)
        else:
            # Simulate payment after 3 seconds
            self._simulate_payment()

    def _simulate_payment(self):
        """Simulate payment processing (for demo)"""
        # This would be replaced by actual Windcave payment
        # For now, auto-complete after delay
        pass

    def _process_payment(self, amount):
        """Process payment via Windcave API"""
        try:
            result = payment.process(amount)
            if result.success:
                self._on_payment_complete()
            else:
                print(f"[POS] Payment failed: {result.error}")
        except Exception as e:
            print(f"[POS] Payment error: {e}")

    def _on_payment_cancel(self):
        """Handle payment cancellation"""
        pass

    def _on_payment_complete(self):
        """Handle successful payment"""
        # Record transaction
        if HAS_NETWORK and BACKEND_URL:
            try:
                transaction = {
                    "items": self.cart,
                    "total": sum(item['price'] * item['qty'] for item in self.cart) * (1 + TAX_RATE),
                    "payment_method": "card"
                }
                requests.post(f"{BACKEND_URL}/api/transactions", json=transaction)
            except Exception as e:
                print(f"[POS] Failed to record transaction: {e}")

        # Show success and clear cart
        self.payment_screen.show_success()
        self.cart = []

        # Close after delay
        # In LVGL, would use lv.timer_t

    def run(self):
        """Main loop"""
        print("[POS] Starting main loop")

        while True:
            # Handle LVGL tasks
            lv.task_handler()

            # Periodic sync
            if HAS_NETWORK and BACKEND_URL:
                if time.ticks_diff(time.ticks_ms(), self.last_sync) > SYNC_INTERVAL_MS:
                    try:
                        self._sync_with_backend()
                        self._update_display()
                    except Exception as e:
                        print(f"[POS] Background sync failed: {e}")

            time.sleep_ms(5)


def main():
    """Entry point"""
    print()
    print("=" * 40)
    print("  WINDCAVE TERMINAL POS")
    print(f"  Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print("=" * 40)
    print()

    app = POSApp()
    app.run()


if __name__ == "__main__":
    main()
