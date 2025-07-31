// Restaurant Management System - Utility Functions

/**
 * Format currency values
 * @param {number} amount - The amount to format
 * @param {string} currency - Currency code (default: USD)
 * @returns {string} Formatted currency string
 */
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

/**
 * Format date and time
 * @param {Date|string} date - Date to format
 * @param {Object} options - Formatting options
 * @returns {string} Formatted date string
 */
function formatDateTime(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    };

    const formatOptions = { ...defaultOptions, ...options };
    const dateObj = date instanceof Date ? date : new Date(date);

    return dateObj.toLocaleDateString('en-US', formatOptions);
}

/**
 * Generate unique ID
 * @param {string} prefix - Optional prefix for the ID
 * @returns {string} Unique identifier
 */
function generateId(prefix = '') {
    const timestamp = Date.now().toString(36);
    const randomStr = Math.random().toString(36).substring(2);
    return prefix ? `${prefix}_${timestamp}_${randomStr}` : `${timestamp}_${randomStr}`;
}

/**
 * Debounce function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @param {boolean} immediate - Execute immediately on first call
 * @returns {Function} Debounced function
 */
function debounce(func, wait, immediate = false) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func.apply(this, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(this, args);
    };
}

/**
 * Throttle function calls
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} Throttled function
 */
function throttle(func, limit) {
    let inThrottle;
    return function (...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Deep clone an object
 * @param {Object} obj - Object to clone
 * @returns {Object} Cloned object
 */
function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj.getTime());
    if (obj instanceof Array) return obj.map(item => deepClone(item));
    if (typeof obj === 'object') {
        const cloned = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                cloned[key] = deepClone(obj[key]);
            }
        }
        return cloned;
    }
}

/**
 * Validate email address
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid email
 */
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Validate phone number
 * @param {string} phone - Phone number to validate
 * @returns {boolean} True if valid phone number
 */
function validatePhone(phone) {
    const regex = /^[\+]?[1-9][\d]{0,15}$/;
    return regex.test(phone.replace(/[\s\-\(\)]/g, ''));
}

/**
 * Sanitize string for HTML output
 * @param {string} str - String to sanitize
 * @returns {string} Sanitized string
 */
function sanitizeHtml(str) {
    const temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
}

/**
 * Format file size
 * @param {number} bytes - File size in bytes
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted file size
 */
function formatFileSize(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];
}

/**
 * Calculate percentage
 * @param {number} part - Part value
 * @param {number} total - Total value
 * @param {number} decimals - Number of decimal places
 * @returns {number} Percentage value
 */
function calculatePercentage(part, total, decimals = 2) {
    if (total === 0) return 0;
    return parseFloat(((part / total) * 100).toFixed(decimals));
}

/**
 * Create element with attributes and children
 * @param {string} tag - HTML tag name
 * @param {Object} attributes - Element attributes
 * @param {Array|string} children - Child elements or text content
 * @returns {HTMLElement} Created element
 */
function createElement(tag, attributes = {}, children = []) {
    const element = document.createElement(tag);

    // Set attributes
    Object.entries(attributes).forEach(([key, value]) => {
        if (key === 'className') {
            element.className = value;
        } else if (key === 'innerHTML') {
            element.innerHTML = value;
        } else if (key === 'textContent') {
            element.textContent = value;
        } else {
            element.setAttribute(key, value);
        }
    });

    // Add children
    if (typeof children === 'string') {
        element.textContent = children;
    } else if (Array.isArray(children)) {
        children.forEach(child => {
            if (typeof child === 'string') {
                element.appendChild(document.createTextNode(child));
            } else if (child instanceof HTMLElement) {
                element.appendChild(child);
            }
        });
    }

    return element;
}

/**
 * Show notification
 * @param {string} message - Notification message
 * @param {string} type - Notification type (success, error, warning, info)
 * @param {number} duration - Display duration in milliseconds
 */
function showNotification(message, type = 'info', duration = 5000) {
    const notification = createElement('div', {
        className: `notification notification-${type}`,
        innerHTML: `
            <div class="notification-content">
                <i class="fas fa-${getNotificationIcon(type)}"></i>
                <span class="notification-message">${sanitizeHtml(message)}</span>
                <button class="notification-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `
    });

    // Add to container
    let container = document.querySelector('.notification-container');
    if (!container) {
        container = createElement('div', { className: 'notification-container' });
        document.body.appendChild(container);
    }

    container.appendChild(notification);

    // Add show class for animation
    setTimeout(() => notification.classList.add('show'), 10);

    // Auto remove
    if (duration > 0) {
        setTimeout(() => removeNotification(notification), duration);
    }

    // Close button handler
    notification.querySelector('.notification-close').addEventListener('click', () => {
        removeNotification(notification);
    });
}

/**
 * Remove notification
 * @param {HTMLElement} notification - Notification element to remove
 */
function removeNotification(notification) {
    notification.classList.add('hide');
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

/**
 * Get notification icon based on type
 * @param {string} type - Notification type
 * @returns {string} Font Awesome icon name
 */
function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || icons.info;
}

/**
 * Show loading spinner
 * @param {string} message - Loading message
 */
function showLoading(message = 'Loading...') {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.querySelector('p').textContent = message;
        spinner.classList.add('active');
    }
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        console.log('🔧 UTILS: Hiding loading spinner...');
        spinner.style.display = 'none';
        console.log('✅ UTILS: Loading spinner hidden successfully');
    } else {
        console.warn('⚠️ UTILS: Loading spinner element not found');
    }
}

/**
 * Show modal
 * @param {string} title - Modal title
 * @param {string|HTMLElement} content - Modal content
 * @param {Object} options - Modal options
 */
function showModal(title, content, options = {}) {
    const overlay = document.getElementById('modalOverlay');
    const modalContent = document.getElementById('modalContent');

    if (!overlay || !modalContent) return;

    // Apply modal size class
    const sizeClass = options.size ? `modal-${options.size}` : '';
    modalContent.className = `modal-content ${sizeClass}`.trim();

    const modalHtml = `
        <div class="modal-header">
            <h2 class="modal-title">${sanitizeHtml(title)}</h2>
            <button class="modal-close" type="button">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="modal-body">
            ${typeof content === 'string' ? content : ''}
        </div>
        ${options.showFooter !== false ? `
            <div class="modal-footer">
                ${options.footerContent || `
                    <button class="btn btn-secondary modal-cancel">Cancel</button>
                    <button class="btn btn-primary modal-confirm">Confirm</button>
                `}
            </div>
        ` : ''}
    `;

    modalContent.innerHTML = modalHtml;

    // Add content if it's an element
    if (content instanceof HTMLElement) {
        modalContent.querySelector('.modal-body').appendChild(content);
    }

    // Show modal
    overlay.classList.add('active');

    // Event handlers
    const closeModal = () => {
        overlay.classList.remove('active');
        if (options.onClose) options.onClose();
    };

    modalContent.querySelector('.modal-close').addEventListener('click', closeModal);

    if (modalContent.querySelector('.modal-cancel')) {
        modalContent.querySelector('.modal-cancel').addEventListener('click', closeModal);
    }

    if (modalContent.querySelector('.modal-confirm')) {
        modalContent.querySelector('.modal-confirm').addEventListener('click', () => {
            if (options.onConfirm) {
                const result = options.onConfirm();
                if (result !== false) closeModal();
            } else {
                closeModal();
            }
        });
    }

    // Close on overlay click
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeModal();
    });

    // Close on escape key
    const handleEscape = (e) => {
        if (e.key === 'Escape') {
            closeModal();
            document.removeEventListener('keydown', handleEscape);
        }
    };
    document.addEventListener('keydown', handleEscape);
}

/**
 * Hide modal
 */
function hideModal() {
    const overlay = document.getElementById('modalOverlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

/**
 * Storage utilities
 */
const Storage = {
    /**
     * Set item in localStorage
     * @param {string} key - Storage key
     * @param {*} value - Value to store
     */
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('Storage.set error:', error);
        }
    },

    /**
     * Get item from localStorage
     * @param {string} key - Storage key
     * @param {*} defaultValue - Default value if key doesn't exist
     * @returns {*} Stored value or default
     */
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Storage.get error:', error);
            return defaultValue;
        }
    },

    /**
     * Remove item from localStorage
     * @param {string} key - Storage key
     */
    remove(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('Storage.remove error:', error);
        }
    },

    /**
     * Clear all localStorage
     */
    clear() {
        try {
            localStorage.clear();
        } catch (error) {
            console.error('Storage.clear error:', error);
        }
    }
};

/**
 * Event emitter class for custom events
 */
class EventEmitter {
    constructor() {
        this.events = {};
    }

    /**
     * Subscribe to an event
     * @param {string} eventName - Event name
     * @param {Function} callback - Event handler
     */
    on(eventName, callback) {
        if (!this.events[eventName]) {
            this.events[eventName] = [];
        }
        this.events[eventName].push(callback);
    }

    /**
     * Unsubscribe from an event
     * @param {string} eventName - Event name
     * @param {Function} callback - Event handler to remove
     */
    off(eventName, callback) {
        if (!this.events[eventName]) return;

        this.events[eventName] = this.events[eventName].filter(cb => cb !== callback);
    }

    /**
     * Emit an event
     * @param {string} eventName - Event name
     * @param {...*} args - Event arguments
     */
    emit(eventName, ...args) {
        if (!this.events[eventName]) return;

        this.events[eventName].forEach(callback => {
            try {
                callback(...args);
            } catch (error) {
                console.error(`Event handler error for ${eventName}:`, error);
            }
        });
    }

    /**
     * Subscribe to an event once
     * @param {string} eventName - Event name
     * @param {Function} callback - Event handler
     */
    once(eventName, callback) {
        const onceCallback = (...args) => {
            callback(...args);
            this.off(eventName, onceCallback);
        };
        this.on(eventName, onceCallback);
    }
}

/**
 * Escape HTML characters for safe display
 * @param {string} str - String to escape
 * @returns {string} Escaped string
 */
function escapeHtml(str) {
    if (typeof str !== 'string') return str;
    const escapeMap = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '/': '&#x2F;'
    };
    return str.replace(/[&<>"'\/]/g, (match) => escapeMap[match]);
}

// Export utilities for use in other modules
console.log('🔧 UTILS: Creating RestaurantUtils global object...');
window.RestaurantUtils = {
    formatCurrency,
    formatDateTime,
    generateId,
    debounce,
    throttle,
    deepClone,
    validateEmail,
    validatePhone,
    sanitizeHtml,
    escapeHtml,
    formatFileSize,
    calculatePercentage,
    createElement,
    showNotification,
    showLoading,
    hideLoading,
    showModal,
    hideModal,
    Storage,
    EventEmitter
};
window.Utils = window.RestaurantUtils; // Alias for compatibility
console.log('✅ UTILS: RestaurantUtils loaded and exported');