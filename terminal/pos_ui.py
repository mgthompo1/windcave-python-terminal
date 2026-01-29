"""
Windcave Terminal POS - UI Components
MicroPython + LVGL UI widgets and styling
"""

import lvgl as lv


class Theme:
    """Color theme constants - matches web simulator"""

    # Dark theme (default)
    BG_PRIMARY = 0x1A1A2E
    BG_SECONDARY = 0x16213E
    BG_CARD = 0x0F3460
    ACCENT = 0x00D9FF
    ACCENT_GREEN = 0x00C853
    ACCENT_ORANGE = 0xFF6B35
    TEXT_PRIMARY = 0xFFFFFF
    TEXT_SECONDARY = 0xA0A0A0
    DANGER = 0xFF5252
    SUCCESS = 0x4CAF50
    DIVIDER = 0x2A2A4A

    @classmethod
    def hex(cls, color):
        return lv.color_hex(color)


class Styles:
    """Reusable LVGL styles"""

    _initialized = False
    card = None
    btn = None
    btn_pressed = None
    category = None
    category_active = None
    cart_item = None

    @classmethod
    def init(cls):
        if cls._initialized:
            return

        # Card style
        cls.card = lv.style_t()
        cls.card.init()
        cls.card.set_bg_color(Theme.hex(Theme.BG_CARD))
        cls.card.set_bg_opa(lv.OPA.COVER)
        cls.card.set_radius(12)
        cls.card.set_border_width(0)
        cls.card.set_shadow_width(8)
        cls.card.set_shadow_opa(lv.OPA._30)
        cls.card.set_shadow_color(lv.color_hex(0x000000))
        cls.card.set_pad_all(8)

        # Button style
        cls.btn = lv.style_t()
        cls.btn.init()
        cls.btn.set_bg_color(Theme.hex(Theme.BG_CARD))
        cls.btn.set_radius(8)
        cls.btn.set_border_width(0)
        cls.btn.set_shadow_width(4)
        cls.btn.set_shadow_opa(lv.OPA._20)

        # Button pressed
        cls.btn_pressed = lv.style_t()
        cls.btn_pressed.init()
        cls.btn_pressed.set_bg_color(Theme.hex(Theme.ACCENT))
        cls.btn_pressed.set_transform_width(-2)
        cls.btn_pressed.set_transform_height(-2)

        # Category button
        cls.category = lv.style_t()
        cls.category.init()
        cls.category.set_bg_color(Theme.hex(Theme.BG_SECONDARY))
        cls.category.set_radius(20)
        cls.category.set_pad_hor(16)
        cls.category.set_pad_ver(8)
        cls.category.set_border_width(1)
        cls.category.set_border_color(Theme.hex(Theme.DIVIDER))

        # Category active
        cls.category_active = lv.style_t()
        cls.category_active.init()
        cls.category_active.set_bg_color(Theme.hex(Theme.ACCENT))
        cls.category_active.set_border_width(0)

        # Cart item
        cls.cart_item = lv.style_t()
        cls.cart_item.init()
        cls.cart_item.set_bg_color(Theme.hex(Theme.BG_SECONDARY))
        cls.cart_item.set_radius(8)
        cls.cart_item.set_pad_all(12)
        cls.cart_item.set_border_width(0)

        cls._initialized = True


class Header:
    """Terminal header bar"""

    def __init__(self, parent, width, height, on_settings=None):
        self.on_settings = on_settings

        self.container = lv.obj(parent)
        self.container.set_size(width, height)
        self.container.set_style_bg_color(Theme.hex(Theme.BG_SECONDARY), 0)
        self.container.set_style_radius(0, 0)
        self.container.set_style_border_width(0, 0)
        self.container.set_style_pad_all(0, 0)
        self.container.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

        # Title
        self.title = lv.label(self.container)
        self.title.set_text("WINDCAVE POS")
        self.title.set_style_text_color(Theme.hex(Theme.TEXT_PRIMARY), 0)
        self.title.set_style_text_font(lv.font_montserrat_16, 0)
        self.title.align(lv.ALIGN.LEFT_MID, 12, 0)

        # Settings button
        self.settings_btn = lv.button(self.container)
        self.settings_btn.set_size(32, 32)
        self.settings_btn.set_style_bg_opa(lv.OPA.TRANSP, 0)
        self.settings_btn.set_style_border_width(0, 0)
        self.settings_btn.set_style_shadow_width(0, 0)
        self.settings_btn.align(lv.ALIGN.RIGHT_MID, -70, 0)

        settings_icon = lv.label(self.settings_btn)
        settings_icon.set_text(lv.SYMBOL.SETTINGS)
        settings_icon.set_style_text_color(Theme.hex(Theme.TEXT_SECONDARY), 0)
        settings_icon.center()

        if on_settings:
            self.settings_btn.add_event_cb(lambda e: on_settings(), lv.EVENT.CLICKED, None)

        # Status LED
        self.status = lv.obj(self.container)
        self.status.set_size(10, 10)
        self.status.set_style_bg_color(Theme.hex(Theme.SUCCESS), 0)
        self.status.set_style_radius(5, 0)
        self.status.set_style_border_width(0, 0)
        self.status.align(lv.ALIGN.RIGHT_MID, -46, 0)

        # Time
        self.time_label = lv.label(self.container)
        self.time_label.set_text("12:00")
        self.time_label.set_style_text_color(Theme.hex(Theme.TEXT_SECONDARY), 0)
        self.time_label.align(lv.ALIGN.RIGHT_MID, -10, 0)

    def set_time(self, time_str):
        self.time_label.set_text(time_str)

    def set_status(self, connected):
        color = Theme.SUCCESS if connected else Theme.DANGER
        self.status.set_style_bg_color(Theme.hex(color), 0)


class CategoryBar:
    """Horizontal scrolling category selector"""

    def __init__(self, parent, width, height, on_select=None):
        self.on_select = on_select
        self.buttons = []
        self.active_id = None

        self.container = lv.obj(parent)
        self.container.set_size(width, height)
        self.container.set_style_bg_opa(lv.OPA.TRANSP, 0)
        self.container.set_style_border_width(0, 0)
        self.container.set_style_pad_all(4, 0)
        self.container.set_flex_flow(lv.FLEX_FLOW.ROW)
        self.container.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        self.container.set_style_pad_column(8, 0)
        self.container.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        self.container.set_scroll_dir(lv.DIR.HOR)

        # Add "All" button
        self._add_button("All", "🏪", None, is_all=True)

    def _add_button(self, name, icon, cat_id, is_all=False):
        btn = lv.button(self.container)
        btn.set_size(lv.SIZE_CONTENT, 36)
        btn.add_style(Styles.category, 0)
        btn.add_style(Styles.category_active, lv.STATE.CHECKED)
        btn.add_flag(lv.obj.FLAG.CHECKABLE)

        if is_all:
            btn.add_state(lv.STATE.CHECKED)
            self.active_id = None

        label = lv.label(btn)
        label.set_text(f"{icon} {name}")
        label.set_style_text_color(Theme.hex(Theme.TEXT_PRIMARY), 0)
        label.center()

        btn.add_event_cb(lambda e: self._on_click(e, cat_id), lv.EVENT.CLICKED, None)
        self.buttons.append((btn, cat_id))

        return btn

    def _on_click(self, event, cat_id):
        btn = event.get_target()

        # Uncheck all others
        for b, _ in self.buttons:
            if b != btn:
                b.clear_state(lv.STATE.CHECKED)

        self.active_id = cat_id
        if self.on_select:
            self.on_select(cat_id)

    def set_categories(self, categories):
        # Clear existing (except "All")
        for btn, _ in self.buttons[1:]:
            btn.delete()
        self.buttons = self.buttons[:1]

        # Add new categories
        for cat in categories:
            self._add_button(cat['name'], cat.get('icon', '📦'), cat['id'])


class ProductGrid:
    """Grid of product buttons"""

    def __init__(self, parent, btn_size=95, on_select=None):
        self.btn_size = btn_size
        self.on_select = on_select
        self.buttons = []

        self.container = lv.obj(parent)
        self.container.set_size(lv.pct(100), lv.SIZE_CONTENT)
        self.container.set_style_bg_opa(lv.OPA.TRANSP, 0)
        self.container.set_style_border_width(0, 0)
        self.container.set_style_pad_all(0, 0)
        self.container.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.container.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
        self.container.set_style_pad_row(8, 0)
        self.container.set_style_pad_column(8, 0)
        self.container.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

    def _create_product_button(self, product):
        btn = lv.button(self.container)
        btn.set_size(self.btn_size, self.btn_size)
        btn.add_style(Styles.btn, 0)
        btn.add_style(Styles.btn_pressed, lv.STATE.PRESSED)

        # Set color
        if product.get('color'):
            color = int(product['color'].replace('#', ''), 16)
            btn.set_style_bg_color(lv.color_hex(color), 0)

        # Content container
        cont = lv.obj(btn)
        cont.set_size(lv.pct(100), lv.pct(100))
        cont.set_style_bg_opa(lv.OPA.TRANSP, 0)
        cont.set_style_border_width(0, 0)
        cont.set_style_pad_all(4, 0)
        cont.clear_flag(lv.obj.FLAG.CLICKABLE)
        cont.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

        # Name
        name = lv.label(cont)
        name.set_text(product['name'])
        name.set_style_text_color(Theme.hex(Theme.TEXT_PRIMARY), 0)
        name.set_style_text_font(lv.font_montserrat_12, 0)
        name.set_long_mode(lv.label.LONG.WRAP)
        name.set_width(self.btn_size - 16)
        name.align(lv.ALIGN.TOP_LEFT, 0, 0)

        # Price
        price = lv.label(cont)
        price.set_text(f"${product['price']:.2f}")
        price.set_style_text_color(Theme.hex(Theme.TEXT_PRIMARY), 0)
        price.set_style_text_font(lv.font_montserrat_14, 0)
        price.align(lv.ALIGN.BOTTOM_LEFT, 0, 0)

        btn.add_event_cb(lambda e: self._on_click(product), lv.EVENT.CLICKED, None)
        self.buttons.append(btn)

        return btn

    def _on_click(self, product):
        if self.on_select:
            self.on_select(product)

    def set_products(self, products):
        # Clear existing
        for btn in self.buttons:
            btn.delete()
        self.buttons = []

        # Add new products
        for product in products:
            self._create_product_button(product)


class CartPanel:
    """Cart display panel for compact layout"""

    def __init__(self, parent, width, height, on_pay=None, on_item_click=None):
        self.on_pay = on_pay
        self.on_item_click = on_item_click
        self.cart = []

        self.container = lv.obj(parent)
        self.container.set_size(width, height)
        self.container.add_style(Styles.card, 0)
        self.container.set_style_radius(16, 0)
        self.container.set_style_pad_all(12, 0)
        self.container.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

        self._build_ui()

    def _build_ui(self):
        # Header
        header = lv.obj(self.container)
        header.set_size(lv.pct(100), 24)
        header.set_style_bg_opa(lv.OPA.TRANSP, 0)
        header.set_style_border_width(0, 0)
        header.set_style_pad_all(0, 0)
        header.align(lv.ALIGN.TOP_LEFT, 0, 0)
        header.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

        cart_label = lv.label(header)
        cart_label.set_text("Cart")
        cart_label.set_style_text_color(Theme.hex(Theme.TEXT_SECONDARY), 0)
        cart_label.align(lv.ALIGN.LEFT_MID, 0, 0)

        self.count_label = lv.label(header)
        self.count_label.set_text("0 items")
        self.count_label.set_style_text_color(Theme.hex(Theme.TEXT_SECONDARY), 0)
        self.count_label.align(lv.ALIGN.RIGHT_MID, 0, 0)

        # Items scroll area
        self.items_container = lv.obj(self.container)
        self.items_container.set_size(lv.pct(100), 40)
        self.items_container.set_pos(0, 28)
        self.items_container.set_style_bg_opa(lv.OPA.TRANSP, 0)
        self.items_container.set_style_border_width(0, 0)
        self.items_container.set_style_pad_all(0, 0)
        self.items_container.set_flex_flow(lv.FLEX_FLOW.ROW)
        self.items_container.set_style_pad_column(4, 0)
        self.items_container.set_scroll_dir(lv.DIR.HOR)
        self.items_container.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

        # Divider
        divider = lv.obj(self.container)
        divider.set_size(lv.pct(100), 1)
        divider.set_pos(0, 72)
        divider.set_style_bg_color(Theme.hex(Theme.DIVIDER), 0)
        divider.set_style_border_width(0, 0)

        # Total
        total_cont = lv.obj(self.container)
        total_cont.set_size(lv.pct(100), 28)
        total_cont.set_pos(0, 76)
        total_cont.set_style_bg_opa(lv.OPA.TRANSP, 0)
        total_cont.set_style_border_width(0, 0)
        total_cont.set_style_pad_all(0, 0)
        total_cont.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

        total_text = lv.label(total_cont)
        total_text.set_text("Total")
        total_text.set_style_text_color(Theme.hex(Theme.TEXT_PRIMARY), 0)
        total_text.set_style_text_font(lv.font_montserrat_14, 0)
        total_text.align(lv.ALIGN.LEFT_MID, 0, 0)

        self.total_label = lv.label(total_cont)
        self.total_label.set_text("$0.00")
        self.total_label.set_style_text_color(Theme.hex(Theme.ACCENT), 0)
        self.total_label.set_style_text_font(lv.font_montserrat_20, 0)
        self.total_label.align(lv.ALIGN.RIGHT_MID, 0, 0)

        # Pay button
        self.pay_btn = lv.button(self.container)
        self.pay_btn.set_size(lv.pct(100), 44)
        self.pay_btn.align(lv.ALIGN.BOTTOM_MID, 0, 0)
        self.pay_btn.set_style_bg_color(Theme.hex(Theme.ACCENT_GREEN), 0)
        self.pay_btn.set_style_radius(10, 0)
        self.pay_btn.add_event_cb(self._on_pay_click, lv.EVENT.CLICKED, None)

        pay_label = lv.label(self.pay_btn)
        pay_label.set_text("TAP TO PAY")
        pay_label.set_style_text_color(Theme.hex(Theme.TEXT_PRIMARY), 0)
        pay_label.set_style_text_font(lv.font_montserrat_16, 0)
        pay_label.center()

    def _on_pay_click(self, event):
        if self.cart and self.on_pay:
            self.on_pay()

    def update(self, cart, total):
        self.cart = cart

        # Update count
        count = sum(item['qty'] for item in cart)
        self.count_label.set_text(f"{count} item{'s' if count != 1 else ''}")

        # Update total
        self.total_label.set_text(f"${total:.2f}")

        # Update items
        self.items_container.clean()

        if not cart:
            empty = lv.label(self.items_container)
            empty.set_text("Tap items to add")
            empty.set_style_text_color(Theme.hex(Theme.TEXT_SECONDARY), 0)
        else:
            for item in cart:
                self._create_chip(item)

    def _create_chip(self, item):
        chip = lv.button(self.items_container)
        chip.set_size(lv.SIZE_CONTENT, 32)
        chip.set_style_bg_color(Theme.hex(Theme.BG_SECONDARY), 0)
        chip.set_style_radius(16, 0)
        chip.set_style_pad_hor(12, 0)

        text = f"{item['qty']}x {item['name'][:10]}" if item['qty'] > 1 else item['name'][:12]
        label = lv.label(chip)
        label.set_text(text)
        label.set_style_text_color(Theme.hex(Theme.TEXT_PRIMARY), 0)
        label.set_style_text_font(lv.font_montserrat_12, 0)

        if self.on_item_click:
            chip.add_event_cb(lambda e: self.on_item_click(item), lv.EVENT.CLICKED, None)


class PaymentScreen:
    """Payment processing overlay"""

    def __init__(self, parent, width, height, amount, on_cancel=None, on_complete=None):
        self.on_cancel = on_cancel
        self.on_complete = on_complete
        self.amount = amount

        # Overlay
        self.overlay = lv.obj(parent)
        self.overlay.set_size(width, height)
        self.overlay.set_style_bg_color(lv.color_hex(0x000000), 0)
        self.overlay.set_style_bg_opa(lv.OPA._80, 0)
        self.overlay.set_style_border_width(0, 0)
        self.overlay.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

        # Card
        card = lv.obj(self.overlay)
        card_width = min(280, width - 40)
        card.set_size(card_width, 300)
        card.center()
        card.add_style(Styles.card, 0)
        card.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

        # Icon
        icon = lv.label(card)
        icon.set_text("📶")
        icon.set_style_text_font(lv.font_montserrat_48, 0)
        icon.align(lv.ALIGN.TOP_MID, 0, 20)

        # Amount
        amt = lv.label(card)
        amt.set_text(f"${amount:.2f}")
        amt.set_style_text_color(Theme.hex(Theme.ACCENT), 0)
        amt.set_style_text_font(lv.font_montserrat_28, 0)
        amt.align(lv.ALIGN.TOP_MID, 0, 90)

        # Instructions
        instruction = lv.label(card)
        instruction.set_text("Tap, insert or swipe\nyour card")
        instruction.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        instruction.set_style_text_color(Theme.hex(Theme.TEXT_SECONDARY), 0)
        instruction.align(lv.ALIGN.CENTER, 0, 20)

        # Cancel button
        cancel_btn = lv.button(card)
        cancel_btn.set_size(lv.pct(80), 44)
        cancel_btn.align(lv.ALIGN.BOTTOM_MID, 0, -16)
        cancel_btn.set_style_bg_color(Theme.hex(Theme.DANGER), 0)
        cancel_btn.set_style_radius(10, 0)

        cancel_label = lv.label(cancel_btn)
        cancel_label.set_text("CANCEL")
        cancel_label.set_style_text_color(Theme.hex(Theme.TEXT_PRIMARY), 0)
        cancel_label.center()

        cancel_btn.add_event_cb(self._on_cancel, lv.EVENT.CLICKED, None)

    def _on_cancel(self, event):
        self.close()
        if self.on_cancel:
            self.on_cancel()

    def close(self):
        self.overlay.delete()

    def show_success(self):
        """Transform to success state"""
        self.overlay.set_style_bg_color(Theme.hex(Theme.ACCENT_GREEN), 0)
        self.overlay.set_style_bg_opa(lv.OPA._95, 0)
        self.overlay.clean()

        # Success icon
        icon = lv.label(self.overlay)
        icon.set_text("✓")
        icon.set_style_text_font(lv.font_montserrat_48, 0)
        icon.set_style_text_color(Theme.hex(Theme.TEXT_PRIMARY), 0)
        icon.align(lv.ALIGN.CENTER, 0, -40)

        # Text
        text = lv.label(self.overlay)
        text.set_text("Payment Approved")
        text.set_style_text_color(Theme.hex(Theme.TEXT_PRIMARY), 0)
        text.set_style_text_font(lv.font_montserrat_24, 0)
        text.align(lv.ALIGN.CENTER, 0, 20)

        # Amount
        amt = lv.label(self.overlay)
        amt.set_text(f"${self.amount:.2f}")
        amt.set_style_text_color(Theme.hex(Theme.TEXT_PRIMARY), 0)
        amt.set_style_text_font(lv.font_montserrat_20, 0)
        amt.align(lv.ALIGN.CENTER, 0, 60)
