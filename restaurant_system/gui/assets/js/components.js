// Restaurant Management System - UI Components

/**
 * Menu Item Card Component
 */
class MenuItemCard {
    constructor(item, onAddToOrder) {
        this.item = item;
        this.onAddToOrder = onAddToOrder;
        this.element = this.createElement();
    }

    createElement() {
        const { formatCurrency, createElement, sanitizeHtml } = RestaurantUtils;

        const card = createElement('div', {
            className: `menu-item-card ${!this.item.is_available ? 'unavailable' : ''}`,
            'data-item-id': this.item.id,
            'data-category': this.item.category
        });

        // Add click handler for available items
        if (this.item.is_available) {
            card.addEventListener('click', (e) => {
                if (!e.target.closest('.quick-add-btn')) {
                    this.showItemDetails();
                }
            });
        }

        card.innerHTML = `
            <div class="menu-item-image">
                ${this.item.image ?
                `<img src="${this.item.image}" alt="${sanitizeHtml(this.item.name)}" loading="lazy">` :
                `<i class="menu-item-placeholder fas fa-utensils"></i>`
            }
                ${this.item.is_popular ? '<div class="menu-item-badge popular">Popular</div>' : ''}
                ${this.item.is_new ? '<div class="menu-item-badge new">New</div>' : ''}
            </div>
            <div class="menu-item-info">
                <div class="menu-item-header">
                    <h3 class="menu-item-name">${sanitizeHtml(this.item.name)}</h3>
                    <span class="menu-item-price">${formatCurrency(this.item.price)}</span>
                </div>
                <p class="menu-item-description">${sanitizeHtml(this.item.description || '')}</p>
                <div class="menu-item-category">${sanitizeHtml(this.item.category)}</div>
                <div class="menu-item-actions">
                    <button class="add-to-order-btn" ${!this.item.is_available ? 'disabled' : ''}>
                        <i class="fas fa-plus"></i>
                        Add to Order
                    </button>
                    <button class="quick-add-btn" ${!this.item.is_available ? 'disabled' : ''} title="Quick Add">
                        <i class="fas fa-shopping-cart"></i>
                    </button>
                </div>
            </div>
        `;

        // Event handlers
        const addBtn = card.querySelector('.add-to-order-btn');
        const quickAddBtn = card.querySelector('.quick-add-btn');

        if (this.item.is_available) {
            addBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.addToOrder();
            });

            quickAddBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.quickAdd();
            });
        }

        return card;
    }

    addToOrder(quantity = 1) {
        if (this.onAddToOrder) {
            this.onAddToOrder(this.item, quantity);
        }

        // Visual feedback
        const btn = this.element.querySelector('.add-to-order-btn');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check"></i> Added!';
        btn.classList.add('btn-success');

        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.classList.remove('btn-success');
        }, 1500);
    }

    quickAdd() {
        this.addToOrder(1);

        // Animate quick add button
        const btn = this.element.querySelector('.quick-add-btn');
        btn.classList.add('bounce-in');
        setTimeout(() => btn.classList.remove('bounce-in'), 600);
    }

    showItemDetails() {
        const { showModal, formatCurrency, sanitizeHtml } = RestaurantUtils;

        const modalContent = `
            <div class="item-details-modal">
                <div class="item-image-large">
                    ${this.item.image ?
                `<img src="${this.item.image}" alt="${sanitizeHtml(this.item.name)}">` :
                `<i class="fas fa-utensils"></i>`
            }
                </div>
                <div class="item-details">
                    <h2>${sanitizeHtml(this.item.name)}</h2>
                    <p class="item-price">${formatCurrency(this.item.price)}</p>
                    <p class="item-description">${sanitizeHtml(this.item.description || 'No description available.')}</p>
                    <div class="quantity-selector">
                        <label for="itemQuantity">Quantity:</label>
                        <div class="quantity-control">
                            <button type="button" class="quantity-btn" id="decreaseQty">-</button>
                            <input type="number" id="itemQuantity" value="1" min="1" max="99" class="quantity-input">
                            <button type="button" class="quantity-btn" id="increaseQty">+</button>
                        </div>
                    </div>
                    <div class="special-instructions">
                        <label for="specialInstructions">Special Instructions:</label>
                        <textarea id="specialInstructions" placeholder="Any special requests..." rows="3"></textarea>
                    </div>
                </div>
            </div>
        `;

        showModal(`${this.item.name} Details`, modalContent, {
            footerContent: `
                <button class="btn btn-secondary modal-cancel">Cancel</button>
                <button class="btn btn-primary" id="addItemToOrder">
                    <i class="fas fa-plus"></i>
                    Add to Order
                </button>
            `,
            onConfirm: () => {
                const quantity = parseInt(document.getElementById('itemQuantity').value) || 1;
                const instructions = document.getElementById('specialInstructions').value;

                this.addToOrder(quantity, instructions);
                return true; // Close modal
            }
        });

        // Quantity controls
        const modal = document.getElementById('modalContent');
        const qtyInput = modal.querySelector('#itemQuantity');
        const decreaseBtn = modal.querySelector('#decreaseQty');
        const increaseBtn = modal.querySelector('#increaseQty');

        decreaseBtn.addEventListener('click', () => {
            const current = parseInt(qtyInput.value) || 1;
            if (current > 1) qtyInput.value = current - 1;
        });

        increaseBtn.addEventListener('click', () => {
            const current = parseInt(qtyInput.value) || 1;
            if (current < 99) qtyInput.value = current + 1;
        });
    }

    update(newItem) {
        this.item = { ...this.item, ...newItem };
        const newElement = this.createElement();
        this.element.parentNode.replaceChild(newElement, this.element);
        this.element = newElement;
    }
}

/**
 * Order Item Component
 */
class OrderItemComponent {
    constructor(orderItem, onUpdate, onRemove) {
        this.orderItem = orderItem;
        this.onUpdate = onUpdate;
        this.onRemove = onRemove;
        this.element = this.createElement();
    }

    createElement() {
        const { formatCurrency, createElement, sanitizeHtml } = RestaurantUtils;

        const orderItem = createElement('div', {
            className: 'order-item',
            'data-item-id': this.orderItem.id
        });

        orderItem.innerHTML = `
            <div class="order-item-image">
                ${this.orderItem.image ?
                `<img src="${this.orderItem.image}" alt="${sanitizeHtml(this.orderItem.name)}">` :
                `<i class="order-item-placeholder fas fa-utensils"></i>`
            }
            </div>
            <div class="order-item-details">
                <div class="order-item-name">${sanitizeHtml(this.orderItem.name)}</div>
                <div class="order-item-price">${formatCurrency(this.orderItem.price)} each</div>
                ${this.orderItem.instructions ?
                `<div class="order-item-instructions">${sanitizeHtml(this.orderItem.instructions)}</div>` :
                ''
            }
            </div>
            <div class="order-item-controls">
                <div class="quantity-control">
                    <button class="quantity-btn decrease-btn" ${this.orderItem.quantity <= 1 ? 'disabled' : ''}>-</button>
                    <input type="number" class="quantity-input" value="${this.orderItem.quantity}" min="1" max="99">
                    <button class="quantity-btn increase-btn">+</button>
                </div>
                <button class="remove-item-btn" title="Remove item">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;

        // Event handlers
        this.setupEventHandlers(orderItem);

        return orderItem;
    }

    setupEventHandlers(element) {
        const decreaseBtn = element.querySelector('.decrease-btn');
        const increaseBtn = element.querySelector('.increase-btn');
        const quantityInput = element.querySelector('.quantity-input');
        const removeBtn = element.querySelector('.remove-item-btn');

        decreaseBtn.addEventListener('click', () => {
            if (this.orderItem.quantity > 1) {
                this.updateQuantity(this.orderItem.quantity - 1);
            }
        });

        increaseBtn.addEventListener('click', () => {
            if (this.orderItem.quantity < 99) {
                this.updateQuantity(this.orderItem.quantity + 1);
            }
        });

        quantityInput.addEventListener('change', (e) => {
            const newQuantity = parseInt(e.target.value) || 1;
            this.updateQuantity(Math.max(1, Math.min(99, newQuantity)));
        });

        removeBtn.addEventListener('click', () => {
            this.removeItem();
        });
    }

    updateQuantity(newQuantity) {
        this.orderItem.quantity = newQuantity;

        // Update UI
        const quantityInput = this.element.querySelector('.quantity-input');
        const decreaseBtn = this.element.querySelector('.decrease-btn');

        quantityInput.value = newQuantity;
        decreaseBtn.disabled = newQuantity <= 1;

        // Callback
        if (this.onUpdate) {
            this.onUpdate(this.orderItem);
        }

        // Animation
        this.element.classList.add('flash');
        setTimeout(() => this.element.classList.remove('flash'), 500);
    }

    removeItem() {
        // Animation before removal
        this.element.classList.add('slide-out');

        setTimeout(() => {
            if (this.onRemove) {
                this.onRemove(this.orderItem);
            }
        }, 300);
    }

    update(newOrderItem) {
        this.orderItem = { ...this.orderItem, ...newOrderItem };
        const newElement = this.createElement();
        this.element.parentNode.replaceChild(newElement, this.element);
        this.element = newElement;
    }
}

/**
 * Queue Order Component
 */
class QueueOrderComponent {
    constructor(order, onStatusUpdate) {
        this.order = order;
        this.onStatusUpdate = onStatusUpdate;

        this.element = this.createElement();
    }

    createElement() {
        const { formatCurrency, formatDateTime, createElement, sanitizeHtml } = RestaurantUtils;

        const queueItem = createElement('div', {
            className: `queue-item status-${this.order.status || 'unknown'}`,
            'data-order-id': this.order.id || 'unknown'
        });

        // Safely handle items list - handle both frontend and backend data structures
        const items = Array.isArray(this.order.items) ? this.order.items : [];
        const itemsList = items.length > 0 ?
            items.map(item => {
                // Handle both frontend (name) and backend (menu_item_name) structures
                const itemName = item.name || item.menu_item_name || 'Unknown Item';
                const quantity = item.quantity || 0;
                return `${quantity}x ${itemName}`;
            }).join(', ') :
            'No items';

        // Extract order number safely - handle both ORD-YYYYMMDDHHMM-XXXX and order_timestamp formats
        let orderNumber = 'Unknown';
        if (this.order.id) {
            if (this.order.id.startsWith('ORD-')) {
                // Backend format: ORD-202507301938-3F9BCD21
                const parts = this.order.id.split('-');
                orderNumber = parts.length >= 2 ? parts[1] : this.order.id;
            } else if (this.order.id.includes('_')) {
                // Mock API format: order_timestamp
                orderNumber = this.order.id.split('_')[1];
            } else {
                orderNumber = this.order.id;
            }
        }

        // Safely handle total - handle both frontend (total) and backend (total_amount) structures
        const total = this.order.total || this.order.total_amount || 0;

        queueItem.innerHTML = `
            <div class="queue-item-header">
                <div class="order-id">Order #${orderNumber}</div>
                <div class="queue-header-right">
                    <div class="queue-status ${this.order.status || 'unknown'}">${this.getStatusText()}</div>
                    <div class="order-time">${formatDateTime(this.order.created_at || new Date().toISOString())}</div>
                </div>
            </div>
            <div class="customer-info-display">
                <div class="customer-name">${sanitizeHtml(this.order.customer_name || 'Walk-in Customer')}</div>
                <div class="customer-details">
                    ${this.order.customer_phone ? `Phone: ${sanitizeHtml(this.order.customer_phone)}` : ''}
                    ${this.order.table_number ? ` | Table: ${sanitizeHtml(this.order.table_number)}` : ''}
                    ${this.order.order_type ? ` | Type: ${this.order.order_type.replace('_', ' ').toUpperCase()}` : ''}
                </div>
            </div>
            <div class="order-items-summary">
                <div class="order-items-list">${sanitizeHtml(itemsList)}</div>
            </div>
            <div class="order-total-display">${formatCurrency(total)}</div>
            <div class="queue-actions">
                ${this.getActionButtons()}
            </div>
        `;

        // Event handlers
        this.setupEventHandlers(queueItem);

        return queueItem;
    }

    getStatusText() {
        const statusMap = {
            'pending': 'Pending',
            'cooking': 'Cooking',
            'ready': 'Ready',
            'completed': 'Completed',
            'cancelled': 'Cancelled'
        };
        return statusMap[this.order.status] || 'Unknown';
    }

    getActionButtons() {
        switch (this.order.status) {
            case 'pending':
                return `
                    <button class="btn btn-primary start-cooking-btn">
                        <i class="fas fa-fire"></i>
                        Start Cooking
                    </button>
                    <button class="btn btn-danger cancel-order-btn">
                        <i class="fas fa-times"></i>
                        Cancel
                    </button>
                `;
            case 'cooking':
                return `
                    <button class="btn btn-success mark-ready-btn">
                        <i class="fas fa-check"></i>
                        Mark Ready
                    </button>
                `;
            case 'ready':
                return `
                    <button class="btn btn-success complete-order-btn">
                        <i class="fas fa-check-double"></i>
                        Complete Order
                    </button>
                `;
            default:
                return '';
        }
    }

    setupEventHandlers(element) {
        // Start cooking
        const startCookingBtn = element.querySelector('.start-cooking-btn');
        if (startCookingBtn) {
            startCookingBtn.addEventListener('click', () => {
                this.updateStatus('cooking');
            });
        }

        // Mark ready
        const markReadyBtn = element.querySelector('.mark-ready-btn');
        if (markReadyBtn) {
            markReadyBtn.addEventListener('click', () => {
                this.updateStatus('ready');
            });
        }

        // Complete order
        const completeBtn = element.querySelector('.complete-order-btn');
        if (completeBtn) {
            completeBtn.addEventListener('click', () => {
                this.updateStatus('completed');
            });
        }

        // Cancel order
        const cancelBtn = element.querySelector('.cancel-order-btn');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => {
                this.confirmCancel();
            });
        }
    }

    updateStatus(newStatus) {
        const oldStatus = this.order.status;
        this.order.status = newStatus;

        // Update UI immediately for responsiveness
        this.element.className = `queue-item status-${newStatus}`;
        this.element.querySelector('.queue-status').className = `queue-status ${newStatus}`;
        this.element.querySelector('.queue-status').textContent = this.getStatusText();
        this.element.querySelector('.queue-actions').innerHTML = this.getActionButtons();

        // Re-setup event handlers
        this.setupEventHandlers(this.element);

        // Call update callback
        if (this.onStatusUpdate) {
            this.onStatusUpdate(this.order.id, newStatus, oldStatus);
        }

        // Animation
        this.element.classList.add('bounce-in');
        setTimeout(() => this.element.classList.remove('bounce-in'), 600);
    }

    confirmCancel() {
        const { showModal } = RestaurantUtils;

        showModal(
            'Cancel Order',
            `<p>Are you sure you want to cancel order #${this.order.id.split('_')[1]}?</p>
             <p>This action cannot be undone.</p>`,
            {
                onConfirm: () => {
                    this.updateStatus('cancelled');
                    return true;
                }
            }
        );
    }

    update(newOrder) {
        this.order = { ...this.order, ...newOrder };
        const newElement = this.createElement();
        this.element.parentNode.replaceChild(newElement, this.element);
        this.element = newElement;
    }
}

/**
 * Menu Management Row Component
 */
class MenuManagementRow {
    constructor(item, onEdit, onDelete, onToggleStatus) {
        this.item = item;
        this.onEdit = onEdit;
        this.onDelete = onDelete;
        this.onToggleStatus = onToggleStatus;
        this.element = this.createElement();
    }

    createElement() {
        const { formatCurrency, createElement, sanitizeHtml } = RestaurantUtils;

        const row = createElement('tr', {
            'data-item-id': this.item.id
        });

        row.innerHTML = `
            <td>${sanitizeHtml(this.item.name)}</td>
            <td>${sanitizeHtml(this.item.category)}</td>
            <td>${formatCurrency(this.item.price)}</td>
            <td>
                <span class="status-badge ${this.item.is_available ? 'available' : 'unavailable'}">
                    ${this.item.is_available ? 'Available' : 'Unavailable'}
                </span>
            </td>
            <td>
                <div class="table-actions">
                    <button class="action-btn-sm edit" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="action-btn-sm toggle-status" title="${this.item.is_available ? 'Disable' : 'Enable'}">
                        <i class="fas fa-${this.item.is_available ? 'eye-slash' : 'eye'}"></i>
                    </button>
                    <button class="action-btn-sm delete" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        `;

        // Event handlers
        this.setupEventHandlers(row);

        return row;
    }

    setupEventHandlers(element) {
        const editBtn = element.querySelector('.edit');
        const deleteBtn = element.querySelector('.delete');
        const toggleBtn = element.querySelector('.toggle-status');

        editBtn.addEventListener('click', () => {
            if (this.onEdit) this.onEdit(this.item);
        });

        deleteBtn.addEventListener('click', () => {
            this.confirmDelete();
        });

        toggleBtn.addEventListener('click', () => {
            this.toggleStatus();
        });
    }

    confirmDelete() {
        const { showModal } = RestaurantUtils;

        showModal(
            'Delete Menu Item',
            `<p>Are you sure you want to delete <strong>${this.item.name}</strong>?</p>
             <p>This action cannot be undone.</p>`,
            {
                onConfirm: () => {
                    if (this.onDelete) {
                        this.onDelete(this.item.id);
                    }
                    return true;
                }
            }
        );
    }

    toggleStatus() {
        const newStatus = !this.item.is_available;
        this.item.is_available = newStatus;

        // Update UI
        const statusBadge = this.element.querySelector('.status-badge');
        const toggleBtn = this.element.querySelector('.toggle-status');

        statusBadge.className = `status-badge ${newStatus ? 'available' : 'unavailable'}`;
        statusBadge.textContent = newStatus ? 'Available' : 'Unavailable';

        toggleBtn.title = newStatus ? 'Disable' : 'Enable';
        toggleBtn.querySelector('i').className = `fas fa-${newStatus ? 'eye-slash' : 'eye'}`;

        // Callback
        if (this.onToggleStatus) {
            this.onToggleStatus(this.item.id, newStatus);
        }

        // Animation
        this.element.classList.add('flash');
        setTimeout(() => this.element.classList.remove('flash'), 500);
    }

    update(newItem) {
        this.item = { ...this.item, ...newItem };
        const newElement = this.createElement();
        this.element.parentNode.replaceChild(newElement, this.element);
        this.element = newElement;
    }
}

/**
 * Notification Component
 */
class NotificationComponent {
    constructor(message, type = 'info', duration = 5000) {
        this.message = message;
        this.type = type;
        this.duration = duration;
        this.element = this.createElement();
        this.show();
    }

    createElement() {
        const { createElement, sanitizeHtml } = RestaurantUtils;

        const notification = createElement('div', {
            className: `notification notification-${this.type}`
        });

        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${this.getIcon()}"></i>
                <span class="notification-message">${sanitizeHtml(this.message)}</span>
                <button class="notification-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // Close button handler
        notification.querySelector('.notification-close').addEventListener('click', () => {
            this.hide();
        });

        return notification;
    }

    getIcon() {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[this.type] || icons.info;
    }

    show() {
        // Add to container
        let container = document.querySelector('.notification-container');
        if (!container) {
            container = RestaurantUtils.createElement('div', { className: 'notification-container' });
            document.body.appendChild(container);
        }

        container.appendChild(this.element);

        // Animation
        setTimeout(() => this.element.classList.add('show'), 10);

        // Auto hide
        if (this.duration > 0) {
            setTimeout(() => this.hide(), this.duration);
        }
    }

    hide() {
        this.element.classList.add('hide');
        setTimeout(() => {
            if (this.element.parentNode) {
                this.element.parentNode.removeChild(this.element);
            }
        }, 300);
    }
}

// Export components
console.log('🔧 COMPONENTS: Creating RestaurantComponents global object...');
window.RestaurantComponents = {
    MenuItemCard,
    OrderItemComponent,
    QueueOrderComponent,
    MenuManagementRow,
    NotificationComponent
};
window.UIComponents = window.RestaurantComponents; // Alias for compatibility
console.log('✅ COMPONENTS: RestaurantComponents loaded and exported');