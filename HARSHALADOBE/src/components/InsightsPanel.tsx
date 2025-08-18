import { useState, useEffect } from 'react';
import { Brain, FileText, Quote, Loader2, ExternalLink, AlertCircle, CheckCircle, XCircle, Info, BarChart3, Link2, Tag } from 'lucide-react';
import { apiService, RelatedSection } from '@/lib/api';
import { integratedApiService, DetailedAnalysisResult, PassageAnalysis } from '@/lib/integrated-api';
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
  const [detailedAnalysis, setDetailedAnalysis] = useState<DetailedAnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isQueryAnalyzing, setIsQueryAnalyzing] = useState(false);
  const [customQuery, setCustomQuery] = useState('');
  const [queryAnalysis, setQueryAnalysis] = useState<DetailedAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [persona, setPersona] = useState(propPersona || '');
  const [jobToBeDone, setJobToBeDone] = useState(propJobToBeDone || '');
  const [activeFilter, setActiveFilter] = useState<'all' | 'relevant' | 'related'>('all');

  // Fetch related sections and detailed analysis when text is selected
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

        // Automatically trigger detailed analysis when text is selected
        if (currentText && currentText.length >= 20) {
          console.log('Auto-triggering detailed analysis for selected text');
          await fetchDetailedAnalysis();
        }
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

  const fetchDetailedAnalysis = async () => {
    if (!persona || !jobToBeDone || documentIds.length === 0) {
      setError('Please set persona and job to be done, and ensure documents are selected');
      return;
    }

    // Use selected text as query if available, otherwise use a default query
    const queryText = currentText || `Analysis for ${persona} doing ${jobToBeDone}`;

    setIsAnalyzing(true);
    setError(null);

    try {
      const analysis = await integratedApiService.getDetailedAnalysis(
        documentIds,
        persona,
        jobToBeDone,
        queryText
      );
      setDetailedAnalysis(analysis);
    } catch (err) {
      console.error('Error fetching detailed analysis:', err);
      setError('Failed to fetch detailed analysis');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const analyzeCustomQuery = async () => {
    if (!customQuery.trim()) {
      setError('Please enter a query to analyze');
      return;
    }

    setIsQueryAnalyzing(true);
    setError(null);

    try {
      // Pass document IDs if available
      const analysis = await integratedApiService.analyzeQuery(customQuery.trim(), documentIds);
      setQueryAnalysis(analysis);
    } catch (err) {
      console.error('Error analyzing custom query:', err);
      setError('Failed to analyze custom query');
    } finally {
      setIsQueryAnalyzing(false);
    }
  };

  const getCategoryBadge = (category: string) => {
    switch (category.toLowerCase()) {
      case 'agreement': return <Badge variant="default" className="bg-green-100 text-green-800">Agreement</Badge>;
      case 'conflict': return <Badge variant="destructive">Conflict</Badge>;
      case 'related point': return <Badge variant="secondary" className="bg-blue-100 text-blue-800">Related Point</Badge>;
      case 'example': return <Badge variant="outline" className="border-purple-500 text-purple-700">Example</Badge>;
      default: return <Badge variant="outline">{category}</Badge>;
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

           {/* Custom Query Analysis */}
           <Card className="bg-background/80 border-primary/20">
             <CardHeader>
               <CardTitle className="flex items-center gap-2 text-lg">
                 <Brain className="h-5 w-5 text-primary" />
                 Custom Query Analysis
               </CardTitle>
             </CardHeader>
             <CardContent className="space-y-4">
               <div className="flex gap-2">
                 <input
                   type="text"
                   value={customQuery}
                   onChange={(e) => setCustomQuery(e.target.value)}
                   placeholder="Enter your query (e.g., What are the challenges of Mars colonization?)"
                   className="flex-1 px-3 py-2 border border-border rounded-md bg-background text-sm"
                   onKeyPress={(e) => e.key === 'Enter' && analyzeCustomQuery()}
                 />
                 <Button 
                   onClick={analyzeCustomQuery}
                   disabled={isQueryAnalyzing || !customQuery.trim()}
                   size="sm"
                 >
                   {isQueryAnalyzing ? (
                     <>
                       <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                       Analyzing...
                     </>
                   ) : (
                     <>
                       <Brain className="h-4 w-4 mr-2" />
                       Analyze
                     </>
                   )}
                 </Button>
               </div>
               <p className="text-xs text-muted-foreground">
                 Use the adobev4 backend's analyze-query endpoint to get insights on any topic
               </p>
             </CardContent>
           </Card>

          {/* Detailed Analysis Button */}
          {persona && jobToBeDone && documentIds.length > 0 && (
            <Card className="bg-background/80 border-primary/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <BarChart3 className="h-5 w-5 text-primary" />
                  Document Analysis
                </CardTitle>
              </CardHeader>
              <CardContent>
                                 <Button 
                   onClick={fetchDetailedAnalysis}
                   disabled={isAnalyzing}
                   className="w-full"
                 >
                   {isAnalyzing ? (
                     <>
                       <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                       Analyzing Selected Text...
                     </>
                   ) : (
                     <>
                       <Brain className="h-4 w-4 mr-2" />
                       {currentText ? 'Re-analyze Selected Text' : 'Run Document Analysis'}
                     </>
                   )}
                 </Button>
                 <p className="text-xs text-muted-foreground mt-2">
                   {currentText 
                     ? 'Get detailed analysis of the selected text with passage-by-passage breakdown'
                     : 'Get comprehensive analysis of your documents with passage-by-passage breakdown'
                   }
                 </p>
              </CardContent>
            </Card>
          )}

                                {/* Detailed Analysis Results */}
           {detailedAnalysis && (
             <Card className="bg-background/80 border-primary/20">
               <CardHeader>
                 <CardTitle className="flex items-center gap-2 text-lg">
                   <BarChart3 className="h-5 w-5 text-primary" />
                   Analysis Results
                   {currentText && (
                     <Badge variant="secondary" className="ml-2 text-xs">
                       Based on Selected Text
                     </Badge>
                   )}
                 </CardTitle>
               </CardHeader>
               <CardContent className="space-y-4">
                 {/* Query */}
                 <div>
                   <h4 className="font-semibold text-sm mb-2">
                     Query: {currentText && (
                       <span className="text-xs text-muted-foreground font-normal">
                         (using selected text: {currentText.length} chars)
                       </span>
                     )}
                   </h4>
                   <p className="text-sm text-muted-foreground bg-muted/50 p-3 rounded-lg">
                     {detailedAnalysis.query}
                   </p>
                 </div>

                 {/* Summary */}
                 {detailedAnalysis.summary && (
                   <div>
                     <h4 className="font-semibold text-sm mb-2">Summary:</h4>
                     <p className="text-sm text-foreground bg-muted/50 p-3 rounded-lg">
                       {detailedAnalysis.summary}
                     </p>
                   </div>
                 )}

                 {/* Passage Analysis */}
                 <div>
                   <div className="flex items-center justify-between mb-3">
                     <h4 className="font-semibold text-sm">Relevant Passages:</h4>
                     <div className="flex items-center gap-2">
                       <Badge variant="outline" className="text-xs">
                         {detailedAnalysis.analysis.filter(p => p.category === 'Key Insight' || p.category === 'Direct Answer').length} Highly Relevant
                       </Badge>
                       <Badge variant="outline" className="text-xs">
                         {detailedAnalysis.analysis.length} Total
                       </Badge>
                     </div>
                   </div>
                   
                   {/* Filter Tabs */}
                   <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
                     <Button
                       variant={activeFilter === 'all' ? 'default' : 'outline'}
                       size="sm"
                       onClick={() => setActiveFilter('all')}
                       className="text-xs whitespace-nowrap"
                     >
                       All Passages ({detailedAnalysis.analysis.length})
                     </Button>
                     <Button
                       variant={activeFilter === 'relevant' ? 'default' : 'outline'}
                       size="sm"
                       onClick={() => setActiveFilter('relevant')}
                       className="text-xs whitespace-nowrap"
                     >
                       Highly Relevant ({detailedAnalysis.analysis.filter(p => p.category === 'Key Insight' || p.category === 'Direct Answer').length})
                     </Button>
                     <Button
                       variant={activeFilter === 'related' ? 'default' : 'outline'}
                       size="sm"
                       onClick={() => setActiveFilter('related')}
                       className="text-xs whitespace-nowrap"
                     >
                       Related ({detailedAnalysis.analysis.filter(p => p.category === 'Related Point').length})
                     </Button>
                   </div>

                   {/* Scrollable Passage Grid */}
                   <div className="max-h-96 overflow-y-auto pr-2 border border-gray-200/50 rounded-lg p-2 hover:border-gray-300/70 transition-colors bg-gradient-to-br from-gray-50/50 to-gray-100/30" style={{ scrollbarWidth: 'thin', scrollbarColor: '#9ca3af #f3f4f6' }}>
                     <div className="flex flex-col gap-4 w-full">
                       {detailedAnalysis.analysis
                         .filter(passage => {
                           if (activeFilter === 'relevant') {
                             return passage.category === 'Key Insight' || passage.category === 'Direct Answer';
                           } else if (activeFilter === 'related') {
                             return passage.category === 'Related Point';
                           }
                           return true;
                         })
                         .map((passage, index) => (
                           <Card key={index} className="w-full bg-gradient-to-br from-background to-muted/20 border-2 border-primary/20 hover:border-primary/40 transition-all duration-200 shadow-lg hover:shadow-xl">
                             <CardHeader className="pb-3">
                               <div className="flex items-center justify-between">
                                 <div className="flex items-center gap-2">
                                   <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                                     passage.category === 'Key Insight' || passage.category === 'Direct Answer' 
                                       ? 'bg-green-500/20' 
                                       : 'bg-primary/20'
                                   }`}>
                                     <span className={`text-sm font-bold ${
                                       passage.category === 'Key Insight' || passage.category === 'Direct Answer' 
                                         ? 'text-green-600' 
                                         : 'text-primary'
                                     }`}>
                                       {index + 1}
                                     </span>
                                   </div>
                                   <div>
                                     <h5 className="font-semibold text-sm text-foreground">Passage {index + 1}</h5>
                                     {passage.source && (
                                       <p className="text-xs text-muted-foreground truncate max-w-32">
                                         {passage.source.replace('.pdf', '').replace('.docx', '').replace('.txt', '')}
                                       </p>
                                     )}
                                   </div>
                                 </div>
                                 <div className="flex flex-col items-end gap-1">
                                   {getCategoryBadge(passage.category)}
                                 </div>
                               </div>
                             </CardHeader>
                             
                             <CardContent className="space-y-3">
                               {/* Justification Box - Enhanced */}
                               <div className="bg-muted/30 rounded-lg p-3 border-l-4 border-blue-500/50 w-full">
                                 <h6 className="font-medium text-xs text-blue-600 mb-1 flex items-center gap-1">
                                   <Info className="h-3 w-3" />
                                   Analysis
                                 </h6>
                                 <div className="max-h-24 overflow-y-auto w-full relative border border-blue-200/50 rounded-md p-2 hover:border-blue-300/70 transition-colors" style={{ scrollbarWidth: 'thin', scrollbarColor: '#60a5fa #dbeafe' }}>
                                   <p className="text-xs text-foreground leading-relaxed">
                                     {passage.justification}
                                   </p>
                                   <div className="absolute bottom-0 left-0 right-0 h-4 bg-gradient-to-t from-muted/30 to-transparent pointer-events-none"></div>
                                 </div>
                               </div>

                               {/* Quote Box - Enhanced */}
                               {passage.quote && (
                                 <div className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-950/20 dark:to-blue-950/20 rounded-lg p-3 border-l-4 border-green-500/50 w-full">
                                   <h6 className="font-medium text-xs text-green-600 mb-1 flex items-center gap-1">
                                     <Quote className="h-3 w-3" />
                                     Key Quote
                                   </h6>
                                   <div className="bg-background/80 p-2 rounded border max-h-20 overflow-y-auto w-full border-green-200/50 hover:border-green-300/70 transition-colors" style={{ scrollbarWidth: 'thin', scrollbarColor: '#4ade80 #dcfce7' }}>
                                     <p className="text-xs text-foreground italic leading-relaxed">
                                       "{passage.quote}"
                                     </p>
                                   </div>
                                 </div>
                               )}

                               {/* Preview Box - Enhanced */}
                               {passage.passage_preview && (
                                 <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-950/20 dark:to-pink-950/20 rounded-lg p-3 border-l-4 border-purple-500/50 w-full">
                                   <h6 className="font-medium text-xs text-purple-600 mb-1 flex items-center gap-1">
                                     <FileText className="h-3 w-3" />
                                     Content Preview
                                   </h6>
                                   <div className="max-h-16 overflow-y-auto w-full border border-purple-200/50 rounded-md p-2 hover:border-purple-300/70 transition-colors" style={{ scrollbarWidth: 'thin', scrollbarColor: '#a855f7 #f3e8ff' }}>
                                     <p className="text-xs text-foreground leading-relaxed">
                                       {passage.passage_preview}
                                     </p>
                                   </div>
                                 </div>
                               )}
                             </CardContent>
                           </Card>
                         ))}
                     </div>
                   </div>
                 </div>
               </CardContent>
             </Card>
           )}

           {/* Custom Query Analysis Results */}
           {queryAnalysis && (
             <Card className="bg-background/80 border-primary/20">
               <CardHeader>
                 <CardTitle className="flex items-center gap-2 text-lg">
                   <BarChart3 className="h-5 w-5 text-primary" />
                   Custom Query Analysis Results
                   <Badge variant="secondary" className="ml-2 text-xs">
                     Using adobev4 /analyze-query
                   </Badge>
                 </CardTitle>
               </CardHeader>
               <CardContent className="space-y-4">
                 {/* Query */}
                 <div>
                   <h4 className="font-semibold text-sm mb-2">Query:</h4>
                   <p className="text-sm text-muted-foreground bg-muted/50 p-3 rounded-lg">
                     {queryAnalysis.query}
                   </p>
                 </div>

                 {/* Summary */}
                 {queryAnalysis.summary && (
                   <div>
                     <h4 className="font-semibold text-sm mb-2">Summary:</h4>
                     <div className="bg-muted/50 p-3 rounded-lg border border-gray-200/50 hover:border-gray-300/70 transition-colors" style={{ scrollbarWidth: 'thin', scrollbarColor: '#9ca3af #f3f4f6' }}>
                       <p className="text-sm text-foreground leading-relaxed max-h-32 overflow-y-auto">
                         {queryAnalysis.summary}
                       </p>
                     </div>
                   </div>
                 )}

                 {/* Passage Analysis */}
                 <div>
                   <h4 className="font-semibold text-sm mb-3">Passage Analysis:</h4>
                   {/* Scrollable Passage Grid */}
                   <div className="max-h-96 overflow-y-auto pr-2 border border-gray-200/50 rounded-lg p-2 hover:border-gray-300/70 transition-colors bg-gradient-to-br from-gray-50/50 to-gray-100/30" style={{ scrollbarWidth: 'thin', scrollbarColor: '#9ca3af #f3f4f6' }}>
                     <div className="flex flex-col gap-4 w-full">
                       {queryAnalysis.analysis.map((passage, index) => (
                         <Card key={index} className="w-full bg-gradient-to-br from-background to-muted/20 border-2 border-primary/20 hover:border-primary/40 transition-all duration-200 shadow-lg hover:shadow-xl">
                           <CardHeader className="pb-3">
                             <div className="flex items-center justify-between">
                               <div className="flex items-center gap-2">
                                 <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                                   passage.category === 'Key Insight' || passage.category === 'Direct Answer' 
                                     ? 'bg-green-500/20' 
                                     : 'bg-primary/20'
                                 }`}>
                                   <span className={`text-sm font-bold ${
                                     passage.category === 'Key Insight' || passage.category === 'Direct Answer' 
                                       ? 'text-green-600' 
                                       : 'text-primary'
                                   }`}>
                                     {index + 1}
                                   </span>
                                 </div>
                                 <div>
                                   <h5 className="font-semibold text-sm text-foreground">Passage {index + 1}</h5>
                                   {passage.source && (
                                     <p className="text-xs text-muted-foreground truncate max-w-32">
                                       {passage.source.replace('.pdf', '').replace('.docx', '').replace('.txt', '')}
                                     </p>
                                   )}
                                 </div>
                               </div>
                               <div className="flex flex-col items-end gap-1">
                                 {getCategoryBadge(passage.category)}
                               </div>
                             </div>
                           </CardHeader>
                           
                           <CardContent className="space-y-3">
                             {/* Justification Box - Enhanced */}
                             <div className="bg-muted/30 rounded-lg p-3 border-l-4 border-blue-500/50 w-full relative border border-blue-200/50 rounded-md p-2 hover:border-blue-300/70 transition-colors" style={{ scrollbarWidth: 'thin', scrollbarColor: '#60a5fa #dbeafe' }}>
                               <h6 className="font-medium text-xs text-blue-600 mb-1 flex items-center gap-1">
                                 <Info className="h-3 w-3" />
                                 Analysis
                               </h6>
                               <div className="max-h-24 overflow-y-auto w-full relative border border-blue-200/50 rounded-md p-2 hover:border-blue-300/70 transition-colors" style={{ scrollbarWidth: 'thin', scrollbarColor: '#60a5fa #dbeafe' }}>
                                 <p className="text-xs text-foreground leading-relaxed">
                                   {passage.justification}
                                 </p>
                                 <div className="absolute bottom-0 left-0 right-0 h-4 bg-gradient-to-t from-muted/30 to-transparent pointer-events-none"></div>
                               </div>
                             </div>

                             {/* Quote Box - Enhanced */}
                             {passage.quote && (
                               <div className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-950/20 dark:to-blue-950/20 rounded-lg p-3 border-l-4 border-green-500/50 w-full">
                                 <h6 className="font-medium text-xs text-green-600 mb-1 flex items-center gap-1">
                                   <Quote className="h-3 w-3" />
                                   Key Quote
                                 </h6>
                                 <div className="bg-background/80 p-2 rounded border max-h-20 overflow-y-auto w-full border-green-200/50 hover:border-green-300/70 transition-colors" style={{ scrollbarWidth: 'thin', scrollbarColor: '#4ade80 #dcfce7' }}>
                                   <p className="text-xs text-foreground italic leading-relaxed">
                                     "{passage.quote}"
                                   </p>
                                 </div>
                               </div>
                             )}

                             {/* Preview Box - Enhanced */}
                             {passage.passage_preview && (
                               <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-950/20 dark:to-pink-950/20 rounded-lg p-3 border-l-4 border-purple-500/50 w-full">
                                 <h6 className="font-medium text-xs text-purple-600 mb-1 flex items-center gap-1">
                                   <FileText className="h-3 w-3" />
                                   Content Preview
                                 </h6>
                                 <div className="max-h-16 overflow-y-auto w-full border border-purple-200/50 rounded-md p-2 hover:border-purple-300/70 transition-colors" style={{ scrollbarWidth: 'thin', scrollbarColor: '#a855f7 #f3e8ff' }}>
                                   <p className="text-xs text-foreground leading-relaxed">
                                     {passage.passage_preview}
                                   </p>
                                 </div>
                               </div>
                             )}
                           </CardContent>
                         </Card>
                       ))}
                     </div>
                   </div>
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
            <Card className="bg-background/80 border-primary/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <FileText className="h-5 w-5 text-primary" />
                  Top Relevant Passages
                  <Badge variant="outline" className="ml-2 text-xs">
                    {relatedSections.length} found
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="max-h-64 overflow-y-auto pr-2 border border-gray-200/50 rounded-lg p-2 hover:border-gray-300/70 transition-colors bg-gradient-to-br from-gray-50/50 to-gray-100/30" style={{ scrollbarWidth: 'thin', scrollbarColor: '#9ca3af #f3f4f6' }}>
                  <div className="flex flex-col gap-3 w-full">
                    {relatedSections.map((section, index) => {
                      const insightType = getInsightType(section.relevance_score, section.explanation);
                      return (
                        <Card key={index} className="w-full bg-gradient-to-br from-background to-muted/20 border-2 border-primary/20 hover:border-primary/40 transition-all duration-200 shadow-lg hover:shadow-xl">
                          <CardHeader className="pb-3">
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-2">
                                <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                                  {getInsightIcon(insightType)}
                                </div>
                                <div>
                                  <h5 className="font-semibold text-sm text-foreground">
                                    {section.document.replace('.pdf', '').replace('.docx', '').replace('.txt', '')}
                                  </h5>
                                  <p className="text-xs text-muted-foreground">
                                    Page {section.page_number}
                                  </p>
                                </div>
                              </div>
                              <div className="flex flex-col items-end gap-1">
                                {getInsightBadge(insightType)}
                                <Badge variant="outline" className="text-xs">
                                  {Math.round(section.relevance_score * 100)}% relevant
                                </Badge>
                              </div>
                            </div>
                          </CardHeader>

                          <CardContent className="space-y-3">
                            {/* Section Title Box */}
                            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20 rounded-lg p-3 border-l-4 border-blue-500/50 w-full">
                              <h6 className="font-medium text-xs text-blue-600 mb-1 flex items-center gap-1">
                                <FileText className="h-3 w-3" />
                                Section Title
                              </h6>
                              <div className="max-h-16 overflow-y-auto w-full border border-blue-200/50 rounded-md p-2 hover:border-blue-300/70 transition-colors" style={{ scrollbarWidth: 'thin', scrollbarColor: '#60a5fa #dbeafe' }}>
                                <p className="text-xs text-foreground font-medium leading-relaxed">
                                  {section.section_title}
                                </p>
                              </div>
                            </div>

                            {/* Explanation Box */}
                            <div className="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-950/20 dark:to-emerald-950/20 rounded-lg p-3 border-l-4 border-green-500/50 w-full">
                              <h6 className="font-medium text-xs text-green-600 mb-1 flex items-center gap-1">
                                <Info className="h-3 w-3" />
                                Relevance Explanation
                              </h6>
                              <div className="max-h-20 overflow-y-auto w-full border border-green-200/50 rounded-md p-2 hover:border-green-300/70 transition-colors" style={{ scrollbarWidth: 'thin', scrollbarColor: '#4ade80 #dcfce7' }}>
                                <p className="text-xs text-foreground leading-relaxed">
                                  {section.explanation}
                                </p>
                              </div>
                            </div>

                            {/* Enhanced Fields */}
                            {(section.relationship_type || section.key_concepts) && (
                              <div className="bg-gradient-to-r from-orange-50 to-amber-50 dark:from-orange-950/20 dark:to-amber-950/20 rounded-lg p-3 border-l-4 border-orange-500/50 w-full">
                                <div className="space-y-2">
                                  {section.relationship_type && (
                                    <div>
                                      <h6 className="font-medium text-xs text-orange-600 mb-1 flex items-center gap-1">
                                        <Link2 className="h-3 w-3" />
                                        Relationship Type
                                      </h6>
                                      <Badge variant="secondary" className="text-xs">
                                        {section.relationship_type}
                                      </Badge>
                                    </div>
                                  )}
                                  
                                  {section.key_concepts && section.key_concepts.length > 0 && (
                                    <div>
                                      <h6 className="font-medium text-xs text-orange-600 mb-1 flex items-center gap-1">
                                        <Tag className="h-3 w-3" />
                                        Key Concepts
                                      </h6>
                                      <div className="flex flex-wrap gap-1">
                                        {section.key_concepts.map((concept, idx) => (
                                          <Badge key={idx} variant="outline" className="text-xs">
                                            {concept}
                                          </Badge>
                                        ))}
                                      </div>
                                    </div>
                                  )}
                                </div>
                              </div>
                            )}

                            {/* Action Box */}
                            <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-950/20 dark:to-pink-950/20 rounded-lg p-3 border-l-4 border-purple-500/50 w-full">
                              <div className="flex items-center justify-between">
                                <div>
                                  <h6 className="font-medium text-xs text-purple-600 mb-1 flex items-center gap-1">
                                    <ExternalLink className="h-3 w-3" />
                                    Quick Action
                                  </h6>
                                  <p className="text-xs text-foreground">
                                    Navigate to this section
                                  </p>
                                </div>
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
                            </div>
                          </CardContent>
                        </Card>
                      );
                    })}
                  </div>
                </div>
              </CardContent>
            </Card>
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