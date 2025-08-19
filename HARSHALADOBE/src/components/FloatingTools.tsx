import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { useToast } from '@/hooks/use-toast';
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { 
  Lightbulb, 
  Mic, 
  BookOpen, 
  Settings, 
  Download,
  Sparkles,
  ChevronUp,
  ChevronDown,
  Copy,
  Search,
  X,
  Star
} from 'lucide-react';
import { PDFDocument, Highlight } from './PDFReader';

interface FloatingToolsProps {
  currentDocument: PDFDocument | null;
  currentPage: number;
  onHighlight: (highlight: Highlight) => void;
}

export function FloatingTools({ currentDocument, currentPage, onHighlight }: FloatingToolsProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [pinnedTools, setPinnedTools] = useState<Record<string, boolean>>({});
  const { toast } = useToast();

  const handleHighlightInsights = () => {
    if (!currentDocument) return;
    console.log('Generating AI-powered highlights for current content...');
    toast({
      title: "Feature requires content",
      description: "Highlight generation will work once you upload and load a PDF document.",
      variant: "default"
    });
  };

  const handlePodcastGeneration = async () => {
    if (!currentDocument) return;
    console.log('Generating podcast for current section...');
  };

  const handleToolSelect = (toolId: string) => {
    switch (toolId) {
      case 'insights':
        handleHighlightInsights();
        break;
      case 'podcast':
        handlePodcastGeneration();
        break;
      case 'smart-highlight':
        console.log('Smart highlighting...');
        break;
      default:
        break;
    }
  };

  const togglePin = (toolId: string) => {
    setPinnedTools(prev => ({
      ...prev,
      [toolId]: !prev[toolId]
    }));
  };

  const tools = [
    {
      id: 'insights',
      name: 'Insights Bulb',
      shortLabel: 'Insights',
      descShort: 'Generate AI insights',
      icon: Lightbulb,
      shortcut: 'Ctrl+I',
      className: 'bg-brand-primary hover:bg-brand-primary/90 text-text-on-brand'
    },
    {
      id: 'podcast',
      name: 'Podcast Mode',
      shortLabel: 'Podcast',
      descShort: 'Listen to summary',
      icon: Mic,
      shortcut: 'Ctrl+P',
      className: 'bg-brand-secondary hover:bg-brand-secondary/90 text-text-on-brand'
    },
    {
      id: 'smart-highlight',
      name: 'Smart Highlight',
      shortLabel: 'Highlight',
      descShort: 'AI-powered highlighting',
      icon: BookOpen,
      shortcut: 'Ctrl+H',
      className: 'bg-brand-accent hover:bg-brand-accent/90 text-text-primary'
    }
  ];

  const quickActions = [
    {
      id: 'copy',
      icon: Copy,
      label: 'Copy selection',
      action: () => navigator.clipboard?.writeText('Selected text would be copied')
    },
    {
      id: 'download',
      icon: Download,
      label: 'Download highlights',
      action: () => console.log('Downloading highlights...')
    }
  ];

  const filteredTools = tools.filter(tool => 
    tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    tool.descShort.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (!currentDocument) {
    return null;
  }

  return (
    <div className="absolute bottom-6 right-6 z-50">
      <div className={`
        floating-tool transition-all duration-300 bg-background border border-border rounded-xl shadow-lg
        ${isExpanded ? 'w-80' : 'w-auto'}
      `}>
        {/* Header */}
        <div className="sticky top-0 z-10 bg-gradient-to-br from-background via-background to-muted/10 border-b border-border/60 rounded-t-xl backdrop-blur-sm">
          {/* Main Header Row */}
          <div className="p-4 pb-3">
            <div className="flex items-center justify-between">
              {/* Left Side - Brand and Title */}
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary via-primary/90 to-primary/80 flex items-center justify-center shadow-lg">
                    <Sparkles className="h-4 w-4 text-primary-foreground" />
                  </div>
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-gradient-to-r from-accent to-accent/80 rounded-full border-2 border-background animate-pulse"></div>
                </div>
                <div className="flex flex-col">
                  <h3 className="text-base font-bold text-foreground tracking-tight">Smart Tools</h3>
                  <p className="text-xs text-muted-foreground bg-muted/30 px-2 py-0.5 rounded-full">AI-powered assistance</p>
                </div>
              </div>
              
              {/* Right Side - Badge and Toggle */}
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gradient-to-r from-muted/60 to-muted/40 border border-border/40 shadow-sm">
                  <div className="w-2 h-2 rounded-full bg-gradient-to-r from-primary to-accent animate-pulse"></div>
                  <Badge variant="secondary" className="text-xs font-semibold bg-transparent border-0 px-1">
                    {tools.length} tools
                  </Badge>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsExpanded(!isExpanded)}
                  className="h-8 w-8 p-0 rounded-lg hover:bg-muted/60 transition-all duration-200 hover:scale-105"
                >
                  {isExpanded ? (
                    <ChevronDown className="h-4 w-4" />
                  ) : (
                    <ChevronUp className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </div>
          </div>
          
          {/* Search Section */}
          {isExpanded && (
            <div className="px-4 pb-4">
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Search className="h-4 w-4 text-muted-foreground group-focus-within:text-primary transition-colors duration-200" />
                </div>
                <Input
                  placeholder="Search tools..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 pr-10 h-10 text-sm bg-muted/30 border-border/50 focus:border-primary/50 focus:bg-background transition-all duration-200 rounded-xl shadow-sm"
                />
                {searchQuery && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setSearchQuery('')}
                    className="absolute right-1 top-1/2 transform -translate-y-1/2 h-8 w-8 p-0 rounded-lg hover:bg-muted/60 transition-all duration-200"
                  >
                    <X className="h-3 w-3" />
                  </Button>
                )}
                {searchQuery && (
                  <div className="absolute right-10 top-1/2 transform -translate-y-1/2">
                    <div className="text-xs text-muted-foreground bg-gradient-to-r from-muted/60 to-muted/40 px-2 py-1 rounded-lg border border-border/30">
                      {filteredTools.length} found
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Expanded Content */}
        {isExpanded && (
          <div className="p-3 space-y-4">
            {/* Tool Cards Grid */}
            <div className="space-y-2">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                AI Tools
              </p>
              
              <div className="grid gap-3">
                {filteredTools.map((tool) => {
                  const Icon = tool.icon;
                  const isPinned = pinnedTools[tool.id];
                  
                  return (
                    <button
                      key={tool.id}
                      onClick={() => handleToolSelect(tool.id)}
                      onContextMenu={(e) => {
                        e.preventDefault();
                        togglePin(tool.id);
                      }}
                      className={`
                        relative grid grid-cols-[48px_1fr_auto] items-center gap-4 p-4 min-h-[80px]
                        rounded-2xl border border-border/50 bg-gradient-to-br from-card via-card to-card/80 hover:from-card/90 hover:via-card/90 hover:to-card/90
                        transition-all duration-300 hover:shadow-xl hover:-translate-y-1 hover:border-border/70
                        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
                        ${isPinned ? 'border-l-4 border-l-primary shadow-lg' : ''}
                      `}
                      aria-label={`${tool.name}${tool.shortcut ? `, shortcut ${tool.shortcut}` : ''}`}
                    >
                      {/* Icon */}
                      <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-muted/60 to-muted/40 flex items-center justify-center shadow-sm border border-border/30">
                        <Icon className="h-6 w-6 text-foreground" />
                      </div>
                      
                      {/* Text Content */}
                      <div className="min-w-0 flex flex-col gap-1.5">
                        <div 
                          className="text-sm font-bold text-foreground truncate"
                          title={tool.name}
                        >
                          {tool.shortLabel || tool.name}
                        </div>
                        {tool.descShort && (
                          <div 
                            className="text-xs text-muted-foreground truncate leading-relaxed"
                            title={tool.descShort}
                          >
                            {tool.descShort}
                          </div>
                        )}
                      </div>
                      
                      {/* Right Area - Shortcuts and Pin */}
                      <div className="flex items-center gap-3 min-w-[80px] justify-end">
                        {tool.shortcut && (
                          <kbd className="text-xs font-mono text-muted-foreground bg-gradient-to-r from-muted/60 to-muted/40 px-2.5 py-1.5 rounded-lg border border-border/30 shadow-sm">
                            {tool.shortcut}
                          </kbd>
                        )}
                        <button
                          className={`
                            p-2 rounded-xl transition-all duration-200
                            ${isPinned ? 'opacity-100 text-primary bg-primary/10' : 'opacity-0 group-hover:opacity-100 hover:bg-muted/60'}
                            hover:scale-110
                          `}
                          onClick={(e) => {
                            e.stopPropagation();
                            togglePin(tool.id);
                          }}
                          aria-pressed={isPinned}
                          aria-label={`${isPinned ? 'Unpin' : 'Pin'} ${tool.name}`}
                        >
                          <Star className={`h-4 w-4 ${isPinned ? 'fill-current' : ''}`} />
                        </button>
                      </div>
                    </button>
                  );
                })}
              </div>
              
              {isGenerating && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <div className="h-3 w-3 border-2 border-current border-t-transparent rounded-full animate-spin" />
                  <span>Generating insights...</span>
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="space-y-3">
              <p className="text-xs font-bold text-muted-foreground uppercase tracking-wider">
                Quick Actions
              </p>
              
              <div className="flex gap-3">
                {quickActions.map((action) => {
                  const Icon = action.icon;
                  return (
                    <Button
                      key={action.id}
                      variant="outline"
                      size="sm"
                      onClick={action.action}
                      className="flex-1 gap-2 h-10 rounded-xl border-border/50 hover:bg-muted/60 transition-all duration-200 hover:scale-105"
                      title={action.label}
                    >
                      <Icon className="h-4 w-4" />
                      <span className="sr-only">{action.label}</span>
                    </Button>
                  );
                })}
              </div>
            </div>

            {/* Page Info */}
            <div className="pt-4 border-t border-border/50">
              <div className="text-xs text-muted-foreground space-y-2">
                <div className="flex justify-between items-center">
                  <span className="font-medium">Current Page</span>
                  <span className="font-mono text-foreground bg-muted/50 px-2 py-1 rounded-lg">{currentPage}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="font-medium">Document</span>
                  <span className="truncate max-w-32 text-foreground bg-muted/50 px-2 py-1 rounded-lg" title={currentDocument.name}>
                    {currentDocument.name.split('.')[0]}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}