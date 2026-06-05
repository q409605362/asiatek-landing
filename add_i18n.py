#!/usr/bin/env python3
"""
Add i18n support to Asiatek AI Landing Page
"""
import re

# Read original file
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
# 2. Add language switcher in nav-cta
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
                <a href="https://api.asiatekai.com" class="btn btn-ghost" data-i18n="nav_signin">Sign In</a>
                <a href="https://api.asiatekai.com" class="btn btn-primary" data-i18n="nav_get_api_key">Get API Key</a>
            </div>'''

content = content.replace(old_nav_cta, new_nav_cta)

# ============================================
# 3. Add data-i18n attributes to text elements
# ============================================

# Navigation links
content = content.replace('>Pricing</a>', ' data-i18n="nav_pricing">Pricing</a>', 1)
content = content.replace('>Languages</a>', ' data-i18n="nav_languages">Languages</a>', 1)
content = content.replace('>Features</a>', ' data-i18n="nav_features">Features</a>', 1)
content = content.replace('>API Docs</a>', ' data-i18n="nav_api_docs">API Docs</a>', 1)

# Hero section
content = content.replace('<span>Now available in Singapore</span>', '<span data-i18n="hero_badge">Now available in Singapore</span>')
content = content.replace('>Built for Southeast Asia<', ' data-i18n="hero_title_highlight">Built for Southeast Asia</')
content = content.replace('>Get API Key — Free<', ' data-i18n="hero_btn_api_key">Get API Key — Free</')
content = content.replace('>Get Started Free<', ' data-i18n="hero_btn_start">Get Started Free</')
content = content.replace('>View Documentation<', ' data-i18n="hero_btn_docs">View Documentation</')

# Hero stats
content = content.replace('>Languages<', ' data-i18n="stat_languages">Languages</', 1)
content = content.replace('>Cost Savings<', ' data-i18n="stat_cost_savings">Cost Savings</', 1)
content = content.replace('>Migration<', ' data-i18n="stat_migration">Migration</', 1)
content = content.replace('>SLA Uptime<', ' data-i18n="stat_sla">SLA Uptime</', 1)

# Pricing comparison
content = content.replace('>Pricing Comparison<', ' data-i18n="pricing_compare_label">Pricing Comparison</')
content = content.replace('>Dramatically Lower Cost<', ' data-i18n="pricing_compare_title">Dramatically Lower Cost</')
content = content.replace('>Provider<', ' data-i18n="table_provider">Provider</')
content = content.replace('>Model<', ' data-i18n="table_model">Model</')
content = content.replace('>Input ($/M tokens)<', ' data-i18n="table_input">Input ($/M tokens)</')
content = content.replace('>Output ($/M tokens)<', ' data-i18n="table_output">Output ($/M tokens)</')

# Languages section
content = content.replace('>Language Support<', ' data-i18n="lang_section_label">Language Support</')
content = content.replace('>201 Languages, Including All Southeast Asian<', ' data-i18n="lang_section_title">201 Languages, Including All Southeast Asian</')
content = content.replace('>More languages including regional dialects<', ' data-i18n="lang_more">More languages including regional dialects</')

# Quickstart
content = content.replace('>Start in 3 Lines of Code<', ' data-i18n="quickstart_title">Start in 3 Lines of Code</')
content = content.replace('>Get started with Asiatek AI in seconds. No complex setup required.<', ' data-i18n="quickstart_desc">Get started with Asiatek AI in seconds. No complex setup required.</')

# Models section
content = content.replace('>Supported Models<', ' data-i18n="models_label">Supported Models</')
content = content.replace('>9 Models Available<', ' data-i18n="models_title">9 Models Available</')
content = content.replace('>Choose from a variety of models optimized for different use cases.<', ' data-i18n="models_desc">Choose from a variety of models optimized for different use cases.</')
content = content.replace('>Category<', ' data-i18n="table_category">Category</')
content = content.replace('>Input Price<', ' data-i18n="table_input_price">Input Price</')
content = content.replace('>Output Price<', ' data-i18n="table_output_price">Output Price</')

# Features section
content = content.replace('>Features<', ' data-i18n="features_label">Features</', 1)
content = content.replace('>Everything You Need<', ' data-i18n="features_title">Everything You Need</')
content = content.replace('>Built for production with enterprise-grade reliability and developer-friendly tools.<', ' data-i18n="features_desc">Built for production with enterprise-grade reliability and developer-friendly tools.</')

# Pricing plans
content = content.replace('>Pricing Plans<', ' data-i18n="pricing_label">Pricing Plans</')
content = content.replace('>Simple, Transparent Pricing<', ' data-i18n="pricing_title">Simple, Transparent Pricing</', 1)
content = content.replace('>Start free, scale as you grow. No hidden fees, no surprises.<', ' data-i18n="pricing_desc">Start free, scale as you grow. No hidden fees, no surprises.</')

# Pricing cards - Starter
starter_card = '''<div class="pricing-name">Starter</div>
                    <div class="pricing-desc">Perfect for prototypes and experiments</div>'''
new_starter = '''<div class="pricing-name" data-i18n="starter_name">Starter</div>
                    <div class="pricing-desc" data-i18n="starter_desc">Perfect for prototypes and experiments</div>'''
content = content.replace(starter_card, new_starter)

# Starter features
content = content.replace('>Free API key, no credit card<', ' data-i18n="starter_feat_1">Free API key, no credit card</')
content = content.replace('>DeepSeek &amp; Qwen models<', ' data-i18n="starter_feat_2">DeepSeek &amp; Qwen models</')
content = content.replace('>OpenAI-compatible API<', ' data-i18n="starter_feat_3">OpenAI-compatible API</')
content = content.replace('>10 RPM rate limit<', ' data-i18n="starter_feat_4">10 RPM rate limit</')
content = content.replace('>Community support<', ' data-i18n="starter_feat_5">Community support</')
content = content.replace('>Get Free API Key<', ' data-i18n="starter_btn">Get Free API Key</')

# Pricing cards - Pro
pro_card = '''<div class="pricing-name">Pro</div>
                    <div class="pricing-desc">For growing applications and teams</div>'''
new_pro = '''<div class="pricing-name" data-i18n="pro_name">Pro</div>
                    <div class="pricing-desc" data-i18n="pro_desc">For growing applications and teams</div>'''
content = content.replace(pro_card, new_pro)

# Pro features
content = content.replace('>Pay-per-use (token billing)<', ' data-i18n="pro_feat_1">Pay-per-use (token billing)</')
content = content.replace('>All models: DeepSeek + Qwen<', ' data-i18n="pro_feat_2">All models: DeepSeek + Qwen</')
content = content.replace('>Higher rate limits (60 RPM)<', ' data-i18n="pro_feat_3">Higher rate limits (60 RPM)</')
content = content.replace('>Priority API access<', ' data-i18n="pro_feat_4">Priority API access</')
content = content.replace('>Email support<', ' data-i18n="pro_feat_5">Email support</')
content = content.replace('>Usage analytics dashboard<', ' data-i18n="pro_feat_6">Usage analytics dashboard</')
content = content.replace('>Get Started<', ' data-i18n="pro_btn">Get Started</', 1)

# Pricing cards - Enterprise
enterprise_card = '''<div class="pricing-name">Enterprise</div>
                    <div class="pricing-desc">Custom solutions for high volume</div>'''
new_enterprise = '''<div class="pricing-name" data-i18n="enterprise_name">Enterprise</div>
                    <div class="pricing-desc" data-i18n="enterprise_desc">Custom solutions for high volume</div>'''
content = content.replace(enterprise_card, new_enterprise)

# Enterprise features
content = content.replace('>Volume discounts on tokens<', ' data-i18n="enterprise_feat_1">Volume discounts on tokens</')
content = content.replace('>All models + priority routing<', ' data-i18n="enterprise_feat_2">All models + priority routing</')
content = content.replace('>Custom rate limits<', ' data-i18n="enterprise_feat_3">Custom rate limits</')
content = content.replace('>99.9% SLA guarantee<', ' data-i18n="enterprise_feat_4">99.9% SLA guarantee</')
content = content.replace('>Dedicated support channel<', ' data-i18n="enterprise_feat_5">Dedicated support channel</')
content = content.replace('>Custom model fine-tuning<', ' data-i18n="enterprise_feat_6">Custom model fine-tuning</')
content = content.replace('>Contact Sales<', ' data-i18n="enterprise_btn">Contact Sales</')

# Code section
content = content.replace('>Quick Integration<', ' data-i18n="code_label">Quick Integration</')
content = content.replace('>5 Minutes to Migrate<', ' data-i18n="code_title">5 Minutes to Migrate</')
content = content.replace('>Replace your OpenAI API key with Asiatek AI and you\'re ready.<br>                    Same API, better pricing.<', ' data-i18n="code_desc">Replace your OpenAI API key with Asiatek AI and you\'re ready. Same API, better pricing.</')
content = content.replace('>Copy<', ' data-i18n="code_copy">Copy</')
content = content.replace('>Migration completed in 5 minutes.<', ' data-i18n="code_migration_title">Migration completed in 5 minutes.</')
content = content.replace('>No code refactoring needed. Your existing OpenAI SDK code works with Asiatek AI <br>                    after just changing the API key and base URL.<', ' data-i18n="code_migration_desc">No code refactoring needed. Your existing OpenAI SDK code works with Asiatek AI after just changing the API key and base URL.</')

# Footer
content = content.replace('>Product<', ' data-i18n="footer_product">Product</')
content = content.replace('>Resources<', ' data-i18n="footer_resources">Resources</')
content = content.replace('>Company<', ' data-i18n="footer_company">Company</')
content = content.replace('>Getting Started<', ' data-i18n="footer_getting_started">Getting Started</')
content = content.replace('>API Reference<', ' data-i18n="footer_api_ref">API Reference</')
content = content.replace('>SDK Libraries<', ' data-i18n="footer_sdk">SDK Libraries</')
content = content.replace('>Status Page<', ' data-i18n="footer_status">Status Page</')
content = content.replace('>About Us<', ' data-i18n="footer_about">About Us</')
content = content.replace('>Blog<', ' data-i18n="footer_blog">Blog</')
content = content.replace('>Contact<', ' data-i18n="footer_contact">Contact</')
content = content.replace('>Privacy Policy<', ' data-i18n="footer_privacy">Privacy Policy</')
content = content.replace('>Changelog<', ' data-i18n="footer_changelog">Changelog</')

# ============================================
# 4. Add i18n JavaScript before </body>
# ============================================
i18n_js = '''
    <script>
        // ============================================
        // i18n - Internationalization System
        // ============================================
        const i18n = {
            en: {
                // Navigation
                nav_signin: 'Sign In',
                nav_get_api_key: 'Get API Key',
                nav_pricing: 'Pricing',
                nav_languages: 'Languages',
                nav_features: 'Features',
                nav_api_docs: 'API Docs',
                // Hero
                hero_badge: 'Now available in Singapore',
                hero_title_highlight: 'Built for Southeast Asia',
                hero_btn_api_key: 'Get API Key — Free',
                hero_btn_start: 'Get Started Free',
                hero_btn_docs: 'View Documentation',
                hero_subtitle: '201 languages supported including Thai, Vietnamese, Indonesian, and Malay. Up to 98% cheaper than GPT-4o with OpenAI-compatible API.',
                stat_languages: 'Languages',
                stat_cost_savings: 'Cost Savings',
                stat_migration: 'Migration',
                stat_sla: 'SLA Uptime',
                // Pricing Comparison
                pricing_compare_label: 'Pricing Comparison',
                pricing_compare_title: 'Dramatically Lower Cost',
                pricing_compare_desc: 'Compare our pricing with major providers. Asiatek AI offers enterprise-grade quality at startup-friendly prices.',
                table_provider: 'Provider',
                table_model: 'Model',
                table_input: 'Input ($/M tokens)',
                table_output: 'Output ($/M tokens)',
                // Languages Section
                lang_section_label: 'Language Support',
                lang_section_title: '201 Languages, Including All Southeast Asian',
                lang_section_desc: 'Native-level understanding of Thai, Vietnamese, Indonesian, Malay, and more. Perfect for building products for the 700M+ Southeast Asian market.',
                lang_more: 'More languages including regional dialects',
                // Quickstart
                quickstart_title: 'Start in 3 Lines of Code',
                quickstart_desc: 'Get started with Asiatek AI in seconds. No complex setup required.',
                quickstart_step1: 'Install the OpenAI SDK — it\'s the same one you already use',
                quickstart_step2: 'Set your API key and base URL to Asiatek AI endpoint',
                quickstart_step3: 'Start building — all existing OpenAI code works instantly',
                // Models Section
                models_label: 'Supported Models',
                models_title: '9 Models Available',
                models_desc: 'Choose from a variety of models optimized for different use cases.',
                table_category: 'Category',
                table_input_price: 'Input Price',
                table_output_price: 'Output Price',
                // Features Section
                features_label: 'Features',
                features_title: 'Everything You Need',
                features_desc: 'Built for production with enterprise-grade reliability and developer-friendly tools.',
                feature_dual_engine_title: 'Dual Engine Architecture',
                feature_dual_engine_desc: 'Choose between Qwen for enterprise-grade multilingual tasks with SLA guarantees, or DeepSeek for cost-effective inference. Switch anytime based on your needs.',
                feature_openai_title: 'OpenAI Compatible API',
                feature_openai_desc: 'Drop-in replacement for OpenAI. Change one line of code and you\'re done. Supports Chat Completions, Completions, Embeddings, and more.',
                feature_singapore_title: 'Singapore Data Centers',
                feature_singapore_desc: 'Low latency for Southeast Asian users. PDPA compliant with enterprise-grade security including SOC 2, ISO 27001 certifications.',
                feature_regional_title: 'Regional Optimization',
                feature_regional_desc: 'Models specifically fine-tuned for Southeast Asian languages, cultures, and business contexts. Better understanding of local nuances.',
                feature_sla_title: '99.9% SLA',
                feature_sla_desc: 'Enterprise-grade uptime guarantee with redundant infrastructure. 24/7 support for business-critical applications.',
                feature_scaling_title: 'Flexible Scaling',
                feature_scaling_desc: 'From prototype to production. Auto-scaling infrastructure handles from 1 to billions of requests seamlessly.',
                // Pricing Section
                pricing_label: 'Pricing Plans',
                pricing_title: 'Simple, Transparent Pricing',
                pricing_desc: 'Start free, scale as you grow. No hidden fees, no surprises.',
                // Starter
                starter_name: 'Starter',
                starter_desc: 'Perfect for prototypes and experiments',
                starter_feat_1: 'Free API key, no credit card',
                starter_feat_2: 'DeepSeek & Qwen models',
                starter_feat_3: 'OpenAI-compatible API',
                starter_feat_4: '10 RPM rate limit',
                starter_feat_5: 'Community support',
                starter_btn: 'Get Free API Key',
                // Pro
                pro_name: 'Pro',
                pro_desc: 'For growing applications and teams',
                pro_feat_1: 'Pay-per-use (token billing)',
                pro_feat_2: 'All models: DeepSeek + Qwen',
                pro_feat_3: 'Higher rate limits (60 RPM)',
                pro_feat_4: 'Priority API access',
                pro_feat_5: 'Email support',
                pro_feat_6: 'Usage analytics dashboard',
                pro_btn: 'Get Started',
                // Enterprise
                enterprise_name: 'Enterprise',
                enterprise_desc: 'Custom solutions for high volume',
                enterprise_feat_1: 'Volume discounts on tokens',
                enterprise_feat_2: 'All models + priority routing',
                enterprise_feat_3: 'Custom rate limits',
                enterprise_feat_4: '99.9% SLA guarantee',
                enterprise_feat_5: 'Dedicated support channel',
                enterprise_feat_6: 'Custom model fine-tuning',
                enterprise_btn: 'Contact Sales',
                // Code Section
                code_label: 'Quick Integration',
                code_title: '5 Minutes to Migrate',
                code_desc: 'Replace your OpenAI API key with Asiatek AI and you\'re ready. Same API, better pricing.',
                code_copy: 'Copy',
                code_copied: 'Copied!',
                code_migration_title: 'Migration completed in 5 minutes.',
                code_migration_desc: 'No code refactoring needed. Your existing OpenAI SDK code works with Asiatek AI after just changing the API key and base URL.',
                // Footer
                footer_product: 'Product',
                footer_resources: 'Resources',
                footer_company: 'Company',
                footer_pricing: 'Pricing',
                footer_languages: 'Languages',
                footer_features: 'Features',
                footer_changelog: 'Changelog',
                footer_getting_started: 'Getting Started',
                footer_api_ref: 'API Reference',
                footer_sdk: 'SDK Libraries',
                footer_status: 'Status Page',
                footer_about: 'About Us',
                footer_blog: 'Blog',
                footer_contact: 'Contact',
                footer_privacy: 'Privacy Policy',
                footer_copyright: '© 2025 Asiatek AI. All rights reserved. Singapore.'
            },
            zh: {
                // Navigation
                nav_signin: '登录',
                nav_get_api_key: '获取 API Key',
                nav_pricing: '价格',
                nav_languages: '语言',
                nav_features: '功能',
                nav_api_docs: 'API 文档',
                // Hero
                hero_badge: '现已支持新加坡',
                hero_title_highlight: '专为东南亚打造',
                hero_btn_api_key: '免费获取 API Key',
                hero_btn_start: '免费开始',
                hero_btn_docs: '查看文档',
                hero_subtitle: '支持 201 种语言，包括泰语、越南语、印尼语和马来语。比 GPT-4o 便宜高达 98%，兼容 OpenAI API。',
                stat_languages: '支持语言',
                stat_cost_savings: '成本节省',
                stat_migration: '迁移时间',
                stat_sla: 'SLA 可用性',
                // Pricing Comparison
                pricing_compare_label: '价格对比',
                pricing_compare_title: '成本大幅降低',
                pricing_compare_desc: '与主要供应商比较价格。Asiatek AI 以初创企业友好的价格提供企业级质量。',
                table_provider: '供应商',
                table_model: '模型',
                table_input: '输入 ($/M tokens)',
                table_output: '输出 ($/M tokens)',
                // Languages Section
                lang_section_label: '语言支持',
                lang_section_title: '201 种语言，覆盖所有东南亚语言',
                lang_section_desc: '原生级别的泰语、越南语、印尼语、马来语等理解。非常适合为 7 亿+ 东南亚市场开发产品。',
                lang_more: '更多语言，包括地区方言',
                // Quickstart
                quickstart_title: '三行代码快速开始',
                quickstart_desc: '几秒钟内开始使用 Asiatek AI。无需复杂设置。',
                quickstart_step1: '安装 OpenAI SDK — 就是你已经在用的那个',
                quickstart_step2: '设置你的 API key 和 base URL 指向 Asiatek AI',
                quickstart_step3: '开始构建 — 所有现有的 OpenAI 代码都能立即工作',
                // Models Section
                models_label: '支持的模型',
                models_title: '9 种模型可选',
                models_desc: '选择针对不同用例优化的各种模型。',
                table_category: '类别',
                table_input_price: '输入价格',
                table_output_price: '输出价格',
                // Features Section
                features_label: '功能',
                features_title: '您需要的一切',
                features_desc: '为企业生产环境构建，具有企业级可靠性和开发者友好的工具。',
                feature_dual_engine_title: '双引擎架构',
                feature_dual_engine_desc: '选择 Qwen 处理具有 SLA 保证的企业级多语言任务，或选择 DeepSeek 进行成本效益高的推理。可随时根据需求切换。',
                feature_openai_title: '兼容 OpenAI API',
                feature_openai_desc: 'OpenAI 的直接替代品。只需修改一行代码即可。支持聊天补全、补全、嵌入等。',
                feature_singapore_title: '新加坡数据中心',
                feature_singapore_desc: '为东南亚用户提供低延迟。符合 PDPA 法规，拥有 SOC 2、ISO 27001 等企业级安全认证。',
                feature_regional_title: '区域优化',
                feature_regional_desc: '针对东南亚语言、文化和商业环境特别微调的模型。更深入理解当地细微差别。',
                feature_sla_title: '99.9% SLA',
                feature_sla_desc: '具有冗余基础设施的企业级正常运行时间保证。24/7 全天候支持关键业务应用。',
                feature_scaling_title: '灵活扩展',
                feature_scaling_desc: '从原型到生产。自动扩展基础设施可无缝处理从 1 次到数十亿次请求。',
                // Pricing Section
                pricing_label: '定价方案',
                pricing_title: '简单透明的定价',
                pricing_desc: '免费开始，随成长付费。无隐藏费用，无意外惊喜。',
                // Starter
                starter_name: '入门版',
                starter_desc: '非常适合原型和实验',
                starter_feat_1: '免费 API key，无需信用卡',
                starter_feat_2: 'DeepSeek 和 Qwen 模型',
                starter_feat_3: 'OpenAI 兼容 API',
                starter_feat_4: '10 RPM 速率限制',
                starter_feat_5: '社区支持',
                starter_btn: '获取免费 API Key',
                // Pro
                pro_name: '专业版',
                pro_desc: '适合成长中的应用和团队',
                pro_feat_1: '按需付费（按 token 计费）',
                pro_feat_2: '所有模型：DeepSeek + Qwen',
                pro_feat_3: '更高速率限制 (60 RPM)',
                pro_feat_4: '优先 API 访问',
                pro_feat_5: '邮件支持',
                pro_feat_6: '使用分析仪表板',
                pro_btn: '立即开始',
                // Enterprise
                enterprise_name: '企业版',
                enterprise_desc: '高容量的定制解决方案',
                enterprise_feat_1: '批量 token 折扣',
                enterprise_feat_2: '所有模型 + 优先路由',
                enterprise_feat_3: '自定义速率限制',
                enterprise_feat_4: '99.9% SLA 保证',
                enterprise_feat_5: '专属支持通道',
                enterprise_feat_6: '自定义模型微调',
                enterprise_btn: '联系销售',
                // Code Section
                code_label: '快速集成',
                code_title: '5 分钟完成迁移',
                code_desc: '将您的 OpenAI API key 替换为 Asiatek AI 即可。同样的 API，更好的价格。',
                code_copy: '复制',
                code_copied: '已复制！',
                code_migration_title: '5 分钟完成迁移。',
                code_migration_desc: '无需代码重构。您现有的 OpenAI SDK 代码只需更改 API key 和 base URL 即可与 Asiatek AI 配合使用。',
                // Footer
                footer_product: '产品',
                footer_resources: '资源',
                footer_company: '公司',
                footer_pricing: '价格',
                footer_languages: '语言',
                footer_features: '功能',
                footer_changelog: '更新日志',
                footer_getting_started: '快速开始',
                footer_api_ref: 'API 参考',
                footer_sdk: 'SDK 库',
                footer_status: '状态页面',
                footer_about: '关于我们',
                footer_blog: '博客',
                footer_contact: '联系我们',
                footer_privacy: '隐私政策',
                footer_copyright: '© 2025 Asiatek AI. 保留所有权利。新加坡。'
            },
            th: {
                // Navigation
                nav_signin: 'เข้าสู่ระบบ',
                nav_get_api_key: 'รับ API Key',
                nav_pricing: 'ราคา',
                nav_languages: 'ภาษา',
                nav_features: 'ฟีเจอร์',
                nav_api_docs: 'เอกสาร API',
                // Hero
                hero_badge: 'พร้อมให้บริการแล้วในสิงคโปร์',
                hero_title_highlight: 'สร้างมาเพื่อเอเชียตะวันออกเฉียงใต้',
                hero_btn_api_key: 'รับ API Key ฟรี',
                hero_btn_start: 'เริ่มต้นฟรี',
                hero_btn_docs: 'ดูเอกสาร',
                hero_subtitle: 'รองรับ 201 ภาษา รวมถึงภาษาไทย เวียดนาม อินโดนีเซีย และมลายู ราคาถูกกว่า GPT-4o สูงสุด 98% พร้อม API ที่เข้ากันได้กับ OpenAI',
                stat_languages: 'ภาษา',
                stat_cost_savings: 'ประหยัดค่าใช้จ่าย',
                stat_migration: 'ย้ายระบบ',
                stat_sla: 'SLA Uptime',
                // Pricing Comparison
                pricing_compare_label: 'เปรียบเทียบราคา',
                pricing_compare_title: 'ต้นทุนต่ำลงอย่างมาก',
                pricing_compare_desc: 'เปรียบเทียบราคากับผู้ให้บริการรายใหญ่ Asiatek AI นำเสนอคุณภาพระดับองค์กรในราคาที่เป็นมิตรกับสตาร์ทอัพ',
                table_provider: 'ผู้ให้บริการ',
                table_model: 'โมเดล',
                table_input: 'อินพุต ($/M tokens)',
                table_output: 'เอาต์พุต ($/M tokens)',
                // Languages Section
                lang_section_label: 'รองรับภาษา',
                lang_section_title: '201 ภาษา รวมถึงภาษาเอเชียตะวันออกเฉียงใต้ทั้งหมด',
                lang_section_desc: 'ความเข้าใจระดับเจ้าของภาษาสำหรับภาษาไทย เวียดนาม อินโดนีเซีย มลายู และอื่นๆ เหมาะสำหรับการสร้างผลิตภัณฑ์สำหรับตลาดเอเชียตะวันออกเฉียงใต้กว่า 700 ล้านคน',
                lang_more: 'ภาษาอื่นๆ อีกมากมาย รวมถึงภาษาถิ่น',
                // Quickstart
                quickstart_title: 'เริ่มต้นด้วยโค้ดเพียง 3 บรรทัด',
                quickstart_desc: 'เริ่มใช้ Asiatek AI ในไม่กี่วินาที ไม่ต้องตั้งค่าซับซ้อน',
                quickstart_step1: 'ติดตั้ง OpenAI SDK — ใช้ตัวเดียวกับที่คุณมีอยู่แล้ว',
                quickstart_step2: 'ตั้งค่า API key และ base URL ไปยัง Asiatek AI endpoint',
                quickstart_step3: 'เริ่มสร้าง — โค้ด OpenAI ที่มีอยู่ทำงานได้ทันที',
                // Models Section
                models_label: 'โมเดลที่รองรับ',
                models_title: '9 โมเดลให้เลือก',
                models_desc: 'เลือกจากโมเดลต่างๆ ที่ปรับให้เหมาะกับกรณีการใช้งานที่แตกต่างกัน',
                table_category: 'หมวดหมู่',
                table_input_price: 'ราคาอินพุต',
                table_output_price: 'ราคาเอาต์พุต',
                // Features Section
                features_label: 'ฟีเจอร์',
                features_title: 'ทุกอย่างที่คุณต้องการ',
                features_desc: 'สร้างมาเพื่อการผลิตจริง พร้อมความน่าเชื่อถือระดับองค์กรและเครื่องมือที่เป็นมิตรกับนักพัฒนา',
                feature_dual_engine_title: 'สถาปัตยกรรม Dual Engine',
                feature_dual_engine_desc: 'เลือก Qwen สำหรับงานหลายภาษาระดับองค์กรพร้อม SLA หรือ DeepSeek สำหรับการอนุมานที่คุ้มค่า สลับได้ตามต้องการ',
                feature_openai_title: 'API เข้ากันได้กับ OpenAI',
                feature_openai_desc: 'ทดแทน OpenAI ได้ทันที แก้ไขโค้ดแค่บรรทัดเดียว แล้วเริ่มใช้งานได้เลย รองรับ Chat Completions, Completions, Embeddings และอื่นๆ',
                feature_singapore_title: 'ดาต้าเซนเตอร์สิงคโปร์',
                feature_singapore_desc: 'เลเทนซี่ต่ำสำหรับผู้ใช้เอเชียตะวันออกเฉียงใต้ ปฏิบัติตาม PDPA พร้อมความปลอดภัยระดับองค์กร รวมถึง SOC 2, ISO 27001',
                feature_regional_title: 'การปรับให้เหมาะกับภูมิภาค',
                feature_regional_desc: 'โมเดลที่ปรับแต่งเฉพาะสำหรับภาษา วัฒนธรรม และบริบททางธุรกิจของเอเชียตะวันออกเฉียงใต้ เข้าใจความแตกต่างในพื้นที่ได้ดีขึ้น',
                feature_sla_title: 'SLA 99.9%',
                feature_sla_desc: 'รับประกัน uptime ระดับองค์กรพร้อมโครงสร้างพื้นฐานสำรอง สนับสนุน 24/7 สำหรับแอปพลิเคชันที่สำคัญต่อธุรกิจ',
                feature_scaling_title: 'การขยายขนาดแบบยืดหยุ่น',
                feature_scaling_desc: 'จากต้นแบบสู่การผลิตจริง โครงสร้างพื้นฐาน auto-scaling รองรับตั้งแต่ 1 ถึงพันล้านคำขอได้อย่างราบรื่น',
                // Pricing Section
                pricing_label: 'แพ็กเกจราคา',
                pricing_title: 'ราคาชัดเจน โปร่งใส',
                pricing_desc: 'เริ่มต้นฟรี ขยายตามที่คุณเติบโต ไม่มีค่าซ่อน ไม่มีเซอร์ไพรส์',
                // Starter
                starter_name: 'สำหรับผู้เริ่มต้น',
                starter_desc: 'เหมาะสำหรับต้นแบบและการทดลอง',
                starter_feat_1: 'API key ฟรี ไม่ต้องใช้บัตรเครดิต',
                starter_feat_2: 'โมเดล DeepSeek และ Qwen',
                starter_feat_3: 'API เข้ากันได้กับ OpenAI',
                starter_feat_4: 'จำกัด 10 RPM',
                starter_feat_5: 'สนับสนุนจากชุมชน',
                starter_btn: 'รับ API Key ฟรี',
                // Pro
                pro_name: 'Pro',
                pro_desc: 'สำหรับแอปที่กำลังเติบโตและทีม',
                pro_feat_1: 'จ่ายตามการใช้ (คิดตาม token)',
                pro_feat_2: 'โมเดลทั้งหมด: DeepSeek + Qwen',
                pro_feat_3: 'จำกัดสูงขึ้น (60 RPM)',
                pro_feat_4: 'API แบบอำนาจจริง',
                pro_feat_5: 'สนับสนุนทางอีเมล',
                pro_feat_6: 'แดชบอร์ดวิเคราะห์การใช้งาน',
                pro_btn: 'เริ่มต้น',
                // Enterprise
                enterprise_name: 'สำหรับองค์กร',
                enterprise_desc: 'โซลูชันแบบกำหนดเองสำหรับปริมาณสูง',
                enterprise_feat_1: 'ส่วนลด token จำนวนมาก',
                enterprise_feat_2: 'โมเดลทั้งหมด + การกำหนดเส้นทางแบบอำนาจจริง',
                enterprise_feat_3: 'จำกัดแบบกำหนดเอง',
                enterprise_feat_4: 'รับประกัน SLA 99.9%',
                enterprise_feat_5: 'ช่องสนับสนุนเฉพาะ',
                enterprise_feat_6: 'ปรับแต่งโมเดล',
                enterprise_btn: 'ติดต่อฝ่ายขาย',
                // Code Section
                code_label: 'การรวมเข้าอย่างรวดเร็ว',
                code_title: 'ย้ายระบบใน 5 นาที',
                code_desc: 'แทนที่ OpenAI API key ด้วย Asiatek AI แล้วเริ่มใช้งานได้เลย API เดิม ราคาดีกว่า',
                code_copy: 'คัดลอก',
                code_copied: 'คัดลอกแล้ว!',
                code_migration_title: 'ย้ายระบบเสร็จใน 5 นาที',
                code_migration_desc: 'ไม่ต้อง refactor โค้ด โค้ด OpenAI SDK ที่มีอยู่ใช้งานกับ Asiatek AI ได้หลังแก้ API key และ base URL',
                // Footer
                footer_product: 'ผลิตภัณฑ์',
                footer_resources: 'แหล่งข้อมูล',
                footer_company: 'บริษัท',
                footer_pricing: 'ราคา',
                footer_languages: 'ภาษา',
                footer_features: 'ฟีเจอร์',
                footer_changelog: 'บันทึกการอัปเดต',
                footer_getting_started: 'เริ่มต้นใช้งาน',
                footer_api_ref: 'API Reference',
                footer_sdk: 'ไลบรารี SDK',
                footer_status: 'หน้าสถานะ',
                footer_about: 'เกี่ยวกับเรา',
                footer_blog: 'บล็อก',
                footer_contact: 'ติดต่อ',
                footer_privacy: 'นโยบายความเป็นส่วนตัว',
                footer_copyright: '© 2025 Asiatek AI. สงวนลิขสิทธิ์ สิงคโปร์'
            },
            vi: {
                // Navigation
                nav_signin: 'Đăng nhập',
                nav_get_api_key: 'Lấy API Key',
                nav_pricing: 'Bảng giá',
                nav_languages: 'Ngôn ngữ',
                nav_features: 'Tính năng',
                nav_api_docs: 'Tài liệu API',
                // Hero
                hero_badge: 'Đã có mặt tại Singapore',
                hero_title_highlight: 'Được xây dựng cho Đông Nam Á',
                hero_btn_api_key: 'Lấy API Key — Miễn phí',
                hero_btn_start: 'Bắt đầu miễn phí',
                hero_btn_docs: 'Xem tài liệu',
                hero_subtitle: 'Hỗ trợ 201 ngôn ngữ bao gồm Thái, Việt, Indonesia và Malay. Giá rẻ hơn GPT-4o tới 98% với API tương thích OpenAI.',
                stat_languages: 'Ngôn ngữ',
                stat_cost_savings: 'Tiết kiệm chi phí',
                stat_migration: 'Di chuyển',
                stat_sla: 'SLA Uptime',
                // Pricing Comparison
                pricing_compare_label: 'So sánh giá',
                pricing_compare_title: 'Chi phí thấp hơn đáng kể',
                pricing_compare_desc: 'So sánh giá với các nhà cung cấp lớn. Asiatek AI cung cấp chất lượng doanh nghiệp với giá thân thiện với startup.',
                table_provider: 'Nhà cung cấp',
                table_model: 'Mô hình',
                table_input: 'Đầu vào ($/M tokens)',
                table_output: 'Đầu ra ($/M tokens)',
                // Languages Section
                lang_section_label: 'Hỗ trợ ngôn ngữ',
                lang_section_title: '201 ngôn ngữ, bao gồm tất cả Đông Nam Á',
                lang_section_desc: 'Hiểu ngôn ngữ gốc về tiếng Thái, Việt, Indonesia, Malay và hơn thế nữa. Hoàn hảo để xây dựng sản phẩm cho thị trường 700M+ Đông Nam Á.',
                lang_more: 'Nhiều ngôn ngữ hơn, bao gồm cả phương ngữ',
                // Quickstart
                quickstart_title: 'Bắt đầu với 3 dòng code',
                quickstart_desc: 'Bắt đầu với Asiatek AI trong vài giây. Không cần cài đặt phức tạp.',
                quickstart_step1: 'Cài đặt OpenAI SDK — cùng một SDK mà bạn đang dùng',
                quickstart_step2: 'Đặt API key và base URL thành Asiatek AI endpoint',
                quickstart_step3: 'Bắt đầu xây dựng — tất cả code OpenAI hiện có đều hoạt động ngay',
                // Models Section
                models_label: 'Mô hình được hỗ trợ',
                models_title: '9 mô hình có sẵn',
                models_desc: 'Chọn từ nhiều mô hình được tối ưu cho các trường hợp sử dụng khác nhau.',
                table_category: 'Danh mục',
                table_input_price: 'Giá đầu vào',
                table_output_price: 'Giá đầu ra',
                // Features Section
                features_label: 'Tính năng',
                features_title: 'Tất cả những gì bạn cần',
                features_desc: 'Được xây dựng cho sản xuất với độ tin cậy cấp doanh nghiệp và công cụ thân thiện với nhà phát triển.',
                feature_dual_engine_title: 'Kiến trúc Dual Engine',
                feature_dual_engine_desc: 'Chọn Qwen cho các tác vụ đa ngôn ngữ cấp doanh nghiệp với SLA, hoặc DeepSeek để suy luận tiết kiệm chi phí. Chuyển đổi bất kỳ lúc nào theo nhu cầu.',
                feature_openai_title: 'API tương thích OpenAI',
                feature_openai_desc: 'Thay thế trực tiếp cho OpenAI. Chỉ cần thay đổi một dòng code là xong. Hỗ trợ Chat Completions, Completions, Embeddings và hơn thế.',
                feature_singapore_title: 'Trung tâm dữ liệu Singapore',
                feature_singapore_desc: 'Độ trễ thấp cho người dùng Đông Nam Á. Tuân thủ PDPA với bảo mật cấp doanh nghiệp bao gồm SOC 2, ISO 27001.',
                feature_regional_title: 'Tối ưu hóa theo khu vực',
                feature_regional_desc: 'Mô hình được tinh chỉnh đặc biệt cho ngôn ngữ, văn hóa và bối cảnh kinh doanh Đông Nam Á. Hiểu rõ hơn về sắc thái địa phương.',
                feature_sla_title: 'SLA 99.9%',
                feature_sla_desc: 'Đảm bảo uptime cấp doanh nghiệp với cơ sở hạ tầng dự phòng. Hỗ trợ 24/7 cho các ứng dụng quan trọng cho kinh doanh.',
                feature_scaling_title: 'Mở rộng linh hoạt',
                feature_scaling_desc: 'Từ prototype đến production. Cơ sở hạ tầng auto-scaling xử lý từ 1 đến hàng tỷ yêu cầu một cách liền mạch.',
                // Pricing Section
                pricing_label: 'Gói giá',
                pricing_title: 'Giá cả minh bạch, đơn giản',
                pricing_desc: 'Bắt đầu miễn phí, mở rộng khi bạn phát triển. Không phí ẩn, không bất ngờ.',
                // Starter
                starter_name: 'Starter',
                starter_desc: 'Hoàn hảo cho prototype và thử nghiệm',
                starter_feat_1: 'API key miễn phí, không cần thẻ tín dụng',
                starter_feat_2: 'Mô hình DeepSeek & Qwen',
                starter_feat_3: 'API tương thích OpenAI',
                starter_feat_4: 'Giới hạn 10 RPM',
                starter_feat_5: 'Hỗ trợ cộng đồng',
                starter_btn: 'Lấy API Key miễn phí',
                // Pro
                pro_name: 'Pro',
                pro_desc: 'Cho ứng dụng và nhóm đang phát triển',
                pro_feat_1: 'Trả tiền theo sử dụng (tính theo token)',
                pro_feat_2: 'Tất cả mô hình: DeepSeek + Qwen',
                pro_feat_3: 'Giới hạn cao hơn (60 RPM)',
                pro_feat_4: 'API ưu tiên',
                pro_feat_5: 'Hỗ trợ qua email',
                pro_feat_6: 'Bảng phân tích sử dụng',
                pro_btn: 'Bắt đầu',
                // Enterprise
                enterprise_name: 'Doanh nghiệp',
                enterprise_desc: 'Giải pháp tùy chỉnh cho khối lượng lớn',
                enterprise_feat_1: 'Giảm giá token số lượng lớn',
                enterprise_feat_2: 'Tất cả mô hình + định tuyến ưu tiên',
                enterprise_feat_3: 'Giới hạn tùy chỉnh',
                enterprise_feat_4: 'Đảm bảo SLA 99.9%',
                enterprise_feat_5: 'Kênh hỗ trợ riêng',
                enterprise_feat_6: 'Tinh chỉnh mô hình tùy chỉnh',
                enterprise_btn: 'Liên hệ bán hàng',
                // Code Section
                code_label: 'Tích hợp nhanh',
                code_title: 'Di chuyển trong 5 phút',
                code_desc: 'Thay API key OpenAI của bạn bằng Asiatek AI và sẵn sàng sử dụng. Cùng API, giá tốt hơn.',
                code_copy: 'Sao chép',
                code_copied: 'Đã sao chép!',
                code_migration_title: 'Di chuyển hoàn tất trong 5 phút.',
                code_migration_desc: 'Không cần refactor code. Code OpenAI SDK hiện có hoạt động với Asiatek AI chỉ sau khi thay đổi API key và base URL.',
                // Footer
                footer_product: 'Sản phẩm',
                footer_resources: 'Tài nguyên',
                footer_company: 'Công ty',
                footer_pricing: 'Bảng giá',
                footer_languages: 'Ngôn ngữ',
                footer_features: 'Tính năng',
                footer_changelog: 'Nhật ký thay đổi',
                footer_getting_started: 'Bắt đầu',
                footer_api_ref: 'API Reference',
                footer_sdk: 'Thư viện SDK',
                footer_status: 'Trang trạng thái',
                footer_about: 'Về chúng tôi',
                footer_blog: 'Blog',
                footer_contact: 'Liên hệ',
                footer_privacy: 'Chính sách bảo mật',
                footer_copyright: '© 2025 Asiatek AI. Bảo lưu mọi quyền. Singapore.'
            },
            id: {
                // Navigation
                nav_signin: 'Masuk',
                nav_get_api_key: 'Dapatkan API Key',
                nav_pricing: 'Harga',
                nav_languages: 'Bahasa',
                nav_features: 'Fitur',
                nav_api_docs: 'Dokumentasi API',
                // Hero
                hero_badge: 'Tersedia di Singapura',
                hero_title_highlight: 'Dibangun untuk Asia Tenggara',
                hero_btn_api_key: 'Dapatkan API Key — Gratis',
                hero_btn_start: 'Mulai Gratis',
                hero_btn_docs: 'Lihat Dokumentasi',
                hero_subtitle: 'Mendukung 201 bahasa termasuk Thai, Vietnam, Indonesia, dan Melayu. Hingga 98% lebih murah dari GPT-4o dengan API yang kompatibel dengan OpenAI.',
                stat_languages: 'Bahasa',
                stat_cost_savings: 'Hemat Biaya',
                stat_migration: 'Migrasi',
                stat_sla: 'SLA Uptime',
                // Pricing Comparison
                pricing_compare_label: 'Perbandingan Harga',
                pricing_compare_title: 'Biaya Lebih Rendah Signifikan',
                pricing_compare_desc: 'Bandingkan harga kami dengan penyedia besar. Asiatek AI menawarkan kualitas enterprise dengan harga yang ramah startup.',
                table_provider: 'Penyedia',
                table_model: 'Model',
                table_input: 'Input ($/M tokens)',
                table_output: 'Output ($/M tokens)',
                // Languages Section
                lang_section_label: 'Dukungan Bahasa',
                lang_section_title: '201 Bahasa, Termasuk Semua Asia Tenggara',
                lang_section_desc: 'Pemahaman tingkat asli untuk Thai, Vietnam, Indonesia, Melayu dan lainnya. Sempurna untuk membangun produk untuk pasar 700M+ Asia Tenggara.',
                lang_more: 'Lebih banyak bahasa termasuk dialek regional',
                // Quickstart
                quickstart_title: 'Mulai dengan 3 Baris Kode',
                quickstart_desc: 'Mulai dengan Asiatek AI dalam hitungan detik. Tidak perlu setup kompleks.',
                quickstart_step1: 'Instal OpenAI SDK — sama dengan yang sudah Anda gunakan',
                quickstart_step2: 'Atur API key dan base URL ke endpoint Asiatek AI',
                quickstart_step3: 'Mulai membangun — semua kode OpenAI yang ada langsung berfungsi',
                // Models Section
                models_label: 'Model yang Didukung',
                models_title: '9 Model Tersedia',
                models_desc: 'Pilih dari berbagai model yang dioptimalkan untuk kasus penggunaan berbeda.',
                table_category: 'Kategori',
                table_input_price: 'Harga Input',
                table_output_price: 'Harga Output',
                // Features Section
                features_label: 'Fitur',
                features_title: 'Segalanya yang Anda Butuhkan',
                features_desc: 'Dibangun untuk produksi dengan keandalan enterprise dan alat yang ramah pengembang.',
                feature_dual_engine_title: 'Arsitektur Dual Engine',
                feature_dual_engine_desc: 'Pilih Qwen untuk tugas multibahasa enterprise dengan SLA, atau DeepSeek untuk inferensi hemat biaya. Beralih kapan saja sesuai kebutuhan.',
                feature_openai_title: 'API Kompatibel OpenAI',
                feature_openai_desc: 'Pengganti langsung untuk OpenAI. Ubah satu baris kode dan selesai. Mendukung Chat Completions, Completions, Embeddings, dan lainnya.',
                feature_singapore_title: 'Data Center Singapura',
                feature_singapore_desc: 'Latensi rendah untuk pengguna Asia Tenggara. Sesuai PDPA dengan keamanan enterprise termasuk sertifikasi SOC 2, ISO 27001.',
                feature_regional_title: 'Optimasi Regional',
                feature_regional_desc: 'Model yang disesuaikan khusus untuk bahasa, budaya, dan konteks bisnis Asia Tenggara. Pemahaman lebih baik tentang nuansa lokal.',
                feature_sla_title: 'SLA 99.9%',
                feature_sla_desc: 'Jaminan uptime enterprise dengan infrastruktur redundan. Dukungan 24/7 untuk aplikasi kritis bisnis.',
                feature_scaling_title: 'Skalabilitas Fleksibel',
                feature_scaling_desc: 'Dari prototipe hingga produksi. Infrastruktur auto-scaling menangani dari 1 hingga miliaran permintaan dengan mulus.',
                // Pricing Section
                pricing_label: 'Paket Harga',
                pricing_title: 'Harga Sederhana, Transparan',
                pricing_desc: 'Mulai gratis, skala sesuai pertumbuhan Anda. Tanpa biaya tersembunyi, tanpa kejutan.',
                // Starter
                starter_name: 'Starter',
                starter_desc: 'Sempurna untuk prototipe dan eksperimen',
                starter_feat_1: 'API key gratis, tanpa kartu kredit',
                starter_feat_2: 'Model DeepSeek & Qwen',
                starter_feat_3: 'API kompatibel OpenAI',
                starter_feat_4: 'Batas 10 RPM',
                starter_feat_5: 'Dukungan komunitas',
                starter_btn: 'Dapatkan API Key Gratis',
                // Pro
                pro_name: 'Pro',
                pro_desc: 'Untuk aplikasi dan tim yang berkembang',
                pro_feat_1: 'Bayar per penggunaan (tagihan token)',
                pro_feat_2: 'Semua model: DeepSeek + Qwen',
                pro_feat_3: 'Batas lebih tinggi (60 RPM)',
                pro_feat_4: 'Akses API prioritas',
                pro_feat_5: 'Dukungan email',
                pro_feat_6: 'Dashboard analitik penggunaan',
                pro_btn: 'Mulai',
                // Enterprise
                enterprise_name: 'Enterprise',
                enterprise_desc: 'Solusi kustom untuk volume tinggi',
                enterprise_feat_1: 'Diskon token volume',
                enterprise_feat_2: 'Semua model + routing prioritas',
                enterprise_feat_3: 'Batas kustom',
                enterprise_feat_4: 'Jaminan SLA 99.9%',
                enterprise_feat_5: 'Kanal dukungan khusus',
                enterprise_feat_6: 'Fine-tuning model kustom',
                enterprise_btn: 'Hubungi Penjualan',
                // Code Section
                code_label: 'Integrasi Cepat',
                code_title: 'Migrasi dalam 5 Menit',
                code_desc: 'Ganti API key OpenAI Anda dengan Asiatek AI dan siap. API sama, harga lebih baik.',
                code_copy: 'Salin',
                code_copied: 'Disalin!',
                code_migration_title: 'Migrasi selesai dalam 5 menit.',
                code_migration_desc: 'Tidak perlu refactor kode. Kode SDK OpenAI yang ada berfungsi dengan Asiatek AI hanya dengan mengubah API key dan base URL.',
                // Footer
                footer_product: 'Produk',
                footer_resources: 'Sumber daya',
                footer_company: 'Perusahaan',
                footer_pricing: 'Harga',
                footer_languages: 'Bahasa',
                footer_features: 'Fitur',
                footer_changelog: 'Catatan Perubahan',
                footer_getting_started: 'Memulai',
                footer_api_ref: 'Referensi API',
                footer_sdk: 'Pustaka SDK',
                footer_status: 'Halaman Status',
                footer_about: 'Tentang Kami',
                footer_blog: 'Blog',
                footer_contact: 'Kontak',
                footer_privacy: 'Kebijakan Privasi',
                footer_copyright: '© 2025 Asiatek AI. Hak cipta dilindungi. Singapura.'
            },
            ms: {
                // Navigation
                nav_signin: 'Daftar Masuk',
                nav_get_api_key: 'Dapatkan API Key',
                nav_pricing: 'Harga',
                nav_languages: 'Bahasa',
                nav_features: 'Ciri-ciri',
                nav_api_docs: 'Dokumentasi API',
                // Hero
                hero_badge: 'Tersedia di Singapura',
                hero_title_highlight: 'Dibina untuk Asia Tenggara',
                hero_btn_api_key: 'Dapatkan API Key — Percuma',
                hero_btn_start: 'Mula Percuma',
                hero_btn_docs: 'Lihat Dokumentasi',
                hero_subtitle: 'Menyokong 201 bahasa termasuk Thai, Vietnam, Indonesia dan Melayu. Harga sehingga 98% lebih murah daripada GPT-4o dengan API yang serasi dengan OpenAI.',
                stat_languages: 'Bahasa',
                stat_cost_savings: 'Jimat Kos',
                stat_migration: 'Pemindahan',
                stat_sla: 'SLA Uptime',
                // Pricing Comparison
                pricing_compare_label: 'Perbandingan Harga',
                pricing_compare_title: 'Kos Lebih Rendah dengan Drastik',
                pricing_compare_desc: 'Bandingkan harga kami dengan pembekal utama. Asiatek AI menawarkan kualiti enterprise dengan harga mesra pemula.',
                table_provider: 'Pembekal',
                table_model: 'Model',
                table_input: 'Input ($/M tokens)',
                table_output: 'Output ($/M tokens)',
                // Languages Section
                lang_section_label: 'Sokongan Bahasa',
                lang_section_title: '201 Bahasa, Termasuk Semua Asia Tenggara',
                lang_section_desc: 'Pemahaman peringkat asli untuk Thai, Vietnam, Indonesia, Melayu dan banyak lagi. Sesuai untuk membina produk untuk pasaran 700M+ Asia Tenggara.',
                lang_more: 'Lebih banyak bahasa termasuk dialek serantau',
                // Quickstart
                quickstart_title: 'Mula dengan 3 Baris Kod',
                quickstart_desc: 'Mula dengan Asiatek AI dalam beberapa saat. Tiada persediaan kompleks diperlukan.',
                quickstart_step1: 'Pasang OpenAI SDK — ia adalah yang sama yang anda sudah gunakan',
                quickstart_step2: 'Tetapkan API key dan base URL anda ke endpoint Asiatek AI',
                quickstart_step3: 'Mula membina — semua kod OpenAI sedia ada berfungsi dengan serta-merta',
                // Models Section
                models_label: 'Model Disokong',
                models_title: '9 Model Tersedia',
                models_desc: 'Pilih dari pelbagai model yang dioptimumkan untuk kes penggunaan berbeza.',
                table_category: 'Kategori',
                table_input_price: 'Harga Input',
                table_output_price: 'Harga Output',
                // Features Section
                features_label: 'Ciri-ciri',
                features_title: 'Segala yang Anda Perlukan',
                features_desc: 'Dibina untuk pengeluaran dengan kebolehpercayaan enterprise dan alat yang mesra pembangun.',
                feature_dual_engine_title: 'Seni Bina Dual Engine',
                feature_dual_engine_desc: 'Pilih Qwen untuk tugas berbilang bahasa enterprise dengan SLA, atau DeepSeek untuk inferens yang menjimatkan kos. Tukar bila-bila masa mengikut keperluan anda.',
                feature_openai_title: 'API Serasi OpenAI',
                feature_openai_desc: 'Penggantian terus untuk OpenAI. Tukar satu baris kod dan anda sudah selesai. Menyokong Chat Completions, Completions, Embeddings dan banyak lagi.',
                feature_singapore_title: 'Pusat Data Singapura',
                feature_singapore_desc: 'Latensi rendah untuk pengguna Asia Tenggara. Pematuhan PDPA dengan keselamatan enterprise termasuk pensijilan SOC 2, ISO 27001.',
                feature_regional_title: 'Pengoptimuman Serantau',
                feature_regional_desc: 'Model yang disesuaikan khusus untuk bahasa, budaya dan konteks perniagaan Asia Tenggara. Pemahaman yang lebih baik tentang nuansa tempatan.',
                feature_sla_title: 'SLA 99.9%',
                feature_sla_desc: 'Jaminan uptime enterprise dengan infrastruktur redundan. Sokongan 24/7 untuk aplikasi kritikal perniagaan.',
                feature_scaling_title: 'Skalabiliti Fleksibel',
                feature_scaling_desc: 'Dari prototaip ke pengeluaran. Infrastruktur auto-scaling mengendalikan dari 1 hingga berbilion permintaan dengan licin.',
                // Pricing Section
                pricing_label: 'Pelan Harga',
                pricing_title: 'Harga Mudah, Telus',
                pricing_desc: 'Mula secara percuma, skala mengikut pertumbuhan anda. Tiada yuran tersembunyi, tiada kejutan.',
                // Starter
                starter_name: 'Starter',
                starter_desc: 'Sempurna untuk prototaip dan eksperimen',
                starter_feat_1: 'API key percuma, tanpa kad kredit',
                starter_feat_2: 'Model DeepSeek & Qwen',
                starter_feat_3: 'API serasi OpenAI',
                starter_feat_4: 'Had 10 RPM',
                starter_feat_5: 'Sokongan komuniti',
                starter_btn: 'Dapatkan API Key Percuma',
                // Pro
                pro_name: 'Pro',
                pro_desc: 'Untuk aplikasi dan pasukan yang berkembang',
                pro_feat_1: 'Bayar-guna (bil tokens)',
                pro_feat_2: 'Semua model: DeepSeek + Qwen',
                pro_feat_3: 'Had lebih tinggi (60 RPM)',
                pro_feat_4: 'Akses API keutamaan',
                pro_feat_5: 'Sokongan e-mel',
                pro_feat_6: 'Papan pemuka analitik penggunaan',
                pro_btn: 'Mula',
                // Enterprise
                enterprise_name: 'Enterprise',
                enterprise_desc: 'Penyelesaian tersuai untuk volum tinggi',
                enterprise_feat_1: 'Diskaun token volum',
                enterprise_feat_2: 'Semua model + penghalaan keutamaan',
                enterprise_feat_3: 'Had tersuai',
                enterprise_feat_4: 'Jaminan SLA 99.9%',
                enterprise_feat_5: 'Saluran sokongan khusus',
                enterprise_feat_6: 'Fine-tuning model tersuai',
                enterprise_btn: 'Hubungi Jualan',
                // Code Section
                code_label: 'Integrasi Pantas',
                code_title: 'Pemindahan dalam 5 Minit',
                code_desc: 'Gantikan API key OpenAI anda dengan Asiatek AI dan anda sudah bersedia. API yang sama, harga lebih baik.',
                code_copy: 'Salin',
                code_copied: 'Disalin!',
                code_migration_title: 'Pemindahan selesai dalam 5 minit.',
                code_migration_desc: 'Tiada refaktor kod diperlukan. Kod SDK OpenAI sedia ada berfungsi dengan Asiatek AI hanya dengan menukar API key dan base URL.',
                // Footer
                footer_product: 'Produk',
                footer_resources: 'Sumber',
                footer_company: 'Syarikat',
                footer_pricing: 'Harga',
                footer_languages: 'Bahasa',
                footer_features: 'Ciri-ciri',
                footer_changelog: 'Log Perubahan',
                footer_getting_started: ' Bermula',
                footer_api_ref: 'Rujukan API',
                footer_sdk: 'Pustaka SDK',
                footer_status: 'Halaman Status',
                footer_about: 'Tentang Kami',
                footer_blog: 'Blog',
                footer_contact: 'Hubungi',
                footer_privacy: 'Dasar Privasi',
                footer_copyright: '© 2025 Asiatek AI. Hak cipta terpelihara. Singapura.'
            }
        };

        // Language configuration
        const languageConfig = {
            en: { flag: '🇺🇸', name: 'English', native: 'English' },
            zh: { flag: '🇨🇳', name: '中文', native: 'Chinese' },
            th: { flag: '🇹🇭', name: 'ไทย', native: 'Thai' },
            vi: { flag: '🇻🇳', name: 'Tiếng Việt', native: 'Vietnamese' },
            id: { flag: '🇮🇩', name: 'Bahasa Indonesia', native: 'Indonesian' },
            ms: { flag: '🇲🇾', name: 'Bahasa Melayu', native: 'Malay' }
        };

        // Country code to language mapping
        const countryToLang = {
            // Southeast Asia
            TH: 'th', VI: 'vi', VN: 'vi',
            ID: 'id', MY: 'ms', SG: 'en',
            PH: 'en', MM: 'en', KH: 'en', LA: 'en',
            // East Asia
            CN: 'zh', HK: 'zh', TW: 'zh', MO: 'zh',
            JP: 'en', KR: 'en',
            // South Asia
            IN: 'en', BD: 'en', PK: 'en', LK: 'en',
            // Others
            US: 'en', GB: 'en', AU: 'en', CA: 'en',
            DEFAULT: 'en'
        };

        // Current language
        let currentLang = 'en';

        // Get saved language preference
        function getSavedLanguage() {
            return localStorage.getItem('asiatek_language');
        }

        // Save language preference
        function saveLanguage(lang) {
            localStorage.setItem('asiatek_language', lang);
        }

        // Detect language from GeoIP
        async function detectLanguageFromGeoIP() {
            try {
                // Try ip-api.com first (free, no API key required)
                const response = await fetch('https://ip-api.com/json/?fields=status,countryCode');
                const data = await response.json();
                if (data.status === 'success' && data.countryCode) {
                    return countryToLang[data.countryCode] || countryToLang.DEFAULT;
                }
            } catch (e) {
                console.log('GeoIP detection failed, falling back to browser language');
            }
            return null;
        }

        // Detect language from browser
        function detectBrowserLanguage() {
            const browserLang = navigator.language || navigator.userLanguage || '';
            const langCode = browserLang.split('-')[0].toLowerCase();
            if (i18n[langCode]) {
                return langCode;
            }
            // Check if it's a regional variant
            if (browserLang.includes('-')) {
                const region = browserLang.split('-')[1].toUpperCase();
                if (countryToLang[region]) {
                    return countryToLang[region];
                }
            }
            return null;
        }

        // Initialize i18n
        async function initI18n() {
            // Priority: localStorage > GeoIP > Browser > English
            let detectedLang = getSavedLanguage();
            
            if (!detectedLang) {
                detectedLang = await detectLanguageFromGeoIP();
            }
            
            if (!detectedLang) {
                detectedLang = detectBrowserLanguage();
            }
            
            if (!detectedLang) {
                detectedLang = 'en';
            }
            
            setLanguage(detectedLang);
        }

        // Set language
        function setLanguage(lang) {
            if (!i18n[lang]) {
                lang = 'en';
            }
            
            currentLang = lang;
            saveLanguage(lang);
            
            // Update all translatable elements
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (i18n[lang][key]) {
                    el.textContent = i18n[lang][key];
                }
            });
            
            // Update document language
            document.documentElement.lang = lang;
            
            // Update language switcher UI
            updateLanguageSwitcherUI(lang);
            
            // Update copy button text
            updateCopyButtonText();
        }

        // Update language switcher UI
        function updateLanguageSwitcherUI(lang) {
            const config = languageConfig[lang];
            if (config) {
                document.getElementById('currentLangFlag').textContent = config.flag;
                document.getElementById('currentLangName').textContent = config.name;
            }
            
            // Update active state
            document.querySelectorAll('.lang-option').forEach(opt => {
                opt.classList.toggle('active', opt.dataset.lang === lang);
            });
        }

        // Update copy button text
        function updateCopyButtonText() {
            const copyBtn = document.querySelector('.code-copy');
            if (copyBtn) {
                const text = i18n[currentLang]['code_copy'] || i18n['en']['code_copy'];
                copyBtn.textContent = text;
            }
        }

        // Language switcher toggle
        document.getElementById('langBtn').addEventListener('click', (e) => {
            e.stopPropagation();
            document.getElementById('langSwitcher').classList.toggle('open');
        });

        // Language option click
        document.querySelectorAll('.lang-option').forEach(opt => {
            opt.addEventListener('click', () => {
                const lang = opt.dataset.lang;
                setLanguage(lang);
                document.getElementById('langSwitcher').classList.remove('open');
            });
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            document.getElementById('langSwitcher').classList.remove('open');
        });

        // Initialize
        initI18n();
    </script>
'''

content = content.replace('</body>', i18n_js + '</body>')

# Write modified content
with open('/tmp/asiatek-landing/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("i18n support added successfully!")
