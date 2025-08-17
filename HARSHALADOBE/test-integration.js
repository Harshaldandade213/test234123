// Test script for integrated backend system
const fetch = require('node-fetch');

const ADOBEV4_URL = 'http://localhost:8000';
const HARSHALADOBE_URL = 'http://localhost:8001';

async function testHealth() {
  console.log('🔍 Testing backend health...\n');
  
  try {
    const adobev4Health = await fetch(`${ADOBEV4_URL}/health`);
    console.log(`✅ adobev4 backend (port 8000): ${adobev4Health.ok ? 'HEALTHY' : 'UNHEALTHY'}`);
  } catch (error) {
    console.log(`❌ adobev4 backend (port 8000): ERROR - ${error.message}`);
  }
  
  try {
    const harshalaHealth = await fetch(`${HARSHALADOBE_URL}/health`);
    console.log(`✅ HARSHALADOBE backend (port 8001): ${harshalaHealth.ok ? 'HEALTHY' : 'UNHEALTHY'}`);
  } catch (error) {
    console.log(`❌ HARSHALADOBE backend (port 8001): ERROR - ${error.message}`);
  }
}

async function testInsightsRouting() {
  console.log('\n🧠 Testing insights routing to adobev4...\n');
  
  try {
    const response = await fetch(`${ADOBEV4_URL}/analyze-documents`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        document_ids: [],
        persona: "Student",
        job_to_be_done: "Research Paper"
      }),
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ adobev4 analyze_documents endpoint working');
      console.log(`   Response: ${JSON.stringify(data, null, 2).substring(0, 200)}...`);
    } else {
      console.log(`❌ adobev4 analyze_documents failed: ${response.status}`);
    }
  } catch (error) {
    console.log(`❌ adobev4 analyze_documents error: ${error.message}`);
  }
}

async function testHarshalaEndpoints() {
  console.log('\n📄 Testing HARSHALADOBE endpoints...\n');
  
  try {
    const response = await fetch(`${HARSHALADOBE_URL}/documents`);
    if (response.ok) {
      const data = await response.json();
      console.log('✅ HARSHALADOBE documents endpoint working');
      console.log(`   Documents count: ${data.length}`);
    } else {
      console.log(`❌ HARSHALADOBE documents failed: ${response.status}`);
    }
  } catch (error) {
    console.log(`❌ HARSHALADOBE documents error: ${error.message}`);
  }
  
  try {
    const response = await fetch(`${HARSHALADOBE_URL}/insights`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: "Test text for insights",
        persona: "Student",
        job_to_be_done: "Research"
      }),
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ HARSHALADOBE insights endpoint working');
      console.log(`   Insights count: ${data.insights?.length || 0}`);
    } else {
      console.log(`❌ HARSHALADOBE insights failed: ${response.status}`);
    }
  } catch (error) {
    console.log(`❌ HARSHALADOBE insights error: ${error.message}`);
  }
}

async function testPodcastGeneration() {
  console.log('\n🎙️ Testing podcast generation...\n');
  
  try {
    const response = await fetch(`${ADOBEV4_URL}/generate-podcast`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: "Test podcast query",
        output_filename: "test_podcast.mp3"
      }),
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ adobev4 podcast generation working');
      console.log(`   Status: ${data.status}`);
    } else {
      console.log(`❌ adobev4 podcast generation failed: ${response.status}`);
    }
  } catch (error) {
    console.log(`❌ adobev4 podcast generation error: ${error.message}`);
  }
}

async function runAllTests() {
  console.log('🚀 Starting Integration Tests...\n');
  console.log('=====================================\n');
  
  await testHealth();
  await testInsightsRouting();
  await testHarshalaEndpoints();
  await testPodcastGeneration();
  
  console.log('\n=====================================');
  console.log('🎉 Integration tests completed!');
  console.log('\n📋 Summary:');
  console.log('- adobev4 backend should handle analysis and podcast generation');
  console.log('- HARSHALADOBE backend should handle document management and insights');
  console.log('- Frontend can use integrated API service for seamless routing');
}

// Run tests if this file is executed directly
if (require.main === module) {
  runAllTests().catch(console.error);
}

module.exports = {
  testHealth,
  testInsightsRouting,
  testHarshalaEndpoints,
  testPodcastGeneration,
  runAllTests
};
