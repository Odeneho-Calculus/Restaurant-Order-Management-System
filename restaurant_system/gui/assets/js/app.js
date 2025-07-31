// Restaurant Management System - Main Application

/**
 * Main Restaurant Management Application Class
 */
class RestaurantApp {
    constructor() {
        this.currentTab = 'orders';
        this.menuItems = [];
        this.currentOrder = {
            items: [],
            customer: {},
            total: 0,
            subtotal: 0,
            tax: 0
        };
        this.orders = [];
        this.taxRate = 0.08; // 8% tax

        // Initialize application
        this.init();
    }

    /**
     * Initialize the application
     */
    async init() {
        console.log('🚀 RestaurantApp.init() - Starting initialization...');

        try {
            console.log('📱 Step 1: Showing loading overlay...');
            this.showLoading('Initializing application...');

            console.log('🎯 Step 2: Setting up event listeners...');
            this.setupEventListeners();
            console.log('✅ Event listeners setup completed');

            console.log('📊 Step 3: Loading initial data...');
            await this.loadInitialData();
            console.log('✅ Initial data loaded successfully');

            console.log('🎨 Step 4: Initializing UI components...');
            this.initializeUI();
            console.log('✅ UI initialization completed');

            console.log('🎉 Step 5: Initializing footer...');
            this.initializeFooter();

            console.log('🎉 Step 6: Hiding loading overlay...');
            this.hideLoading();

            console.log('🎊 Restaurant Management System initialized successfully!');
        } catch (error) {
            console.error('❌ Failed to initialize application:', error);
            console.error('Error details:', error.stack);
            this.showNotification('Failed to initialize application: ' + error.message, 'error');
            this.hideLoading();
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const tabName = tab.dataset.tab;
                this.switchTab(tabName);
            });
        });

        // Menu search
        const searchInput = document.getElementById('menuSearch');
        if (searchInput) {
            searchInput.addEventListener('input', RestaurantUtils.debounce((e) => {
                this.filterMenuItems(e.target.value);
            }, 300));
        }

        // Category filter
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const category = btn.dataset.category;
                this.filterByCategory(category);

                // Update active state
                document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });

        // Order actions
        document.getElementById('clearOrderBtn')?.addEventListener('click', () => {
            this.clearOrder();
        });

        document.getElementById('previewOrderBtn')?.addEventListener('click', () => {
            this.showOrderPreview();
        });

        document.getElementById('submitOrderBtn')?.addEventListener('click', () => {
            this.submitCurrentOrder();
        });

        // Customer form changes
        ['customerName', 'customerPhone', 'tableNumber', 'orderType'].forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('change', () => {
                    this.updateCustomerInfo();
                });
            }
        });

        // Menu management
        document.getElementById('addMenuItemBtn')?.addEventListener('click', () => {
            this.showAddMenuItemModal();
        });

        // Reports
        document.getElementById('reportPeriod')?.addEventListener('change', (e) => {
            this.handlePeriodChange(e.target.value);
        });

        document.getElementById('exportReportBtn')?.addEventListener('click', () => {
            this.exportReport();
        });

        document.getElementById('refreshReportBtn')?.addEventListener('click', () => {
            this.refreshReports();
        });

        document.getElementById('applyDateRange')?.addEventListener('click', () => {
            this.applyCustomDateRange();
        });

        // Settings and help
        document.getElementById('settingsBtn')?.addEventListener('click', () => {
            this.showSettings();
        });

        document.getElementById('helpBtn')?.addEventListener('click', () => {
            this.showHelp();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });


    }

    /**
     * Load initial data from API
     */
    async loadInitialData() {
        console.log('📊 loadInitialData() - Starting data loading...');

        try {
            console.log('🍽️ Loading menu items from API...');
            console.log('API object available:', typeof restaurantAPI !== 'undefined');

            if (typeof restaurantAPI === 'undefined') {
                throw new Error('restaurantAPI is not available - API module may not be loaded');
            }

            this.menuItems = await restaurantAPI.getMenuItems();
            console.log(`✅ Loaded ${this.menuItems.length} menu items:`, this.menuItems.slice(0, 3));

            // Debug: Check the structure of menu items
            if (this.menuItems.length > 0) {
                const firstItem = this.menuItems[0];
                console.log('🔍 First menu item structure:', firstItem);
                console.log('🔍 Available fields:', Object.keys(firstItem));
                console.log('🔍 is_available field:', firstItem.is_available);
            }

            console.log('📋 Loading existing orders from API...');
            this.orders = await restaurantAPI.getOrders();
            console.log(`✅ Loaded ${this.orders.length} orders:`, this.orders.slice(0, 2));

            console.log('📊 Initial data loading completed successfully');

            // Render menu items now that data is loaded
            console.log('🎨 Rendering menu items after data load...');
            this.renderMenuItems();

            // Also force render after a short delay to ensure DOM is ready
            setTimeout(() => {
                console.log('🕐 Force rendering menu items after 1 second delay...');
                this.renderMenuItems();
            }, 1000);
        } catch (error) {
            console.error('❌ Error loading initial data:', error);
            console.error('Error stack:', error.stack);
            this.showNotification('Error loading data: ' + error.message, 'error');
            throw error; // Re-throw to stop initialization
        }
    }

    /**
     * Initialize UI components
     */
    initializeUI() {
        console.log('🎨 initializeUI() - Setting up UI components...');
        // Note: renderMenuItems() is now called after data is loaded in loadInitialData()
        this.updateOrderDisplay();
        this.updateQueueDisplay();
        this.updateMenuManagement();
        this.updateReportsData();
        console.log('✅ UI components setup completed');
    }

    /**
     * Switch between tabs
     */
    switchTab(tabName) {
        if (this.currentTab === tabName) return;

        // Update navigation
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });

        // Update content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `${tabName}-tab`);
        });

        this.currentTab = tabName;

        // Refresh data for specific tabs
        switch (tabName) {
            case 'orders':
                this.updateOrdersTab();
                break;
            case 'queue':
                this.updateQueueDisplay();
                break;
            case 'menu':
                this.updateMenuManagement();
                break;
            case 'reports':
                this.updateReportsData();
                break;
        }
    }

    /**
     * Render menu items
     */
    renderMenuItems() {
        console.log('🎨 renderMenuItems() - Starting menu rendering...');

        const menuGrid = document.getElementById('menuGrid');
        if (!menuGrid) {
            console.error('❌ Menu grid element not found');
            return;
        }

        console.log('✅ Menu grid element found:', menuGrid);
        console.log(`🍽️ Menu items available: ${this.menuItems ? this.menuItems.length : 'undefined'}`);

        // Debug: Check if Order tab is active and visible
        const orderTab = document.getElementById('orders-tab');
        const isOrderTabActive = orderTab && orderTab.classList.contains('active');
        console.log(`🔍 Order tab active: ${isOrderTabActive}`);
        console.log(`🔍 Order tab display: ${orderTab ? getComputedStyle(orderTab).display : 'not found'}`);
        console.log(`🔍 Menu grid display: ${getComputedStyle(menuGrid).display}`);
        console.log(`🔍 Menu grid visibility: ${getComputedStyle(menuGrid).visibility}`);
        console.log(`🔍 Menu grid opacity: ${getComputedStyle(menuGrid).opacity}`);

        // Fix parent container scrolling issues
        const menuPanel = menuGrid.closest('.menu-panel');
        if (menuPanel) {
            menuPanel.style.overflow = 'visible';
            menuPanel.style.height = '100%';
            console.log('🔧 Fixed menu panel overflow for scrolling');
        }

        if (!this.menuItems || this.menuItems.length === 0) {
            console.warn('⚠️ No menu items available to render');
            menuGrid.innerHTML = '<div class="no-items">No menu items available</div>';
            return;
        }

        // Clear existing content - same pattern as updateMenuManagement()
        menuGrid.innerHTML = '';

        // Force menu grid visibility and fix layout constraints
        menuGrid.style.opacity = '1';
        menuGrid.style.visibility = 'visible';
        menuGrid.style.display = 'grid';
        menuGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(300px, 1fr))';
        menuGrid.style.gap = '20px';
        menuGrid.style.padding = '20px';
        menuGrid.style.height = '100%';
        menuGrid.style.maxHeight = 'calc(100vh - 200px)';
        menuGrid.style.overflowY = 'auto';
        menuGrid.style.overflowX = 'hidden';

        // Simple iteration through all menu items - same pattern as updateMenuManagement()
        this.menuItems.forEach((item, index) => {
            console.log(`📋 Rendering menu item ${index + 1}/${this.menuItems.length}: ${item.name}`);

            const menuCard = document.createElement('div');
            menuCard.className = 'menu-item-card';
            menuCard.setAttribute('data-item-id', item.id);
            menuCard.setAttribute('data-category', item.category);

            // Add necessary classes and data attributes for filtering
            menuCard.classList.add('menu-item-card');
            menuCard.dataset.category = item.category;

            // Use completely basic HTML with inline styles to bypass CSS issues
            menuCard.innerHTML = `
                <div style="padding: 15px; background: white; border: 1px solid #ddd; border-radius: 8px; margin: 10px;">
                    <div style="background: #f5f5f5; height: 120px; border-radius: 4px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
                        <span style="font-size: 24px; color: #666;">🍽️</span>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <h3 class="menu-item-name" style="margin: 0; font-size: 18px; font-weight: bold; color: #333;">${item.name}</h3>
                        <span style="font-size: 16px; font-weight: bold; color: #e44d26;">$${parseFloat(item.price).toFixed(2)}</span>
                    </div>
                    <p class="menu-item-description" style="margin: 10px 0; color: #666; font-size: 14px;">${item.description || 'No description available'}</p>
                    <div class="menu-item-category" style="margin: 10px 0; padding: 4px 8px; background: #f0f0f0; border-radius: 4px; display: inline-block; font-size: 12px; color: #666; text-transform: capitalize;">${item.category}</div>
                    <div style="margin-top: 15px;">
                        <button onclick="window.restaurantApp.addItemToOrder('${item.id}', '${item.name}', ${item.price})"
                                style="background: #e44d26; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 14px; width: 100%;">
                            ➕ Add to Order
                        </button>
                    </div>
                </div>
            `;

            // Simple appendChild - same pattern as updateMenuManagement()
            menuGrid.appendChild(menuCard);

            // Force visibility and fix height/overflow issues
            menuCard.style.opacity = '1';
            menuCard.style.visibility = 'visible';
            menuCard.style.display = 'block';
            menuCard.style.height = 'auto';
            menuCard.style.minHeight = 'auto';
            menuCard.style.maxHeight = 'none';
            menuCard.style.overflow = 'visible';
            menuCard.style.position = 'relative';
            menuCard.style.flexShrink = '0';

            console.log(`✅ Successfully added menu item: ${item.name}`);
            console.log(`🔍 Card innerHTML length: ${menuCard.innerHTML.length}`);
            console.log(`🔍 Card has content: ${menuCard.innerHTML.includes(item.name)}`);
        });

        console.log(`🎉 Rendered ${this.menuItems.length} menu items successfully`);

        // Debug: Check if items are actually in the DOM
        const renderedCards = menuGrid.querySelectorAll('.menu-item-card');
        console.log(`🔍 DOM Check: ${renderedCards.length} menu cards found in DOM`);
        console.log(`🔍 Menu grid innerHTML length: ${menuGrid.innerHTML.length}`);

        // Force hide loading spinner after rendering
        setTimeout(() => {
            const spinner = document.getElementById('loadingSpinner');
            if (spinner && spinner.style.display !== 'none') {
                console.log('🔧 Force hiding loading spinner after menu render...');
                spinner.style.display = 'none';
            }
        }, 100);
    }

    /**
     * Add item to current order
     */
    addItemToOrder(itemId, itemName, itemPrice, quantity = 1) {
        console.log(`🛒 Adding to order: ${itemName} (${quantity}x) - $${itemPrice}`);

        // Find the full item details
        const menuItem = this.menuItems.find(item => item.id === itemId);
        if (!menuItem) {
            console.error(`❌ Menu item not found: ${itemId}`);
            return;
        }

        // Check if item already exists in order
        const existingItem = this.currentOrder.items.find(orderItem => orderItem.id === itemId);

        if (existingItem) {
            // Update quantity if item already exists
            existingItem.quantity += quantity;
            console.log(`📈 Updated quantity for ${itemName}: ${existingItem.quantity}`);
        } else {
            // Add new item to order
            const orderItem = {
                id: itemId,
                name: itemName,
                price: parseFloat(itemPrice),
                quantity: quantity,
                category: menuItem.category,
                description: menuItem.description
            };
            this.currentOrder.items.push(orderItem);
            console.log(`➕ Added new item to order: ${itemName}`);
        }

        // Update order totals
        this.updateOrderTotals();

        // Update order display
        this.updateOrderDisplay();

        // Show visual feedback
        this.showAddToOrderFeedback(itemName);
    }

    /**
     * Update order totals
     */
    updateOrderTotals() {
        this.currentOrder.subtotal = this.currentOrder.items.reduce((total, item) => {
            return total + (item.price * item.quantity);
        }, 0);

        this.currentOrder.tax = this.currentOrder.subtotal * this.taxRate;
        this.currentOrder.total = this.currentOrder.subtotal + this.currentOrder.tax;

        console.log(`💰 Order totals updated - Subtotal: $${this.currentOrder.subtotal.toFixed(2)}, Tax: $${this.currentOrder.tax.toFixed(2)}, Total: $${this.currentOrder.total.toFixed(2)}`);
    }

    /**
     * Update order display in the UI
     */
    updateOrderDisplay() {
        const orderItemsList = document.getElementById('orderList');
        const orderSubtotal = document.getElementById('subtotal');
        const orderTax = document.getElementById('tax');
        const orderTotal = document.getElementById('total');

        if (orderItemsList) {
            if (this.currentOrder.items.length === 0) {
                orderItemsList.innerHTML = `
                    <div class="empty-order">
                        <i class="fas fa-shopping-cart"></i>
                        <p>No items in order</p>
                        <small>Add items from the menu to get started</small>
                    </div>
                `;
            } else {
                orderItemsList.innerHTML = this.currentOrder.items.map(item => `
                    <div class="order-item">
                        <div class="order-item-info">
                            <div class="order-item-name">${item.name}</div>
                            <div class="order-item-price">$${parseFloat(item.price).toFixed(2)} each</div>
                        </div>
                        <div class="order-item-controls">
                            <button class="quantity-btn" onclick="window.restaurantApp.updateItemQuantity('${item.id}', ${item.quantity - 1})">-</button>
                            <span class="quantity">${item.quantity}</span>
                            <button class="quantity-btn" onclick="window.restaurantApp.updateItemQuantity('${item.id}', ${item.quantity + 1})">+</button>
                            <div class="item-total">$${(parseFloat(item.price) * item.quantity).toFixed(2)}</div>
                        </div>
                    </div>
                `).join('');
            }
        }

        // Update totals with proper null checks
        const subtotal = this.currentOrder.subtotal || 0;
        const tax = this.currentOrder.tax || 0;
        const total = this.currentOrder.total || 0;

        if (orderSubtotal) orderSubtotal.textContent = `$${subtotal.toFixed(2)}`;
        if (orderTax) orderTax.textContent = `$${tax.toFixed(2)}`;
        if (orderTotal) orderTotal.textContent = `$${total.toFixed(2)}`;
    }

    /**
     * Update item quantity in order
     */
    updateItemQuantity(itemId, newQuantity) {
        if (newQuantity <= 0) {
            // Remove item if quantity is 0 or less
            this.currentOrder.items = this.currentOrder.items.filter(item => item.id !== itemId);
            console.log(`🗑️ Removed item from order: ${itemId}`);
        } else {
            // Update quantity
            const item = this.currentOrder.items.find(item => item.id === itemId);
            if (item) {
                item.quantity = newQuantity;
                console.log(`📊 Updated quantity for ${item.name}: ${newQuantity}`);
            }
        }

        this.updateOrderTotals();
        this.updateOrderDisplay();
    }

    /**
     * Show visual feedback when item is added to order
     */
    showAddToOrderFeedback(itemName) {
        // Create a temporary notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            font-weight: bold;
            animation: slideInRight 0.3s ease-out;
        `;
        notification.innerHTML = `✅ ${itemName} added to order!`;

        document.body.appendChild(notification);

        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    /**
     * Update Orders Tab - Initialize all order functionality
     */
    updateOrdersTab() {
        console.log('🛒 Updating Orders Tab...');

        // Initialize search functionality
        this.initializeMenuSearch();

        // Initialize category filters
        this.initializeCategoryFilters();

        // Initialize order actions
        this.initializeOrderActions();

        // Update order display
        this.updateOrderDisplay();

        // Render menu items if not already rendered
        if (!this.menuItems || this.menuItems.length === 0) {
            this.loadMenuItems();
        } else {
            this.renderMenuItems();
        }

        console.log('✅ Orders Tab updated successfully');
    }

    /**
     * Initialize menu search functionality
     */
    initializeMenuSearch() {
        const searchInput = document.getElementById('menuSearch');
        if (searchInput) {
            // Remove existing listener
            const existingHandler = searchInput._searchHandler;
            if (existingHandler) {
                searchInput.removeEventListener('input', existingHandler);
            }

            // Create new handler
            const handler = (e) => {
                const searchTerm = e.target.value.toLowerCase().trim();
                this.filterMenuItems(searchTerm);
            };

            // Store handler reference and add listener
            searchInput._searchHandler = handler;
            searchInput.addEventListener('input', handler);
            console.log('🔍 Menu search initialized');
        }
    }

    /**
     * Initialize category filter buttons
     */
    initializeCategoryFilters() {
        const categoryButtons = document.querySelectorAll('.category-btn');

        // Remove existing listeners from all buttons
        categoryButtons.forEach(button => {
            const existingHandler = button._categoryHandler;
            if (existingHandler) {
                button.removeEventListener('click', existingHandler);
            }
        });

        // Add new listeners to each button
        categoryButtons.forEach(button => {
            const handler = (e) => {
                const category = e.target.dataset.category;
                console.log(`🏷️ Category button clicked: ${category}`);

                // Update active button
                categoryButtons.forEach(btn => btn.classList.remove('active'));
                e.target.classList.add('active');

                // Filter menu items
                this.filterMenuByCategory(category);
            };

            // Store handler reference for cleanup
            button._categoryHandler = handler;
            button.addEventListener('click', handler);
        });

        console.log(`🏷️ Category filters initialized for ${categoryButtons.length} buttons`);
    }

    /**
     * Initialize order action buttons
     */
    initializeOrderActions() {
        // Clear Order button
        const clearOrderBtn = document.getElementById('clearOrderBtn');
        if (clearOrderBtn) {
            clearOrderBtn.removeEventListener('click', this.handleClearOrder);
            this.handleClearOrder = () => {
                if (confirm('Are you sure you want to clear the current order?')) {
                    this.currentOrder.items = [];
                    this.updateOrderTotals();
                    this.updateOrderDisplay();
                    console.log('🗑️ Order cleared');
                }
            };
            clearOrderBtn.addEventListener('click', this.handleClearOrder);
        }

        // Submit Order button
        const submitOrderBtn = document.getElementById('submitOrderBtn');
        if (submitOrderBtn) {
            submitOrderBtn.removeEventListener('click', this.handleSubmitOrder);
            this.handleSubmitOrder = () => {
                this.submitCurrentOrder();
            };
            submitOrderBtn.addEventListener('click', this.handleSubmitOrder);
        }

        // Preview Order button
        const previewOrderBtn = document.getElementById('previewOrderBtn');
        if (previewOrderBtn) {
            previewOrderBtn.removeEventListener('click', this.handlePreviewOrder);
            this.handlePreviewOrder = () => {
                this.showOrderPreview();
            };
            previewOrderBtn.addEventListener('click', this.handlePreviewOrder);
        }

        console.log('⚡ Order actions initialized');
    }

    /**
     * Filter menu items by category
     */
    filterMenuByCategory(category) {
        const menuCards = document.querySelectorAll('.menu-item-card');
        console.log(`🏷️ Filtering ${menuCards.length} menu cards by category: ${category}`);

        let visibleCount = 0;
        menuCards.forEach((card, index) => {
            const itemCategory = card.dataset.category;
            console.log(`Card ${index}: category="${itemCategory}", target="${category}"`);

            if (category === 'all') {
                card.style.display = 'block';
                visibleCount++;
            } else {
                const shouldShow = itemCategory === category;
                card.style.display = shouldShow ? 'block' : 'none';
                if (shouldShow) visibleCount++;
            }
        });

        console.log(`🏷️ Filtered menu by category: ${category} - ${visibleCount} items visible`);
    }

    /**
     * Submit current order
     */
    async submitCurrentOrder() {
        try {
            if (this.currentOrder.items.length === 0) {
                alert('Please add items to the order before submitting.');
                return;
            }

            // Get customer information
            const customerName = document.getElementById('customerName')?.value || 'Walk-in Customer';
            const customerPhone = document.getElementById('customerPhone')?.value || '';
            const tableNumber = document.getElementById('tableNumber')?.value || '';
            const orderType = document.getElementById('orderType')?.value || 'dine_in';

            // Prepare order data
            const orderData = {
                customer_name: customerName,
                customer_phone: customerPhone,
                table_number: tableNumber,
                order_type: orderType,
                items: this.currentOrder.items.map(item => ({
                    id: item.id,
                    name: item.name,
                    price: parseFloat(item.price),
                    quantity: item.quantity,
                    instructions: item.instructions || ''
                })),
                subtotal: this.currentOrder.subtotal,
                tax: this.currentOrder.tax,
                total: this.currentOrder.total
            };

            console.log('📤 Submitting order:', orderData);

            // Submit to backend
            const response = await restaurantAPI.submitOrder(orderData);

            if (response.success) {
                // Add the new order to local orders array
                if (response.order) {
                    // Ensure the new order has a current timestamp for proper sorting
                    response.order.created_at = response.order.created_at || new Date().toISOString();
                    response.order.timestamp = response.order.timestamp || new Date().toISOString();



                    // Add new order at the beginning for immediate visibility
                    this.orders.unshift(response.order);
                }

                // Clear current order
                this.currentOrder.items = [];
                this.updateOrderTotals();
                this.updateOrderDisplay();

                // Reset form
                this.resetOrderForm();

                // Update queue display to show new order
                this.updateQueueDisplay();

                // Show success message
                this.showOrderSuccessMessage(response.order_id);

                console.log('✅ Order submitted successfully');
            } else {
                throw new Error(response.error || 'Failed to submit order');
            }

        } catch (error) {
            console.error('❌ Error submitting order:', error);
            alert(`Failed to submit order: ${error.message}`);
        }
    }

    /**
     * Show order preview modal
     */
    showOrderPreview() {
        if (this.currentOrder.items.length === 0) {
            alert('Please add items to the order before previewing.');
            return;
        }

        // Get customer information
        const customerName = document.getElementById('customerName')?.value || 'Walk-in Customer';
        const customerPhone = document.getElementById('customerPhone')?.value || 'N/A';
        const tableNumber = document.getElementById('tableNumber')?.value || 'N/A';
        const orderType = document.getElementById('orderType')?.value || 'dine_in';

        // Create preview modal content
        const previewContent = `
            <div class="order-preview">
                <h3>Order Preview</h3>

                <div class="customer-info">
                    <h4>Customer Information</h4>
                    <div class="info-row"><strong>Name:</strong> ${customerName}</div>
                    <div class="info-row"><strong>Phone:</strong> ${customerPhone}</div>
                    <div class="info-row"><strong>Table:</strong> ${tableNumber}</div>
                    <div class="info-row"><strong>Type:</strong> ${orderType.replace('_', ' ').toUpperCase()}</div>
                </div>

                <div class="order-items-preview">
                    <h4>Order Items</h4>
                    ${this.currentOrder.items.map(item => `
                        <div class="preview-item">
                            <span>${item.quantity}x ${item.name}</span>
                            <span>$${(parseFloat(item.price) * item.quantity).toFixed(2)}</span>
                        </div>
                    `).join('')}
                </div>

                <div class="order-totals-preview">
                    <div class="total-row"><span>Subtotal:</span> <span>$${this.currentOrder.subtotal.toFixed(2)}</span></div>
                    <div class="total-row"><span>Tax (8%):</span> <span>$${this.currentOrder.tax.toFixed(2)}</span></div>
                    <div class="total-row total"><span><strong>Total:</strong></span> <span><strong>$${this.currentOrder.total.toFixed(2)}</strong></span></div>
                </div>
            </div>
        `;

        // Create modal using utils function
        RestaurantUtils.showModal('Order Preview', previewContent, {
            showFooter: true,
            footerContent: `
                <button class="btn btn-secondary modal-cancel">Cancel</button>
                <button class="btn btn-primary modal-confirm">Submit Order</button>
            `,
            onConfirm: () => {
                this.submitCurrentOrder();
                return true; // Close modal
            }
        });
    }

    /**
     * Update order preview display
     */
    updateOrderPreview() {
        // Get customer information
        const customerName = document.getElementById('customerName')?.value || 'Walk-in Customer';
        const customerPhone = document.getElementById('customerPhone')?.value || 'N/A';
        const tableNumber = document.getElementById('tableNumber')?.value || 'N/A';
        const orderType = document.getElementById('orderType')?.value || 'dine_in';

        // Update preview elements
        const previewElements = {
            customerName: document.querySelector('.preview-customer-name'),
            customerPhone: document.querySelector('.preview-customer-phone'),
            tableNumber: document.querySelector('.preview-table-number'),
            orderType: document.querySelector('.preview-order-type')
        };

        if (previewElements.customerName) previewElements.customerName.textContent = customerName;
        if (previewElements.customerPhone) previewElements.customerPhone.textContent = customerPhone;
        if (previewElements.tableNumber) previewElements.tableNumber.textContent = tableNumber;
        if (previewElements.orderType) previewElements.orderType.textContent = orderType.replace('_', ' ').toUpperCase();

        console.log('👁️ Order preview updated');
    }

    /**
     * Reset order form
     */
    resetOrderForm() {
        const formElements = ['customerName', 'customerPhone', 'tableNumber'];
        formElements.forEach(id => {
            const element = document.getElementById(id);
            if (element) element.value = '';
        });

        // Reset order type to default
        const orderType = document.getElementById('orderType');
        if (orderType) orderType.value = 'dine_in';
    }

    /**
     * Show order success message
     */
    showOrderSuccessMessage(orderId) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 20px 25px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            font-weight: bold;
            max-width: 300px;
        `;
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-check-circle" style="font-size: 24px;"></i>
                <div>
                    <div>Order Submitted Successfully!</div>
                    <div style="font-size: 14px; opacity: 0.9; margin-top: 5px;">Order ID: ${orderId}</div>
                </div>
            </div>
        `;

        document.body.appendChild(notification);

        // Remove notification after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }

    /**
     * Filter menu items by search term
     */
    filterMenuItems(searchTerm) {
        const menuCards = document.querySelectorAll('.menu-item-card');
        const term = searchTerm.toLowerCase();

        menuCards.forEach(card => {
            const name = card.querySelector('.menu-item-name').textContent.toLowerCase();
            const description = card.querySelector('.menu-item-description').textContent.toLowerCase();
            const category = card.querySelector('.menu-item-category').textContent.toLowerCase();

            const matches = name.includes(term) || description.includes(term) || category.includes(term);

            card.style.display = matches ? 'block' : 'none';

            if (matches) {
                card.classList.add('slide-up');
                setTimeout(() => card.classList.remove('slide-up'), 300);
            }
        });
    }

    /**
     * Filter menu items by category
     */
    filterByCategory(category) {
        console.log(`🏷️ filterByCategory called with: ${category}`);
        this.selectedCategory = category;
        this.renderMenuItems();
    }

    /**
     * Add item to current order
     */
    addToOrder(menuItem, quantity = 1, instructions = '') {
        const existingItem = this.currentOrder.items.find(item =>
            item.id === menuItem.id && item.instructions === instructions
        );

        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.currentOrder.items.push({
                id: menuItem.id,
                name: menuItem.name,
                price: menuItem.price,
                quantity: quantity,
                instructions: instructions,
                image: menuItem.image
            });
        }

        this.updateOrderDisplay();
        this.showNotification(`Added ${menuItem.name} to order`, 'success', 2000);
    }

    /**
     * Update order item
     */
    updateOrderItem(orderItem) {
        const index = this.currentOrder.items.findIndex(item =>
            item.id === orderItem.id && item.instructions === orderItem.instructions
        );

        if (index !== -1) {
            this.currentOrder.items[index] = orderItem;
            this.updateOrderDisplay();
        }
    }

    /**
     * Remove item from order
     */
    removeOrderItem(orderItem) {
        this.currentOrder.items = this.currentOrder.items.filter(item =>
            !(item.id === orderItem.id && item.instructions === orderItem.instructions)
        );

        this.updateOrderDisplay();
        this.showNotification(`Removed ${orderItem.name} from order`, 'info', 2000);
    }

    /**
     * Update order display
     */
    updateOrderDisplay() {
        const orderList = document.getElementById('orderList');
        if (!orderList) return;

        // Calculate totals
        this.currentOrder.subtotal = this.currentOrder.items.reduce((sum, item) =>
            sum + (item.price * item.quantity), 0
        );
        this.currentOrder.tax = this.currentOrder.subtotal * this.taxRate;
        this.currentOrder.total = this.currentOrder.subtotal + this.currentOrder.tax;

        // Update order items display
        if (this.currentOrder.items.length === 0) {
            orderList.innerHTML = `
                <div class="empty-order">
                    <i class="fas fa-shopping-cart"></i>
                    <p>No items in order</p>
                </div>
            `;
        } else {
            orderList.innerHTML = '';
            this.currentOrder.items.forEach(item => {
                const orderItemComponent = new RestaurantComponents.OrderItemComponent(
                    item,
                    (updatedItem) => this.updateOrderItem(updatedItem),
                    (removedItem) => this.removeOrderItem(removedItem)
                );
                orderList.appendChild(orderItemComponent.element);
            });
        }



        // Update totals
        document.getElementById('subtotal').textContent = RestaurantUtils.formatCurrency(this.currentOrder.subtotal);
        document.getElementById('tax').textContent = RestaurantUtils.formatCurrency(this.currentOrder.tax);
        document.getElementById('total').textContent = RestaurantUtils.formatCurrency(this.currentOrder.total);

        // Update submit button state
        const submitBtn = document.getElementById('submitOrderBtn');
        if (submitBtn) {
            submitBtn.disabled = this.currentOrder.items.length === 0;
        }
    }



    /**
     * Update customer information
     */
    updateCustomerInfo() {
        this.currentOrder.customer = {
            name: document.getElementById('customerName')?.value || '',
            phone: document.getElementById('customerPhone')?.value || '',
            table: document.getElementById('tableNumber')?.value || '',
            orderType: document.getElementById('orderType')?.value || 'dine_in'
        };
    }

    /**
     * Clear current order
     */
    clearOrder() {
        RestaurantUtils.showModal(
            'Clear Order',
            '<p>Are you sure you want to clear the current order?</p><p>All items will be removed.</p>',
            {
                onConfirm: () => {
                    this.currentOrder.items = [];
                    this.updateOrderDisplay();
                    this.showNotification('Order cleared', 'info');
                    return true;
                }
            }
        );
    }

    /**
     * Preview order before submission
     */
    previewOrder() {
        if (this.currentOrder.items.length === 0) {
            this.showNotification('No items in order', 'warning');
            return;
        }

        const itemsList = this.currentOrder.items.map(item => `
            <div class="preview-item">
                <span class="item-name">${item.quantity}x ${RestaurantUtils.sanitizeHtml(item.name)}</span>
                <span class="item-total">${RestaurantUtils.formatCurrency(item.price * item.quantity)}</span>
                ${item.instructions ? `<div class="item-instructions">${RestaurantUtils.sanitizeHtml(item.instructions)}</div>` : ''}
            </div>
        `).join('');

        const previewContent = `
            <div class="order-preview">
                <div class="customer-preview">
                    <h4>Customer Information</h4>
                    <p><strong>Name:</strong> ${RestaurantUtils.sanitizeHtml(this.currentOrder.customer.name || 'Walk-in Customer')}</p>
                    <p><strong>Phone:</strong> ${RestaurantUtils.sanitizeHtml(this.currentOrder.customer.phone || 'N/A')}</p>
                    <p><strong>Table:</strong> ${RestaurantUtils.sanitizeHtml(this.currentOrder.customer.table || 'N/A')}</p>
                    <p><strong>Type:</strong> ${(this.currentOrder.customer.orderType || 'dine_in').replace('_', ' ').toUpperCase()}</p>
                </div>
                <div class="items-preview">
                    <h4>Order Items</h4>
                    ${itemsList}
                </div>
                <div class="totals-preview">
                    <div class="total-row">
                        <span>Subtotal:</span>
                        <span>${RestaurantUtils.formatCurrency(this.currentOrder.subtotal)}</span>
                    </div>
                    <div class="total-row">
                        <span>Tax (8%):</span>
                        <span>${RestaurantUtils.formatCurrency(this.currentOrder.tax)}</span>
                    </div>
                    <div class="total-row final-total">
                        <span>Total:</span>
                        <span>${RestaurantUtils.formatCurrency(this.currentOrder.total)}</span>
                    </div>
                </div>
            </div>
        `;

        RestaurantUtils.showModal('Order Preview', previewContent, {
            footerContent: `
                <button class="btn btn-secondary modal-cancel">Back to Edit</button>
                <button class="btn btn-primary" id="confirmSubmitOrder">
                    <i class="fas fa-check"></i>
                    Confirm & Submit
                </button>
            `,
            onConfirm: () => {
                this.submitCurrentOrder();
                return true;
            }
        });
    }



    /**
     * Update queue display
     */
    updateQueueDisplay() {
        const queueGrid = document.getElementById('queueGrid');
        if (!queueGrid) return;

        // Filter orders by status
        const activeOrders = this.orders.filter(order =>
            ['pending', 'preparing', 'ready'].includes(order.status)
        );

        // Update stats
        const pendingCount = activeOrders.filter(o => o.status === 'pending').length;
        const preparingCount = activeOrders.filter(o => o.status === 'preparing').length;
        const readyCount = activeOrders.filter(o => o.status === 'ready').length;

        document.getElementById('pendingCount').textContent = pendingCount;
        document.getElementById('cookingCount').textContent = preparingCount;
        document.getElementById('readyCount').textContent = readyCount;

        // Render queue items
        queueGrid.innerHTML = '';

        if (activeOrders.length === 0) {
            queueGrid.innerHTML = `
                <div class="empty-queue">
                    <i class="fas fa-clock"></i>
                    <h3>No Active Orders</h3>
                    <p>All orders are completed or there are no orders yet.</p>
                </div>
            `;
        } else {


            activeOrders
                .sort((a, b) => {
                    // Use timestamp or created_at, whichever is available
                    const dateA = new Date(a.timestamp || a.created_at);
                    const dateB = new Date(b.timestamp || b.created_at);



                    // Primary sort: by date (newest first)
                    const timeDiff = dateB.getTime() - dateA.getTime();

                    // If dates are the same (or very close), sort by order ID (newer IDs typically have higher timestamps)
                    if (Math.abs(timeDiff) < 1000) { // Within 1 second
                        // Extract timestamp from order ID for secondary sorting
                        const getOrderTimestamp = (orderId) => {
                            if (orderId.startsWith('ORD-')) {
                                // Extract YYYYMMDDHHMM from ORD-YYYYMMDDHHMM-XXXX
                                const parts = orderId.split('-');
                                if (parts.length >= 2) {
                                    return parseInt(parts[1]) || 0;
                                }
                            }
                            return 0;
                        };

                        const timestampA = getOrderTimestamp(a.id);
                        const timestampB = getOrderTimestamp(b.id);


                        return timestampB - timestampA; // Newer timestamp first
                    }

                    return timeDiff;
                })
                .forEach(order => {
                    const queueComponent = new RestaurantComponents.QueueOrderComponent(
                        order,
                        (orderId, newStatus, oldStatus) => this.updateOrderStatus(orderId, newStatus)
                    );
                    queueGrid.appendChild(queueComponent.element);
                });


        }
    }

    /**
     * Update order status
     */
    async updateOrderStatus(orderId, newStatus) {
        try {
            await restaurantAPI.updateOrderStatus(orderId, newStatus);

            // Update local order
            const order = this.orders.find(o => o.id === orderId);
            if (order) {
                order.status = newStatus;
            }

            // Update displays
            this.updateQueueDisplay();

            this.showNotification(`Order status updated to ${newStatus}`, 'success', 2000);

        } catch (error) {
            console.error('Error updating order status:', error);
            this.showNotification('Failed to update order status', 'error');
        }
    }

    /**
     * Update menu management display
     */
    updateMenuManagement() {
        const menuTableBody = document.getElementById('menuTableBody');
        if (!menuTableBody) return;

        menuTableBody.innerHTML = '';

        this.menuItems.forEach(item => {
            const row = new RestaurantComponents.MenuManagementRow(
                item,
                (item) => this.editMenuItem(item),
                (itemId) => this.deleteMenuItem(itemId),
                (itemId, status) => this.toggleMenuItemStatus(itemId, status)
            );
            menuTableBody.appendChild(row.element);
        });
    }

    /**
     * Show add menu item modal
     */
    showAddMenuItemModal(editItem = null) {
        const isEdit = !!editItem;
        const title = isEdit ? 'Edit Menu Item' : 'Add Menu Item';

        const modalContent = `
            <form id="menuItemForm" class="menu-item-form">
                <div class="form-row">
                    <div class="form-group">
                        <label for="itemName">Name *</label>
                        <input type="text" id="itemName" required value="${editItem?.name || ''}">
                    </div>
                    <div class="form-group">
                        <label for="itemCategory">Category *</label>
                        <select id="itemCategory" required>
                            <option value="">Select category</option>
                            <option value="appetizers" ${editItem?.category === 'appetizers' ? 'selected' : ''}>Appetizers</option>
                            <option value="mains" ${editItem?.category === 'mains' ? 'selected' : ''}>Main Course</option>
                            <option value="desserts" ${editItem?.category === 'desserts' ? 'selected' : ''}>Desserts</option>
                            <option value="beverages" ${editItem?.category === 'beverages' ? 'selected' : ''}>Beverages</option>
                        </select>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="itemPrice">Price *</label>
                        <input type="number" id="itemPrice" step="0.01" min="0" required value="${editItem?.price || ''}">
                    </div>
                    <div class="form-group">
                        <label for="itemStatus">Status</label>
                        <select id="itemStatus">
                            <option value="true" ${editItem?.is_available !== false ? 'selected' : ''}>Available</option>
                            <option value="false" ${editItem?.is_available === false ? 'selected' : ''}>Unavailable</option>
                        </select>
                    </div>
                </div>
                <div class="form-group">
                    <label for="itemDescription">Description</label>
                    <textarea id="itemDescription" rows="3" placeholder="Item description...">${editItem?.description || ''}</textarea>
                </div>
            </form>
        `;

        RestaurantUtils.showModal(title, modalContent, {
            footerContent: `
                <button class="btn btn-secondary modal-cancel">Cancel</button>
                <button class="btn btn-primary" id="saveMenuItem">
                    <i class="fas fa-save"></i>
                    ${isEdit ? 'Update' : 'Add'} Item
                </button>
            `,
            onConfirm: () => {
                return this.saveMenuItem(editItem);
            }
        });
    }

    /**
     * Save menu item (add or edit)
     */
    async saveMenuItem(editItem = null) {
        try {
            const form = document.getElementById('menuItemForm');
            const formData = new FormData(form);

            const itemData = {
                name: document.getElementById('itemName').value.trim(),
                category: document.getElementById('itemCategory').value,
                price: parseFloat(document.getElementById('itemPrice').value),
                description: document.getElementById('itemDescription').value.trim(),
                is_available: document.getElementById('itemStatus').value === 'true'
            };

            // Validation
            if (!itemData.name || !itemData.category || !itemData.price) {
                this.showNotification('Please fill in all required fields', 'warning');
                return false;
            }

            if (itemData.price <= 0) {
                this.showNotification('Price must be greater than 0', 'warning');
                return false;
            }

            let savedItem;

            if (editItem) {
                // Update existing item
                savedItem = await restaurantAPI.updateMenuItem(editItem.id, itemData);

                // Update local data
                const index = this.menuItems.findIndex(item => item.id === editItem.id);
                if (index !== -1) {
                    this.menuItems[index] = savedItem;
                }

                this.showNotification('Menu item updated successfully', 'success');
            } else {
                // Add new item
                savedItem = await restaurantAPI.addMenuItem(itemData);

                // Add to local data
                this.menuItems.push(savedItem);

                this.showNotification('Menu item added successfully', 'success');
            }

            // Update displays
            this.renderMenuItems();
            this.updateMenuManagement();

            return true; // Close modal

        } catch (error) {
            console.error('Error saving menu item:', error);
            this.showNotification('Failed to save menu item', 'error');
            return false; // Keep modal open
        }
    }

    /**
     * Edit menu item
     */
    editMenuItem(item) {
        this.showAddMenuItemModal(item);
    }

    /**
     * Delete menu item
     */
    async deleteMenuItem(itemId) {
        try {
            await restaurantAPI.deleteMenuItem(itemId);

            // Remove from local data
            this.menuItems = this.menuItems.filter(item => item.id !== itemId);

            // Update displays
            this.renderMenuItems();
            this.updateMenuManagement();

            this.showNotification('Menu item deleted successfully', 'success');

        } catch (error) {
            console.error('Error deleting menu item:', error);
            this.showNotification('Failed to delete menu item', 'error');
        }
    }

    /**
     * Toggle menu item status
     */
    async toggleMenuItemStatus(itemId, newStatus) {
        try {
            await restaurantAPI.updateMenuItem(itemId, { is_available: newStatus });

            // Update local data
            const item = this.menuItems.find(item => item.id === itemId);
            if (item) {
                item.is_available = newStatus;
            }

            // Update menu display
            this.renderMenuItems();

        } catch (error) {
            console.error('Error updating menu item status:', error);
            this.showNotification('Failed to update item status', 'error');
        }
    }

    /**
     * Update reports data with enhanced visualization
     */
    async updateReportsData(period = 'today') {
        try {
            console.log(`📊 Loading sales data for period: ${period}`);
            this.showLoading('Loading reports...');

            const salesData = await restaurantAPI.getSalesData({ period });
            console.log('📈 Sales data received:', salesData);

            // Get period label
            const periodText = {
                'today': 'Today',
                'week': 'This Week',
                'month': 'This Month'
            };

            this.displaySalesData(salesData, periodText[period] || period);
            this.hideLoading();

        } catch (error) {
            console.error('Error loading reports data:', error);
            this.hideLoading();
            this.showNotification('Failed to load reports data', 'error');

            // Show error state
            this.showReportsErrorState();
        }
    }

    /**
     * Update popular items display
     */
    updatePopularItems(popularItems) {
        const popularItemsList = document.getElementById('popularItems');
        if (!popularItemsList) return;

        if (!popularItems || popularItems.length === 0) {
            popularItemsList.innerHTML = '<div class="no-data">No sales data available</div>';
            return;
        }

        popularItemsList.innerHTML = popularItems
            .map((item, index) => `
                <div class="popular-item">
                    <div class="popular-item-rank">${index + 1}</div>
                    <div class="popular-item-info">
                        <div class="popular-item-name">${RestaurantUtils.escapeHtml(item.name)}</div>
                        <div class="popular-item-stats">${item.count} sold • ${item.percentage}% of total</div>
                    </div>
                </div>
            `)
            .join('');
    }

    /**
     * Update time breakdown chart
     */
    updateTimeBreakdown(timeBreakdown, period) {
        const timeBreakdownContainer = document.getElementById('timeBreakdown');
        if (!timeBreakdownContainer) return;

        if (!timeBreakdown || timeBreakdown.length === 0) {
            timeBreakdownContainer.innerHTML = '<div class="no-data">No time breakdown data available</div>';
            return;
        }

        // Find maximum sales value for chart scaling
        const maxSales = Math.max(...timeBreakdown.map(([_, data]) => data.sales));

        timeBreakdownContainer.innerHTML = timeBreakdown
            .map(([timeKey, data]) => {
                const percentage = maxSales > 0 ? (data.sales / maxSales) * 100 : 0;
                return `
                    <div class="time-breakdown-item">
                        <div class="time-breakdown-label">${timeKey}</div>
                        <div class="time-breakdown-bar">
                            <div class="time-breakdown-fill" style="width: ${percentage}%"></div>
                        </div>
                        <div class="time-breakdown-value">$${data.sales.toFixed(2)}</div>
                    </div>
                `;
            })
            .join('');
    }

    /**
     * Show error state for reports
     */
    showReportsErrorState() {
        // Reset all values to default
        document.getElementById('totalSales').textContent = '$0.00';
        document.getElementById('ordersCount').textContent = '0';
        document.getElementById('avgOrder').textContent = '$0.00';
        document.getElementById('totalItemsSold').textContent = '0';

        // Show error messages
        const popularItemsList = document.getElementById('popularItems');
        if (popularItemsList) {
            popularItemsList.innerHTML = '<div class="no-data">Error loading data</div>';
        }

        const timeBreakdownContainer = document.getElementById('timeBreakdown');
        if (timeBreakdownContainer) {
            timeBreakdownContainer.innerHTML = '<div class="no-data">Error loading data</div>';
        }
    }

    /**
     * Handle period change
     */
    handlePeriodChange(period) {
        const customDateRange = document.getElementById('customDateRange');

        if (period === 'custom') {
            customDateRange.style.display = 'flex';

            // Set default dates
            const today = new Date();
            const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);

            document.getElementById('startDate').valueAsDate = weekAgo;
            document.getElementById('endDate').valueAsDate = today;
        } else {
            customDateRange.style.display = 'none';
            this.updateReportsData(period);
        }
    }

    /**
     * Apply custom date range
     */
    async applyCustomDateRange() {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;

        if (!startDate || !endDate) {
            this.showNotification('Please select both start and end dates', 'warning');
            return;
        }

        if (new Date(startDate) > new Date(endDate)) {
            this.showNotification('Start date must be before end date', 'warning');
            return;
        }

        try {
            this.showLoading('Loading custom date range...');

            // Create custom period object for backend
            const customPeriod = {
                type: 'custom',
                startDate: startDate,
                endDate: endDate
            };

            const salesData = await restaurantAPI.getSalesData(customPeriod);

            // Update displays with custom data
            this.displaySalesData(salesData, `${startDate} to ${endDate}`);

            this.hideLoading();
            this.showNotification('Custom date range applied successfully', 'success');

        } catch (error) {
            console.error('Error applying custom date range:', error);
            this.hideLoading();
            this.showNotification('Failed to load custom date range', 'error');
        }
    }

    /**
     * Refresh reports
     */
    async refreshReports() {
        const period = document.getElementById('reportPeriod')?.value || 'today';
        const refreshBtn = document.getElementById('refreshReportBtn');

        // Add spinning animation
        const icon = refreshBtn.querySelector('i');
        icon.style.animation = 'spin 1s linear infinite';

        try {
            if (period === 'custom') {
                await this.applyCustomDateRange();
            } else {
                await this.updateReportsData(period);
            }

            this.showNotification('Reports refreshed successfully', 'success');

        } catch (error) {
            console.error('Error refreshing reports:', error);
            this.showNotification('Failed to refresh reports', 'error');
        } finally {
            // Remove spinning animation
            setTimeout(() => {
                icon.style.animation = '';
            }, 1000);
        }
    }

    /**
     * Display sales data (consolidated method)
     */
    displaySalesData(salesData, periodLabel) {
        // Update metric cards
        document.getElementById('totalSales').textContent = RestaurantUtils.formatCurrency(salesData.totalSales || 0);
        document.getElementById('ordersCount').textContent = salesData.ordersCount || 0;
        document.getElementById('avgOrder').textContent = RestaurantUtils.formatCurrency(salesData.avgOrderValue || 0);
        document.getElementById('totalItemsSold').textContent = salesData.totalItemsSold || 0;

        // Update period label
        const reportPeriodLabel = document.getElementById('reportPeriodLabel');
        if (reportPeriodLabel) {
            reportPeriodLabel.textContent = periodLabel;
        }

        // Update popular items and time breakdown
        this.updatePopularItems(salesData.popularItems || []);
        this.updateTimeBreakdown(salesData.timeBreakdown || [], salesData.period || 'custom');

        // Update time breakdown title
        const timeBreakdownTitle = document.getElementById('timeBreakdownTitle');
        if (timeBreakdownTitle) {
            const titleText = salesData.period === 'custom' ? 'Sales Breakdown' : {
                'today': 'Sales by Hour',
                'week': 'Sales by Day',
                'month': 'Sales by Date'
            }[salesData.period] || 'Sales Breakdown';
            timeBreakdownTitle.textContent = titleText;
        }
    }

    /**
     * Export report with enhanced options
     */
    async exportReport() {
        try {
            const period = document.getElementById('reportPeriod')?.value || 'today';

            let exportOptions = { period };

            // Handle custom date range
            if (period === 'custom') {
                const startDate = document.getElementById('startDate').value;
                const endDate = document.getElementById('endDate').value;

                if (!startDate || !endDate) {
                    this.showNotification('Please select date range first', 'warning');
                    return;
                }

                exportOptions = {
                    period: 'custom',
                    startDate,
                    endDate
                };
            }

            this.showLoading('Exporting report...');

            const result = await restaurantAPI.exportData('csv', exportOptions);

            this.hideLoading();
            this.showNotification(`Report exported: ${result.filename}`, 'success');

        } catch (error) {
            console.error('Error exporting report:', error);
            this.hideLoading();
            this.showNotification('Failed to export report', 'error');
        }
    }

    /**
     * Show settings modal
     */
    showSettings() {
        const settingsContent = `
            <div class="settings-content">
                <div class="settings-grid">
                    <div class="settings-section">
                        <div class="settings-section-header">
                            <i class="fas fa-store"></i>
                            <h4>Restaurant Information</h4>
                        </div>
                        <div class="settings-section-body">
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="restaurantName">Restaurant Name</label>
                                    <input type="text" id="restaurantName" value="My Restaurant" placeholder="Enter restaurant name">
                                </div>
                                <div class="form-group">
                                    <label for="restaurantPhone">Phone Number</label>
                                    <input type="tel" id="restaurantPhone" value="(555) 123-4567" placeholder="(555) 123-4567">
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="restaurantAddress">Address</label>
                                <textarea id="restaurantAddress" rows="3" placeholder="Enter full address">123 Main St, City, State 12345</textarea>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="restaurantEmail">Email</label>
                                    <input type="email" id="restaurantEmail" value="info@myrestaurant.com" placeholder="restaurant@example.com">
                                </div>
                                <div class="form-group">
                                    <label for="restaurantWebsite">Website</label>
                                    <input type="url" id="restaurantWebsite" value="https://myrestaurant.com" placeholder="https://example.com">
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="settings-section">
                        <div class="settings-section-header">
                            <i class="fas fa-cog"></i>
                            <h4>Order Settings</h4>
                        </div>
                        <div class="settings-section-body">
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="taxRate">Tax Rate (%)</label>
                                    <input type="number" id="taxRate" step="0.01" min="0" max="100" value="${this.taxRate * 100}" placeholder="8.25">
                                </div>
                                <div class="form-group">
                                    <label for="serviceCharge">Service Charge (%)</label>
                                    <input type="number" id="serviceCharge" step="0.01" min="0" max="100" value="0" placeholder="0">
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="currency">Currency</label>
                                <select id="currency">
                                    <option value="USD" selected>USD ($)</option>
                                    <option value="EUR">EUR (€)</option>
                                    <option value="GBP">GBP (£)</option>
                                    <option value="CAD">CAD (C$)</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div class="settings-section">
                        <div class="settings-section-header">
                            <i class="fas fa-bell"></i>
                            <h4>Notifications & Display</h4>
                        </div>
                        <div class="settings-section-body">
                            <div class="settings-toggle-group">
                                <div class="settings-toggle">
                                    <label class="toggle-label">
                                        <input type="checkbox" id="enableSounds">
                                        <span class="toggle-slider"></span>
                                        <span class="toggle-text">Enable notification sounds</span>
                                    </label>
                                    <p class="toggle-description">Play sounds for new orders and updates</p>
                                </div>
                                <div class="settings-toggle">
                                    <label class="toggle-label">
                                        <input type="checkbox" id="autoRefresh" checked>
                                        <span class="toggle-slider"></span>
                                        <span class="toggle-text">Auto-refresh queue display</span>
                                    </label>
                                    <p class="toggle-description">Automatically update order queue every 30 seconds</p>
                                </div>
                                <div class="settings-toggle">
                                    <label class="toggle-label">
                                        <input type="checkbox" id="showOrderNumbers" checked>
                                        <span class="toggle-slider"></span>
                                        <span class="toggle-text">Show order numbers</span>
                                    </label>
                                    <p class="toggle-description">Display order numbers on receipts and queue</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="settings-section">
                        <div class="settings-section-header">
                            <i class="fas fa-print"></i>
                            <h4>Receipt Settings</h4>
                        </div>
                        <div class="settings-section-body">
                            <div class="form-group">
                                <label for="receiptFooter">Receipt Footer Message</label>
                                <textarea id="receiptFooter" rows="2" placeholder="Thank you for your business!">Thank you for dining with us!</textarea>
                            </div>
                            <div class="settings-toggle-group">
                                <div class="settings-toggle">
                                    <label class="toggle-label">
                                        <input type="checkbox" id="printAutomatically">
                                        <span class="toggle-slider"></span>
                                        <span class="toggle-text">Print receipts automatically</span>
                                    </label>
                                    <p class="toggle-description">Automatically print receipt when order is submitted</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        RestaurantUtils.showModal('Settings', settingsContent, {
            size: 'lg', // Use large modal for settings
            footerContent: `
                <button class="btn btn-secondary modal-cancel">Cancel</button>
                <button class="btn btn-primary" id="saveSettings">
                    <i class="fas fa-save"></i>
                    Save Settings
                </button>
            `,
            onConfirm: () => {
                this.saveSettings();
                return true;
            }
        });
    }

    /**
     * Save settings
     */
    saveSettings() {
        const newTaxRate = parseFloat(document.getElementById('taxRate').value) / 100;

        if (newTaxRate !== this.taxRate) {
            this.taxRate = newTaxRate;
            this.updateOrderDisplay(); // Recalculate totals
        }

        this.showNotification('Settings saved successfully', 'success');
    }

    /**
     * Show help modal
     */
    showHelp() {
        const helpContent = `
            <div class="help-content">
                <div class="help-section">
                    <h4>Getting Started</h4>
                    <ul>
                        <li>Use the <strong>Orders</strong> tab to take new orders</li>
                        <li>Browse menu items and click to add them to the current order</li>
                        <li>Fill in customer information and submit the order</li>
                        <li>Monitor order progress in the <strong>Queue</strong> tab</li>
                    </ul>
                </div>
                <div class="help-section">
                    <h4>Keyboard Shortcuts</h4>
                    <ul>
                        <li><kbd>Ctrl + 1</kbd> - Switch to Orders tab</li>
                        <li><kbd>Ctrl + 2</kbd> - Switch to Menu Management tab</li>
                        <li><kbd>Ctrl + 3</kbd> - Switch to Queue tab</li>
                        <li><kbd>Ctrl + 4</kbd> - Switch to Reports tab</li>
                        <li><kbd>Ctrl + Enter</kbd> - Submit current order</li>
                        <li><kbd>Ctrl + Delete</kbd> - Clear current order</li>
                    </ul>
                </div>
                <div class="help-section">
                    <h4>Tips</h4>
                    <ul>
                        <li>Use the search box to quickly find menu items</li>
                        <li>Double-click on order items to edit quantity</li>
                        <li>Right-click on queue items for quick actions</li>
                        <li>Export reports regularly for business insights</li>
                    </ul>
                </div>
            </div>
        `;

        RestaurantUtils.showModal('Help & Tips', helpContent, {
            size: 'lg', // Use large modal for help content
            showFooter: false
        });
    }

    /**
     * Handle keyboard shortcuts
     */
    handleKeyboardShortcuts(e) {
        if (!e.ctrlKey) return;

        switch (e.key) {
            case '1':
                e.preventDefault();
                this.switchTab('orders');
                break;
            case '2':
                e.preventDefault();
                this.switchTab('menu');
                break;
            case '3':
                e.preventDefault();
                this.switchTab('queue');
                break;
            case '4':
                e.preventDefault();
                this.switchTab('reports');
                break;
            case 'Enter':
                e.preventDefault();
                if (this.currentTab === 'orders') {
                    this.submitCurrentOrder();
                }
                break;
            case 'Delete':
                e.preventDefault();
                if (this.currentTab === 'orders') {
                    this.clearOrder();
                }
                break;
        }
    }

    /**
     * Initialize footer functionality
     */
    initializeFooter() {
        // Update current year
        const currentYear = new Date().getFullYear();
        document.getElementById('currentYear').textContent = currentYear;
        document.getElementById('copyrightYear').textContent = currentYear;

        // Start real-time clock
        this.updateFooterTime();
        setInterval(() => this.updateFooterTime(), 1000);

        // Add footer link handlers
        this.setupFooterHandlers();
    }

    /**
     * Update footer time display
     */
    updateFooterTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit'
        });

        const timeElement = document.getElementById('currentTime');
        if (timeElement) {
            timeElement.textContent = timeString;
        }
    }

    /**
     * Setup footer link handlers
     */
    setupFooterHandlers() {
        // Make footer functions globally available
        window.showHelp = () => this.showHelp();
        window.showSettings = () => this.showSettings();
        window.exportData = () => this.exportReport();
        window.showAbout = () => this.showAboutModal();
    }

    /**
     * Show about modal
     */
    showAboutModal() {
        const aboutContent = `
            <div class="about-modal">
                <div class="about-header">
                    <i class="fas fa-utensils"></i>
                    <h2>Restaurant Management System</h2>
                    <span class="version-badge">v1.0.0</span>
                </div>

                <div class="about-content">
                    <div class="about-section">
                        <h3><i class="fas fa-info-circle"></i> About</h3>
                        <p>A comprehensive restaurant order management solution designed for modern food service establishments. Built with cutting-edge web technologies to provide a seamless, efficient, and reliable experience.</p>
                    </div>

                    <div class="about-section">
                        <h3><i class="fas fa-star"></i> Key Features</h3>
                        <ul class="feature-list">
                            <li><i class="fas fa-check"></i> Real-time order management</li>
                            <li><i class="fas fa-check"></i> Dynamic menu administration</li>
                            <li><i class="fas fa-check"></i> Comprehensive sales analytics</li>
                            <li><i class="fas fa-check"></i> Multi-device responsive design</li>
                            <li><i class="fas fa-check"></i> Professional receipt generation</li>
                            <li><i class="fas fa-check"></i> Data export capabilities</li>
                        </ul>
                    </div>

                    <div class="about-section">
                        <h3><i class="fas fa-code"></i> Technology Stack</h3>
                        <div class="tech-grid">
                            <div class="tech-item">
                                <i class="fab fa-html5"></i>
                                <span>HTML5</span>
                            </div>
                            <div class="tech-item">
                                <i class="fab fa-css3-alt"></i>
                                <span>CSS3</span>
                            </div>
                            <div class="tech-item">
                                <i class="fab fa-js"></i>
                                <span>JavaScript ES6+</span>
                            </div>
                            <div class="tech-item">
                                <i class="fab fa-python"></i>
                                <span>Python Backend</span>
                            </div>
                        </div>
                    </div>

                    <div class="about-section">
                        <h3><i class="fas fa-chart-line"></i> System Status</h3>
                        <div class="status-grid">
                            <div class="status-item">
                                <span class="status-label">System Status:</span>
                                <span class="status-value online">
                                    <i class="fas fa-circle"></i> Online
                                </span>
                            </div>
                            <div class="status-item">
                                <span class="status-label">Menu Items:</span>
                                <span class="status-value">${this.menuItems.length}</span>
                            </div>
                            <div class="status-item">
                                <span class="status-label">Total Orders:</span>
                                <span class="status-value">${this.orders.length}</span>
                            </div>
                            <div class="status-item">
                                <span class="status-label">Build Date:</span>
                                <span class="status-value">${new Date().toLocaleDateString()}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="about-footer">
                    <p>&copy; ${new Date().getFullYear()} Restaurant Management System. All rights reserved.</p>
                </div>
            </div>
        `;

        RestaurantUtils.showModal('About Restaurant Management System', aboutContent, {
            size: 'lg', // Use large modal for about dialog
            showFooter: false // No footer needed for about dialog
        });
    }

    /**
     * Utility methods
     */
    showLoading(message) {
        RestaurantUtils.showLoading(message);
    }

    hideLoading() {
        RestaurantUtils.hideLoading();
    }

    showNotification(message, type = 'info', duration = 5000) {
        new RestaurantComponents.NotificationComponent(message, type, duration);
    }
}

// Export RestaurantApp class for manual initialization
console.log('🔧 APP: RestaurantApp class defined and exported');
window.RestaurantApp = RestaurantApp;
console.log('✅ APP: RestaurantApp loaded and ready for initialization');

// Note: Initialization is handled by script loading tracker in index.html