// Restaurant Management System - API Communication Layer

/**
 * API Client for communicating with Python backend via webview
 */
class RestaurantAPI {
    constructor() {
        this.eventEmitter = new RestaurantUtils.EventEmitter();
        this.requestId = 0;
        this.pendingRequests = new Map();
        this.isReady = false;

        // Initialize Python communication bridge
        this.initializeBridge();
    }

    /**
     * Initialize communication bridge with Python backend
     */
    initializeBridge() {
        console.log('🔗 API: Initializing communication bridge...');

        // Check if pywebview is available with retry mechanism
        this.checkPyWebViewAvailability();
    }

    /**
     * Check for pywebview availability with retry mechanism
     */
    checkPyWebViewAvailability(retryCount = 0) {
        const maxRetries = 10;
        const retryDelay = 100; // ms

        console.log(`🔍 API: Checking pywebview availability (attempt ${retryCount + 1}/${maxRetries + 1})...`);
        console.log('🌐 API: window.pywebview type:', typeof window.pywebview);
        console.log('🌐 API: global pywebview type:', typeof pywebview);

        if (typeof pywebview !== 'undefined' && pywebview.api) {
            this.usePyWebview = true;
            console.log('✅ API: Using pywebview bridge for API communication');
            console.log('🔍 API: pywebview.api methods:', Object.keys(pywebview.api || {}));
            console.log('🔍 API: pywebview.api object:', pywebview.api);
            this.notifyReady();
        } else if (retryCount < maxRetries) {
            console.log(`⏳ API: pywebview not ready yet, retrying in ${retryDelay}ms...`);
            setTimeout(() => {
                this.checkPyWebViewAvailability(retryCount + 1);
            }, retryDelay);
            return;
        } else {
            this.usePyWebview = false;
            console.log('⚠️ API: pywebview not available after retries, using mock API for development');
            this.initializeMockData();
            this.notifyReady();
        }
    }

    /**
     * Notify that API is ready for use
     */
    notifyReady() {
        this.isReady = true;
        console.log('🎉 API: RestaurantAPI is now ready for use');

        // Emit ready event
        window.dispatchEvent(new CustomEvent('restaurantapi-ready', {
            detail: { api: this }
        }));

        // Listen for responses from Python
        window.addEventListener('python-response', (event) => {
            this.handlePythonResponse(event.detail);
        });
    }

    /**
     * Initialize mock data for development
     */
    initializeMockData() {
        this.mockData = {
            menuItems: [
                {
                    id: 'item_1',
                    name: 'Classic Burger',
                    category: 'mains',
                    price: 12.99,
                    description: 'Juicy beef patty with lettuce, tomato, and cheese',
                    is_available: true,
                    image: null
                },
                {
                    id: 'item_2',
                    name: 'Caesar Salad',
                    category: 'appetizers',
                    price: 8.99,
                    description: 'Fresh romaine lettuce with Caesar dressing and croutons',
                    is_available: true,
                    image: null
                },
                {
                    id: 'item_3',
                    name: 'Chocolate Cake',
                    category: 'desserts',
                    price: 6.99,
                    description: 'Rich chocolate cake with chocolate frosting',
                    is_available: true,
                    image: null
                },
                {
                    id: 'item_4',
                    name: 'Coffee',
                    category: 'beverages',
                    price: 2.99,
                    description: 'Freshly brewed coffee',
                    is_available: true,
                    image: null
                },
                {
                    id: 'item_5',
                    name: 'Margherita Pizza',
                    category: 'mains',
                    price: 14.99,
                    description: 'Traditional pizza with tomato sauce, mozzarella, and basil',
                    is_available: true,
                    image: null
                }
            ],
            orders: [],
            salesData: {
                totalSales: 0,
                ordersCount: 0,
                avgOrderValue: 0,
                popularItems: []
            }
        };
    }

    /**
     * Make API request to Python backend
     * @param {string} method - API method name
     * @param {Object} data - Request data
     * @returns {Promise} Request promise
     */
    async request(method, data = {}) {
        const requestId = ++this.requestId;

        return new Promise((resolve, reject) => {
            // Store request for response handling
            this.pendingRequests.set(requestId, { resolve, reject, method });

            if (this.usePyWebview) {
                // Send request to Python via pywebview
                try {
                    pywebview.api.handleRequest({
                        id: requestId,
                        method: method,
                        data: data
                    });
                } catch (error) {
                    console.error('Error sending request to Python:', error);
                    this.pendingRequests.delete(requestId);
                    reject(error);
                }
            } else {
                // Handle with mock data
                setTimeout(() => {
                    this.handleMockRequest(requestId, method, data);
                }, 100); // Simulate network delay
            }
        });
    }

    /**
     * Handle response from Python backend
     * @param {Object} response - Response data
     */
    handlePythonResponse(response) {
        const { id, success, data, error } = response;
        const request = this.pendingRequests.get(id);

        if (!request) {
            console.warn('Received response for unknown request:', id);
            return;
        }

        this.pendingRequests.delete(id);

        if (success) {
            request.resolve(data);
        } else {
            request.reject(new Error(error || 'Unknown error'));
        }
    }

    /**
     * Handle mock API requests for development
     * @param {number} requestId - Request ID
     * @param {string} method - API method
     * @param {Object} data - Request data
     */
    handleMockRequest(requestId, method, data) {
        const request = this.pendingRequests.get(requestId);
        if (!request) return;

        this.pendingRequests.delete(requestId);

        try {
            let result;

            switch (method) {
                case 'getMenuItems':
                    result = this.mockData.menuItems;
                    break;

                case 'addMenuItem':
                    const newItem = {
                        id: `item_${Date.now()}`,
                        ...data,
                        is_available: true
                    };
                    this.mockData.menuItems.push(newItem);
                    result = newItem;
                    break;

                case 'updateMenuItem':
                    const itemIndex = this.mockData.menuItems.findIndex(item => item.id === data.id);
                    if (itemIndex !== -1) {
                        this.mockData.menuItems[itemIndex] = { ...this.mockData.menuItems[itemIndex], ...data };
                        result = this.mockData.menuItems[itemIndex];
                    } else {
                        throw new Error('Menu item not found');
                    }
                    break;

                case 'deleteMenuItem':
                    const deleteIndex = this.mockData.menuItems.findIndex(item => item.id === data.id);
                    if (deleteIndex !== -1) {
                        this.mockData.menuItems.splice(deleteIndex, 1);
                        result = { success: true };
                    } else {
                        throw new Error('Menu item not found');
                    }
                    break;

                case 'submitOrder':
                    const order = {
                        id: `order_${Date.now()}`,
                        ...data,
                        status: 'pending',
                        created_at: new Date().toISOString(),
                        total: data.total || data.items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
                    };
                    this.mockData.orders.push(order);
                    this.updateSalesData();
                    result = { success: true, order_id: order.id, order: order };
                    break;

                case 'getOrders':
                    result = this.mockData.orders;
                    break;

                case 'updateOrderStatus':
                    const orderIndex = this.mockData.orders.findIndex(order => order.id === data.orderId);
                    if (orderIndex !== -1) {
                        this.mockData.orders[orderIndex].status = data.status;
                        result = this.mockData.orders[orderIndex];
                    } else {
                        throw new Error('Order not found');
                    }
                    break;

                case 'getSalesData':
                    result = this.mockData.salesData;
                    break;

                case 'exportData':
                    result = { success: true, message: 'Data exported successfully' };
                    break;

                default:
                    throw new Error(`Unknown API method: ${method}`);
            }

            request.resolve(result);
        } catch (error) {
            request.reject(error);
        }
    }

    /**
     * Update sales data for mock API
     */
    updateSalesData() {
        const orders = this.mockData.orders;
        const completedOrders = orders.filter(order => order.status === 'completed');

        this.mockData.salesData = {
            totalSales: completedOrders.reduce((sum, order) => sum + order.total, 0),
            ordersCount: completedOrders.length,
            avgOrderValue: completedOrders.length > 0 ?
                completedOrders.reduce((sum, order) => sum + order.total, 0) / completedOrders.length : 0,
            popularItems: this.calculatePopularItems(completedOrders)
        };
    }

    /**
     * Calculate popular items from completed orders
     * @param {Array} orders - Completed orders
     * @returns {Array} Popular items list
     */
    calculatePopularItems(orders) {
        const itemCounts = {};

        orders.forEach(order => {
            order.items.forEach(item => {
                if (itemCounts[item.name]) {
                    itemCounts[item.name] += item.quantity;
                } else {
                    itemCounts[item.name] = item.quantity;
                }
            });
        });

        return Object.entries(itemCounts)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 5)
            .map(([name, count]) => ({ name, count }));
    }

    // API Methods

    /**
     * Get all menu items
     * @returns {Promise<Array>} Menu items array
     */
    async getMenuItems() {
        return this.request('getMenuItems');
    }

    /**
     * Add new menu item
     * @param {Object} item - Menu item data
     * @returns {Promise<Object>} Created menu item
     */
    async addMenuItem(item) {
        return this.request('addMenuItem', item);
    }

    /**
     * Update menu item
     * @param {string} id - Item ID
     * @param {Object} updates - Item updates
     * @returns {Promise<Object>} Updated menu item
     */
    async updateMenuItem(id, updates) {
        return this.request('updateMenuItem', { id, ...updates });
    }

    /**
     * Delete menu item
     * @param {string} id - Item ID
     * @returns {Promise<Object>} Success response
     */
    async deleteMenuItem(id) {
        return this.request('deleteMenuItem', { id });
    }

    /**
     * Submit new order
     * @param {Object} order - Order data
     * @returns {Promise<Object>} Created order
     */
    async submitOrder(order) {
        return this.request('submitOrder', order);
    }

    /**
     * Get all orders
     * @param {Object} filters - Optional filters
     * @returns {Promise<Array>} Orders array
     */
    async getOrders(filters = {}) {
        return this.request('getOrders', filters);
    }

    /**
     * Update order status
     * @param {string} orderId - Order ID
     * @param {string} status - New status
     * @returns {Promise<Object>} Updated order
     */
    async updateOrderStatus(orderId, status) {
        return this.request('updateOrderStatus', { orderId, status });
    }

    /**
     * Get sales data and reports
     * @param {Object} filters - Date filters
     * @returns {Promise<Object>} Sales data
     */
    async getSalesData(filters = {}) {
        return this.request('getSalesData', filters);
    }

    /**
     * Export data
     * @param {string} type - Export type (csv, json, etc.)
     * @param {Object} options - Export options
     * @returns {Promise<Object>} Export result
     */
    async exportData(type, options = {}) {
        return this.request('exportData', { type, options });
    }

    /**
     * Get application settings
     * @returns {Promise<Object>} Settings object
     */
    async getSettings() {
        return this.request('getSettings');
    }

    /**
     * Update application settings
     * @param {Object} settings - Settings to update
     * @returns {Promise<Object>} Updated settings
     */
    async updateSettings(settings) {
        return this.request('updateSettings', settings);
    }

    /**
     * Backup data
     * @param {Object} options - Backup options
     * @returns {Promise<Object>} Backup result
     */
    async backupData(options = {}) {
        return this.request('backupData', options);
    }

    /**
     * Restore data from backup
     * @param {string} backupFile - Backup file path
     * @returns {Promise<Object>} Restore result
     */
    async restoreData(backupFile) {
        return this.request('restoreData', { backupFile });
    }

    /**
     * Generate receipt
     * @param {string} orderId - Order ID
     * @param {Object} options - Receipt options
     * @returns {Promise<Object>} Receipt data
     */
    async generateReceipt(orderId, options = {}) {
        return this.request('generateReceipt', { orderId, options });
    }

    /**
     * Subscribe to real-time events
     * @param {string} eventType - Event type to subscribe to
     * @param {Function} callback - Event callback
     */
    on(eventType, callback) {
        this.eventEmitter.on(eventType, callback);
    }

    /**
     * Unsubscribe from real-time events
     * @param {string} eventType - Event type
     * @param {Function} callback - Event callback
     */
    off(eventType, callback) {
        this.eventEmitter.off(eventType, callback);
    }

    /**
     * Emit event (for internal use)
     * @param {string} eventType - Event type
     * @param {*} data - Event data
     */
    emit(eventType, data) {
        this.eventEmitter.emit(eventType, data);
    }
}

// Create global API instance
console.log('🔧 API: Creating global RestaurantAPI instance...');
window.restaurantAPI = new RestaurantAPI();
window.RestaurantAPI = RestaurantAPI; // Also expose the class
console.log('✅ API: RestaurantAPI loaded and global instance created');

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RestaurantAPI;
}