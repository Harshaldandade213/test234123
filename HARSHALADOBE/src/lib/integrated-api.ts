// Integrated API Service that routes between adobev4 and HARSHALADOBE backend
const ADOBEV4_API_URL = 'http://localhost:8000'; // adobev4 backend
const HARSHALADOBE_API_URL = 'http://localhost:8001'; // HARSHALADOBE backend

export interface DocumentInfo {
  id: string;
  name: string;
  title: string;
  outline: OutlineItem[];
  language: string;
  upload_timestamp: string;
}

export interface OutlineItem {
  level: string;
  text: string;
  page: number;
}

export interface RelatedSection {
  document: string;
  section_title: string;
  page_number: number;
  relevance_score: number;
  explanation: string;
}

export interface Insight {
  type: 'takeaway' | 'fact' | 'contradiction' | 'connection' | 'info' | 'error';
  content: string;
}

export interface ComprehensiveInsights {
  insights: Insight[];
  persona_insights: Array<{
    type: 'relevance' | 'action' | 'skill';
    content: string;
  }>;
  topic_analysis: {
    main_themes?: string;
    trending_topics?: string;
    research_opportunities?: string;
  };
  web_facts: Array<{
    type: string;
    query: string;
    description: string;
  }>;
  keywords: string[];
  search_queries: string[];
}

export interface ReadingProgress {
  progress_percentage: number;
  time_spent_minutes: number;
  estimated_remaining_minutes: number;
  estimated_total_minutes: number;
}

export interface HighlightData {
  text: string;
  color: string;
  page: number;
  documentName: string;
}

export interface SimplifiedText {
  text: string;
  original: string;
}

export interface PassageAnalysis {
  category: string;
  justification: string;
  quote: string;
  source: string;
}

export interface DetailedAnalysisResult {
  query: string;
  analysis: PassageAnalysis[];
  summary: string;
}

export interface AnalysisResult {
  analysis_results: DetailedAnalysisResult;
  insights: string[];
}

class IntegratedApiService {
  private adobev4Url: string;
  private harshalaUrl: string;

  constructor() {
    this.adobev4Url = ADOBEV4_API_URL;
    this.harshalaUrl = HARSHALADOBE_API_URL;
  }

  // Route insights calls to adobev4's analyze_and_categorize function
  async generateInsights(
    text: string,
    persona: string,
    jobToBeDone: string,
    documentContext?: string
  ): Promise<Insight[]> {
    try {
      // First, try to use adobev4's analyze_and_categorize function
      const analysisResponse = await fetch(`${this.adobev4Url}/analyze-documents`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document_ids: [], // Empty for text-based analysis
          persona: persona,
          job_to_be_done: jobToBeDone,
        }),
      });

      if (analysisResponse.ok) {
        const analysisData: AnalysisResult = await analysisResponse.json();
        
        // Convert analysis results to insights format
        const insights: Insight[] = analysisData.insights.map((insight, index) => ({
          type: 'takeaway' as const,
          content: insight
        }));

        return insights;
      } else {
        // Fallback to HARSHALADOBE backend if adobev4 fails
        console.warn('adobev4 analysis failed, falling back to HARSHALADOBE backend');
        return this.fallbackToHarshalaInsights(text, persona, jobToBeDone, documentContext);
      }
    } catch (error) {
      console.error('Error calling adobev4 analysis:', error);
      // Fallback to HARSHALADOBE backend
      return this.fallbackToHarshalaInsights(text, persona, jobToBeDone, documentContext);
    }
  }

  private async fallbackToHarshalaInsights(
    text: string,
    persona: string,
    jobToBeDone: string,
    documentContext?: string
  ): Promise<Insight[]> {
    const response = await fetch(`${this.harshalaUrl}/insights`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        persona,
        job_to_be_done: jobToBeDone,
        document_context: documentContext,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate insights: ${response.statusText}`);
    }

    const data = await response.json();
    return data.insights;
  }

  // Get detailed passage analysis results
  async getDetailedAnalysis(
    documentIds: string[],
    persona: string,
    jobToBeDone: string,
    query?: string
  ): Promise<DetailedAnalysisResult> {
    try {
      // Route through HARSHALADOBE backend which has access to the documents
      const analysisResponse = await fetch(`${this.harshalaUrl}/analyze-documents`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document_ids: documentIds,
          persona: persona,
          job_to_be_done: jobToBeDone,
          query: query || `${persona} ${jobToBeDone}`, // Use provided query or default
        }),
      });

      if (analysisResponse.ok) {
        const analysisData: AnalysisResult = await analysisResponse.json();
        return analysisData.analysis_results;
      } else {
        throw new Error(`Analysis failed: ${analysisResponse.statusText}`);
      }
    } catch (error) {
      console.error('Error getting detailed analysis:', error);
      throw error;
    }
  }

  // Analyze query using adobev4's analyze-query endpoint
  async analyzeQuery(query: string, documentIds?: string[]): Promise<DetailedAnalysisResult> {
    try {
      const formData = new FormData();
      formData.append('query', query);
      
      // Add document IDs if provided
      if (documentIds && documentIds.length > 0) {
        formData.append('document_ids', JSON.stringify(documentIds));
      }

      const analysisResponse = await fetch(`${this.adobev4Url}/analyze-query`, {
        method: 'POST',
        body: formData,
      });

      if (analysisResponse.ok) {
        const analysisData = await analysisResponse.json();
        return analysisData;
      } else {
        throw new Error(`Query analysis failed: ${analysisResponse.statusText}`);
      }
    } catch (error) {
      console.error('Error analyzing query:', error);
      throw error;
    }
  }

  // Route comprehensive insights to adobev4 first, then HARSHALADOBE
  async generateComprehensiveInsights(
    text: string,
    persona: string,
    jobToBeDone: string,
    documentContext?: string
  ): Promise<ComprehensiveInsights> {
    try {
      // Try adobev4's analyze_and_categorize with enhanced processing
      const analysisResponse = await fetch(`${this.adobev4Url}/analyze-documents`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document_ids: [],
          persona: persona,
          job_to_be_done: jobToBeDone,
        }),
      });

      if (analysisResponse.ok) {
        const analysisData: AnalysisResult = await analysisResponse.json();
        
        // Convert to comprehensive insights format
        const comprehensiveInsights: ComprehensiveInsights = {
          insights: analysisData.insights.map((insight, index) => ({
            type: 'takeaway' as const,
            content: insight
          })),
          persona_insights: [{
            type: 'relevance' as const,
            content: `Analysis relevant to ${persona} for ${jobToBeDone}`
          }],
          topic_analysis: {
            main_themes: 'Analysis from adobev4 backend',
            trending_topics: 'Based on document analysis',
            research_opportunities: 'Further research opportunities identified'
          },
          web_facts: [],
          keywords: [persona, jobToBeDone],
          search_queries: [`${persona} ${jobToBeDone}`, text.substring(0, 50)]
        };

        return comprehensiveInsights;
      } else {
        // Fallback to HARSHALADOBE backend
        console.warn('adobev4 comprehensive analysis failed, falling back to HARSHALADOBE backend');
        return this.fallbackToHarshalaComprehensiveInsights(text, persona, jobToBeDone, documentContext);
      }
    } catch (error) {
      console.error('Error calling adobev4 comprehensive analysis:', error);
      return this.fallbackToHarshalaComprehensiveInsights(text, persona, jobToBeDone, documentContext);
    }
  }

  private async fallbackToHarshalaComprehensiveInsights(
    text: string,
    persona: string,
    jobToBeDone: string,
    documentContext?: string
  ): Promise<ComprehensiveInsights> {
    const response = await fetch(`${this.harshalaUrl}/comprehensive-insights`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        persona,
        job_to_be_done: jobToBeDone,
        document_context: documentContext,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate comprehensive insights: ${response.statusText}`);
    }

    return response.json();
  }

  // Document upload - use HARSHALADOBE backend
  async uploadPDFs(files: File[], persona?: string, jobToBeDone?: string): Promise<DocumentInfo[]> {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });
    
    if (persona) {
      formData.append('persona', persona);
    }
    if (jobToBeDone) {
      formData.append('job_to_be_done', jobToBeDone);
    }

    const response = await fetch(`${this.harshalaUrl}/upload-pdfs`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return response.json();
  }

  // Document management - use HARSHALADOBE backend
  async getDocuments(): Promise<DocumentInfo[]> {
    const response = await fetch(`${this.harshalaUrl}/documents`);
    if (!response.ok) {
      throw new Error(`Failed to fetch documents: ${response.statusText}`);
    }
    return response.json();
  }

  async deleteDocument(docId: string): Promise<void> {
    const response = await fetch(`${this.harshalaUrl}/documents/${docId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error(`Failed to delete document: ${response.statusText}`);
    }
  }

  // Search - try adobev4 first, then HARSHALADOBE
  async searchDocuments(query: string, k: number = 5): Promise<any> {
    try {
      const response = await fetch(`${this.adobev4Url}/search-documents`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          query: query,
          k: k.toString(),
        }),
      });

      if (response.ok) {
        return response.json();
      } else {
        // Fallback to HARSHALADOBE
        return this.fallbackToHarshalaSearch(query, k);
      }
    } catch (error) {
      console.error('Error calling adobev4 search:', error);
      return this.fallbackToHarshalaSearch(query, k);
    }
  }

  private async fallbackToHarshalaSearch(query: string, k: number): Promise<any> {
    const response = await fetch(`${this.harshalaUrl}/search-documents`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        query: query,
        k: k.toString(),
      }),
    });

    if (!response.ok) {
      throw new Error(`Search failed: ${response.statusText}`);
    }

    return response.json();
  }

  // Podcast generation - use adobev4's generate_podcast function
  async generatePodcast(
    text: string,
    relatedSections: string[],
    insights: string[]
  ): Promise<{ script: string; audio_url: string }> {
    try {
      // Use adobev4's generate_podcast function
      const response = await fetch(`${this.adobev4Url}/generate-podcast`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: text,
          output_filename: `podcast_${Date.now()}.mp3`
        }),
      });

      if (response.ok) {
        const data = await response.json();
        return {
          script: text,
          audio_url: `/audio/${data.file}`
        };
      } else {
        // Fallback to HARSHALADOBE
        return this.fallbackToHarshalaPodcast(text, relatedSections, insights);
      }
    } catch (error) {
      console.error('Error calling adobev4 podcast generation:', error);
      return this.fallbackToHarshalaPodcast(text, relatedSections, insights);
    }
  }

  private async fallbackToHarshalaPodcast(
    text: string,
    relatedSections: string[],
    insights: string[]
  ): Promise<{ script: string; audio_url: string }> {
    const response = await fetch(`${this.harshalaUrl}/podcast`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        related_sections: relatedSections,
        insights,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate podcast: ${response.statusText}`);
    }

    return response.json();
  }

  // Text simplification - use HARSHALADOBE backend
  async simplifyText(text: string): Promise<SimplifiedText> {
    const response = await fetch(`${this.harshalaUrl}/simplify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`Failed to simplify text: ${response.statusText}`);
    }

    return response.json();
  }

  // Term definition - use HARSHALADOBE backend
  async defineTerm(term: string, context: string): Promise<string> {
    const response = await fetch(`${this.harshalaUrl}/define-term`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        term,
        context,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to define term: ${response.statusText}`);
    }

    const data = await response.json();
    return data.definition;
  }

  // Reading progress - use HARSHALADOBE backend
  async trackReadingProgress(
    docId: string,
    currentPage: number,
    totalPages: number,
    timeSpent: number
  ): Promise<ReadingProgress> {
    const formData = new FormData();
    formData.append('doc_id', docId);
    formData.append('current_page', currentPage.toString());
    formData.append('total_pages', totalPages.toString());
    formData.append('time_spent', timeSpent.toString());

    const response = await fetch(`${this.harshalaUrl}/reading-progress`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Failed to track reading progress: ${response.statusText}`);
    }

    return response.json();
  }

  // PDF viewing - use HARSHALADOBE backend
  async getPDF(docId: string): Promise<Blob> {
    const response = await fetch(`${this.harshalaUrl}/pdf/${docId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch PDF: ${response.statusText}`);
    }
    return response.blob();
  }

  // Audio files - try both backends
  async getAudio(filename: string): Promise<Blob> {
    try {
      // Try adobev4 first
      const response = await fetch(`${this.adobev4Url}/audio/${filename}`);
      if (response.ok) {
        return response.blob();
      } else {
        // Fallback to HARSHALADOBE
        const harshalaResponse = await fetch(`${this.harshalaUrl}/audio/${filename}`);
        if (!harshalaResponse.ok) {
          throw new Error(`Audio file not found: ${filename}`);
        }
        return harshalaResponse.blob();
      }
    } catch (error) {
      console.error('Error fetching audio:', error);
      throw new Error(`Failed to fetch audio: ${filename}`);
    }
  }

  // Related sections - use adobev4's perform_search
  async getRelatedSections(
    documentIds: string[],
    currentPage: number,
    currentSection: string,
    persona: string,
    jobToBeDone: string
  ): Promise<RelatedSection[]> {
    try {
      const response = await fetch(`${this.adobev4Url}/related-sections`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          document_ids: JSON.stringify(documentIds),
          current_page: currentPage.toString(),
          current_section: currentSection,
          persona: persona,
          job_to_be_done: jobToBeDone,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        return data.related_sections;
      } else {
        // Fallback to HARSHALADOBE
        return this.fallbackToHarshalaRelatedSections(documentIds, currentPage, currentSection, persona, jobToBeDone);
      }
    } catch (error) {
      console.error('Error calling adobev4 related sections:', error);
      return this.fallbackToHarshalaRelatedSections(documentIds, currentPage, currentSection, persona, jobToBeDone);
    }
  }

  private async fallbackToHarshalaRelatedSections(
    documentIds: string[],
    currentPage: number,
    currentSection: string,
    persona: string,
    jobToBeDone: string
  ): Promise<RelatedSection[]> {
    const response = await fetch(`${this.harshalaUrl}/related-sections`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        document_ids: JSON.stringify(documentIds),
        current_page: currentPage.toString(),
        current_section: currentSection,
        persona: persona,
        job_to_be_done: jobToBeDone,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to get related sections: ${response.statusText}`);
    }

    const data = await response.json();
    return data.related_sections;
  }

  // Library endpoints - use HARSHALADOBE backend
  async getLibraryDocuments(persona?: string, jobToBeDone?: string): Promise<DocumentInfo[]> {
    const params = new URLSearchParams();
    if (persona) params.append('persona', persona);
    if (jobToBeDone) params.append('job_to_be_done', jobToBeDone);

    const response = await fetch(`${this.harshalaUrl}/library/documents?${params}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch library documents: ${response.statusText}`);
    }
    return response.json();
  }

  async getPersonas(): Promise<string[]> {
    const response = await fetch(`${this.harshalaUrl}/library/personas`);
    if (!response.ok) {
      throw new Error(`Failed to fetch personas: ${response.statusText}`);
    }
    return response.json();
  }

  async getJobs(): Promise<string[]> {
    const response = await fetch(`${this.harshalaUrl}/library/jobs`);
    if (!response.ok) {
      throw new Error(`Failed to fetch jobs: ${response.statusText}`);
    }
    return response.json();
  }

  // Highlights - use HARSHALADOBE backend
  async addHighlight(highlight: HighlightData): Promise<void> {
    const response = await fetch(`${this.harshalaUrl}/highlights`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(highlight),
    });

    if (!response.ok) {
      throw new Error(`Failed to add highlight: ${response.statusText}`);
    }
  }

  async getHighlights(documentName: string): Promise<HighlightData[]> {
    const response = await fetch(`${this.harshalaUrl}/highlights/${encodeURIComponent(documentName)}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch highlights: ${response.statusText}`);
    }
    return response.json();
  }

  // Cross connections - use adobev4's perform_search
  async getCrossConnections(docId: string): Promise<any> {
    try {
      const response = await fetch(`${this.adobev4Url}/cross-connections/${docId}`);
      if (response.ok) {
        return response.json();
      } else {
        // Fallback to HARSHALADOBE
        return this.fallbackToHarshalaCrossConnections(docId);
      }
    } catch (error) {
      console.error('Error calling adobev4 cross connections:', error);
      return this.fallbackToHarshalaCrossConnections(docId);
    }
  }

  private async fallbackToHarshalaCrossConnections(docId: string): Promise<any> {
    const response = await fetch(`${this.harshalaUrl}/cross-connections/${docId}`);
    if (!response.ok) {
      throw new Error(`Failed to get cross connections: ${response.statusText}`);
    }
    return response.json();
  }

  // Strategic insights - use HARSHALADOBE backend
  async generateStrategicInsights(
    text: string,
    persona: string,
    jobToBeDone: string,
    documentContext?: string
  ): Promise<any> {
    const response = await fetch(`${this.harshalaUrl}/strategic-insights`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        persona,
        job_to_be_done: jobToBeDone,
        document_context: documentContext,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate strategic insights: ${response.statusText}`);
    }

    return response.json();
  }

  // Contextual analysis - use HARSHALADOBE backend
  async analyzeDocumentContext(
    docId: string,
    pageNumber: number,
    sectionText: string
  ): Promise<any> {
    const formData = new FormData();
    formData.append('doc_id', docId);
    formData.append('page_number', pageNumber.toString());
    formData.append('section_text', sectionText);

    const response = await fetch(`${this.harshalaUrl}/contextual-analysis`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Failed to analyze document context: ${response.statusText}`);
    }

    return response.json();
  }

  // Multi-document insights - use adobev4's analyze_and_categorize
  async generateMultiDocumentInsights(
    documentIds: string[],
    persona: string,
    jobToBeDone: string
  ): Promise<any> {
    try {
      const response = await fetch(`${this.adobev4Url}/analyze-documents`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document_ids: documentIds,
          persona: persona,
          job_to_be_done: jobToBeDone,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        return {
          analyzed_documents: documentIds.length,
          document_titles: documentIds,
          insights: {
            overarching_patterns: [],
            contradictions: [],
            knowledge_gaps: [],
            synthesis_insights: data.insights.map((insight: string, index: number) => ({
              insight: insight,
              supporting_documents: documentIds,
              implications: 'Based on adobev4 analysis',
              confidence: 0.85
            })),
            actionable_recommendations: []
          }
        };
      } else {
        // Fallback to HARSHALADOBE
        return this.fallbackToHarshalaMultiDocumentInsights(documentIds, persona, jobToBeDone);
      }
    } catch (error) {
      console.error('Error calling adobev4 multi-document insights:', error);
      return this.fallbackToHarshalaMultiDocumentInsights(documentIds, persona, jobToBeDone);
    }
  }

  private async fallbackToHarshalaMultiDocumentInsights(
    documentIds: string[],
    persona: string,
    jobToBeDone: string
  ): Promise<any> {
    const response = await fetch(`${this.harshalaUrl}/multi-document-insights`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        document_ids: documentIds,
        persona: persona,
        job_to_be_done: jobToBeDone,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate multi-document insights: ${response.statusText}`);
    }

    return response.json();
  }

  // Health check - check both backends
  async healthCheck(): Promise<{ adobev4: boolean; harshala: boolean }> {
    const adobev4Health = await fetch(`${this.adobev4Url}/health`).then(r => r.ok).catch(() => false);
    const harshalaHealth = await fetch(`${this.harshalaUrl}/health`).then(r => r.ok).catch(() => false);
    
    return {
      adobev4: adobev4Health,
      harshala: harshalaHealth
    };
  }
}

// Export singleton instance
export const integratedApiService = new IntegratedApiService();
export default integratedApiService;
