// lang-detect.js - IP-based Language Detection for Asiatek AI Tools
// Must be loaded before i18n.js

(function() {
  'use strict';
  
  // Configuration
  const CACHE_DURATION = 7 * 24 * 60 * 60 * 1000; // 7 days in milliseconds
  const STORAGE_KEY = 'asiatek_lang_detection';
  const API_URL = 'https://ipapi.co/json/';
  
  // Country code to language mapping
  const COUNTRY_TO_LANG = {
    // Chinese regions
    'CN': 'zh', 'TW': 'zh', 'HK': 'zh', 'SG': 'zh',
    // Japanese
    'JP': 'ja',
    // Korean
    'KR': 'ko',
    // Russian
    'RU': 'ru',
    // Arabic speaking
    'SA': 'ar', 'AE': 'ar', 'EG': 'ar', 'IQ': 'ar', 'JO': 'ar', 'KW': 'ar', 'LB': 'ar', 'LY': 'ar', 'MA': 'ar', 'OM': 'ar', 'QA': 'ar', 'SY': 'ar', 'TN': 'ar', 'YE': 'ar', 'DZ': 'ar', 'BH': 'ar', 'SD': 'ar', 'SO': 'ar', 'ER': 'ar',
    // Hindi speaking
    'IN': 'hi',
    // German speaking
    'DE': 'de', 'AT': 'de', 'CH': 'de', 'LI': 'de', 'LU': 'de',
    // French speaking
    'FR': 'fr', 'BE': 'fr', 'MC': 'fr', 'CA': 'fr',
    // Portuguese speaking
    'BR': 'pt', 'PT': 'pt', 'AO': 'pt', 'MZ': 'pt', 'GW': 'pt', 'CV': 'pt', 'TL': 'pt',
    // Spanish speaking
    'ES': 'es', 'MX': 'es', 'AR': 'es', 'CO': 'es', 'CL': 'es', 'PE': 'es', 'VE': 'es', 'EC': 'es', 'UY': 'es', 'PY': 'es', 'BO': 'es', 'HN': 'es', 'GT': 'es', 'SV': 'es', 'NI': 'es', 'CR': 'es', 'PA': 'es', 'DO': 'es', 'CU': 'es', 'PR': 'es',
    // English default
    'US': 'en', 'GB': 'en', 'AU': 'en', 'CA': 'en', 'NZ': 'en', 'IE': 'en', 'ZA': 'en', 'NG': 'en', 'KE': 'en', 'PH': 'en', 'MY': 'en', 'ID': 'en', 'TH': 'en', 'VN': 'en', 'PK': 'en', 'BD': 'en', 'EG': 'en', 'NL': 'en', 'IT': 'en', 'PL': 'en', 'TR': 'en', 'UA': 'en', 'RO': 'en', 'GR': 'en', 'CZ': 'en', 'SE': 'en', 'NO': 'en', 'DK': 'en', 'FI': 'en', 'HU': 'en', 'IL': 'en', 'RS': 'en', 'BG': 'en', 'HR': 'en', 'SK': 'en', 'LT': 'en', 'SI': 'en', 'LV': 'en', 'EE': 'en', 'IE': 'en'
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
  
  // Get browser language
  function getBrowserLang() {
    const navLang = navigator.language || navigator.userLanguage || '';
    const shortLang = navLang.split('-')[0].toLowerCase();
    
    if (SUPPORTED_LANGS.includes(shortLang)) {
      return shortLang;
    }
    
    // Check for Chinese variants
    if (navLang.startsWith('zh')) {
      return 'zh';
    }
    
    return 'en';
  }
  
  // Map country code to language
  function countryToLang(countryCode) {
    if (!countryCode) return 'en';
    return COUNTRY_TO_LANG[countryCode.toUpperCase()] || 'en';
  }
  
  // Detect language from IP
  function detectFromIP(callback) {
    const cached = getCachedData();
    if (cached) {
      callback(cached.lang);
      return;
    }
    
    // Use ipapi.co for geolocation
    fetch(API_URL)
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => {
        if (data && data.country_code) {
          const lang = countryToLang(data.country_code);
          setCachedData(data.country_code, lang);
          callback(lang);
        } else {
          callback(getBrowserLang());
        }
      })
      .catch(error => {
        console.warn('IP detection failed, using browser language:', error);
        callback(getBrowserLang());
      });
  }
  
  // Main detection function
  function detectLanguage() {
    // Priority 1: Check if user already selected a language
    const savedLang = localStorage.getItem('asiatek_lang');
    if (savedLang && SUPPORTED_LANGS.includes(savedLang)) {
      return savedLang;
    }
    
    // Priority 2: Check cache
    const cached = getCachedData();
    if (cached && cached.lang) {
      // Apply cached language but don't save again
      return cached.lang;
    }
    
    // Priority 3: Get from IP (async, will update page later)
    detectFromIP(function(ipLang) {
      // Only apply if no saved preference
      const currentSaved = localStorage.getItem('asiatek_lang');
      if (!currentSaved && typeof i18nUtils !== 'undefined') {
        i18nUtils.setLang(ipLang);
      }
    });
    
    // Return browser language immediately while IP detection runs
    return getBrowserLang();
  }
  
  // Initialize language detection
  function init() {
    // Check if already initialized
    if (window.asiatekLangInitialized) return;
    window.asiatekLangInitialized = true;
    
    // Run detection
    const detectedLang = detectLanguage();
    
    // If detected lang is different from current, update
    if (typeof i18nUtils !== 'undefined' && !localStorage.getItem('asiatek_lang')) {
      // Small delay to ensure i18n.js is loaded
      setTimeout(function() {
        if (detectedLang !== 'en' && i18n[detectedLang]) {
          i18nUtils.setLang(detectedLang);
        }
      }, 10);
    }
  }
  
  // Create language selector HTML
  function createLanguageSelector() {
    const currentLang = localStorage.getItem('asiatek_lang') || 'en';
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
  
  // Change language function (called from selector)
  window.changeLanguage = function(lang) {
    if (typeof i18nUtils !== 'undefined') {
      i18nUtils.setLang(lang);
    }
  };
  
  // Expose functions globally
  window.asiatekLang = {
    detect: detectLanguage,
    getSupportedLangs: function() { return SUPPORTED_LANGS; },
    getLangNames: function() { return LANG_NAMES; },
    createSelector: createLanguageSelector,
    isRTL: function(lang) { return lang === 'ar'; }
  };
  
  // Auto-init on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
