import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { useToast } from '@/hooks/use-toast';
import { apiService, CrossConnectionsResponse, RelatedDocument, Contradiction, CrossDocumentInsight } from '@/lib/api';
import { ExpandablePanelModal } from '@/components/ui/ExpandablePanelModal';
import { 
  Link2, 
  AlertTriangle, 
  Lightbulb, 
  ExternalLink, 
  ChevronDown, 
  ChevronRight,
  Loader2,
  TrendingUp,
  Target,
  Zap,
  BookOpen,
  AlertCircle
} from 'lucide-react';

interface CrossConnectionsPanelProps {
  documentId: string;
  persona?: string;
  jobToBeDone?: string;
  selectedText?: string;
  onNavigateToDocument?: (documentId: string) => void;
  className?: string;
}

export function CrossConnectionsPanel({ documentId, persona, jobToBeDone, selectedText, onNavigateToDocument, className = '' }: CrossConnectionsPanelProps) {
  const [connections, setConnections] = useState<CrossConnectionsResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(['related']));
  const { toast } = useToast();

  useEffect(() => {
    loadConnections();
  }, [documentId, selectedText]);

  const loadConnections = async () => {
    try {
      setIsLoading(true);
      // Use selected text as current_section parameter if available
      const data = await apiService.getCrossConnections(documentId, persona, jobToBeDone, selectedText);
      setConnections(data);
    } catch (error) {
      console.error('Failed to load related sections:', error);
      toast({
        title: "Error",
        description: "Failed to analyze related sections. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const toggleSection = (section: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(section)) {
      newExpanded.delete(section);
    } else {
      newExpanded.add(section);
    }
    setExpandedSections(newExpanded);
  };

  const getConnectionTypeIcon = (type: string) => {
    switch (type) {
      case 'complementary': return <Link2 className="h-4 w-4 text-green-600" />;
      case 'contradictory': return <AlertTriangle className="h-4 w-4 text-red-600" />;
      case 'similar': return <BookOpen className="h-4 w-4 text-blue-600" />;
      default: return <Link2 className="h-4 w-4 text-gray-600" />;
    }
  };

  const getConnectionTypeColor = (type: string) => {
    switch (type) {
      case 'complementary': return 'bg-green-100 text-green-800 border-green-200';
      case 'contradictory': return 'bg-red-100 text-red-800 border-red-200';
      case 'similar': return 'bg-blue-100 text-blue-800 border-blue-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'pattern': return <TrendingUp className="h-4 w-4 text-secondary" />;
      case 'opportunity': return <Target className="h-4 w-4 text-accent-foreground" />;
      case 'recommendation': return <Zap className="h-4 w-4 text-primary" />;
      default: return <Lightbulb className="h-4 w-4 text-primary" />;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-orange-100 text-orange-800 border-orange-200';
      default: return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    }
  };

  if (isLoading) {
    return (
      <Card className={`${className}`}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Link2 className="h-5 w-5" />
            Related Sections
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="text-center">
              <Loader2 className="h-6 w-6 animate-spin mx-auto mb-2 text-blue-600" />
              <p className="text-sm text-gray-600">Analyzing connections...</p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!connections || connections.related_sections.length === 0) {
    return (
      <Card className={`${className}`}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Link2 className="h-5 w-5" />
            Related Sections
          </CardTitle>
        </CardHeader>
        <CardContent>
          {selectedText ? (
            <div className="space-y-4">
              {/* Selected Text Box */}
              <Card className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200">
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <BookOpen className="h-4 w-4 text-blue-600" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-blue-900 text-sm mb-2">Selected Text</h4>
                    <div className="bg-white p-3 rounded border border-blue-200">
                      <p className="text-sm text-gray-800 leading-relaxed">
                        "{selectedText.substring(0, 200)}{selectedText.length > 200 ? '...' : ''}"
                      </p>
                    </div>
                  </div>
                </div>
              </Card>
              
              {/* No Results Message */}
              <div className="text-center py-6">
                <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <AlertCircle className="h-6 w-6 text-gray-400" />
                </div>
                <p className="text-sm font-medium text-gray-700 mb-1">No related sections found</p>
                <p className="text-xs text-gray-500">Try selecting different text or upload more documents</p>
              </div>
            </div>
          ) : (
            <div className="text-center py-8">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <Link2 className="h-6 w-6 text-blue-600" />
              </div>
              <p className="text-sm font-medium text-gray-700 mb-1">Select text to find related sections</p>
              <p className="text-xs text-gray-500">Highlight text in the document to automatically find related content</p>
            </div>
          )}
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={`${className}`}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Link2 className="h-5 w-5 text-primary" />
              Related Sections
            </CardTitle>
            <CardDescription className="text-sm">
              {connections.total_related_sections} unique related section{connections.total_related_sections !== 1 ? 's' : ''} found
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Selected Text Box */}
        {selectedText && (
          <Card className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <BookOpen className="h-4 w-4 text-blue-600" />
              </div>
              <div className="flex-1">
                <h4 className="font-semibold text-blue-900 text-sm mb-2">Selected Text</h4>
                <div className="bg-white p-3 rounded border border-blue-200">
                  <p className="text-sm text-gray-800 leading-relaxed">
                    "{selectedText.substring(0, 200)}{selectedText.length > 200 ? '...' : ''}"
                  </p>
                </div>
                                 <div className="flex items-center gap-2 mt-2">
                   <Badge variant="outline" className="text-xs bg-blue-100 border-blue-300 text-blue-800">
                     Auto-analyzed
                   </Badge>
                   <span className="text-xs text-blue-600">
                     {connections.total_related_sections} unique related sections found
                   </span>
                 </div>
              </div>
            </div>
          </Card>
        )}

        {/* Related Sections Grid */}
        {connections.related_sections.length > 0 && (
          <div className="space-y-3">
                         <div className="flex items-center gap-2">
               <h4 className="font-semibold text-gray-900 text-sm">Related Sections</h4>
               <Badge variant="secondary" className="text-xs">
                 {connections.related_sections.length} unique found
               </Badge>
             </div>
            
            <div className="grid gap-3">
              {connections.related_sections.map((section, index) => (
                <Card key={index} className="p-4 hover:shadow-md transition-all duration-200 border border-gray-200 bg-white">
                  <div className="space-y-3">
                    {/* Document Header */}
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h5 className="font-semibold text-gray-900 text-sm line-clamp-1 mb-1">
                          {section.document}
                        </h5>
                        <div className="flex items-center gap-2">
                          <Badge variant="outline" className="text-xs bg-green-50 border-green-200 text-green-800">
                            {Math.round(section.relevance_score * 100)}% match
                          </Badge>
                          <span className="text-xs text-gray-500">
                            Page {section.page_number}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    {/* Section Content */}
                    <div className="bg-gray-50 p-3 rounded border">
                      <p className="text-sm text-gray-700 leading-relaxed line-clamp-3">
                        {section.text}
                      </p>
                    </div>
                    
                    {/* Relationship */}
                    <div className="bg-blue-50 p-2 rounded border border-blue-200">
                      <p className="text-xs text-blue-700">
                        <strong>Why related:</strong> {section.explanation}
                      </p>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Quick Summary */}
        {connections.analysis_summary && (
          <Card className="p-3 bg-gradient-to-r from-gray-50 to-blue-50 border border-gray-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                                 <span className="text-xs font-medium text-gray-700">
                   {connections.analysis_summary.sections_found} unique sections found
                 </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-600">
                  Avg: {Math.round(connections.analysis_summary.average_relevance * 100)}%
                </span>
                <span className="text-xs text-gray-600">
                  High: {connections.analysis_summary.relevance_distribution.high}
                </span>
              </div>
            </div>
          </Card>
        )}
      </CardContent>
    </Card>
  );
}