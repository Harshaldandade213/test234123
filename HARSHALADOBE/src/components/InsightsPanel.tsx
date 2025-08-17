import { useState, useEffect } from 'react';
import { Brain, FileText, Quote, Loader2, ExternalLink, AlertCircle, CheckCircle, XCircle, Info } from 'lucide-react';
import { apiService, RelatedSection } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';

interface InsightsPanelProps {
  documentIds?: string[];
  documentId?: string;
  persona?: string;
  jobToBeDone?: string;
  currentText?: string;
  currentPage?: number;
  insightMode?: boolean;
  onPageNavigate?: (page: number) => void;
}

export function InsightsPanel({ 
  documentIds = [], 
  documentId, 
  persona: propPersona, 
  jobToBeDone: propJobToBeDone, 
  currentText, 
  currentPage, 
  insightMode, 
  onPageNavigate 
}: InsightsPanelProps) {
  const [relatedSections, setRelatedSections] = useState<RelatedSection[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [persona, setPersona] = useState(propPersona || '');
  const [jobToBeDone, setJobToBeDone] = useState(propJobToBeDone || '');

  // Fetch related sections when text is selected
  useEffect(() => {
    const fetchRelatedSections = async () => {
      console.log('InsightsPanel useEffect triggered:', {
        currentText: currentText?.substring(0, 50),
        currentTextLength: currentText?.length,
        persona,
        jobToBeDone,
        documentIds: documentIds.length,
        currentPage
      });

      if (!currentText || currentText.length < 20 || !persona || !jobToBeDone || documentIds.length === 0) {
        console.log('Missing required data for related sections:', {
          hasCurrentText: !!currentText,
          currentTextLength: currentText?.length,
          hasPersona: !!persona,
          hasJobToBeDone: !!jobToBeDone,
          documentIdsCount: documentIds.length
      });
      return;
    }
    
      setIsLoading(true);
      setError(null);

      try {
        console.log('Calling getRelatedSections with:', {
          documentIds,
          currentPage: currentPage || 1,
          currentText: currentText.substring(0, 100),
        persona,
        jobToBeDone
        });

        const sections = await apiService.getRelatedSections(
          documentIds,
          currentPage || 1,
        currentText,
        persona,
          jobToBeDone
        );
        
        console.log('Received sections:', sections);
        
        // Get top 5 most relevant sections
        const topSections = sections
          .sort((a, b) => b.relevance_score - a.relevance_score)
          .slice(0, 5);
        
        console.log('Top sections:', topSections);
        setRelatedSections(topSections);
      } catch (err) {
        console.error('Error fetching related sections:', err);
        setError('Failed to fetch related sections');
    } finally {
        setIsLoading(false);
      }
    };

    fetchRelatedSections();
  }, [currentText, currentPage, persona, jobToBeDone, documentIds]);

  const getInsightType = (relevanceScore: number, explanation: string) => {
    if (relevanceScore > 0.8) return 'related';
    if (explanation.toLowerCase().includes('contradict') || explanation.toLowerCase().includes('conflict')) return 'contradicting';
    if (explanation.toLowerCase().includes('example') || explanation.toLowerCase().includes('instance')) return 'example';
    if (explanation.toLowerCase().includes('overlap') || explanation.toLowerCase().includes('similar')) return 'overlapping';
    return 'related';
  };

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'related': return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'contradicting': return <XCircle className="h-4 w-4 text-red-600" />;
      case 'example': return <Info className="h-4 w-4 text-blue-600" />;
      case 'overlapping': return <AlertCircle className="h-4 w-4 text-yellow-600" />;
      default: return <CheckCircle className="h-4 w-4 text-green-600" />;
    }
  };

  const getInsightBadge = (type: string) => {
    switch (type) {
      case 'related': return <Badge variant="default" className="bg-green-100 text-green-800">Related</Badge>;
      case 'contradicting': return <Badge variant="destructive">Contradicting</Badge>;
      case 'example': return <Badge variant="secondary" className="bg-blue-100 text-blue-800">Example</Badge>;
      case 'overlapping': return <Badge variant="outline" className="border-yellow-500 text-yellow-700">Overlapping</Badge>;
      default: return <Badge variant="default">Related</Badge>;
    }
  };

  return (
    <div className="h-full flex flex-col bg-gradient-to-br from-background via-accent/20 to-secondary/10">
      <div className="p-6 border-b border-border bg-background/80 backdrop-blur-sm">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-gradient-to-br from-primary via-primary/90 to-secondary rounded-xl shadow-lg">
              <Brain className="h-6 w-6 text-primary-foreground" />
            </div>
          <div className="flex-1">
            <h3 className="font-bold text-foreground text-xl">Insights</h3>
              <p className="text-sm text-muted-foreground">
              AI-powered document analysis
              </p>
            </div>
          </div>
      </div>

      <ScrollArea className="flex-1 p-6">
            <div className="space-y-6">
          {/* Selected Text Display */}
          {currentText && currentText.length > 0 && (
            <Card className="bg-background/80 border-primary/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Quote className="h-5 w-5 text-primary" />
                  Selected Text
                </CardTitle>
                </CardHeader>
              <CardContent>
                <div className="bg-muted/50 rounded-lg p-4">
                  <p className="text-sm text-foreground leading-relaxed font-medium">
                    "{currentText}"
                  </p>
                  {currentPage && (
                    <p className="text-xs text-muted-foreground mt-2">
                      Selected from page {currentPage}
                    </p>
                  )}
                          </div>
                        </CardContent>
                      </Card>
              )}

          {/* Persona and Job Setup */}
          {(!persona || !jobToBeDone) && (
            <Card className="bg-background/80 border-yellow-200">
              <CardHeader>
                <CardTitle className="text-lg text-yellow-800">Setup Required</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-foreground">Your Role/Persona</label>
                  <input
                    type="text"
                    value={persona}
                    onChange={(e) => setPersona(e.target.value)}
                    placeholder="e.g., Software Engineer, Student, Researcher"
                    className="w-full mt-1 px-3 py-2 border border-border rounded-md bg-background"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-foreground">Job to be Done</label>
                  <input
                    type="text"
                    value={jobToBeDone}
                    onChange={(e) => setJobToBeDone(e.target.value)}
                    placeholder="e.g., Understand design patterns, Research cloud computing"
                    className="w-full mt-1 px-3 py-2 border border-border rounded-md bg-background"
                  />
                </div>
                <p className="text-xs text-muted-foreground">
                  Set your role and goal to get personalized insights from your document library.
                </p>
            </CardContent>
          </Card>
          )}

          {/* Loading State */}
          {isLoading && (
            <Card className="bg-background/80">
              <CardContent className="flex items-center justify-center py-8">
                <div className="text-center space-y-2">
                  <Loader2 className="h-8 w-8 animate-spin mx-auto text-primary" />
                  <p className="text-sm text-muted-foreground">Finding relevant passages...</p>
                          </div>
                        </CardContent>
                      </Card>
          )}

          {/* Error State */}
          {error && (
            <Card className="bg-background/80 border-destructive">
              <CardContent className="flex items-center gap-2 py-4 text-destructive">
                <AlertCircle className="h-4 w-4" />
                <p className="text-sm">{error}</p>
                              </CardContent>
                            </Card>
          )}

          {/* Related Sections */}
          {relatedSections.length > 0 && (
                                <div className="space-y-4">
              <div className="flex items-center gap-2">
                <FileText className="h-5 w-5 text-primary" />
                <h4 className="font-semibold text-lg">Top 5 Relevant Passages</h4>
                <Badge variant="outline">{relatedSections.length} found</Badge>
                                    </div>
                                    
              <div className="space-y-3">
                {relatedSections.map((section, index) => {
                  const insightType = getInsightType(section.relevance_score, section.explanation);
                  return (
                    <Card key={index} className="bg-background/80 hover:bg-background/90 transition-colors">
                              <CardContent className="p-4">
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center gap-2">
                            {getInsightIcon(insightType)}
                            <span className="text-sm font-medium text-foreground">
                              {section.document}
                            </span>
                            <span className="text-xs text-muted-foreground">
                              Page {section.page_number}
                            </span>
                                    </div>
                          <div className="flex items-center gap-2">
                            {getInsightBadge(insightType)}
                            <Badge variant="outline" className="text-xs">
                              {Math.round(section.relevance_score * 100)}% relevant
                                        </Badge>
                                      </div>
                      </div>

                        <div className="mb-3">
                          <h5 className="font-medium text-sm text-foreground mb-1">
                            {section.section_title}
                          </h5>
                          <p className="text-xs text-muted-foreground leading-relaxed">
                            {section.explanation}
                          </p>
                          </div>

                                <div className="flex items-center gap-2">
                                  <Button
                                    size="sm"
                            variant="outline"
                            onClick={() => onPageNavigate?.(section.page_number)}
                            className="text-xs"
                                  >
                                    <ExternalLink className="h-3 w-3 mr-1" />
                            Go to Page
                                  </Button>
                                </div>
                      </CardContent>
                        </Card>
                  );
                })}
                          </div>
                    </div>
                  )}

          {/* Empty State */}
          {!currentText && !isLoading && !error && (
            <div className="text-center space-y-4 py-8">
                <div className="p-4 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full w-fit mx-auto">
                  <Brain className="h-12 w-12 text-blue-600" />
                </div>
                <div>
                  <h4 className="text-xl font-bold text-gray-900 mb-2">
                  Insights Section
                  </h4>
                <p className="text-sm text-gray-600">
                  Select text from the document to see relevant passages from your document library
                  </p>
                </div>
                </div>
          )}

          {/* No Results */}
          {currentText && !isLoading && !error && relatedSections.length === 0 && persona && jobToBeDone && (
            <Card className="bg-background/80">
              <CardContent className="text-center py-8">
                <AlertCircle className="h-8 w-8 mx-auto text-muted-foreground mb-2" />
                <p className="text-sm text-muted-foreground">
                  No relevant passages found. Try selecting different text or adjusting your persona/job description.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}