#!/usr/bin/env python3
"""
Add i18n support to Asiatek AI Landing Page - Version 2
Uses precise replacements to avoid duplicates
"""
import re

with open('/tmp/asiatek-landing/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================
# 1. Add i18n CSS styles before </head>
# ============================================
i18n_css = '''
    <!-- i18n Language Switcher Styles -->
    <style>
        .lang-switcher {
            position: relative;
            margin-right: 12px;
        }
        .lang-btn {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 8px 12px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-secondary);
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        .lang-btn:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: var(--border-color-hover);
            color: var(--text-primary);
        }
        .lang-btn .arrow {
            font-size: 10px;
            transition: transform 0.2s;
        }
        .lang-switcher.open .lang-btn .arrow {
            transform: rotate(180deg);
        }
        .lang-dropdown {
            position: absolute;
            top: calc(100% + 8px);
            right: 0;
            min-width: 180px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 8px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.2s;
            z-index: 100;
        }
        .lang-switcher.open .lang-dropdown {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }
        .lang-option {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            border-radius: 8px;
            color: var(--text-secondary);
            font-size: 14px;
            cursor: pointer;
            transition: all 0.15s;
        }
        .lang-option:hover {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-primary);
        }
        .lang-option.active {
            background: rgba(99, 102, 241, 0.15);
            color: var(--accent-primary);
        }
        .lang-option .flag {
            font-size: 18px;
        }
        .lang-option .native-name {
            margin-left: auto;
            font-size: 12px;
            opacity: 0.7;
        }
    </style>
'''

content = content.replace('</head>', i18n_css + '</head>')

# ============================================
# 2. Replace nav-cta section with language switcher
# ============================================
old_nav_cta = '''<div class="nav-cta">
                <a href="https://api.asiatekai.com" class="btn btn-ghost">Sign In</a>
                <a href="https://api.asiatekai.com" class="btn btn-primary">Get API Key</a>
            </div>'''

new_nav_cta = '''<div class="nav-cta">
                <!-- Language Switcher -->
                <div class="lang-switcher" id="langSwitcher">
                    <button class="lang-btn" id="langBtn">
                        <span id="currentLangFlag">🌐</span>
                        <span id="currentLangName">English</span>
                        <span class="arrow">▼</span>
                    </button>
                    <div class="lang-dropdown" id="langDropdown">
                        <div class="lang-option" data-lang="en"><span class="flag">🇺🇸</span> English <span class="native-name">English</span></div>
                        <div class="lang-option" data-lang="zh"><span class="flag">🇨🇳</span> 中文 <span class="native-name">Chinese</span></div>
                        <div class="lang-option" data-lang="th"><span class="flag">🇹🇭</span> ไทย <span class="native-name">Thai</span></div>
                        <div class="lang-option" data-lang="vi"><span class="flag">🇻🇳</span> Tiếng Việt <span class="native-name">Vietnamese</span></div>
                        <div class="lang-option" data-lang="id"><span class="flag">🇮🇩</span> Bahasa Indonesia <span class="native-name">Indonesian</span></div>
                        <div class="lang-option" data-lang="ms"><span class="flag">🇲🇾</span> Bahasa Melayu <span class="native-name">Malay</span></div>
                    </div>
                </div>
                <a href="https://api.asiatekai.com" class="btn btn-ghost">Sign In</a>
                <a href="https://api.asiatekai.com" class="btn btn-primary">Get API Key</a>
            </div>'''

content = content.replace(old_nav_cta, new_nav_cta)

# ============================================
# 3. Add data-i18n attributes using tuples
# ============================================
# Format: (old, new) or (old, new, limit)
replacements = [
    # Nav links
    ('<li><a href="pricing.html">Pricing</a></li>', '<li><a href="pricing.html" data-i18n="nav_pricing">Pricing</a></li>'),
    ('<li><a href="#languages">Languages</a></li>', '<li><a href="#languages" data-i18n="nav_languages">Languages</a></li>'),
    ('<li><a href="#features">Features</a></li>', '<li><a href="#features" data-i18n="nav_features">Features</a></li>'),
    ('<li><a href="#code">API Docs</a></li>', '<li><a href="#code" data-i18n="nav_api_docs">API Docs</a></li>'),
    
    # Nav buttons - only first occurrence
    ('>Sign In</a>', ' data-i18n="nav_signin">Sign In</a>'),
    ('>Get API Key</a>', ' data-i18n="nav_get_api_key">Get API Key</a>'),
    
    # Hero
    ('<span>Now available in Singapore</span>', '<span data-i18n="hero_badge">Now available in Singapore</span>'),
    ('<span class="gradient-text">Built for Southeast Asia</span>', '<span class="gradient-text" data-i18n="hero_title_highlight">Built for Southeast Asia</span>'),
    ('>Get API Key — Free<', ' data-i18n="hero_btn_api_key">Get API Key — Free</'),
    ('>Get Started Free<', ' data-i18n="hero_btn_start">Get Started Free</'),
    ('>View Documentation<', ' data-i18n="hero_btn_docs">View Documentation</'),
    
    # Hero stats
    ('<div class="hero-stat-label">Languages</div>', '<div class="hero-stat-label" data-i18n="stat_languages">Languages</div>'),
    ('<div class="hero-stat-label">Cost Savings</div>', '<div class="hero-stat-label" data-i18n="stat_cost_savings">Cost Savings</div>'),
    ('<div class="hero-stat-label">Migration</div>', '<div class="hero-stat-label" data-i18n="stat_migration">Migration</div>'),
    ('<div class="hero-stat-label">SLA Uptime</div>', '<div class="hero-stat-label" data-i18n="stat_sla">SLA Uptime</div>'),
    
    # Pricing comparison
    ('<span class="section-label">Pricing Comparison</span>', '<span class="section-label" data-i18n="pricing_compare_label">Pricing Comparison</span>'),
    ('<h2 class="section-title">Dramatically Lower Cost</h2>', '<h2 class="section-title" data-i18n="pricing_compare_title">Dramatically Lower Cost</h2>'),
    ('<th>Provider</th>', '<th data-i18n="table_provider">Provider</th>'),
    ('<th>Model</th>', '<th data-i18n="table_model">Model</th>'),
    ('<th>Input ($/M tokens)</th>', '<th data-i18n="table_input">Input ($/M tokens)</th>'),
    ('<th>Output ($/M tokens)</th>', '<th data-i18n="table_output">Output ($/M tokens)</th>'),
    
    # Languages section
    ('<span class="section-label">Language Support</span>', '<span class="section-label" data-i18n="lang_section_label">Language Support</span>'),
    ('<h2 class="section-title">201 Languages, Including All Southeast Asian</h2>', '<h2 class="section-title" data-i18n="lang_section_title">201 Languages, Including All Southeast Asian</h2>'),
    ('<div class="languages-total-label">More languages including regional dialects</div>', '<div class="languages-total-label" data-i18n="lang_more">More languages including regional dialects</div>'),
    
    # Quickstart
    ('<h3>Start in 3 Lines of Code</h3>', '<h3 data-i18n="quickstart_title">Start in 3 Lines of Code</h3>'),
    ('<p>Get started with Asiatek AI in seconds. No complex setup required.</p>', '<p data-i18n="quickstart_desc">Get started with Asiatek AI in seconds. No complex setup required.</p>'),
    
    # Models section
    ('<span class="section-label">Supported Models</span>', '<span class="section-label" data-i18n="models_label">Supported Models</span>'),
    ('<h2 class="section-title">9 Models Available</h2>', '<h2 class="section-title" data-i18n="models_title">9 Models Available</h2>'),
    ('<p class="section-desc">Choose from a variety of models optimized for different use cases.</p>', '<p class="section-desc" data-i18n="models_desc">Choose from a variety of models optimized for different use cases.</p>'),
    ('<th>Category</th>', '<th data-i18n="table_category">Category</th>'),
    ('<th>Input Price</th>', '<th data-i18n="table_input_price">Input Price</th>'),
    ('<th>Output Price</th>', '<th data-i18n="table_output_price">Output Price</th>'),
    
    # Features section
    ('<span class="section-label">Features</span>', '<span class="section-label" data-i18n="features_label">Features</span>'),
    ('<h2 class="section-title">Everything You Need</h2>', '<h2 class="section-title" data-i18n="features_title">Everything You Need</h2>'),
    ('<p class="section-desc">Built for production with enterprise-grade reliability and developer-friendly tools.</p>', '<p class="section-desc" data-i18n="features_desc">Built for production with enterprise-grade reliability and developer-friendly tools.</p>'),
    
    # Pricing section
    ('<span class="section-label">Pricing Plans</span>', '<span class="section-label" data-i18n="pricing_label">Pricing Plans</span>'),
    ('<h2 class="section-title">Simple, Transparent Pricing</h2>', '<h2 class="section-title" data-i18n="pricing_title">Simple, Transparent Pricing</h2>'),
    ('<p class="section-desc">Start free, scale as you grow. No hidden fees, no surprises.</p>', '<p class="section-desc" data-i18n="pricing_desc">Start free, scale as you grow. No hidden fees, no surprises.</p>'),
    
    # Pricing cards
    ('<div class="pricing-name">Starter</div>', '<div class="pricing-name" data-i18n="starter_name">Starter</div>'),
    ('<div class="pricing-desc">Perfect for prototypes and experiments</div>', '<div class="pricing-desc" data-i18n="starter_desc">Perfect for prototypes and experiments</div>'),
    ('>Free API key, no credit card<', ' data-i18n="starter_feat_1">Free API key, no credit card</'),
    ('>DeepSeek &amp; Qwen models<', ' data-i18n="starter_feat_2">DeepSeek &amp; Qwen models</'),
    ('>OpenAI-compatible API<', ' data-i18n="starter_feat_3">OpenAI-compatible API</'),
    ('>10 RPM rate limit<', ' data-i18n="starter_feat_4">10 RPM rate limit</'),
    ('>Community support<', ' data-i18n="starter_feat_5">Community support</'),
    ('>Get Free API Key<', ' data-i18n="starter_btn">Get Free API Key</'),
    
    ('<div class="pricing-name">Pro</div>', '<div class="pricing-name" data-i18n="pro_name">Pro</div>'),
    ('<div class="pricing-desc">For growing applications and teams</div>', '<div class="pricing-desc" data-i18n="pro_desc">For growing applications and teams</div>'),
    ('>Pay-per-use (token billing)<', ' data-i18n="pro_feat_1">Pay-per-use (token billing)</'),
    ('>All models: DeepSeek + Qwen<', ' data-i18n="pro_feat_2">All models: DeepSeek + Qwen</'),
    ('>Higher rate limits (60 RPM)<', ' data-i18n="pro_feat_3">Higher rate limits (60 RPM)</'),
    ('>Priority API access<', ' data-i18n="pro_feat_4">Priority API access</'),
    ('>Email support<', ' data-i18n="pro_feat_5">Email support</'),
    ('>Usage analytics dashboard<', ' data-i18n="pro_feat_6">Usage analytics dashboard</'),
    (' pricing.html" class="btn btn-primary">Get Started</a>', ' pricing.html" class="btn btn-primary" data-i18n="pro_btn">Get Started</a>'),
    
    ('<div class="pricing-name">Enterprise</div>', '<div class="pricing-name" data-i18n="enterprise_name">Enterprise</div>'),
    ('<div class="pricing-desc">Custom solutions for high volume</div>', '<div class="pricing-desc" data-i18n="enterprise_desc">Custom solutions for high volume</div>'),
    ('>Volume discounts on tokens<', ' data-i18n="enterprise_feat_1">Volume discounts on tokens</'),
    ('>All models + priority routing<', ' data-i18n="enterprise_feat_2">All models + priority routing</'),
    ('>Custom rate limits<', ' data-i18n="enterprise_feat_3">Custom rate limits</'),
    ('>99.9% SLA guarantee<', ' data-i18n="enterprise_feat_4">99.9% SLA guarantee</'),
    ('>Dedicated support channel<', ' data-i18n="enterprise_feat_5">Dedicated support channel</'),
    ('>Custom model fine-tuning<', ' data-i18n="enterprise_feat_6">Custom model fine-tuning</'),
    ('>Contact Sales<', ' data-i18n="enterprise_btn">Contact Sales</'),
    
    # Code section
    ('<span class="section-label">Quick Integration</span>', '<span class="section-label" data-i18n="code_label">Quick Integration</span>'),
    ('<h2 class="section-title">5 Minutes to Migrate</h2>', '<h2 class="section-title" data-i18n="code_title">5 Minutes to Migrate</h2>'),
    ('>Copy<', ' data-i18n="code_copy">Copy</'),
    ('>Migration completed in 5 minutes.<', ' data-i18n="code_migration_title">Migration completed in 5 minutes.</'),
    
    # Footer
    ('<h4>Product</h4>', '<h4 data-i18n="footer_product">Product</h4>'),
    ('<h4>Resources</h4>', '<h4 data-i18n="footer_resources">Resources</h4>'),
    ('<h4>Company</h4>', '<h4 data-i18n="footer_company">Company</h4>'),
    ('>Changelog<', ' data-i18n="footer_changelog">Changelog</'),
    ('>Getting Started<', ' data-i18n="footer_getting_started">Getting Started</'),
    ('>API Reference<', ' data-i18n="footer_api_ref">API Reference</'),
    ('>SDK Libraries<', ' data-i18n="footer_sdk">SDK Libraries</'),
    ('>Status Page<', ' data-i18n="footer_status">Status Page</'),
    ('>About Us<', ' data-i18n="footer_about">About Us</'),
    ('>Blog<', ' data-i18n="footer_blog">Blog</'),
    ('>Contact<', ' data-i18n="footer_contact">Contact</'),
    ('>Privacy Policy<', ' data-i18n="footer_privacy">Privacy Policy</'),
]

for old, new in replacements:
    content = content.replace(old, new, 1)

# Write modified content
with open('/tmp/asiatek-landing/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("i18n support added successfully!")
print(f"File size: {len(content)} bytes")
print(f"Line count: {content.count(chr(10))}")
