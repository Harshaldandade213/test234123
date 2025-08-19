import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { useToast } from '@/hooks/use-toast';
import { apiService, DocumentInfo } from '@/lib/api';
import { ThemeToggle } from './ThemeToggle';
import { Logo } from './Logo';
import { 
  Upload, 
  Brain, 
  Mic, 
  Eye, 
  Clock, 
  BookOpen,
  Accessibility,
  Palette,
  Volume2,
  Loader2,
  Library,
  ArrowRight,
  Sparkles,
  Zap,
  Shield,
  Globe,
  Target,
  Lightbulb,
  Users,
  BarChart3,
  FileText,
  Play
} from 'lucide-react';
import { useEffect } from 'react';

interface LandingPageProps {
  onStart: (documents: DocumentInfo[], persona: string, jobToBeDone: string) => void;
}

export function LandingPage({ onStart }: LandingPageProps) {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [persona, setPersona] = useState('');
  const [jobToBeDone, setJobToBeDone] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [showFeatureDemo, setShowFeatureDemo] = useState<string | null>(null);
  const { toast } = useToast();
  const navigate = useNavigate();
  
  // Typing animation state
  const [typedText, setTypedText] = useState('');
  const [showRestOfSentence, setShowRestOfSentence] = useState(false);
  const [restSentenceText, setRestSentenceText] = useState('');
  
  const fullText = 'Unlock the Power of';
  const restOfSentence = ' Intelligent Document Reading';
  
  // Typing animation effect
  useEffect(() => {
    let currentIndex = 0;
    const typingInterval = setInterval(() => {
      if (currentIndex <= fullText.length) {
        setTypedText(fullText.slice(0, currentIndex));
        currentIndex++;
      } else {
        clearInterval(typingInterval);
        setTimeout(() => {
          setShowRestOfSentence(true);
          let restIndex = 0;
          const restInterval = setInterval(() => {
            if (restIndex <= restOfSentence.length) {
              setRestSentenceText(restOfSentence.slice(0, restIndex));
              restIndex++;
            } else {
              clearInterval(restInterval);
            }
          }, 80);
        }, 300);
      }
    }, 120);

    return () => clearInterval(typingInterval);
  }, []);

  const handleFileUpload = (files: FileList) => {
    const pdfFiles = Array.from(files).filter(file => file.type === 'application/pdf');
    setSelectedFiles(prev => [...prev, ...pdfFiles]);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files) {
      handleFileUpload(e.dataTransfer.files);
    }
  };

  const handleStart = async () => {
    if (selectedFiles.length === 0) {
      toast({
        title: "No files selected",
        description: "Please upload at least one PDF file to continue.",
        variant: "destructive"
      });
      return;
    }

    const finalPersona = persona.trim() || 'student';
    const finalJobToBeDone = jobToBeDone.trim() || 'read';

    setIsUploading(true);
    try {
      const uploadedDocuments = await apiService.uploadPDFs(selectedFiles, finalPersona, finalJobToBeDone);
      
      toast({
        title: "Upload successful",
        description: `Successfully uploaded ${uploadedDocuments.length} document(s).`
      });
      
      onStart(uploadedDocuments, finalPersona, finalJobToBeDone);
    } catch (error) {
      console.error('Upload failed:', error);
      toast({
        title: "Upload failed",
        description: "Failed to upload and process PDFs. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsUploading(false);
    }
  };

  const handleFeatureClick = (feature: string) => {
    setShowFeatureDemo(feature);
    toast({
      title: `${feature.charAt(0).toUpperCase() + feature.slice(1)} Feature`,
      description: `Learn how to use ${feature} after uploading a PDF and starting your reading session.`
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,119,198,0.1),transparent_50%)]" />
        <div className="absolute top-0 left-0 w-full h-full bg-[linear-gradient(45deg,transparent_25%,rgba(255,255,255,0.02)_25%,rgba(255,255,255,0.02)_50%,transparent_50%,transparent_75%,rgba(255,255,255,0.02)_75%)] bg-[length:20px_20px]" />
      </div>
      
      {/* Floating Particles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-2 h-2 bg-purple-400 rounded-full animate-ping" style={{ animationDelay: '0s' }} />
        <div className="absolute top-40 right-20 w-1 h-1 bg-blue-400 rounded-full animate-ping" style={{ animationDelay: '1s' }} />
        <div className="absolute bottom-32 left-1/3 w-1.5 h-1.5 bg-pink-400 rounded-full animate-ping" style={{ animationDelay: '2s' }} />
        <div className="absolute bottom-20 right-10 w-1 h-1 bg-cyan-400 rounded-full animate-ping" style={{ animationDelay: '3s' }} />
        <div className="absolute top-1/2 left-1/4 w-1 h-1 bg-yellow-400 rounded-full animate-ping" style={{ animationDelay: '4s' }} />
        <div className="absolute top-1/3 right-1/3 w-1.5 h-1.5 bg-green-400 rounded-full animate-ping" style={{ animationDelay: '5s' }} />
      </div>

      {/* Header */}
      <header className="relative z-10 p-6 border-b border-white/10 bg-black/20 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative">
              <Logo size="sm" showText={false} className="h-10 w-10" />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full animate-pulse border-2 border-black" />
            </div>
            <div className="flex flex-col">
              <h1 className="text-xl font-bold text-white">Adobe+</h1>
              <p className="text-xs text-gray-400">Intelligent Reading Platform</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <ThemeToggle />
            <Button
              onClick={() => navigate('/library')}
              variant="outline"
              className="flex items-center gap-2 border-white/20 text-white hover:bg-white/10 hover:border-white/40"
            >
              <Library className="h-4 w-4" />
              My Library
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="relative z-10 flex-1 flex flex-col items-center justify-center p-6">
        <div className="max-w-6xl mx-auto text-center space-y-16 animate-fade-in">
          {/* Hero Content */}
          <div className="space-y-8">
            {/* Status Badge */}
            <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/30 text-purple-300 text-sm font-medium backdrop-blur-sm">
              <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse" />
              <Sparkles className="h-4 w-4" />
              Next-Generation AI Reading Assistant
            </div>

            {/* Main Headline */}
            <div className="space-y-6">
              <h2 className="text-7xl md:text-9xl font-black text-white leading-[0.9] tracking-tight">
                <span className="block">
                  {typedText}
                  {typedText.length < fullText.length && <span className="inline-block w-1 h-20 bg-gradient-to-b from-purple-400 to-pink-400 animate-pulse ml-2" />}
                </span>
                {showRestOfSentence && (
                  <span className="block bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">
                    {restSentenceText}
                  </span>
                )}
              </h2>
              
              <p className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto leading-relaxed font-light">
                Transform your documents into interactive learning experiences with AI-powered insights, 
                personalized analysis, and universal accessibility features.
              </p>
            </div>

            {/* Key Benefits */}
            <div className="flex items-center justify-center gap-8 text-sm text-gray-400">
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4 text-yellow-400" />
                Lightning Fast Processing
              </div>
              <div className="flex items-center gap-2">
                <Shield className="h-4 w-4 text-green-400" />
                Enterprise Security
              </div>
              <div className="flex items-center gap-2">
                <Globe className="h-4 w-4 text-blue-400" />
                Universal Access
              </div>
            </div>
          </div>

          {/* Upload Section */}
          <Card id="upload-section" className="max-w-5xl mx-auto shadow-2xl border-0 bg-black/40 backdrop-blur-xl">
            <CardHeader className="pb-8 text-center">
              <CardTitle className="text-4xl font-bold text-white">Begin Your Journey</CardTitle>
              <CardDescription className="text-xl text-gray-300">
                Upload your documents and discover the future of intelligent reading
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-8">
              {/* File Upload */}
              <div
                className={`
                  border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 relative
                  ${dragActive 
                    ? 'border-purple-400 bg-purple-500/10' 
                    : 'border-gray-600 hover:border-purple-400/50 hover:bg-purple-500/5'
                  }
                `}
                onDragOver={(e) => {
                  e.preventDefault();
                  setDragActive(true);
                }}
                onDragLeave={() => setDragActive(false)}
                onDrop={handleDrop}
              >
                <input
                  type="file"
                  accept=".pdf"
                  multiple
                  onChange={(e) => e.target.files && handleFileUpload(e.target.files)}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                />
                <div className="relative z-20 pointer-events-none">
                  <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <Upload className="h-10 w-10 text-white" />
                  </div>
                  <div className="space-y-3">
                    <p className="text-white font-semibold text-lg">
                      Drop your PDFs here or click to browse
                    </p>
                    <p className="text-gray-400">
                      Supports multiple files • Max 10MB per file • Secure processing
                    </p>
                  </div>
                </div>
                
                {selectedFiles.length > 0 && (
                  <div className="mt-6 space-y-3 relative z-20 pointer-events-none">
                    <p className="text-sm font-medium text-white">
                      {selectedFiles.length} file{selectedFiles.length > 1 ? 's' : ''} selected:
                    </p>
                    {selectedFiles.map((file, index) => (
                      <div key={index} className="text-sm text-gray-300 bg-white/10 rounded-lg px-4 py-2 backdrop-blur-sm">
                        {file.name}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Persona & Job Input */}
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <Label htmlFor="persona" className="text-white font-medium">
                    Your Professional Role
                    <span className="text-sm text-gray-400 ml-2">(Optional)</span>
                  </Label>
                  <Input
                    id="persona"
                    placeholder="e.g., Researcher, Student, Analyst, Executive"
                    value={persona}
                    onChange={(e) => setPersona(e.target.value)}
                    className="bg-white/10 border-gray-600 text-white placeholder-gray-400 focus:border-purple-400"
                  />
                </div>
                <div className="space-y-3">
                  <Label htmlFor="job" className="text-white font-medium">
                    Your Reading Objective
                    <span className="text-sm text-gray-400 ml-2">(Optional)</span>
                  </Label>
                  <Input
                    id="job"
                    placeholder="e.g., Exam preparation, Market research, Learning"
                    value={jobToBeDone}
                    onChange={(e) => setJobToBeDone(e.target.value)}
                    className="bg-white/10 border-gray-600 text-white placeholder-gray-400 focus:border-purple-400"
                  />
                </div>
              </div>

              <Button 
                onClick={handleStart}
                disabled={selectedFiles.length === 0 || isUploading}
                size="lg"
                className="w-full gap-4 h-16 text-xl font-bold shadow-2xl hover:shadow-purple-500/25 transition-all duration-300 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white disabled:opacity-50 rounded-xl"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="h-7 w-7 animate-spin" />
                    Processing Your Documents...
                  </>
                ) : (
                  <>
                    <Play className="h-7 w-7" />
                    Launch Intelligent Reading Experience
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Features Section */}
          <div className="mt-24">
            <div className="text-center mb-16">
              <h3 className="text-5xl font-bold text-white mb-6">Revolutionary Features</h3>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Experience the cutting-edge capabilities that redefine how you interact with documents
              </p>
            </div>
            
            <div className="grid md:grid-cols-3 gap-8">
              {/* AI Insights */}
              <Card 
                className="group text-center transition-all duration-500 border-0 shadow-2xl hover:shadow-purple-500/25 bg-black/40 backdrop-blur-xl cursor-pointer hover:-translate-y-3 relative overflow-hidden"
                onClick={() => handleFeatureClick('ai-insights')}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-pink-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                <CardContent className="p-10 space-y-6 relative z-10">
                  <div className="h-24 w-24 bg-gradient-to-br from-purple-500 to-pink-500 rounded-3xl flex items-center justify-center mx-auto group-hover:scale-110 group-hover:rotate-3 transition-all duration-500 shadow-2xl">
                    <Brain className="h-12 w-12 text-white" />
                  </div>
                  <h3 className="font-bold text-2xl text-white group-hover:text-purple-300 transition-colors">AI-Powered Insights</h3>
                  <p className="text-gray-300 leading-relaxed text-lg">Unlock deep understanding with advanced AI analysis, web research, and personalized insights</p>
                  <div className="text-sm text-purple-300 font-semibold group-hover:text-purple-200 flex items-center justify-center gap-2">
                    Explore capabilities 
                    <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </CardContent>
              </Card>

              {/* Podcast Mode */}
              <Card 
                className="group text-center transition-all duration-500 border-0 shadow-2xl hover:shadow-pink-500/25 bg-black/40 backdrop-blur-xl cursor-pointer hover:-translate-y-3 relative overflow-hidden"
                onClick={() => handleFeatureClick('podcast')}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-pink-500/10 to-cyan-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                <CardContent className="p-10 space-y-6 relative z-10">
                  <div className="h-24 w-24 bg-gradient-to-br from-pink-500 to-cyan-500 rounded-3xl flex items-center justify-center mx-auto group-hover:scale-110 group-hover:rotate-3 transition-all duration-500 shadow-2xl">
                    <Volume2 className="h-12 w-12 text-white" />
                  </div>
                  <h3 className="font-bold text-2xl text-white group-hover:text-pink-300 transition-colors">Audio Narration</h3>
                  <p className="text-gray-300 leading-relaxed text-lg">Transform text into engaging audio summaries perfect for multitasking and accessibility</p>
                  <div className="text-sm text-pink-300 font-semibold group-hover:text-pink-200 flex items-center justify-center gap-2">
                    Explore capabilities 
                    <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </CardContent>
              </Card>

              {/* Universal Access */}
              <Card 
                className="group text-center transition-all duration-500 border-0 shadow-2xl hover:shadow-cyan-500/25 bg-black/40 backdrop-blur-xl cursor-pointer hover:-translate-y-3 relative overflow-hidden"
                onClick={() => handleFeatureClick('accessibility')}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-blue-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                <CardContent className="p-10 space-y-6 relative z-10">
                  <div className="h-24 w-24 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-3xl flex items-center justify-center mx-auto group-hover:scale-110 group-hover:rotate-3 transition-all duration-500 shadow-2xl">
                    <Accessibility className="h-12 w-12 text-white" />
                  </div>
                  <h3 className="font-bold text-2xl text-white group-hover:text-cyan-300 transition-colors">Universal Access</h3>
                  <p className="text-gray-300 leading-relaxed text-lg">Inclusive design with dyslexia-friendly fonts, voice reading, and comprehensive accessibility</p>
                  <div className="text-sm text-cyan-300 font-semibold group-hover:text-cyan-200 flex items-center justify-center gap-2">
                    Explore capabilities 
                    <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </CardContent>
              </Card>

              {/* Smart Highlights */}
              <Card 
                className="group text-center transition-all duration-500 border-0 shadow-2xl hover:shadow-yellow-500/25 bg-black/40 backdrop-blur-xl cursor-pointer hover:-translate-y-3 relative overflow-hidden"
                onClick={() => handleFeatureClick('highlights')}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-yellow-500/10 to-orange-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                <CardContent className="p-10 space-y-6 relative z-10">
                  <div className="h-24 w-24 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-3xl flex items-center justify-center mx-auto group-hover:scale-110 group-hover:rotate-3 transition-all duration-500 shadow-2xl">
                    <Target className="h-12 w-12 text-white" />
                  </div>
                  <h3 className="font-bold text-2xl text-white group-hover:text-yellow-300 transition-colors">Smart Highlights</h3>
                  <p className="text-gray-300 leading-relaxed text-lg">AI-driven content highlighting tailored to your role and reading objectives</p>
                  <div className="text-sm text-yellow-300 font-semibold group-hover:text-yellow-200 flex items-center justify-center gap-2">
                    Explore capabilities 
                    <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </CardContent>
              </Card>

              {/* Reading Progress */}
              <Card 
                className="group text-center transition-all duration-500 border-0 shadow-2xl hover:shadow-green-500/25 bg-black/40 backdrop-blur-xl cursor-pointer hover:-translate-y-3 relative overflow-hidden"
                onClick={() => handleFeatureClick('progress')}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-green-500/10 to-emerald-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                <CardContent className="p-10 space-y-6 relative z-10">
                  <div className="h-24 w-24 bg-gradient-to-br from-green-500 to-emerald-500 rounded-3xl flex items-center justify-center mx-auto group-hover:scale-110 group-hover:rotate-3 transition-all duration-500 shadow-2xl">
                    <BarChart3 className="h-12 w-12 text-white" />
                  </div>
                  <h3 className="font-bold text-2xl text-white group-hover:text-green-300 transition-colors">Progress Analytics</h3>
                  <p className="text-gray-300 leading-relaxed text-lg">Track your reading journey with intelligent progress monitoring and time estimates</p>
                  <div className="text-sm text-green-300 font-semibold group-hover:text-green-200 flex items-center justify-center gap-2">
                    Explore capabilities 
                    <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </CardContent>
              </Card>

              {/* Adaptive Themes */}
              <Card 
                className="group text-center transition-all duration-500 border-0 shadow-2xl hover:shadow-indigo-500/25 bg-black/40 backdrop-blur-xl cursor-pointer hover:-translate-y-3 relative overflow-hidden"
                onClick={() => handleFeatureClick('themes')}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                <CardContent className="p-10 space-y-6 relative z-10">
                  <div className="h-24 w-24 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-3xl flex items-center justify-center mx-auto group-hover:scale-110 group-hover:rotate-3 transition-all duration-500 shadow-2xl">
                    <Palette className="h-12 w-12 text-white" />
                  </div>
                  <h3 className="font-bold text-2xl text-white group-hover:text-indigo-300 transition-colors">Adaptive Themes</h3>
                  <p className="text-gray-300 leading-relaxed text-lg">Personalized reading environments with light, dark, and accessibility-focused themes</p>
                  <div className="text-sm text-indigo-300 font-semibold group-hover:text-indigo-200 flex items-center justify-center gap-2">
                    Explore capabilities 
                    <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Stats Section */}
          <div className="mt-24 grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">10M+</div>
              <div className="text-gray-400">Documents Processed</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">50+</div>
              <div className="text-gray-400">Languages Supported</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">99.9%</div>
              <div className="text-gray-400">Uptime Guarantee</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">24/7</div>
              <div className="text-gray-400">AI Processing</div>
            </div>
          </div>
        </div>
      </main>

      {/* Feature Demo Modal */}
      {showFeatureDemo && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 animate-fade-in">
          <div className="bg-black/90 backdrop-blur-xl border border-white/20 rounded-3xl p-8 max-w-2xl mx-4 max-h-[80vh] overflow-y-auto shadow-2xl">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold text-white">
                {showFeatureDemo === 'ai-insights' && 'AI-Powered Insights'}
                {showFeatureDemo === 'podcast' && 'Audio Narration'}
                {showFeatureDemo === 'accessibility' && 'Universal Access'}
                {showFeatureDemo === 'highlights' && 'Smart Highlights'}
                {showFeatureDemo === 'progress' && 'Progress Analytics'}
                {showFeatureDemo === 'themes' && 'Adaptive Themes'}
              </h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowFeatureDemo(null)}
                className="h-8 w-8 p-0 text-white hover:bg-white/10"
              >
                ✕
              </Button>
            </div>
            
            <div className="space-y-4 text-gray-300">
              {showFeatureDemo === 'ai-insights' && (
                <>
                  <p>AI-Powered Insights provides comprehensive analysis of your documents using advanced language models and web research.</p>
                  <ul className="list-disc list-inside space-y-2 ml-4">
                    <li>Get key takeaways and important facts</li>
                    <li>Discover interesting connections and contradictions</li>
                    <li>Understand complex concepts through AI explanations</li>
                    <li><strong>NEW:</strong> Extract keywords and concepts automatically</li>
                    <li><strong>NEW:</strong> Get persona-specific analysis for your role</li>
                    <li><strong>NEW:</strong> Receive web search suggestions for current facts</li>
                    <li><strong>NEW:</strong> Access topic analysis and research opportunities</li>
                  </ul>
                  <p className="text-sm text-gray-400 mt-4">
                    <strong>How to use:</strong> Upload a PDF, set your role and goals, then click the Insights panel in the right sidebar. Use "Generate Comprehensive Insights" for advanced analysis.
                  </p>
                </>
              )}
              
              {showFeatureDemo === 'podcast' && (
                <>
                  <p>Audio Narration converts your reading material into engaging audio summaries.</p>
                  <ul className="list-disc list-inside space-y-2 ml-4">
                    <li>Listen to AI-narrated summaries of any section</li>
                    <li>Perfect for multitasking or accessibility</li>
                    <li>Customizable audio controls and playback</li>
                  </ul>
                  <p className="text-sm text-gray-400 mt-4">
                    <strong>How to use:</strong> Upload a PDF, then click the Podcast panel in the right sidebar to generate audio summaries.
                  </p>
                </>
              )}
              
              {showFeatureDemo === 'accessibility' && (
                <>
                  <p>Universal Access ensures everyone can read comfortably regardless of their needs.</p>
                  <ul className="list-disc list-inside space-y-2 ml-4">
                    <li>Dyslexia-friendly fonts and spacing</li>
                    <li>Text-to-speech functionality</li>
                    <li>Color blindness support and high contrast</li>
                    <li>Customizable reading experience</li>
                  </ul>
                  <p className="text-sm text-gray-400 mt-4">
                    <strong>How to use:</strong> Upload a PDF, then click the Access panel in the right sidebar to customize your reading experience.
                  </p>
                </>
              )}
              
              {showFeatureDemo === 'highlights' && (
                <>
                  <p>Smart Highlights automatically identifies and highlights content relevant to your role and goals.</p>
                  <ul className="list-disc list-inside space-y-2 ml-4">
                    <li>AI-powered content relevance detection</li>
                    <li>Automatic highlighting of key sections</li>
                    <li>Personalized based on your persona and job</li>
                  </ul>
                  <p className="text-sm text-gray-400 mt-4">
                    <strong>How to use:</strong> Upload a PDF and set your role - highlights will appear automatically as you read.
                  </p>
                </>
              )}
              
              {showFeatureDemo === 'progress' && (
                <>
                  <p>Progress Analytics helps you track your document consumption and stay organized.</p>
                  <ul className="list-disc list-inside space-y-2 ml-4">
                    <li>Track reading time and progress</li>
                    <li>Monitor completion across multiple documents</li>
                    <li>Set reading goals and milestones</li>
                  </ul>
                  <p className="text-sm text-gray-400 mt-4">
                    <strong>How to use:</strong> Progress is tracked automatically as you read through your uploaded documents.
                  </p>
                </>
              )}
              
              {showFeatureDemo === 'themes' && (
                <>
                  <p>Adaptive Themes provide multiple visual options for comfortable reading in any environment.</p>
                  <ul className="list-disc list-inside space-y-2 ml-4">
                    <li>Light, dark, and high-contrast themes</li>
                    <li>Automatic theme switching</li>
                    <li>Customizable color schemes</li>
                  </ul>
                  <p className="text-sm text-gray-400 mt-4">
                    <strong>How to use:</strong> Click the theme toggle button in the top navigation bar to switch between themes.
                  </p>
                </>
              )}
            </div>
            
            <div className="mt-6 flex gap-3">
              <Button
                onClick={() => setShowFeatureDemo(null)}
                className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500"
              >
                Got it!
              </Button>
              <Button
                variant="outline"
                onClick={() => {
                  setShowFeatureDemo(null);
                  document.getElementById('upload-section')?.scrollIntoView({ behavior: 'smooth' });
                }}
                className="border-white/20 text-white hover:bg-white/10"
              >
                Start Reading
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="relative z-10 p-8 border-t border-white/10 bg-black/20 backdrop-blur-xl">
        <div className="max-w-6xl mx-auto text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Logo size="sm" showText={false} className="h-8 w-8" />
            <span className="text-white font-semibold">Adobe+</span>
          </div>
          <p className="text-gray-400 text-sm">
            Powered by advanced AI • Built for universal access • Designed for the future of reading
          </p>
        </div>
      </footer>
    </div>
  );
}