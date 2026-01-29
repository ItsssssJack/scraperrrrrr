// AI News Dashboard - JavaScript
// Handles data fetching, rendering, and interactivity

// ============================================
// Configuration
// ============================================
const SUPABASE_CONFIG = {
    url: 'https://hqxxapqukrzawrvdlwmu.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhxeHhhcHF1a3J6YXdydmRsd211Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkyNzU5MTMsImV4cCI6MjA4NDg1MTkxM30.eGrFJ7HgXdhjfiyq7G8rEb0gitp0pF2pq9ZLzbnGB_4'
};

let supabaseClient = null;
let currentFilter = 'all';
let allArticles = [];
let savedArticleIds = new Set();

// ============================================
// Initialize
// ============================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 AI News Dashboard initializing...');

    // Initialize Supabase client
    try {
        supabaseClient = window.supabase.createClient(SUPABASE_CONFIG.url, SUPABASE_CONFIG.anonKey);
        console.log('✅ Supabase client initialized');
    } catch (error) {
        console.error('❌ Failed to initialize Supabase:', error);
        showError('Failed to connect to database. Please check your configuration.');
        return;
    }

    // Set up event listeners
    setupEventListeners();

    // Load data
    await loadData();
});

// ============================================
// Event Listeners
// ============================================
function setupEventListeners() {
    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const source = e.currentTarget.dataset.source;
            setFilter(source);
        });
    });

    // Refresh button
    document.getElementById('refresh-btn').addEventListener('click', async () => {
        await loadData();
    });
}

// ============================================
// Data Loading
// ============================================
async function loadData() {
    showLoading();

    try {
        // Fetch articles from last 24 hours
        const twentyFourHoursAgo = new Date();
        twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24);

        const { data: articles, error: articlesError } = await supabaseClient
            .from('articles')
            .select('*')
            .gte('published_date', twentyFourHoursAgo.toISOString())
            .order('published_date', { ascending: false });

        if (articlesError) throw articlesError;

        // Fetch saved articles
        const { data: savedArticles, error: savedError } = await supabaseClient
            .from('saved_articles')
            .select('article_id');

        if (savedError) throw savedError;

        // Fetch saved enrichments
        const { data: savedEnrichments, error: savedEnrichmentsError } = await supabaseClient
            .from('saved_enrichments')
            .select('enrichment_id');

        if (savedEnrichmentsError) {
            console.warn('⚠️ Could not load saved enrichments:', savedEnrichmentsError);
        }

        // Fetch all enrichments
        const { data: enrichments, error: enrichmentsError } = await supabaseClient
            .from('article_enrichments')
            .select('*')
            .order('position', { ascending: true });

        if (enrichmentsError) {
            console.warn('⚠️ Could not load enrichments:', enrichmentsError);
        }

        // Group enrichments by article_id
        const enrichmentsByArticle = {};
        if (enrichments) {
            enrichments.forEach(enrich => {
                if (!enrichmentsByArticle[enrich.article_id]) {
                    enrichmentsByArticle[enrich.article_id] = [];
                }
                enrichmentsByArticle[enrich.article_id].push(enrich);
            });
        }

        // Attach enrichments to articles
        allArticles = (articles || []).map(article => ({
            ...article,
            enrichments: enrichmentsByArticle[article.id] || []
        }));

        // Combine saved articles and enrichments into one Set
        savedArticleIds = new Set([
            ...savedArticles.map(sa => sa.article_id),
            ...(savedEnrichments || []).map(se => se.enrichment_id)
        ]);

        console.log(`✅ Loaded ${allArticles.length} articles, ${savedArticleIds.size} saved items, ${enrichments?.length || 0} enrichments`);

        // Update stats
        updateStats();

        // Render articles
        renderArticles();


        hideLoading();

    } catch (error) {
        console.error('❌ Error loading data:', error);
        showError(`Failed to load articles: ${error.message}`);
    }
}

// ============================================
// Rendering
// ============================================
function renderArticles() {
    const grid = document.getElementById('articles-grid');

    // Filter articles
    let filteredArticles = allArticles;

    if (currentFilter === 'saved') {
        filteredArticles = allArticles.filter(a => savedArticleIds.has(a.id));
    } else if (currentFilter !== 'all') {
        filteredArticles = allArticles.filter(a => a.source === currentFilter);
    }

    // Show empty state if no articles
    if (filteredArticles.length === 0) {
        grid.innerHTML = '';
        showEmpty();
        return;
    }

    hideEmpty();

    // Convert articles to individual cards - enrichments become separate cards
    let allCards = [];

    filteredArticles.forEach(article => {
        if (article.enrichments && article.enrichments.length > 0) {
            // For articles with enrichments, create a card for each enrichment
            article.enrichments.forEach(enrichment => {
                allCards.push({
                    type: 'enrichment',
                    id: enrichment.id,
                    parentArticleId: article.id,
                    parentArticleUrl: article.url,
                    source: article.source,
                    title: enrichment.title,
                    summary: enrichment.summary,
                    content: enrichment.content,
                    image_url: enrichment.image_url,
                    author: article.author,
                    published_date: article.published_date
                });
            });
        } else {
            // For articles without enrichments, show the article itself
            allCards.push({
                type: 'article',
                ...article
            });
        }
    });

    // Render cards
    grid.innerHTML = allCards.map(card => createCard(card)).join('');

    // Add save button listeners
    document.querySelectorAll('.save-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const cardId = e.currentTarget.dataset.cardId;
            const cardElement = e.currentTarget.closest('.article-card');
            const cardType = cardElement ? cardElement.dataset.cardType : 'article';
            await toggleSave(cardId, cardType);
        });
    });

    // Add delete button listeners with animation
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const container = e.currentTarget.closest('.delete-btn-container');
            const deleteBtn = container.querySelector('.delete-btn');
            const cancelBtn = container.querySelector('.cancel-btn');
            const cardId = deleteBtn.dataset.cardId;
            const cardType = deleteBtn.dataset.cardType;

            // If already in confirming state, execute delete
            if (deleteBtn.classList.contains('confirming')) {
                await deleteCard(cardId, cardType);
                return;
            }

            // Enter confirming state
            deleteBtn.classList.add('confirming');
            deleteBtn.querySelector('.delete-btn-icon').textContent = '✓';
            deleteBtn.querySelector('.delete-btn-text').textContent = 'Confirm';
            cancelBtn.classList.add('visible');
        });
    });

    // Add cancel button listeners
    document.querySelectorAll('.cancel-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const container = e.currentTarget.closest('.delete-btn-container');
            const deleteBtn = container.querySelector('.delete-btn');
            const cancelBtn = container.querySelector('.cancel-btn');

            // Reset to initial state
            deleteBtn.classList.remove('confirming');
            deleteBtn.querySelector('.delete-btn-icon').textContent = '🗑️';
            deleteBtn.querySelector('.delete-btn-text').textContent = 'Delete';
            cancelBtn.classList.remove('visible');
        });
    });

    // Add card click listeners (only for article-main, not enrichments)
    document.querySelectorAll('.article-main').forEach(main => {
        main.addEventListener('click', (e) => {
            const url = e.currentTarget.dataset.url;
            window.open(url, '_blank');
        });
    });

    // Add enrichment toggle listeners
    document.querySelectorAll('.toggle-enrichments-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const articleId = e.currentTarget.dataset.cardId;
            const enrichmentsList = document.getElementById(`enrichments-list-${articleId}`);
            const toggleIcon = e.currentTarget.querySelector('.toggle-icon');
            const isHidden = enrichmentsList.classList.contains('hidden');

            if (isHidden) {
                enrichmentsList.classList.remove('hidden');
                toggleIcon.textContent = '▲';
                e.currentTarget.childNodes[2].textContent = ' Hide Details';
            } else {
                enrichmentsList.classList.add('hidden');
                toggleIcon.textContent = '▼';
                e.currentTarget.childNodes[2].textContent = ' Show Details';
            }
        });
    });

    // Add read more button listeners
    document.querySelectorAll('.read-more-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const enrichmentId = e.currentTarget.dataset.enrichmentId;
            const fullContent = document.getElementById(`content-${enrichmentId}`);
            const isHidden = fullContent.classList.contains('hidden');

            if (isHidden) {
                fullContent.classList.remove('hidden');
                e.currentTarget.textContent = 'Read Less';
            } else {
                fullContent.classList.add('hidden');
                e.currentTarget.textContent = 'Read More';
            }
        });
    });
}

function createCard(card) {
    const isSaved = savedArticleIds.has(card.id);
    const sourceLabel = {
        'bensbites': "Ben's Bites",
        'rundown': 'The Rundown',
        'reddit': 'Reddit'
    }[card.source] || card.source;

    const publishedDate = new Date(card.published_date);
    const timeAgo = getTimeAgo(publishedDate);

    const cardUrl = card.type === 'article' ? card.url : card.parentArticleUrl;

    return `
        <div class="article-card" data-card-id="${card.id}" data-card-type="${card.type}">
            ${card.image_url ? `
                <div class="article-image">
                    <img src="${card.image_url}" alt="${escapeHtml(card.title)}" loading="lazy">
                </div>
            ` : ''}
            <div class="article-main" data-url="${cardUrl}">
                <div class="article-header">
                    <span class="article-source">${sourceLabel}</span>
                    <div class="article-actions">
                        <button class="save-btn ${isSaved ? 'saved' : ''}" data-card-id="${card.id}" title="${isSaved ? 'Unsave' : 'Save'}">
                            ${isSaved ? '❤️' : '🤍'}
                        </button>
                        <div class="delete-btn-container">
                            <button class="delete-btn" data-card-id="${card.id}" data-card-type="${card.type}">
                                <span class="delete-btn-icon">🗑️</span>
                                <span class="delete-btn-text">Delete</span>
                            </button>
                            <button class="cancel-btn" title="Cancel">✕</button>
                        </div>
                    </div>
                </div>
                <h3 class="article-title">${escapeHtml(card.title)}</h3>
                ${card.summary ? `<p class="article-summary">${escapeHtml(card.summary)}</p>` : ''}
                ${card.content && card.type === 'enrichment' ? `
                    <div class="article-content">
                        ${escapeHtml(card.content).replace(/\n\n/g, '</p><p>').replace(/^/, '<p>').replace(/$/, '</p>')}
                    </div>
                ` : ''}
                <div class="article-meta">
                    <span class="article-author">${escapeHtml(card.author || 'Unknown')}</span>
                    <span class="article-date">${timeAgo}</span>
                </div>
            </div>
        </div>
    `;
}


// ============================================
// Save/Unsave
// ============================================
async function toggleSave(cardId, cardType) {
    const isSaved = savedArticleIds.has(cardId);

    try {
        // Determine if this is an article or enrichment
        const isEnrichment = cardType === 'enrichment';

        if (isSaved) {
            // Unsave
            if (isEnrichment) {
                const { error } = await supabaseClient
                    .from('saved_enrichments')
                    .delete()
                    .eq('enrichment_id', cardId);

                if (error) throw error;
                console.log('✅ Enrichment unsaved');
            } else {
                const { error } = await supabaseClient
                    .from('saved_articles')
                    .delete()
                    .eq('article_id', cardId);

                if (error) throw error;
                console.log('✅ Article unsaved');
            }

            savedArticleIds.delete(cardId);
        } else {
            // Save
            if (isEnrichment) {
                const { error } = await supabaseClient
                    .from('saved_enrichments')
                    .insert({ enrichment_id: cardId });

                if (error) throw error;
                console.log('✅ Enrichment saved');
            } else {
                const { error } = await supabaseClient
                    .from('saved_articles')
                    .insert({ article_id: cardId });

                if (error) throw error;
                console.log('✅ Article saved');
            }

            savedArticleIds.add(cardId);
        }

        // Update UI
        updateStats();
        renderArticles();

    } catch (error) {
        console.error('❌ Error toggling save:', error);
        alert(`Failed to ${isSaved ? 'unsave' : 'save'} item: ${error.message}`);
    }
}


// ============================================
// Delete Card (Enrichment or Article)
// ============================================
async function deleteCard(cardId, cardType) {
    // Find the card to show its title in confirmation
    const card = cardType === 'enrichment'
        ? allArticles.flatMap(a => a.enrichments || []).find(e => e.id === cardId)
        : allArticles.find(a => a.id === cardId);

    const cardTitle = card ? (card.title || 'this item') : 'this item';

    // Confirm deletion
    if (!confirm(`Are you sure you want to delete "${cardTitle}"?\n\nThis will permanently remove this ${cardType}.`)) {
        return;
    }

    try {
        if (cardType === 'enrichment') {
            // Delete enrichment
            const { error } = await supabaseClient
                .from('article_enrichments')
                .delete()
                .eq('id', cardId);

            if (error) throw error;

            // Remove from local arrays
            allArticles.forEach(article => {
                if (article.enrichments) {
                    article.enrichments = article.enrichments.filter(e => e.id !== cardId);
                }
            });
        } else {
            // Delete article (enrichments will be deleted automatically via CASCADE)
            const { error } = await supabaseClient
                .from('articles')
                .delete()
                .eq('id', cardId);

            if (error) throw error;

            // Remove from local arrays
            allArticles = allArticles.filter(a => a.id !== cardId);
        }

        savedArticleIds.delete(cardId);
        console.log(`✅ ${cardType} deleted`);

        // Update UI
        updateStats();
        renderArticles();

    } catch (error) {
        console.error(`❌ Error deleting ${cardType}:`, error);
        alert(`Failed to delete ${cardType}: ${error.message}`);
    }
}

// ============================================
// Filtering
// ============================================
function setFilter(source) {
    currentFilter = source;

    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.source === source);
    });

    // Re-render
    renderArticles();
}

// ============================================
// UI States
// ============================================
function showLoading() {
    document.getElementById('loading-state').classList.remove('hidden');
    document.getElementById('articles-grid').classList.add('hidden');
    document.getElementById('empty-state').classList.add('hidden');
    document.getElementById('error-state').classList.add('hidden');
}

function hideLoading() {
    document.getElementById('loading-state').classList.add('hidden');
    document.getElementById('articles-grid').classList.remove('hidden');
}

function showEmpty() {
    document.getElementById('empty-state').classList.remove('hidden');
}

function hideEmpty() {
    document.getElementById('empty-state').classList.add('hidden');
}

function showError(message) {
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-state').classList.remove('hidden');
    document.getElementById('loading-state').classList.add('hidden');
    document.getElementById('articles-grid').classList.add('hidden');
}

function updateStats() {
    document.querySelector('#article-count .stat-number').textContent = allArticles.length;
    document.querySelector('#saved-count .stat-number').textContent = savedArticleIds.size;
}

// ============================================
// Utilities
// ============================================
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);

    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };

    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return `${interval} ${unit}${interval > 1 ? 's' : ''} ago`;
        }
    }

    return 'just now';
}
