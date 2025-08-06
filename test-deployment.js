#!/usr/bin/env node

/**
 * Test script to verify Vercel deployment is working
 * Usage: node test-deployment.js [YOUR_VERCEL_URL]
 */

const https = require('https');
const http = require('http');

const VERCEL_URL = process.argv[2] || 'your-app.vercel.app';
const BASE_URL = VERCEL_URL.startsWith('http') ? VERCEL_URL : `https://${VERCEL_URL}`;

console.log('🧪 Testing AI Education Agent Deployment');
console.log('==========================================');
console.log(`🔗 Testing URL: ${BASE_URL}`);
console.log('');

// Test endpoints
const tests = [
  {
    name: 'Main App',
    path: '/',
    expected: 'AI Education Agent'
  },
  {
    name: 'Demo Page',
    path: '/demo.html',
    expected: 'AI Education Agent'
  },
  {
    name: 'Health API',
    path: '/api/health',
    expected: 'AI Education Agent API'
  },
  {
    name: 'Worksheet API',
    path: '/api/worksheets/ai-generate',
    method: 'POST',
    data: JSON.stringify({
      subject: 'mathematics',
      topic: 'algebra',
      questions: 3,
      type: 'mcq'
    }),
    expected: 'worksheet_id'
  }
];

async function testEndpoint(test) {
  return new Promise((resolve) => {
    const url = new URL(test.path, BASE_URL);
    const options = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname,
      method: test.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'AI-Education-Agent-Test/1.0'
      }
    };

    const client = url.protocol === 'https:' ? https : http;
    
    const req = client.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        const success = res.statusCode === 200 && data.includes(test.expected);
        resolve({
          success,
          status: res.statusCode,
          data: data.substring(0, 200) + (data.length > 200 ? '...' : ''),
          test
        });
      });
    });

    req.on('error', (error) => {
      resolve({
        success: false,
        error: error.message,
        test
      });
    });

    if (test.data) {
      req.write(test.data);
    }
    
    req.end();
  });
}

async function runTests() {
  console.log('🚀 Starting tests...\n');
  
  let passed = 0;
  let failed = 0;

  for (const test of tests) {
    process.stdout.write(`Testing ${test.name}... `);
    
    const result = await testEndpoint(test);
    
    if (result.success) {
      console.log('✅ PASS');
      passed++;
    } else {
      console.log('❌ FAIL');
      console.log(`   Status: ${result.status || 'Error'}`);
      console.log(`   Error: ${result.error || 'Response did not contain expected content'}`);
      if (result.data) {
        console.log(`   Response: ${result.data}`);
      }
      failed++;
    }
  }

  console.log('\n📊 Test Results:');
  console.log('================');
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📈 Success Rate: ${Math.round((passed / (passed + failed)) * 100)}%`);

  if (failed === 0) {
    console.log('\n🎉 All tests passed! Your AI Education Agent is working perfectly!');
    console.log(`🔗 Access your app at: ${BASE_URL}`);
  } else {
    console.log('\n⚠️  Some tests failed. Check the deployment and try again.');
    console.log('💡 Tip: Wait a few minutes for deployment to complete, then retest.');
  }
}

// Show usage if no URL provided
if (!process.argv[2]) {
  console.log('Usage: node test-deployment.js YOUR_VERCEL_URL');
  console.log('Example: node test-deployment.js my-ai-agent.vercel.app');
  console.log('Example: node test-deployment.js https://my-ai-agent.vercel.app');
  process.exit(1);
}

runTests().catch(console.error);
