// lang-detect.js - IP-based Language Detection for Asiatek AI Tools
// Must be loaded before i18n.js

(function() {
  'use strict';
  
  // Configuration
  const CACHE_DURATION = 7 * 24 * 60 * 60 * 1000; // 7 days in milliseconds
  const STORAGE_KEY = 'asiatek_lang_detection';
  const IP_APIS = [
    'https://ipapi.co/json/',
    'https://ip-api.com/json/?fields=countryCode',
    'https://api.ipgeolocation.io/ip?fields=country_code'
  ];
  
  // Country code to language mapping
  const COUNTRY_TO_LANG = {
    // Chinese regions
    'CN': 'zh', 'TW': 'zh', 'HK': 'zh', 'MO': 'zh', 'SG': 'zh',
    // Japanese
    'JP': 'ja',
    // Korean
    'KR': 'ko', 'KP': 'ko',
    // Russian
    'RU': 'ru', 'BY': 'ru', 'KZ': 'ru',
    // Arabic speaking
    'SA': 'ar', 'AE': 'ar', 'EG': 'ar', 'IQ': 'ar', 'JO': 'ar', 'KW': 'ar',
    'LB': 'ar', 'LY': 'ar', 'MA': 'ar', 'OM': 'ar', 'QA': 'ar', 'SY': 'ar',
    'TN': 'ar', 'YE': 'ar', 'DZ': 'ar', 'BH': 'ar', 'SD': 'ar', 'PS': 'ar',
    // Hindi speaking
    'IN': 'hi', 'NP': 'hi',
    // German speaking
    'DE': 'de', 'AT': 'de', 'CH': 'de', 'LI': 'de', 'LU': 'de',
    // French speaking
    'FR': 'fr', 'BE': 'fr', 'MC': 'fr',
    // Portuguese speaking
    'BR': 'pt', 'PT': 'pt', 'AO': 'pt', 'MZ': 'pt',
    // Spanish speaking
    'ES': 'es', 'MX': 'es', 'AR': 'es', 'CO': 'es', 'CL': 'es', 'PE': 'es',
    'VE': 'es', 'EC': 'es', 'UY': 'es', 'PY': 'es', 'BO': 'es', 'HN': 'es',
    'GT': 'es', 'SV': 'es', 'NI': 'es', 'CR': 'es', 'PA': 'es', 'DO': 'es',
    'CU': 'es', 'PR': 'es',
    // English default
    'US': 'en', 'GB': 'en', 'AU': 'en', 'CA': 'en', 'NZ': 'en', 'IE': 'en',
    'ZA': 'en', 'NG': 'en', 'KE': 'en', 'PH': 'en', 'MY': 'en', 'ID': 'en',
    'TH': 'en', 'VN': 'en', 'PK': 'en', 'BD': 'en', 'NL': 'en', 'IT': 'en',
    'PL': 'en', 'TR': 'en', 'UA': 'en', 'RO': 'en', 'GR': 'en', 'CZ': 'en',
    'SE': 'en', 'NO': 'en', 'DK': 'en', 'FI': 'en', 'HU': 'en', 'IL': 'en',
    'RS': 'en', 'BG': 'en', 'HR': 'en', 'SK': 'en', 'LT': 'en', 'SI': 'en',
    'LV': 'en', 'EE': 'en'
  };
  
  // Supported languages
  const SUPPORTED_LANGS = ['en', 'zh', 'es', 'pt', 'ja', 'ko', 'ru', 'ar', 'hi', 'de', 'fr'];
  
  // Language names (in their own language)
  const LANG_NAMES = {
    'en': 'English',
    'zh': '中文',
    'es': 'Español',
    'pt': 'Português',
    'ja': '日本語',
    'ko': '한국어',
    'ru': 'Русский',
    'ar': 'العربية',
    'hi': 'हिन्दी',
    'de': 'Deutsch',
    'fr': 'Français'
  };
  
  // Cache management
  function getCachedData() {
    try {
      const cached = localStorage.getItem(STORAGE_KEY);
      if (cached) {
        const data = JSON.parse(cached);
        if (data.timestamp && (Date.now() - data.timestamp < CACHE_DURATION)) {
          return data;
        }
      }
    } catch (e) {
      console.warn('Error reading language cache:', e);
    }
    return null;
  }
  
  function setCachedData(country, lang) {
    try {
      const data = {
        country: country,
        lang: lang,
        timestamp: Date.now()
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      console.warn('Error writing language cache:', e);
    }
  }
  
  // Get browser language - with smart Chinese detection
  function getBrowserLang() {
    const navLang = navigator.language || navigator.userLanguage || '';
    const shortLang = navLang.split('-')[0].toLowerCase();
    
    // Chinese variants all map to zh
    if (navLang.toLowerCase().startsWith('zh')) {
      return 'zh';
    }
    
    if (SUPPORTED_LANGS.includes(shortLang)) {
      return shortLang;
    }
    
    return 'en';
  }
  
  // Map country code to language
  function countryToLang(countryCode) {
    if (!countryCode) return null;
    return COUNTRY_TO_LANG[countryCode.toUpperCase()] || null;
  }
  
  // Fetch with timeout
  function fetchWithTimeout(url, timeout) {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    return fetch(url, { signal: controller.signal })
      .then(response => {
        clearTimeout(id);
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      });
  }
  
  // Try multiple IP APIs in sequence
  function detectFromIP(callback) {
    const cached = getCachedData();
    if (cached && cached.lang) {
      callback(cached.lang);
      return;
    }
    
    let apiIndex = 0;
    
    function tryNext() {
      if (apiIndex >= IP_APIS.length) {
        // All APIs failed, fall back to browser language
        console.warn('All IP APIs failed, using browser language');
        callback(getBrowserLang());
        return;
      }
      
      const apiUrl = IP_APIS[apiIndex++];
      
      fetchWithTimeout(apiUrl, 3000)
        .then(data => {
          // Different APIs return different field names
          const countryCode = data.country_code || data.countryCode || data.country;
          if (countryCode) {
            const lang = countryToLang(countryCode);
            if (lang) {
              setCachedData(countryCode, lang);
              callback(lang);
            } else {
              setCachedData(countryCode, 'en');
              callback('en');
            }
          } else {
            tryNext();
          }
        })
        .catch(() => {
          tryNext();
        });
    }
    
    tryNext();
  }
  
  // Main detection function
  function detectLanguage() {
    // Priority 1: User explicitly selected language
    const savedLang = localStorage.getItem('asiatek_lang');
    if (savedLang && SUPPORTED_LANGS.includes(savedLang)) {
      return savedLang;
    }
    
    // Priority 2: IP detection cache (7 days)
    const cached = getCachedData();
    if (cached && cached.lang) {
      return cached.lang;
    }
    
    // Priority 3: Get from IP (async, will update page when ready)
    detectFromIP(function(ipLang) {
      const currentSaved = localStorage.getItem('asiatek_lang');
      if (!currentSaved && typeof i18nUtils !== 'undefined') {
        i18nUtils.setLang(ipLang);
      }
    });
    
    // Return browser language immediately while IP detection runs async
    // This ensures Chinese browsers show Chinese even if IP API is slow
    return getBrowserLang();
  }
  
  // Initialize
  function init() {
    if (window.asiatekLangInitialized) return;
    window.asiatekLangInitialized = true;
    
    const detectedLang = detectLanguage();
    
    // Apply detected language after a short delay
    if (typeof i18nUtils !== 'undefined' && !localStorage.getItem('asiatek_lang')) {
      setTimeout(function() {
        if (i18n[detectedLang]) {
          i18nUtils.setLang(detectedLang);
        }
      }, 50);
    }
  }
  
  // Create language selector
  function createLanguageSelector() {
    const currentLang = localStorage.getItem('asiatek_lang') || 
                       (getCachedData() ? getCachedData().lang : null) || 
                       getBrowserLang();
    const isRTL = currentLang === 'ar';
    
    let html = '<select id="lang-selector" class="text-xs px-2 py-1 border rounded bg-white cursor-pointer' + 
               (isRTL ? ' rtl:mr-2 rtl:ml-0' : ' ml-2 mr-0') + 
               '" onchange="window.changeLanguage(this.value)" style="min-width:70px;">';
    
    SUPPORTED_LANGS.forEach(lang => {
      const selected = lang === currentLang ? ' selected' : '';
      html += '<option value="' + lang + '"' + selected + '>' + LANG_NAMES[lang] + '</option>';
    });
    
    html += '</select>';
    return html;
  }
  
  // Change language
  window.changeLanguage = function(lang) {
    localStorage.setItem('asiatek_lang', lang);
    if (typeof i18nUtils !== 'undefined') {
      i18nUtils.setLang(lang);
    }
  };
  
  // Expose
  window.asiatekLang = {
    detect: detectLanguage,
    getSupportedLangs: function() { return SUPPORTED_LANGS; },
    getLangNames: function() { return LANG_NAMES; },
    createSelector: createLanguageSelector,
    isRTL: function(lang) { return lang === 'ar'; }
  };
  
  // Auto-init
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
