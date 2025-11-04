#!/usr/bin/env node
/**
 * Fast affiliate database builder using Node.js
 * Parses MASTER lists, verifies URLs in parallel, outputs clean JSON
 */

const fs = require('fs').promises;
const path = require('path');
const https = require('https');
const http = require('http');
const { URL } = require('url');

// Paths
const ROOT = path.join(__dirname, '..', '..');
const MON_DIR = path.join(ROOT, '04-Monetization');
const MASTER_ALL = path.join(MON_DIR, 'MASTER-PRODUCTS-LIST.md');
const MASTER_ACCEPTED = path.join(MON_DIR, 'MASTER-PRODUCTS-LIST.ACCEPTED.md');
const OUTPUT_JSON = path.join(MON_DIR, 'affiliate-database.json');

// Config
const CONCURRENT_CHECKS = 10; // Verify 10 URLs at once
const TIMEOUT_MS = 5000; // 5 second timeout per URL

/**
 * Extract redirect URL from 2Performant quicklink
 */
function extractRedirectUrl(quicklink) {
  try {
    const url = new URL(quicklink);
    const redirectTo = url.searchParams.get('redirect_to');
    return redirectTo ? decodeURIComponent(redirectTo) : null;
  } catch {
    return null;
  }
}

/**
 * Verify URL returns 200 OK (with timeout)
 */
function verifyUrl(url) {
  return new Promise((resolve) => {
    const timeout = setTimeout(() => {
      resolve(false);
    }, TIMEOUT_MS);

    const urlObj = new URL(url);
    const protocol = urlObj.protocol === 'https:' ? https : http;

    const req = protocol.request({
      method: 'HEAD',
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      timeout: TIMEOUT_MS,
      headers: { 'User-Agent': 'Mozilla/5.0 IntelesMon/1.0' }
    }, (res) => {
      clearTimeout(timeout);
      resolve(res.statusCode >= 200 && res.statusCode < 300);
    });

    req.on('error', () => {
      clearTimeout(timeout);
      resolve(false);
    });

    req.on('timeout', () => {
      req.destroy();
      clearTimeout(timeout);
      resolve(false);
    });

    req.end();
  });
}

/**
 * Verify URLs in batches (parallel but controlled)
 */
async function verifyUrlsBatch(products) {
  const results = [];
  
  for (let i = 0; i < products.length; i += CONCURRENT_CHECKS) {
    const batch = products.slice(i, i + CONCURRENT_CHECKS);
    const promises = batch.map(async (product) => {
      const verified = await verifyUrl(product.destination_url);
      return { ...product, verified };
    });
    
    const batchResults = await Promise.all(promises);
    results.push(...batchResults);
    
    // Progress
    process.stdout.write(`\r   Checked ${Math.min(i + CONCURRENT_CHECKS, products.length)}/${products.length}...`);
  }
  
  console.log(''); // New line after progress
  return results;
}

/**
 * Parse a MASTER list markdown file
 */
async function parseMasterList(filePath, source) {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    const lines = content.split('\n');
    
    const products = [];
    let currentCategory = null;
    let currentTags = [];
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      
      // Category header (## 📚 CĂRȚI & PSIHOLOGIE)
      if (line.startsWith('## ') && !line.startsWith('## ✨')) {
        currentCategory = line.substring(3).trim();
        
        // Look for tags on next line
        if (i + 1 < lines.length && lines[i + 1].trim().startsWith('*Tags:')) {
          const tagsMatch = lines[i + 1].match(/\*Tags:\s*(.+?)\*/);
          if (tagsMatch) {
            currentTags = tagsMatch[1].split(',').map(t => t.trim());
          }
        }
      }
      
      // Product section (### Product Name)
      else if (line.startsWith('### ') && currentCategory) {
        const title = line.substring(4).trim();
        let commission = null;
        let cookieDays = null;
        let useCases = [];
        let quicklink = null;
        
        // Scan ahead for metadata
        let j = i + 1;
        while (j < lines.length) {
          const l = lines[j].trim();
          
          // Stop at next section
          if (l.startsWith('###') || l.startsWith('##') || l.startsWith('---')) {
            break;
          }
          
          // Extract commission & cookie
          if (l.startsWith('**Comision:**')) {
            const commMatch = l.match(/(\d+(?:\.\d+)?%)/);
            if (commMatch) commission = commMatch[1];
            
            const cookieMatch = l.match(/Cookie:\*?\*?\s*(\d+)\s*zile/i);
            if (cookieMatch) cookieDays = parseInt(cookieMatch[1]);
            
            const useMatch = l.match(/Potrivit pentru:\*?\*?\s*(.+?)(?:\*\*|$)/i);
            if (useMatch) {
              useCases = useMatch[1].split(',').map(u => u.trim());
            }
          }
          
          // Find quicklink in fenced code block
          if (l === '```') {
            j++;
            while (j < lines.length && lines[j].trim() !== '```') {
              const candidate = lines[j].trim();
              if (candidate.startsWith('http') && candidate.includes('2performant.com')) {
                quicklink = candidate;
                break;
              }
              j++;
            }
          }
          
          j++;
        }
        
        // If we found a valid quicklink, add the product
        if (quicklink && currentCategory) {
          const destUrl = extractRedirectUrl(quicklink) || quicklink;
          const merchant = new URL(destUrl).hostname.replace('www.', '');
          
          products.push({
            name: title,
            merchant,
            category: currentCategory,
            commission,
            cookie_days: cookieDays,
            quicklink,
            destination_url: destUrl,
            tags: [...currentTags],
            use_cases: useCases,
            verified: false,
            last_checked: '',
            source
          });
        }
        
        i = j - 1;
      }
    }
    
    return products;
  } catch (error) {
    console.error(`Error parsing ${filePath}:`, error.message);
    return [];
  }
}

/**
 * Main execution
 */
async function main() {
  console.log('📖 Parsing MASTER lists...\n');
  
  // Parse both sources
  const [acceptedProducts, allProducts] = await Promise.all([
    parseMasterList(MASTER_ACCEPTED, 'accepted'),
    parseMasterList(MASTER_ALL, 'all')
  ]);
  
  console.log(`✅ Parsed ${acceptedProducts.length} products from ACCEPTED`);
  console.log(`✅ Parsed ${allProducts.length} products from ALL`);
  
  // Deduplicate (accepted wins)
  const seenNames = new Set(acceptedProducts.map(p => p.name));
  const uniqueAll = allProducts.filter(p => !seenNames.has(p.name));
  const products = [...acceptedProducts, ...uniqueAll];
  
  console.log(`✅ Total unique products: ${products.length}\n`);
  
  // Verify URLs in parallel batches
  console.log(`🔍 Verifying URLs (${CONCURRENT_CHECKS} at a time)...`);
  const now = new Date().toISOString().split('.')[0] + 'Z';
  const verifiedProducts = await verifyUrlsBatch(products);
  
  // Update last_checked timestamp
  verifiedProducts.forEach(p => p.last_checked = now);
  
  const verifiedCount = verifiedProducts.filter(p => p.verified).length;
  console.log(`✅ Verified ${verifiedCount}/${verifiedProducts.length} URLs\n`);
  
  // Group by category
  const byCategory = {};
  verifiedProducts.forEach(product => {
    const cat = product.category || 'Uncategorized';
    if (!byCategory[cat]) byCategory[cat] = [];
    byCategory[cat].push(product);
  });
  
  // Build database
  const database = {
    meta: {
      generated: now,
      total_products: verifiedProducts.length,
      verified_products: verifiedCount,
      categories: Object.keys(byCategory).length,
      sources: ['MASTER-PRODUCTS-LIST.ACCEPTED.md', 'MASTER-PRODUCTS-LIST.md']
    },
    by_category: byCategory,
    all_products: verifiedProducts
  };
  
  // Save
  await fs.writeFile(OUTPUT_JSON, JSON.stringify(database, null, 2), 'utf-8');
  console.log(`💾 Saved to ${path.relative(ROOT, OUTPUT_JSON)}\n`);
  
  // Summary
  console.log('📊 Database summary:');
  console.log(`   Total products: ${database.meta.total_products}`);
  console.log(`   Verified URLs: ${database.meta.verified_products}`);
  console.log(`   Categories: ${database.meta.categories}\n`);
  
  console.log('📂 Categories:');
  Object.entries(byCategory).sort().forEach(([cat, items]) => {
    const verified = items.filter(i => i.verified).length;
    console.log(`   - ${cat}: ${items.length} products (${verified} verified)`);
  });
  
  console.log('\n✅ Done!');
}

// Run
main().catch(console.error);
