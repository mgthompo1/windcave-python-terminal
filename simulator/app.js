/**
 * Windcave Terminal Simulator
 * Web-based preview for LVGL POS interface
 */

class POSSimulator {
    constructor() {
        this.screenSize = '3.5';
        this.theme = 'dark';
        this.products = [];
        this.categories = [];
        this.cart = [];
        this.activeCategory = null;
        this.taxRate = 0.15;

        this.init();
    }

    init() {
        this.loadDemoData('coffee');
        this.bindEvents();
        this.render();
        this.updateTime();
        setInterval(() => this.updateTime(), 1000);
    }

    loadDemoData(type) {
        const datasets = {
            coffee: {
                categories: [
                    { id: 'cat-1', name: 'Coffee', icon: '☕', color: '#8B4513' },
                    { id: 'cat-2', name: 'Food', icon: '🍽️', color: '#228B22' },
                    { id: 'cat-3', name: 'Drinks', icon: '🥤', color: '#4169E1' },
                    { id: 'cat-4', name: 'Desserts', icon: '🍰', color: '#FF69B4' },
                ],
                products: [
                    { id: 'p1', name: 'Flat White', price: 5.50, categoryId: 'cat-1', color: '#D4A574' },
                    { id: 'p2', name: 'Cappuccino', price: 5.50, categoryId: 'cat-1', color: '#C4A484' },
                    { id: 'p3', name: 'Long Black', price: 5.00, categoryId: 'cat-1', color: '#3C2415' },
                    { id: 'p4', name: 'Latte', price: 5.50, categoryId: 'cat-1', color: '#E8D4B8' },
                    { id: 'p5', name: 'Mocha', price: 6.00, categoryId: 'cat-1', color: '#5C4033' },
                    { id: 'p6', name: 'Espresso', price: 4.00, categoryId: 'cat-1', color: '#2C1810' },
                    { id: 'p7', name: 'Avo Toast', price: 16.00, categoryId: 'cat-2', color: '#568203' },
                    { id: 'p8', name: 'Eggs Bene', price: 22.00, categoryId: 'cat-2', color: '#FFD700' },
                    { id: 'p9', name: 'Bacon Eggs', price: 18.00, categoryId: 'cat-2', color: '#CD853F' },
                    { id: 'p10', name: 'Croissant', price: 6.50, categoryId: 'cat-2', color: '#DEB887' },
                    { id: 'p11', name: 'OJ Fresh', price: 6.00, categoryId: 'cat-3', color: '#FFA500' },
                    { id: 'p12', name: 'Smoothie', price: 8.00, categoryId: 'cat-3', color: '#FF6B6B' },
                    { id: 'p13', name: 'Choc Cake', price: 9.00, categoryId: 'cat-4', color: '#4A2C2A' },
                    { id: 'p14', name: 'Cheesecake', price: 10.00, categoryId: 'cat-4', color: '#FFFACD' },
                    { id: 'p15', name: 'Brownie', price: 7.00, categoryId: 'cat-4', color: '#3D2314' },
                ]
            },
            restaurant: {
                categories: [
                    { id: 'cat-1', name: 'Starters', icon: '🥗', color: '#4CAF50' },
                    { id: 'cat-2', name: 'Mains', icon: '🍖', color: '#FF5722' },
                    { id: 'cat-3', name: 'Drinks', icon: '🍷', color: '#9C27B0' },
                    { id: 'cat-4', name: 'Desserts', icon: '🍮', color: '#E91E63' },
                ],
                products: [
                    { id: 'p1', name: 'Soup', price: 12.00, categoryId: 'cat-1', color: '#FF9800' },
                    { id: 'p2', name: 'Bruschetta', price: 14.00, categoryId: 'cat-1', color: '#F44336' },
                    { id: 'p3', name: 'Calamari', price: 18.00, categoryId: 'cat-1', color: '#FFE0B2' },
                    { id: 'p4', name: 'Salad', price: 15.00, categoryId: 'cat-1', color: '#8BC34A' },
                    { id: 'p5', name: 'Steak', price: 42.00, categoryId: 'cat-2', color: '#8D6E63' },
                    { id: 'p6', name: 'Fish', price: 36.00, categoryId: 'cat-2', color: '#03A9F4' },
                    { id: 'p7', name: 'Pasta', price: 28.00, categoryId: 'cat-2', color: '#FFC107' },
                    { id: 'p8', name: 'Risotto', price: 26.00, categoryId: 'cat-2', color: '#FFEB3B' },
                    { id: 'p9', name: 'Burger', price: 24.00, categoryId: 'cat-2', color: '#795548' },
                    { id: 'p10', name: 'Red Wine', price: 14.00, categoryId: 'cat-3', color: '#880E4F' },
                    { id: 'p11', name: 'White Wine', price: 13.00, categoryId: 'cat-3', color: '#F5F5DC' },
                    { id: 'p12', name: 'Beer', price: 10.00, categoryId: 'cat-3', color: '#FFB300' },
                    { id: 'p13', name: 'Tiramisu', price: 14.00, categoryId: 'cat-4', color: '#D7CCC8' },
                    { id: 'p14', name: 'Panna Cotta', price: 12.00, categoryId: 'cat-4', color: '#FFF8E1' },
                    { id: 'p15', name: 'Gelato', price: 10.00, categoryId: 'cat-4', color: '#FFCCBC' },
                ]
            },
            retail: {
                categories: [
                    { id: 'cat-1', name: 'Apparel', icon: '👕', color: '#2196F3' },
                    { id: 'cat-2', name: 'Accessories', icon: '👜', color: '#9C27B0' },
                    { id: 'cat-3', name: 'Footwear', icon: '👟', color: '#4CAF50' },
                    { id: 'cat-4', name: 'Sale', icon: '🏷️', color: '#F44336' },
                ],
                products: [
                    { id: 'p1', name: 'T-Shirt', price: 35.00, categoryId: 'cat-1', color: '#64B5F6' },
                    { id: 'p2', name: 'Jeans', price: 89.00, categoryId: 'cat-1', color: '#1565C0' },
                    { id: 'p3', name: 'Hoodie', price: 75.00, categoryId: 'cat-1', color: '#455A64' },
                    { id: 'p4', name: 'Jacket', price: 120.00, categoryId: 'cat-1', color: '#37474F' },
                    { id: 'p5', name: 'Dress', price: 95.00, categoryId: 'cat-1', color: '#EC407A' },
                    { id: 'p6', name: 'Watch', price: 199.00, categoryId: 'cat-2', color: '#78909C' },
                    { id: 'p7', name: 'Sunglasses', price: 85.00, categoryId: 'cat-2', color: '#212121' },
                    { id: 'p8', name: 'Belt', price: 45.00, categoryId: 'cat-2', color: '#5D4037' },
                    { id: 'p9', name: 'Bag', price: 149.00, categoryId: 'cat-2', color: '#8D6E63' },
                    { id: 'p10', name: 'Sneakers', price: 129.00, categoryId: 'cat-3', color: '#E0E0E0' },
                    { id: 'p11', name: 'Boots', price: 165.00, categoryId: 'cat-3', color: '#4E342E' },
                    { id: 'p12', name: 'Sandals', price: 55.00, categoryId: 'cat-3', color: '#BCAAA4' },
                    { id: 'p13', name: 'Cap 50%', price: 15.00, categoryId: 'cat-4', color: '#EF5350' },
                    { id: 'p14', name: 'Scarf 40%', price: 25.00, categoryId: 'cat-4', color: '#EF5350' },
                    { id: 'p15', name: 'Gloves 30%', price: 18.00, categoryId: 'cat-4', color: '#EF5350' },
                ]
            }
        };

        const data = datasets[type] || datasets.coffee;
        this.categories = data.categories;
        this.products = data.products;
        this.cart = [];
        this.activeCategory = null;
    }

    bindEvents() {
        // Screen size selector
        document.querySelectorAll('.screen-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.screen-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.screenSize = btn.dataset.screen;
                this.render();
            });
        });

        // Theme selector
        document.querySelectorAll('.theme-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.theme-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.theme = btn.dataset.theme;
                document.body.setAttribute('data-theme', this.theme);
                this.render();
            });
        });

        // Demo data buttons
        document.getElementById('loadCoffeeShop').addEventListener('click', () => {
            this.loadDemoData('coffee');
            this.render();
        });

        document.getElementById('loadRestaurant').addEventListener('click', () => {
            this.loadDemoData('restaurant');
            this.render();
        });

        document.getElementById('loadRetail').addEventListener('click', () => {
            this.loadDemoData('retail');
            this.render();
        });

        // Action buttons
        document.getElementById('clearCart').addEventListener('click', () => {
            this.cart = [];
            this.updateCartDisplay();
        });

        document.getElementById('resetDemo').addEventListener('click', () => {
            this.loadDemoData('coffee');
            this.render();
        });
    }

    updateTime() {
        const timeEl = document.querySelector('.terminal-time');
        if (timeEl) {
            const now = new Date();
            timeEl.textContent = now.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                hour12: false
            });
        }
    }

    render() {
        const screen = document.getElementById('terminalScreen');
        const frame = document.getElementById('terminalFrame');

        frame.setAttribute('data-screen', this.screenSize);
        screen.setAttribute('data-screen', this.screenSize);

        if (this.screenSize === '8') {
            this.renderWidescreen(screen);
        } else {
            this.renderCompact(screen);
        }
    }

    renderCompact(container) {
        const filteredProducts = this.getFilteredProducts();

        // CHU200TxC / MTM300-C: 320x452 usable (28px reserved for system status)
        container.innerHTML = `
            <div class="terminal-header" style="height: 44px;">
                <div class="terminal-title">WINDCAVE POS</div>
                <div class="terminal-status">
                    <div class="status-indicator"></div>
                    <div class="terminal-time">12:00</div>
                </div>
            </div>
            <div class="category-bar" style="height: 40px;">
                <button class="category-btn ${!this.activeCategory ? 'active' : ''}" data-category="">
                    <span class="category-icon">🏪</span>
                    All
                </button>
                ${this.categories.map(cat => `
                    <button class="category-btn ${this.activeCategory === cat.id ? 'active' : ''}" data-category="${cat.id}">
                        <span class="category-icon">${cat.icon}</span>
                        ${cat.name}
                    </button>
                `).join('')}
            </div>
            <div class="product-container" style="height: 228px;">
                <div class="product-grid">
                    ${filteredProducts.map(product => `
                        <button class="product-btn" data-product-id="${product.id}" style="background: ${product.color}">
                            <div class="product-name">${product.name}</div>
                            <div class="product-price">$${product.price.toFixed(2)}</div>
                        </button>
                    `).join('')}
                </div>
            </div>
            <div class="cart-panel">
                <div class="cart-header">
                    <span class="cart-title">Cart</span>
                    <span class="cart-items-count">${this.getCartItemCount()} items</span>
                </div>
                <div class="cart-items-scroll">
                    ${this.cart.length === 0 ?
                        '<div class="empty-cart">Tap items to add</div>' :
                        this.cart.map(item => `
                            <button class="cart-chip" data-cart-item-id="${item.id}">
                                <span class="cart-chip-qty">${item.qty}</span>
                                ${item.name.substring(0, 10)}
                            </button>
                        `).join('')
                    }
                </div>
                <div class="cart-divider"></div>
                <div class="cart-total-row">
                    <span class="cart-total-label">Total</span>
                    <span class="cart-total-amount">$${this.getTotal().toFixed(2)}</span>
                </div>
                <button class="pay-btn" ${this.cart.length === 0 ? 'disabled' : ''}>TAP TO PAY</button>
            </div>
        `;

        this.bindTerminalEvents(container);
    }

    renderWidescreen(container) {
        const filteredProducts = this.getFilteredProducts();
        const subtotal = this.getSubtotal();
        const tax = subtotal * this.taxRate;
        const total = subtotal + tax;

        // CHU200TW: 800x452 usable (28px reserved for system status)
        container.innerHTML = `
            <div class="terminal-header" style="height: 52px;">
                <div class="terminal-title">WINDCAVE POS</div>
                <div class="terminal-status">
                    <div class="status-indicator"></div>
                    <div class="terminal-time">12:00</div>
                </div>
            </div>
            <div class="left-panel" style="position: absolute; left: 0; top: 52px; width: 520px; bottom: 0;">
                <div class="category-bar">
                    <button class="category-btn ${!this.activeCategory ? 'active' : ''}" data-category="">
                        <span class="category-icon">🏪</span>
                        All
                    </button>
                    ${this.categories.map(cat => `
                        <button class="category-btn ${this.activeCategory === cat.id ? 'active' : ''}" data-category="${cat.id}">
                            <span class="category-icon">${cat.icon}</span>
                            ${cat.name}
                        </button>
                    `).join('')}
                </div>
                <div class="product-container" style="height: calc(100% - 50px);">
                    <div class="product-grid">
                        ${filteredProducts.map(product => `
                            <button class="product-btn" data-product-id="${product.id}" style="background: ${product.color}">
                                <div class="product-name">${product.name}</div>
                                <div class="product-price">$${product.price.toFixed(2)}</div>
                            </button>
                        `).join('')}
                    </div>
                </div>
            </div>
            <div class="cart-panel-wide">
                <div class="cart-header-wide">
                    <div class="cart-title-wide">Current Order</div>
                    <div class="cart-items-count">${this.getCartItemCount()} items</div>
                </div>
                <div class="cart-items-list">
                    ${this.cart.length === 0 ?
                        '<div class="empty-cart">Tap items to add to order</div>' :
                        this.cart.map(item => `
                            <div class="cart-item-row">
                                <div class="cart-item-qty">${item.qty}</div>
                                <div class="cart-item-name">${item.name}</div>
                                <div class="cart-item-price">$${(item.price * item.qty).toFixed(2)}</div>
                                <button class="cart-item-remove" data-remove-id="${item.id}">×</button>
                            </div>
                        `).join('')
                    }
                </div>
                <div class="cart-summary">
                    <div class="cart-summary-row">
                        <span class="cart-summary-label">Subtotal</span>
                        <span class="cart-summary-value">$${subtotal.toFixed(2)}</span>
                    </div>
                    <div class="cart-summary-row">
                        <span class="cart-summary-label">GST (15%)</span>
                        <span class="cart-summary-value">$${tax.toFixed(2)}</span>
                    </div>
                    <div class="cart-summary-total">
                        <span class="cart-summary-label">Total</span>
                        <span class="cart-summary-value">$${total.toFixed(2)}</span>
                    </div>
                    <button class="pay-btn" ${this.cart.length === 0 ? 'disabled' : ''}>TAP TO PAY</button>
                </div>
            </div>
        `;

        this.bindTerminalEvents(container);
    }

    bindTerminalEvents(container) {
        // Category buttons
        container.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const categoryId = btn.dataset.category || null;
                this.activeCategory = categoryId;
                this.render();
            });
        });

        // Product buttons
        container.querySelectorAll('.product-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const productId = btn.dataset.productId;
                this.addToCart(productId);
            });
        });

        // Cart chips (compact)
        container.querySelectorAll('.cart-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                const itemId = chip.dataset.cartItemId;
                this.removeFromCart(itemId);
            });
        });

        // Remove buttons (widescreen)
        container.querySelectorAll('.cart-item-remove').forEach(btn => {
            btn.addEventListener('click', () => {
                const itemId = btn.dataset.removeId;
                this.removeFromCart(itemId);
            });
        });

        // Pay button
        const payBtn = container.querySelector('.pay-btn');
        if (payBtn) {
            payBtn.addEventListener('click', () => {
                if (this.cart.length > 0) {
                    this.showPaymentModal();
                }
            });
        }
    }

    getFilteredProducts() {
        if (!this.activeCategory) {
            return this.products;
        }
        return this.products.filter(p => p.categoryId === this.activeCategory);
    }

    addToCart(productId) {
        const product = this.products.find(p => p.id === productId);
        if (!product) return;

        const existingItem = this.cart.find(item => item.id === productId);
        if (existingItem) {
            existingItem.qty += 1;
        } else {
            this.cart.push({
                id: product.id,
                name: product.name,
                price: product.price,
                qty: 1
            });
        }

        this.updateCartDisplay();
    }

    removeFromCart(productId) {
        const index = this.cart.findIndex(item => item.id === productId);
        if (index !== -1) {
            if (this.cart[index].qty > 1) {
                this.cart[index].qty -= 1;
            } else {
                this.cart.splice(index, 1);
            }
        }
        this.updateCartDisplay();
    }

    updateCartDisplay() {
        this.render();
    }

    getCartItemCount() {
        return this.cart.reduce((sum, item) => sum + item.qty, 0);
    }

    getSubtotal() {
        return this.cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
    }

    getTotal() {
        const subtotal = this.getSubtotal();
        return subtotal + (subtotal * this.taxRate);
    }

    showPaymentModal() {
        const screen = document.getElementById('terminalScreen');
        const total = this.getTotal();

        const overlay = document.createElement('div');
        overlay.className = 'payment-overlay';
        overlay.innerHTML = `
            <div class="payment-card">
                <div class="payment-icon">📶</div>
                <div class="payment-amount">$${total.toFixed(2)}</div>
                <div class="payment-instruction">Tap, insert or swipe<br>your card</div>
                <div class="payment-progress">
                    <div class="payment-progress-bar"></div>
                </div>
                <button class="payment-cancel">CANCEL</button>
            </div>
        `;

        screen.appendChild(overlay);

        // Animate progress bar
        const progressBar = overlay.querySelector('.payment-progress-bar');
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 2;
            progressBar.style.width = `${progress}%`;

            if (progress >= 100) {
                clearInterval(progressInterval);
                this.showSuccessModal(total);
                overlay.remove();
            }
        }, 60);

        // Cancel button
        overlay.querySelector('.payment-cancel').addEventListener('click', () => {
            clearInterval(progressInterval);
            overlay.remove();
        });
    }

    showSuccessModal(total) {
        const screen = document.getElementById('terminalScreen');

        const overlay = document.createElement('div');
        overlay.className = 'success-overlay';
        overlay.innerHTML = `
            <div class="success-card">
                <div class="success-icon">✓</div>
                <div class="success-text">Payment Approved</div>
                <div class="success-amount">$${total.toFixed(2)}</div>
            </div>
        `;

        screen.appendChild(overlay);

        // Auto-dismiss and clear cart
        setTimeout(() => {
            this.cart = [];
            overlay.remove();
            this.render();
        }, 2500);
    }
}

// Initialize simulator
document.addEventListener('DOMContentLoaded', () => {
    window.simulator = new POSSimulator();
});
