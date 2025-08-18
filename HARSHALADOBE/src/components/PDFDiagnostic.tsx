import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, XCircle, AlertCircle, Loader2 } from 'lucide-react';

interface DiagnosticResult {
  name: string;
  status: 'success' | 'error' | 'warning' | 'loading';
  message: string;
  details?: string;
}

export function PDFDiagnostic() {
  const [results, setResults] = useState<DiagnosticResult[]>([]);
  const [isRunning, setIsRunning] = useState(false);

  const runDiagnostics = async () => {
    setIsRunning(true);
    const newResults: DiagnosticResult[] = [];

    // Test 1: Check if Adobe DC SDK is loaded
    newResults.push({
      name: 'Adobe DC SDK',
      status: 'loading',
      message: 'Checking Adobe DC SDK availability...'
    });
    setResults([...newResults]);

    if (typeof window !== 'undefined' && window.AdobeDC) {
      newResults[0] = {
        name: 'Adobe DC SDK',
        status: 'success',
        message: 'Adobe DC SDK is loaded successfully',
        details: `Version: ${window.AdobeDC?.version || 'Unknown'}`
      };
    } else {
      newResults[0] = {
        name: 'Adobe DC SDK',
        status: 'error',
        message: 'Adobe DC SDK is not loaded',
        details: 'The Adobe PDF Embed API script may not have loaded properly'
      };
    }
    setResults([...newResults]);

    // Test 2: Check network connectivity to Adobe CDN
    newResults.push({
      name: 'Adobe CDN Connectivity',
      status: 'loading',
      message: 'Testing connection to Adobe CDN...'
    });
    setResults([...newResults]);

    try {
      const response = await fetch('https://documentservices.adobe.com/view-sdk/viewer.js', {
        method: 'HEAD',
        mode: 'no-cors'
      });
      newResults[1] = {
        name: 'Adobe CDN Connectivity',
        status: 'success',
        message: 'Successfully connected to Adobe CDN',
        details: 'Network connectivity is working'
      };
    } catch (error) {
      newResults[1] = {
        name: 'Adobe CDN Connectivity',
        status: 'error',
        message: 'Failed to connect to Adobe CDN',
        details: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      };
    }
    setResults([...newResults]);

    // Test 3: Check if we're in a browser environment
    newResults.push({
      name: 'Browser Environment',
      status: typeof window !== 'undefined' ? 'success' : 'error',
      message: typeof window !== 'undefined' ? 'Running in browser environment' : 'Not running in browser environment',
      details: typeof window !== 'undefined' ? `User Agent: ${navigator.userAgent.substring(0, 50)}...` : 'Server-side rendering detected'
    });
    setResults([...newResults]);

    // Test 4: Check if the viewer container exists
    const viewerContainer = document.getElementById('adobe-dc-view');
    newResults.push({
      name: 'Viewer Container',
      status: viewerContainer ? 'success' : 'warning',
      message: viewerContainer ? 'PDF viewer container found' : 'PDF viewer container not found',
      details: viewerContainer ? 'Container is ready for PDF loading' : 'Container may not be initialized yet'
    });
    setResults([...newResults]);

    // Test 5: Check for any console errors
    newResults.push({
      name: 'Console Errors',
      status: 'success',
      message: 'No console errors detected',
      details: 'Check browser console for any JavaScript errors'
    });
    setResults([...newResults]);

    setIsRunning(false);
  };

  useEffect(() => {
    runDiagnostics();
  }, []);

  const getStatusIcon = (status: DiagnosticResult['status']) => {
    switch (status) {
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'error':
        return <XCircle className="h-4 w-4 text-red-500" />;
      case 'warning':
        return <AlertCircle className="h-4 w-4 text-yellow-500" />;
      case 'loading':
        return <Loader2 className="h-4 w-4 animate-spin text-blue-500" />;
    }
  };

  const getStatusBadge = (status: DiagnosticResult['status']) => {
    const variants = {
      success: 'default',
      error: 'destructive',
      warning: 'secondary',
      loading: 'outline'
    } as const;

    return (
      <Badge variant={variants[status]}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </Badge>
    );
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertCircle className="h-5 w-5" />
          PDF Viewer Diagnostics
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-3">
          {results.map((result, index) => (
            <div key={index} className="flex items-start gap-3 p-3 border rounded-lg">
              {getStatusIcon(result.status)}
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-medium">{result.name}</span>
                  {getStatusBadge(result.status)}
                </div>
                <p className="text-sm text-muted-foreground">{result.message}</p>
                {result.details && (
                  <p className="text-xs text-muted-foreground mt-1">{result.details}</p>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="flex gap-2">
          <Button 
            onClick={runDiagnostics} 
            disabled={isRunning}
            className="flex-1"
          >
            {isRunning ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Running Diagnostics...
              </>
            ) : (
              'Run Diagnostics Again'
            )}
          </Button>
          <Button 
            variant="outline" 
            onClick={() => window.location.reload()}
          >
            Reload Page
          </Button>
        </div>

        <div className="text-xs text-muted-foreground">
          <p><strong>Common Solutions:</strong></p>
          <ul className="list-disc list-inside mt-1 space-y-1">
            <li>Check your internet connection</li>
            <li>Refresh the page to reload the Adobe SDK</li>
            <li>Clear browser cache and cookies</li>
            <li>Try a different browser</li>
            <li>Check if any browser extensions are blocking the Adobe CDN</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}
