# PDF Loading Error Troubleshooting Guide

## Problem
You're seeing the error: **"PDF Loading Error - Failed to initialize PDF viewer: undefined"**

## Root Cause
This error typically occurs when the Adobe PDF Embed API (Adobe DC SDK) fails to load or initialize properly.

## Quick Solutions

### 1. **Refresh the Page** 🔄
- Press `Ctrl + F5` (Windows) or `Cmd + Shift + R` (Mac) to force refresh
- This will reload the Adobe SDK script

### 2. **Check Internet Connection** 🌐
- Ensure you have a stable internet connection
- The Adobe PDF SDK is loaded from Adobe's CDN: `https://documentservices.adobe.com/view-sdk/viewer.js`

### 3. **Clear Browser Cache** 🗑️
- Press `F12` to open Developer Tools
- Right-click the refresh button and select "Empty Cache and Hard Reload"
- Or clear cache manually in browser settings

### 4. **Try Different Browser** 🌍
- Test in Chrome, Firefox, Safari, or Edge
- Some browsers may have different security policies

## Advanced Troubleshooting

### Check Browser Console
1. Press `F12` to open Developer Tools
2. Go to the **Console** tab
3. Look for any red error messages
4. Common errors:
   - `Failed to load resource: https://documentservices.adobe.com/view-sdk/viewer.js`
   - `AdobeDC is not defined`
   - CORS errors

### Check Network Tab
1. In Developer Tools, go to the **Network** tab
2. Refresh the page
3. Look for failed requests to Adobe's CDN
4. Check if the request is being blocked

### Browser Extensions
- Disable ad blockers temporarily
- Disable privacy extensions (uBlock Origin, Privacy Badger, etc.)
- Some extensions block Adobe's CDN

## Technical Details

### Adobe SDK Loading Process
1. **Script Loading**: The Adobe SDK script is loaded from `https://documentservices.adobe.com/view-sdk/viewer.js`
2. **Initialization**: The script creates the `window.AdobeDC` object
3. **Viewer Creation**: The PDF viewer is initialized using `new window.AdobeDC.View()`
4. **PDF Loading**: The actual PDF is loaded into the viewer

### Error Types
- **"Adobe SDK timeout"**: The script took too long to load (15+ seconds)
- **"Adobe DC SDK failed to load"**: Network connectivity issues
- **"Failed to initialize PDF viewer"**: General initialization failure

## Environment-Specific Issues

### Corporate Networks
- Some corporate firewalls block Adobe's CDN
- Contact your IT department to whitelist `documentservices.adobe.com`

### VPN Connections
- VPNs may interfere with CDN connections
- Try disconnecting VPN temporarily

### Mobile Devices
- Some mobile browsers have limited support
- Try desktop browsers for better compatibility

## Prevention

### Reliable Setup
1. **Stable Internet**: Ensure consistent internet connectivity
2. **Modern Browser**: Use latest versions of Chrome, Firefox, Safari, or Edge
3. **No Blocking Extensions**: Avoid extensions that block external scripts

### Alternative Solutions
If Adobe PDF Embed continues to fail:
1. **Use Fallback Viewer**: The app includes a fallback PDF viewer
2. **Download PDF**: Use the download option to view PDFs locally
3. **Contact Support**: If issues persist, contact technical support

## Debug Information

### Check Adobe SDK Status
```javascript
// In browser console
console.log('AdobeDC available:', !!window.AdobeDC);
console.log('AdobeDC.View available:', !!window.AdobeDC?.View);
```

### Test Network Connectivity
```javascript
// Test Adobe CDN connectivity
fetch('https://documentservices.adobe.com/view-sdk/viewer.js', {
  method: 'HEAD',
  mode: 'no-cors'
}).then(() => console.log('Adobe CDN accessible'))
  .catch(err => console.error('Adobe CDN blocked:', err));
```

## Support

If you continue to experience issues:
1. **Check Console**: Look for specific error messages
2. **Test Network**: Verify connectivity to Adobe's CDN
3. **Try Different Device**: Test on another computer/network
4. **Report Issue**: Include browser version, OS, and error messages

## Quick Fix Commands

### Force Reload Adobe SDK
```javascript
// In browser console
const script = document.createElement('script');
script.src = 'https://documentservices.adobe.com/view-sdk/viewer.js';
document.head.appendChild(script);
```

### Check SDK Status
```javascript
// In browser console
setInterval(() => {
  console.log('AdobeDC:', !!window.AdobeDC);
  console.log('AdobeDC.View:', !!window.AdobeDC?.View);
}, 1000);
```

---

**Note**: The Adobe PDF Embed API is a third-party service. If it's consistently unavailable, consider using the built-in fallback PDF viewer or downloading PDFs for local viewing.
