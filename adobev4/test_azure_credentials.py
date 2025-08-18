#!/usr/bin/env python3
"""
Test script to verify Azure Speech SDK credentials
"""
import azure.cognitiveservices.speech as speechsdk

# Azure Configuration
AZURE_SPEECH_KEY = "6LKDbzy1pkGLZNMuTjSxf8hrte5dGlAKFWAHX7R0eczacngvw1reJQQJ99BHACGhslBXJ3w3AAAYACOGhON1"

# Test multiple regions
REGIONS_TO_TEST = ["centralindia", "centralus", "eastus", "westus", "eastus2", "westus2"]

def test_azure_credentials():
    print("🧪 Testing Azure Speech SDK Credentials")
    print("=" * 50)
    
    print(f"🔑 API Key: {AZURE_SPEECH_KEY[:10]}...{AZURE_SPEECH_KEY[-10:]}")
    
    for region in REGIONS_TO_TEST:
        print(f"\n🔧 Testing region: {region}")
        try:
            # Test 1: Basic configuration
            print("  1️⃣ Testing basic configuration...")
            speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=region)
            print("  ✅ Speech config created successfully")
            
            # Test 2: Simple text-to-speech
            print("  2️⃣ Testing simple text-to-speech...")
            speech_config.speech_synthesis_voice_name = "en-US-DavisNeural"
            
            # Create a simple synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
            
            # Try to synthesize a simple text
            result = synthesizer.speak_text_async("Hello, this is a test.").get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("  ✅ Text-to-speech test successful!")
                print(f"\n🎉 Found working region: {region}")
                return True, region
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print(f"  ❌ Speech synthesis canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print(f"  ❌ Error details: {cancellation_details.error_details}")
            else:
                print(f"  ❌ Unexpected result: {result.reason}")
                
        except Exception as e:
            print(f"  ❌ Error during Azure Speech SDK test: {e}")
    
    print(f"\n❌ No working region found from: {REGIONS_TO_TEST}")
    return False, None

if __name__ == "__main__":
    success, working_region = test_azure_credentials()
    if success:
        print(f"\n🎉 Azure Speech SDK credentials are working with region: {working_region}")
        print(f"💡 Update your app.py with: AZURE_SPEECH_REGION = '{working_region}'")
    else:
        print("\n❌ Azure Speech SDK credentials need attention.")
        print("\n💡 Troubleshooting tips:")
        print("1. Check if the API key is correct")
        print("2. Verify the region matches your Azure Speech service")
        print("3. Ensure the Azure Speech service is active")
        print("4. Check if you have sufficient quota/credits")
