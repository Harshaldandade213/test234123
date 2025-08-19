import { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useToast } from '@/hooks/use-toast';
import { DocumentOutline } from './DocumentOutline';
import { 
  FileText, 
  Search, 
  ChevronDown,
  ChevronRight,
  BookOpen,
  List,
  Clock,
  Star,
  Bookmark,
  Eye,
  ArrowRight,
  Play,
  Pause,
  RotateCcw,
  Target,
  Zap,
  Users,
  Filter,
  Library,
  Compass,
  Download
} from 'lucide-react';

interface OutlineItem {
  id: string;
  title: string;
  level: number;
  page: number;
  children?: OutlineItem[];
}

interface PDFDocument {
  id: string;
  name: string;
  title: string;
  url: string;
  outline: OutlineItem[];
}

interface QuickAction {
  id: string;
  label: string;
  description: string;
  icon: any;
  action: () => void;
  shortcut?: string;
}

interface ReadingSession {
  startTime: number;
  currentPage: number;
  totalPages: number;
  bookmarks: number[];
  progress: number;
}

interface EnhancedLeftPanelProps {
  documents?: PDFDocument[];
  currentDocument?: PDFDocument | null;
  currentPage?: number;
  totalPages?: number;
  persona?: string;
  jobToBeDone?: string;
  onDocumentChange?: (document: PDFDocument) => void;
  onPageNavigate?: (page: number) => void;
  onSectionNavigate?: (page: number, section: string) => void;
  onQuickAction?: (actionId: string) => void;
  documentAnalysisStatus?: {[key: string]: string};
}

export function EnhancedLeftPanel({
  documents = [],
  currentDocument,
  currentPage = 1,
  totalPages = 1,
  persona,
  jobToBeDone,
  onDocumentChange,
  onPageNavigate,
  onSectionNavigate,
  onQuickAction,
  documentAnalysisStatus = {}
}: EnhancedLeftPanelProps) {
  // Set default values for persona and jobToBeDone
  const currentPersona = persona || 'student';
  const currentJobToBeDone = jobToBeDone || 'read';
  const [searchTerm, setSearchTerm] = useState('');
  const [activeTab, setActiveTab] = useState('explore');
  const [expandedSections, setExpandedSections] = useState<Set<string>>(
    new Set(['outline', 'actions'])
  );
  const [expandedOutlineItems, setExpandedOutlineItems] = useState<Set<string>>(new Set());
  const [readingSession, setReadingSession] = useState<ReadingSession>({
    startTime: Date.now(),
    currentPage: currentPage,
    totalPages: totalPages,
    bookmarks: [],
    progress: 0
  });
  const { toast } = useToast();

  // Debounce utility function
  const debounce = useCallback((func: Function, delay: number) => {
    let timeoutId: NodeJS.Timeout;
    return (...args: any[]) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => func(...args), delay);
    };
  }, []);

  // Debounced search handler
  const debouncedSearch = useCallback(
    debounce((value: string) => {
      if (value.trim() !== '') {
        setSearchTerm(value);
      }
    }, 250),
    []
  );

  // Update reading session when page changes
  useEffect(() => {
    setReadingSession(prev => ({
      ...prev,
      currentPage,
      totalPages,
      progress: Math.round((currentPage / totalPages) * 100)
    }));
  }, [currentPage, totalPages]);

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev => {
      const newSet = new Set(prev);
      if (newSet.has(sectionId)) {
        newSet.delete(sectionId);
      } else {
        newSet.add(sectionId);
      }
      return newSet;
    });
  };

  const toggleOutlineItem = (itemId: string) => {
    setExpandedOutlineItems(prev => {
      const newSet = new Set(prev);
      if (newSet.has(itemId)) {
        newSet.delete(itemId);
      } else {
        newSet.add(itemId);
      }
      return newSet;
    });
  };

  const handleOutlineClick = (item: OutlineItem) => {
    if (onPageNavigate) {
      onPageNavigate(item.page);
    }
    if (onSectionNavigate) {
      onSectionNavigate(item.page, item.title);
    }
    toast({
      title: "Navigating to Section",
      description: `${item.title} - Page ${item.page}`,
    });
  };

  const handleDocumentChange = (document: PDFDocument) => {
    if (onDocumentChange) {
      onDocumentChange(document);
      toast({
        title: "Document Changed",
        description: `Now viewing: ${document.name}`,
      });
    }
  };

  const addBookmark = () => {
    setReadingSession(prev => ({
      ...prev,
      bookmarks: [...prev.bookmarks, currentPage]
    }));
    toast({
      title: "Bookmark Added",
      description: `Page ${currentPage} bookmarked`,
    });
  };

  const removeBookmark = (page: number) => {
    setReadingSession(prev => ({
      ...prev,
      bookmarks: prev.bookmarks.filter(p => p !== page)
    }));
    toast({
      title: "Bookmark Removed",
      description: `Page ${page} bookmark removed`,
    });
  };

  const quickActions: QuickAction[] = [
    {
      id: 'bookmark',
      label: 'Bookmark Page',
      description: 'Save current page for quick access',
      icon: Bookmark,
      action: addBookmark,
      shortcut: 'Ctrl+B'
    },
    {
      id: 'strategic',
      label: 'AI Recommendations',
      description: 'Get personalized reading suggestions',
      icon: Target,
      action: () => onQuickAction?.('strategic'),
      shortcut: 'Ctrl+R'
    },
    {
      id: 'highlights',
      label: 'View Highlights',
      description: 'See all highlighted content',
      icon: Zap,
      action: () => onQuickAction?.('highlights'),
      shortcut: 'Ctrl+H'
    },
    {
      id: 'insights',
      label: 'Generate Insights',
      description: 'Extract key insights from content',
      icon: Eye,
      action: () => onQuickAction?.('insights'),
      shortcut: 'Ctrl+I'
    },
    {
      id: 'summary',
      label: 'Document Summary',
      description: 'Get AI-generated document summary',
      icon: FileText,
      action: () => onQuickAction?.('summary'),
      shortcut: 'Ctrl+S'
    },
    {
      id: 'export',
      label: 'Export Notes',
      description: 'Export your notes and highlights',
      icon: Download,
      action: () => onQuickAction?.('export'),
      shortcut: 'Ctrl+E'
    }
  ];

  const filteredOutline = currentDocument?.outline?.filter(item =>
    item.title.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  // Debug information for outline data
  console.log('Document Outline Debug:', {
    currentDocument: currentDocument?.name,
    hasOutline: !!currentDocument?.outline,
    outlineLength: currentDocument?.outline?.length || 0,
    outline: currentDocument?.outline
  });

  // Generate basic outline when none exists
  const generateBasicOutline = (): OutlineItem[] => {
    if (!currentDocument || !totalPages) return [];
    
    const basicOutline: OutlineItem[] = [];
    
    // Create smart sections based on document length
    if (totalPages <= 10) {
      // Short document: individual pages
      for (let i = 1; i <= totalPages; i++) {
        basicOutline.push({
          id: `page-${i}`,
          title: `Page ${i}`,
          level: 1,
          page: i,
          children: []
        });
      }
    } else if (totalPages <= 30) {
      // Medium document: 5-page sections
      const pagesPerSection = 5;
      for (let i = 1; i <= totalPages; i += pagesPerSection) {
        const endPage = Math.min(i + pagesPerSection - 1, totalPages);
        basicOutline.push({
          id: `section-${i}`,
          title: `Section ${Math.ceil(i / pagesPerSection)} (Pages ${i}-${endPage})`,
          level: 1,
          page: i,
          children: []
        });
      }
    } else {
      // Long document: logical sections
      const sectionsCount = Math.min(12, Math.max(6, Math.ceil(totalPages / 10)));
      const pagesPerSection = Math.ceil(totalPages / sectionsCount);
      
      for (let i = 0; i < sectionsCount; i++) {
        const startPage = i * pagesPerSection + 1;
        const endPage = Math.min((i + 1) * pagesPerSection, totalPages);
        
        if (startPage <= totalPages) {
          basicOutline.push({
            id: `chapter-${startPage}`,
            title: `Chapter ${i + 1} (Pages ${startPage}-${endPage})`,
            level: 1,
            page: startPage,
            children: []
          });
        }
      }
    }
    
    return basicOutline;
  };

  // Use filtered outline or generate basic outline as fallback
  const displayOutline = filteredOutline.length > 0 ? filteredOutline : generateBasicOutline();

  const renderOutlineItem = (item: OutlineItem, depth: number = 0) => {
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedOutlineItems.has(item.id);
    const paddingLeft = depth * 16 + 8;
    const isActive = Math.abs(currentPage - item.page) <= 1;
    const isGeneratedItem = item.id.startsWith('page-') || item.id.startsWith('section-') || item.id.startsWith('chapter-');

    return (
      <div key={item.id} className="w-full">
        <div 
          className={`
            flex items-center gap-3 py-3 px-3 rounded-lg cursor-pointer transition-all duration-200
            ${isActive 
              ? 'bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border-l-4 border-l-blue-500 text-blue-900 dark:text-blue-100 shadow-sm' 
              : 'hover:bg-slate-50 dark:hover:bg-slate-700/50 border-l-4 border-l-transparent'
            }
            ${isGeneratedItem ? 'border-l-4 border-l-slate-300 dark:border-l-slate-600' : ''}
          `}
          style={{ paddingLeft: `${paddingLeft + 8}px` }}
          onClick={() => handleOutlineClick(item)}
        >
          {hasChildren && (
            <Button
              variant="ghost"
              size="sm"
              className="h-5 w-5 p-0 hover:bg-slate-200 dark:hover:bg-slate-600 rounded"
              onClick={(e) => {
                e.stopPropagation();
                toggleOutlineItem(item.id);
              }}
            >
              {isExpanded ? 
                <ChevronDown className="h-3 w-3 text-slate-600 dark:text-slate-400" /> : 
                <ChevronRight className="h-3 w-3 text-slate-600 dark:text-slate-400" />
              }
            </Button>
          )}
          {!hasChildren && <div className="w-5" />}
          
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <span 
                className={`text-sm overflow-hidden whitespace-nowrap text-ellipsis ${
                  depth === 0 ? 'font-semibold' : 
                  depth === 1 ? 'font-medium' : 'font-normal text-slate-600 dark:text-slate-400'
                } ${isGeneratedItem ? 'italic text-slate-500 dark:text-slate-400' : ''}`}
                title={item.title}
              >
                {item.title}
              </span>
              <Badge variant="outline" className={`text-xs ml-2 flex-shrink-0 ${
                isActive 
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-700' 
                  : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-600'
              }`}>
                {item.page}
              </Badge>
            </div>
          </div>
        </div>
        
        {hasChildren && isExpanded && (
          <div className="ml-2">
            {item.children!.map(child => renderOutlineItem(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  const getPersonaIcon = (persona?: string) => {
    const personaType = persona?.toLowerCase() || 'student';
    switch (personaType) {
      case 'student': return '🎓';
      case 'researcher': return '🔬';
      case 'professional': return '💼';
      case 'expert': return '👨‍🏫';
      default: return '🎓'; // Default to student icon
    }
  };

    return (
    <div className="flex flex-col h-full min-h-0 overflow-hidden bg-gradient-to-b from-slate-50 to-white dark:from-slate-900 dark:to-slate-800 border-r border-slate-200 dark:border-slate-700">
      {/* Sidebar Header - Fixed */}
      <div className="flex-shrink-0 flex flex-col">
        {/* Tabbed Interface */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-700 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList 
              className="grid w-full grid-cols-2 bg-slate-100 dark:bg-slate-700"
              role="tablist"
            >
              <TabsTrigger 
                value="explore" 
                className="flex items-center gap-2 data-[state=active]:bg-white dark:data-[state=active]:bg-slate-800 data-[state=active]:shadow-sm focus-visible:outline-2 focus-visible:outline-blue-500 focus-visible:outline-offset-2"
                role="tab"
                aria-selected={activeTab === 'explore'}
                aria-label="Explore document tools and navigation"
              >
                <Compass className="h-4 w-4" />
                Explore
              </TabsTrigger>
              <TabsTrigger 
                value="library" 
                className="flex items-center gap-2 data-[state=active]:bg-white dark:data-[state=active]:bg-slate-800 data-[state=active]:shadow-sm focus-visible:outline-2 focus-visible:outline-blue-500 focus-visible:outline-offset-2"
                role="tab"
                aria-selected={activeTab === 'library'}
                aria-label="Browse document library"
              >
                <Library className="h-4 w-4" />
                Library
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </div>

        {/* Search Bar - Fixed */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-700 bg-white/50 dark:bg-slate-800/50">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
            <Input
              placeholder="Search sections..."
              value={searchTerm}
              onChange={(e) => debouncedSearch(e.target.value)}
              className="pl-11 text-sm bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-600 focus:border-blue-500 dark:focus:border-blue-400 focus:ring-blue-500/20 dark:focus:ring-blue-400/20 rounded-lg shadow-sm focus-visible:outline-2 focus-visible:outline-blue-500 focus-visible:outline-offset-2"
              aria-label="Search document sections"
            />
          </div>
        </div>
      </div>

      {/* Sidebar Body - Scrollable */}
      <div className="flex-1 min-h-0 overflow-y-auto overflow-x-hidden">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="h-full flex flex-col">
          {/* Explore Tab */}
          <TabsContent value="explore" className="flex-1 flex flex-col mt-0 min-h-0">
            <div className="p-4 space-y-4 flex-1 min-h-0">
              {/* Document Outline */}
              <Collapsible 
                open={expandedSections.has('outline')}
                onOpenChange={() => toggleSection('outline')}
              >
                <CollapsibleTrigger asChild>
                  <Button variant="ghost" className="w-full justify-between p-0 h-auto hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg">
                        <List className="h-4 w-4 text-white" />
                      </div>
                      <div className="text-left">
                        <span className="font-semibold text-sm text-slate-900 dark:text-slate-100">Document Outline</span>
                        <p className="text-xs text-slate-500 dark:text-slate-400">Sections & structure</p>
                      </div>
                    </div>
                    {expandedSections.has('outline') ? 
                      <ChevronDown className="h-4 w-4 text-slate-500" /> : 
                      <ChevronRight className="h-4 w-4 text-slate-500" />
                    }
                  </Button>
                </CollapsibleTrigger>
                <CollapsibleContent className="mt-3">
                  <div className="h-80 overflow-hidden bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-600 shadow-sm">
                    <DocumentOutline
                      documents={documents}
                      outline={currentDocument?.outline}
                      currentDocument={currentDocument}
                      currentPage={currentPage}
                      onItemClick={(item) => {
                        onPageNavigate?.(item.page);
                        onSectionNavigate?.(item.page, item.title);
                      }}
                      onDocumentSwitch={(document) => {
                        onDocumentChange?.(document);
                      }}
                      documentAnalysisStatus={documentAnalysisStatus}
                    />
                  </div>
                </CollapsibleContent>
              </Collapsible>

              {/* Quick Actions */}
              <Collapsible 
                open={expandedSections.has('actions')}
                onOpenChange={() => toggleSection('actions')}
              >
                <CollapsibleTrigger asChild>
                  <Button variant="ghost" className="w-full justify-between p-0 h-auto hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg shadow-sm">
                        <Zap className="h-4 w-4 text-white" />
                      </div>
                      <div className="text-left">
                        <span className="font-semibold text-sm text-slate-900 dark:text-slate-100">Quick Actions</span>
                        <p className="text-xs text-slate-500 dark:text-slate-400">Essential tools & shortcuts</p>
                      </div>
                    </div>
                    {expandedSections.has('actions') ? 
                      <ChevronDown className="h-4 w-4 text-slate-500" /> : 
                      <ChevronRight className="h-4 w-4 text-slate-500" />
                    }
                  </Button>
                </CollapsibleTrigger>
                <CollapsibleContent className="mt-3">
                  <div className="grid grid-cols-2 gap-3">
                    {quickActions.map((action) => {
                      const Icon = action.icon;
                      const getActionColor = (actionId: string) => {
                        switch (actionId) {
                          case 'bookmark': return 'from-blue-400 to-blue-600';
                          case 'strategic': return 'from-purple-400 to-purple-600';
                          case 'highlights': return 'from-yellow-400 to-orange-500';
                          case 'insights': return 'from-green-400 to-emerald-600';
                          case 'summary': return 'from-indigo-400 to-indigo-600';
                          case 'export': return 'from-red-400 to-red-600';
                          default: return 'from-slate-400 to-slate-600';
                        }
                      };
                      
                      return (
                        <Button
                          key={action.id}
                          variant="outline"
                          size="sm"
                          onClick={action.action}
                          className="group flex flex-col gap-3 h-auto p-4 bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-600 hover:border-blue-300 dark:hover:border-blue-500 hover:bg-gradient-to-br hover:from-blue-50 hover:to-indigo-50 dark:hover:from-blue-900/10 dark:hover:to-indigo-900/10 transition-all duration-300 rounded-xl shadow-sm hover:shadow-md hover:-translate-y-0.5"
                          title={action.description}
                        >
                          <div className={`p-3 bg-gradient-to-br ${getActionColor(action.id)} rounded-xl shadow-sm group-hover:shadow-md transition-all duration-300 group-hover:scale-110`}>
                            <Icon className="h-5 w-5 text-white" />
                          </div>
                          <div className="flex flex-col gap-1 min-w-0">
                            <span className="text-xs font-semibold text-slate-700 dark:text-slate-300 overflow-hidden whitespace-nowrap text-ellipsis" title={action.label}>
                              {action.label}
                            </span>
                            {action.shortcut && (
                              <span className="text-xs text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-700 px-2 py-1 rounded-md text-center flex-shrink-0 font-mono" title={action.shortcut}>
                                {action.shortcut}
                              </span>
                            )}
                          </div>
                        </Button>
                      );
                    })}
                  </div>
                  
                  {/* Quick Actions Info */}
                  <div className="mt-4 p-3 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-lg border border-blue-200 dark:border-blue-700">
                    <div className="flex items-center gap-2 mb-2">
                      <div className="p-1 bg-blue-100 dark:bg-blue-800 rounded-lg">
                        <Zap className="h-3 w-3 text-blue-600 dark:text-blue-400" />
                      </div>
                      <span className="text-xs font-medium text-blue-700 dark:text-blue-300">Pro Tips</span>
                    </div>
                    <p className="text-xs text-blue-600 dark:text-blue-400">
                      Use keyboard shortcuts for faster access. Hover over any action to see its description.
                    </p>
                  </div>
                </CollapsibleContent>
              </Collapsible>
            </div>
          </TabsContent>

          {/* Library Tab */}
          <TabsContent value="library" className="flex-1 flex flex-col mt-0 min-h-0">
            <div className="p-4 space-y-4 flex-1 min-h-0">
              {/* Documents */}
              {documents.length > 0 ? (
                <div className="space-y-3 flex flex-col min-h-0">
                  <div className="flex items-center gap-2 mb-4 flex-shrink-0">
                    <div className="p-2 bg-gradient-to-br from-indigo-400 to-blue-500 rounded-lg">
                      <BookOpen className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-sm text-slate-900 dark:text-slate-100">Document Library</h3>
                      <p className="text-xs text-slate-500 dark:text-slate-400">{documents.length} document{documents.length !== 1 ? 's' : ''} available</p>
                    </div>
                  </div>
                  
                  <div className="space-y-3 flex-1 min-h-0">
                    {documents.map((doc) => (
                      <Button
                        key={doc.id}
                        variant={currentDocument?.id === doc.id ? "default" : "ghost"}
                        size="sm"
                        onClick={() => handleDocumentChange(doc)}
                        className={`w-full justify-start h-auto p-4 transition-all duration-200 ${
                          currentDocument?.id === doc.id 
                            ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-lg' 
                            : 'bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-600 hover:border-blue-300 dark:hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20'
                        } rounded-lg shadow-sm`}
                        title={doc.name}
                      >
                        <div className="flex-1 text-left min-w-0">
                          <div className={`text-sm font-semibold overflow-hidden whitespace-nowrap text-ellipsis ${
                            currentDocument?.id === doc.id ? 'text-white' : 'text-slate-700 dark:text-slate-300'
                          }`}>
                            {doc.name}
                          </div>
                          <div className={`text-xs overflow-hidden whitespace-nowrap text-ellipsis ${
                            currentDocument?.id === doc.id ? 'text-blue-100' : 'text-slate-500 dark:text-slate-400'
                          }`}>
                            {doc.outline?.length || 0} sections
                          </div>
                        </div>
                        {currentDocument?.id === doc.id && (
                          <div className="p-1 bg-white/20 rounded-full flex-shrink-0">
                            <ArrowRight className="h-3 w-3 text-white" />
                          </div>
                        )}
                      </Button>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="text-center py-12">
                  <BookOpen className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                  <p className="text-sm text-slate-500 dark:text-slate-400">No documents available</p>
                  <p className="text-xs text-slate-400 dark:text-slate-500 mt-1">Upload documents to get started</p>
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </div>

      {/* Footer - Reading Progress - Fixed */}
      <div className="flex-shrink-0 p-4 border-t border-slate-200 dark:border-slate-700 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-1.5 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg">
            <span className="text-sm text-white">{getPersonaIcon(currentPersona)}</span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-medium capitalize text-slate-900 dark:text-slate-100 overflow-hidden whitespace-nowrap text-ellipsis">{currentPersona} Mode</p>
            <p className="text-xs text-slate-600 dark:text-slate-400 overflow-hidden whitespace-nowrap text-ellipsis" title={currentJobToBeDone}>{currentJobToBeDone}</p>
          </div>
        </div>
        <div className="flex items-center justify-between text-xs text-slate-600 dark:text-slate-400 mb-2">
          <span>Page {readingSession.currentPage} of {readingSession.totalPages}</span>
          <span className="font-semibold">{readingSession.progress}%</span>
        </div>
        <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 overflow-hidden">
          <div 
            className="bg-gradient-to-r from-blue-500 to-indigo-600 h-1.5 rounded-full transition-all duration-300 ease-out" 
            style={{ width: `${readingSession.progress}%` }}
          />
        </div>
      </div>
    </div>
  );
}