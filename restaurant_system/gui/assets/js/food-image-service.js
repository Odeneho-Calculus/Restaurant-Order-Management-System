/**
 * Food Image Service - Fetches real food images from Pixabay API
 * Professional implementation with caching and fallback mechanisms
 */
class FoodImageService {
    constructor() {
        this.apiKey = '51296070-ae5ac953e44dfd8d2c6d2c30b';
        this.apiUrl = 'https://pixabay.com/api/';
        this.imageCache = new Map();
        this.loadingImages = new Set();
        this.apiAvailable = true; // Track API availability

        // Food category mappings for better search results
        this.categoryMappings = {
            'appetizers': ['appetizer', 'starter', 'snack', 'finger food'],
            'mains': ['main course', 'dinner', 'meal', 'entree'],
            'soups': ['soup', 'broth', 'bisque'],
            'desserts': ['dessert', 'cake', 'sweet', 'pastry'],
            'beverages': ['drink', 'beverage', 'cocktail', 'juice'],
            'salads': ['salad', 'greens', 'fresh'],
            'pizza': ['pizza', 'italian'],
            'pasta': ['pasta', 'noodles', 'spaghetti'],
            'seafood': ['fish', 'seafood', 'salmon', 'shrimp'],
            'meat': ['steak', 'beef', 'chicken', 'pork'],
            'vegetarian': ['vegetarian', 'vegan', 'vegetables']
        };

        // Specific food name mappings for exact matches
        this.foodMappings = {
            'caesar salad': 'caesar salad',
            'buffalo wings': 'chicken wings',
            'mozzarella sticks': 'mozzarella sticks',
            'spinach artichoke dip': 'spinach dip',
            'tomato basil soup': 'tomato soup',
            'grilled chicken breast': 'grilled chicken',
            'ribeye steak': 'ribeye steak',
            'salmon fillet': 'salmon fillet',
            'pasta alfredo': 'fettuccine alfredo',
            'bbq ribs': 'bbq ribs',
            'margherita pizza': 'margherita pizza',
            'chicken parmesan': 'chicken parmesan',
            'fish and chips': 'fish and chips',
            'chocolate lava cake': 'chocolate cake',
            'tiramisu': 'tiramisu',
            'new york cheesecake': 'cheesecake',
            'ice cream sundae': 'ice cream sundae',
            'coca cola': 'cola drink',
            'fresh orange juice': 'orange juice',
            'coffee': 'coffee cup',
            'iced tea': 'iced tea',
            'red wine': 'red wine glass',
            'beer': 'beer glass'
        };

        console.log('🖼️ Food Image Service initialized');
    }

    /**
     * Get optimized search terms for a food item
     */
    getSearchTerms(itemName, category) {
        const name = itemName.toLowerCase();

        // Check for exact food mapping first
        if (this.foodMappings[name]) {
            return [this.foodMappings[name]];
        }

        // Extract key words from the item name
        const nameWords = name.split(' ').filter(word =>
            word.length > 2 &&
            !['the', 'and', 'with', 'fresh', 'classic'].includes(word)
        );

        // Get category-specific terms
        const categoryTerms = this.categoryMappings[category] || [category];

        // Combine and prioritize terms
        return [
            name, // Full name first
            ...nameWords, // Individual words
            ...categoryTerms // Category terms as fallback
        ];
    }

    /**
     * Fetch image from Pixabay API
     */
    async fetchImageFromPixabay(searchTerm) {
        // Skip API call if we know it's unavailable
        if (!this.apiAvailable) {
            console.log(`⚠️ Pixabay API unavailable, skipping fetch for "${searchTerm}"`);
            return null;
        }

        try {
            const params = new URLSearchParams({
                key: this.apiKey,
                q: searchTerm,
                image_type: 'photo',
                orientation: 'horizontal',
                category: 'food',
                min_width: 300,
                min_height: 200,
                safesearch: 'true',
                per_page: 5,
                order: 'popular'
            });

            const response = await fetch(`${this.apiUrl}?${params}`, {
                timeout: 10000 // 10 second timeout
            });

            if (!response.ok) {
                if (response.status === 429) {
                    console.warn('⚠️ Pixabay API rate limit exceeded');
                    this.apiAvailable = false;
                    // Re-enable after 1 minute
                    setTimeout(() => {
                        this.apiAvailable = true;
                        console.log('✅ Pixabay API re-enabled after rate limit');
                    }, 60000);
                }
                throw new Error(`Pixabay API error: ${response.status}`);
            }

            const data = await response.json();

            if (data.hits && data.hits.length > 0) {
                // Return the best quality image URL
                const image = data.hits[0];
                return {
                    url: image.webformatURL,
                    thumbnail: image.previewURL,
                    tags: image.tags,
                    source: 'pixabay'
                };
            }

            return null;
        } catch (error) {
            console.error(`❌ Error fetching image for "${searchTerm}":`, error);

            // If network error, temporarily disable API
            if (error.name === 'TypeError' || error.message.includes('fetch')) {
                console.warn('🌐 Network error detected, temporarily disabling Pixabay API');
                this.apiAvailable = false;
                // Re-enable after 2 minutes
                setTimeout(() => {
                    this.apiAvailable = true;
                    console.log('✅ Pixabay API re-enabled after network error');
                }, 120000);
            }

            return null;
        }
    }

    /**
     * Get food image with caching and fallback
     */
    async getFoodImage(itemName, category) {
        const cacheKey = `${itemName}_${category}`.toLowerCase();

        // Check cache first
        if (this.imageCache.has(cacheKey)) {
            return this.imageCache.get(cacheKey);
        }

        // Prevent duplicate requests
        if (this.loadingImages.has(cacheKey)) {
            return this.getPlaceholderImage(category);
        }

        this.loadingImages.add(cacheKey);

        try {
            const searchTerms = this.getSearchTerms(itemName, category);

            // Try each search term until we find an image
            for (const term of searchTerms) {
                console.log(`🔍 Searching for image: "${term}"`);
                const imageData = await this.fetchImageFromPixabay(term);

                if (imageData) {
                    console.log(`✅ Found image for "${itemName}": ${imageData.url}`);
                    this.imageCache.set(cacheKey, imageData);
                    this.loadingImages.delete(cacheKey);
                    return imageData;
                }
            }

            // No image found, use placeholder
            const placeholder = this.getPlaceholderImage(category);
            this.imageCache.set(cacheKey, placeholder);
            this.loadingImages.delete(cacheKey);
            return placeholder;

        } catch (error) {
            console.error(`❌ Error getting image for "${itemName}":`, error);
            this.loadingImages.delete(cacheKey);
            return this.getPlaceholderImage(category);
        }
    }

    /**
     * Get category-specific placeholder image
     */
    getPlaceholderImage(category) {
        const placeholders = {
            'appetizers': { emoji: '🥨', color: '#FF6B6B' },
            'mains': { emoji: '🍽️', color: '#4ECDC4' },
            'soups': { emoji: '🍲', color: '#45B7D1' },
            'desserts': { emoji: '🍰', color: '#96CEB4' },
            'beverages': { emoji: '🥤', color: '#FFEAA7' },
            'salads': { emoji: '🥗', color: '#6C5CE7' },
            'pizza': { emoji: '🍕', color: '#FD79A8' },
            'pasta': { emoji: '🍝', color: '#FDCB6E' },
            'seafood': { emoji: '🐟', color: '#74B9FF' },
            'meat': { emoji: '🥩', color: '#E17055' }
        };

        const placeholder = placeholders[category] || placeholders['mains'];

        return {
            url: null,
            emoji: placeholder.emoji,
            color: placeholder.color,
            source: 'placeholder'
        };
    }

    /**
     * Preload images for menu items
     */
    async preloadMenuImages(menuItems) {
        console.log('🚀 Preloading menu images...');

        const promises = menuItems.map(async (item) => {
            try {
                const imageData = await this.getFoodImage(item.name, item.category);
                return { itemId: item.id, imageData };
            } catch (error) {
                console.error(`❌ Failed to preload image for ${item.name}:`, error);
                return { itemId: item.id, imageData: this.getPlaceholderImage(item.category) };
            }
        });

        const results = await Promise.allSettled(promises);
        const loadedImages = results
            .filter(result => result.status === 'fulfilled')
            .map(result => result.value);

        console.log(`✅ Preloaded ${loadedImages.length} menu images`);
        return loadedImages;
    }

    /**
     * Create image element with loading states
     */
    createImageElement(imageData, itemName, options = {}) {
        const {
            width = '100%',
            height = '120px',
            borderRadius = '4px',
            objectFit = 'cover'
        } = options;

        if (imageData.url) {
            // Real image
            return `
                <img src="${imageData.url}"
                     alt="${itemName}"
                     style="width: ${width}; height: ${height}; border-radius: ${borderRadius}; object-fit: ${objectFit}; transition: transform 0.2s ease;"
                     onload="this.style.opacity='1'"
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
                     loading="lazy">
                <div style="width: ${width}; height: ${height}; border-radius: ${borderRadius}; background: ${imageData.color || '#f5f5f5'}; display: none; align-items: center; justify-content: center; font-size: 24px;">
                    ${imageData.emoji || '🍽️'}
                </div>
            `;
        } else {
            // Placeholder
            return `
                <div style="width: ${width}; height: ${height}; border-radius: ${borderRadius}; background: ${imageData.color}; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                    ${imageData.emoji}
                </div>
            `;
        }
    }

    /**
     * Test Pixabay API connection
     */
    async testApiConnection() {
        try {
            console.log('🧪 Testing Pixabay API connection...');
            const testResult = await this.fetchImageFromPixabay('pizza');

            if (testResult) {
                console.log('✅ Pixabay API connection successful!');
                console.log('📸 Test image URL:', testResult.url);
                return true;
            } else {
                console.warn('⚠️ Pixabay API returned no results for test query');
                return false;
            }
        } catch (error) {
            console.error('❌ Pixabay API connection failed:', error);
            return false;
        }
    }

    /**
     * Get cache statistics
     */
    getCacheStats() {
        return {
            cachedImages: this.imageCache.size,
            loadingImages: this.loadingImages.size,
            cacheKeys: Array.from(this.imageCache.keys())
        };
    }

    /**
     * Clear cache (for testing/debugging)
     */
    clearCache() {
        this.imageCache.clear();
        this.loadingImages.clear();
        console.log('🗑️ Image cache cleared');
    }
}

// Create global instance
window.foodImageService = new FoodImageService();

// Global debugging functions
window.testPixabayAPI = () => window.foodImageService.testApiConnection();
window.getFoodImageCacheStats = () => {
    const stats = window.foodImageService.getCacheStats();
    console.table(stats);
    return stats;
};
window.clearFoodImageCache = () => window.foodImageService.clearCache();
window.testFoodImage = async (itemName, category = 'mains') => {
    console.log(`🧪 Testing image fetch for: ${itemName} (${category})`);
    const result = await window.foodImageService.getFoodImage(itemName, category);
    console.log('Result:', result);
    return result;
};
window.refreshAllFoodImages = () => {
    if (window.restaurantApp && window.restaurantApp.refreshAllFoodImages) {
        window.restaurantApp.refreshAllFoodImages();
    } else {
        console.warn('⚠️ Restaurant app not available');
    }
};

console.log('✅ Food Image Service loaded successfully');
console.log('🔧 Debug functions available:');
console.log('  - testPixabayAPI() - Test API connection');
console.log('  - getFoodImageCacheStats() - Show cache statistics');
console.log('  - clearFoodImageCache() - Clear image cache');
console.log('  - testFoodImage(name, category) - Test specific food image');
console.log('  - refreshAllFoodImages() - Refresh all menu images');