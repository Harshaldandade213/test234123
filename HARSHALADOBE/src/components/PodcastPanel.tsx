import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { apiService } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import { 
  Play, 
  Pause, 
  Square, 
  SkipBack, 
  SkipForward,
  Volume2,
  VolumeX,
  FileText,
  Mic,
  Download,
  Settings,
  Loader2,
  Send
} from 'lucide-react';

interface PodcastPanelProps {
  documentId?: string;
  currentPage: number;
  currentText?: string;
  relatedSections?: string[];
  insights?: string[];
  autoQuery?: string; // New prop for auto-populating query
  onQueryGenerated?: (query: string) => void; // Callback when query is auto-generated
}

interface AudioSection {
  id: string;
  title: string;
  duration: number;
  type: 'summary' | 'insights' | 'content';
  transcript: string;
}

export function PodcastPanel({ 
  documentId, 
  currentPage, 
  currentText, 
  relatedSections = [], 
  insights = [],
  autoQuery,
  onQueryGenerated
}: PodcastPanelProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(180); // 3 minutes
  const [volume, setVolume] = useState([0.7]);
  const [isMuted, setIsMuted] = useState(false);
  const [showTranscript, setShowTranscript] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [audioSections, setAudioSections] = useState<AudioSection[]>([]);
  const [currentSection, setCurrentSection] = useState(0);
  const [podcastScript, setPodcastScript] = useState<string>('');
  const [audioUrl, setAudioUrl] = useState<string>('');
  const [customQuery, setCustomQuery] = useState<string>('');
  const [isGeneratingFromQuery, setIsGeneratingFromQuery] = useState(false);

  const audioRef = useRef<HTMLAudioElement>(null);
  const { toast } = useToast();

  const handleGenerateFromQuery = async (query?: string) => {
    const queryToUse = query || customQuery.trim();
    
    // Debug: Log the query to see what's being passed
    console.log('PodcastPanel - handleGenerateFromQuery called with:', { query, customQuery, queryToUse });
    console.log('PodcastPanel - query type:', typeof queryToUse);
    console.log('PodcastPanel - query stringified:', JSON.stringify(queryToUse));
    
    if (!queryToUse) {
      toast({
        title: "Query required",
        description: "Please enter a query to generate a podcast.",
        variant: "destructive"
      });
      return;
    }
    
    setIsGeneratingFromQuery(true);
    try {
      // Generate podcast using the new API endpoint
      const result = await apiService.generatePodcastFromQuery(queryToUse);
      
              if (result.status === 'success') {
          // Set the audio URL for the generated podcast
          const fullAudioUrl = result.download_url.startsWith('http') 
            ? result.download_url 
            : `${apiService.baseUrl || 'http://localhost:8000'}${result.download_url}`;
          setAudioUrl(fullAudioUrl);
          
          // Create a comprehensive script description
          const scriptDescription = `AI-generated podcast for query: "${queryToUse}". This podcast explores the topic you requested and provides insights based on the available documents. The audio has been automatically combined from multiple segments into a single, seamless podcast file.`;
          setPodcastScript(scriptDescription);
          
          // Create audio section for the combined podcast
          const generatedSection: AudioSection = {
            id: '1',
            title: `Combined Podcast: ${queryToUse}`,
            duration: 180, // Estimated duration - will be updated when audio loads
            type: 'summary',
            transcript: scriptDescription
          };
          
          setAudioSections([generatedSection]);
          setDuration(180);
          
          toast({
            title: "Combined Podcast Generated",
            description: `Your complete podcast for "${queryToUse}" is ready to play. All audio segments have been combined into a single file.`
          });

        // Automatically start playing the generated podcast
        setTimeout(() => {
          handleAutoPlay(fullAudioUrl);
        }, 500); // Small delay to ensure audio is loaded
        
      } else {
        throw new Error("Podcast generation failed");
      }
      
    } catch (error) {
      console.error('Failed to generate podcast from query:', error);
      toast({
        title: "Podcast generation failed",
        description: "Unable to generate podcast. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsGeneratingFromQuery(false);
    }
  };

  const handleAutoPlay = async (audioUrl: string) => {
    try {
      // Set the audio source
      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        audioRef.current.volume = volume[0];
        
        // Wait for audio to load
        await new Promise((resolve, reject) => {
          if (audioRef.current) {
            audioRef.current.onloadedmetadata = resolve;
            audioRef.current.onerror = reject;
          }
        });
        
        // Start playing
        await audioRef.current.play();
        setIsPlaying(true);
        
        // Update duration from actual audio
        if (audioRef.current.duration) {
          setDuration(audioRef.current.duration);
        }
        
        toast({
          title: "Podcast started",
          description: "Your podcast is now playing automatically."
        });
      }
    } catch (error) {
      console.error('Auto-play failed:', error);
      toast({
        title: "Auto-play failed",
        description: "Click the play button to start the podcast manually.",
        variant: "destructive"
      });
    }
  };

  const handleGenerateAudio = async () => {
    if (!currentText) {
      toast({
        title: "No content available",
        description: "Please navigate to a section with content to generate a podcast.",
        variant: "destructive"
      });
      return;
    }
    
    setIsGenerating(true);
    try {
      // Generate podcast using backend API
      const result = await apiService.generatePodcast(
        currentText,
        relatedSections,
        insights
      );
      
      // Check if podcast was generated successfully
      if (result.script && result.script !== "Failed to generate podcast script.") {
        setPodcastScript(result.script);
        // Construct full audio URL from the relative path returned by backend
        const fullAudioUrl = result.audio_url.startsWith('http') 
          ? result.audio_url 
          : apiService.getAudioUrl(result.audio_url.replace('/audio/', ''));
        setAudioUrl(fullAudioUrl);
        
        // Create audio sections from the generated content
        const generatedSection: AudioSection = {
          id: '1',
          title: 'AI-Generated Summary',
          duration: 180, // Estimated duration
          type: 'summary',
          transcript: result.script
        };
        
        setAudioSections([generatedSection]);
        setDuration(180);
        
        toast({
          title: "Podcast generated",
          description: "Your AI-narrated summary is ready to play."
        });

        // Automatically start playing the generated podcast
        setTimeout(() => {
          handleAutoPlay(fullAudioUrl);
        }, 500);
      } else {
        // Fallback to local podcast generation
        throw new Error("API podcast generation failed");
      }
      
    } catch (error) {
      console.error('Failed to generate podcast:', error);
      
      // Fallback: Create a mock podcast with browser text-to-speech
      try {
        const fallbackScript = `Welcome to your AI-generated podcast summary. I'm your AI reading companion, and today we're diving deep into some fascinating content.

        Let me start by giving you the context. We're currently exploring: ${currentText?.slice(0, 300) || 'the current section of your document'}. This is particularly interesting because it connects to several key themes we've been tracking.

        Now, here's what really caught my attention. ${insights.length > 0 ? insights.slice(0, 2).map((insight, i) => `First, ${insight.toLowerCase()}. ${i === 0 && insights.length > 1 ? `And secondly, ${insights[1].toLowerCase()}.` : ''}`).join(' ') : 'The content reveals some compelling insights that align with your learning objectives.'}

        What makes this especially relevant is how it connects to other parts of your reading. ${relatedSections.length > 0 ? `We've seen similar themes in sections covering ${relatedSections.slice(0, 2).join(' and ')}.` : 'This builds on concepts we\'ve encountered throughout the document.'} These connections aren't just coincidental - they're part of a larger narrative that's emerging.

        Let me put this in perspective for you. This isn't just information - it's actionable intelligence. The patterns we're seeing here suggest some practical implications for your work. Think about how you might apply these insights in your current role or upcoming projects.

        As we wrap up this summary, remember that the real value lies not just in understanding these individual points, but in seeing how they interconnect. This is the kind of strategic thinking that separates surface-level reading from deep comprehension.

        That's your personalized podcast summary for this section. Keep reading, keep connecting the dots, and I'll be here to help you make sense of it all.`;
        
        setPodcastScript(fallbackScript);
        
        // Generate audio using browser's speech synthesis
        if ('speechSynthesis' in window) {
          // Create a mock audio URL since we can't generate actual file
          setAudioUrl('browser-tts://mock-audio');
          
          const generatedSection: AudioSection = {
            id: '1',
            title: 'AI-Generated Summary (Browser TTS)',
            duration: Math.floor(fallbackScript.length / 10), // Estimate duration
            type: 'summary',
            transcript: fallbackScript
          };
          
          setAudioSections([generatedSection]);
          setDuration(generatedSection.duration);
          
          toast({
            title: "Podcast generated (Fallback)",
            description: "Using browser text-to-speech. Click play to listen."
          });
        } else {
          throw new Error("Speech synthesis not supported");
        }
        
      } catch (fallbackError) {
        toast({
          title: "Podcast generation failed",
          description: "Unable to generate audio. Please check your connection and try again.",
          variant: "destructive"
        });
        // Don't fallback to mock data - leave sections empty
        setAudioSections([]);
        setPodcastScript('');
        setAudioUrl('');
      }
    } finally {
      setIsGenerating(false);
    }
  };

  const handlePlayPause = async () => {
    if (audioSections.length === 0) {
      handleGenerateAudio();
      return;
    }
    
    if (!audioUrl) {
      toast({
        title: "No audio available",
        description: "Please generate the podcast first.",
        variant: "destructive"
      });
      return;
    }
    
    if (audioRef.current) {
      if (isPlaying) {
        // Pause audio
        audioRef.current.pause();
      } else {
        // Play audio
        try {
          // Set the audio source if not already set
          if (audioRef.current.src !== audioUrl) {
            audioRef.current.src = audioUrl;
            audioRef.current.volume = volume[0];
          }
          
          await audioRef.current.play();
        } catch (error) {
          console.error('Error playing audio:', error);
          toast({
            title: "Playback failed",
            description: "Unable to play audio. Please try again.",
            variant: "destructive"
          });
        }
      }
    } else if (audioUrl.startsWith('browser-tts://')) {
      // Handle browser TTS fallback
      if (isPlaying) {
        window.speechSynthesis?.cancel();
      } else {
        if ('speechSynthesis' in window && podcastScript) {
          const voices = window.speechSynthesis.getVoices();
          let preferredVoice = voices.find(voice => 
            voice.name.toLowerCase().includes('female') || 
            voice.name.toLowerCase().includes('natural')
          ) || voices[0];
          
          const utterance = new SpeechSynthesisUtterance(podcastScript);
          if (preferredVoice) {
            utterance.voice = preferredVoice;
          }
          utterance.rate = 1.1;
          utterance.pitch = 1.0;
          utterance.volume = volume[0];
          
          utterance.onstart = () => setIsPlaying(true);
          utterance.onend = () => setIsPlaying(false);
          
          window.speechSynthesis.cancel();
          window.speechSynthesis.speak(utterance);
        }
      }
    }
  };

  const handleStop = () => {
    setIsPlaying(false);
    setCurrentTime(0);
    setCurrentSection(0);
    
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
  };

  const handleSeek = (newTime: number[]) => {
    const time = newTime[0];
    setCurrentTime(time);
    
    if (audioRef.current && !isNaN(time)) {
      audioRef.current.currentTime = time;
    }
  };

  const handleVolumeChange = (newVolume: number[]) => {
    const vol = newVolume[0];
    setVolume(newVolume);
    setIsMuted(vol === 0);
    
    if (audioRef.current) {
      audioRef.current.volume = vol;
      audioRef.current.muted = vol === 0;
    }
  };

  const toggleMute = () => {
    const newMutedState = !isMuted;
    setIsMuted(newMutedState);
    if (audioRef.current) {
      audioRef.current.muted = newMutedState;
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getCurrentSection = () => {
    let timeAccumulator = 0;
    for (let i = 0; i < audioSections.length; i++) {
      timeAccumulator += audioSections[i].duration;
      if (currentTime <= timeAccumulator) {
        return i;
      }
    }
    return audioSections.length - 1;
  };

  const currentSectionIndex = getCurrentSection();
  const currentSectionData = audioSections[currentSectionIndex];

  // Auto-populate query and generate podcast when autoQuery is provided
  useEffect(() => {
    console.log('PodcastPanel - useEffect triggered with autoQuery:', autoQuery);
    console.log('PodcastPanel - autoQuery type:', typeof autoQuery);
    console.log('PodcastPanel - autoQuery stringified:', JSON.stringify(autoQuery));
    
    if (autoQuery && autoQuery.trim() && !customQuery) {
      console.log('Auto-populating query:', autoQuery);
      setCustomQuery(autoQuery.trim());
      
      // Automatically generate podcast after a short delay
      setTimeout(() => {
        handleGenerateFromQuery(autoQuery.trim());
      }, 1000);
      
      // Notify parent component that query was auto-generated
      if (onQueryGenerated) {
        onQueryGenerated(autoQuery.trim());
      }
    }
  }, [autoQuery, customQuery, onQueryGenerated]);

  // Real audio progress is handled by onTimeUpdate event

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-border-subtle">
        <div className="flex items-center gap-2 mb-2">
          <Mic className="h-5 w-5 text-brand-primary" />
          <h3 className="font-semibold text-text-primary">Podcast Mode</h3>
        </div>
        <p className="text-xs text-text-secondary">
          Listen to AI-generated audio summaries and insights
        </p>
      </div>

      <div className="p-4 space-y-4">
        {/* Custom Query Input */}
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <Mic className="h-4 w-4 text-brand-primary" />
            <h4 className="text-sm font-medium text-text-primary">
              Generate Podcast from Query
            </h4>
          </div>
          
          <div className="space-y-2">
            <Textarea
              placeholder="Enter your query (e.g., 'Alien', 'Space exploration', 'Technology trends')... (Auto-generates when you paste or type substantial text)"
              value={customQuery}
              onChange={(e) => {
                const newValue = e.target.value;
                setCustomQuery(newValue);
                
                // Auto-generate podcast when text is pasted or typed (if it's substantial)
                if (newValue.trim().length >= 10 && !isGeneratingFromQuery) {
                  console.log('Auto-generating podcast for pasted/typed text:', newValue);
                  
                  // Show toast notification
                  toast({
                    title: "Auto-Generating Podcast",
                    description: `Generating podcast for: "${newValue.substring(0, 50)}${newValue.length > 50 ? '...' : ''}"`,
                  });
                  
                  // Add a small delay to allow for pasting to complete
                  setTimeout(() => {
                    handleGenerateFromQuery(newValue);
                  }, 500);
                }
              }}
              onPaste={(e) => {
                // Handle paste event specifically
                setTimeout(() => {
                  const pastedText = e.currentTarget.value;
                  if (pastedText.trim().length >= 10 && !isGeneratingFromQuery) {
                    console.log('Auto-generating podcast for pasted text:', pastedText);
                    
                    // Show toast notification
                    toast({
                      title: "Auto-Generating Podcast",
                      description: `Generating podcast for pasted text: "${pastedText.substring(0, 50)}${pastedText.length > 50 ? '...' : ''}"`,
                    });
                    
                    handleGenerateFromQuery(pastedText);
                  }
                }, 100);
              }}
              className="min-h-[80px] resize-none"
              disabled={isGeneratingFromQuery}
            />
            
            {/* Auto-generation indicator */}
            {customQuery.trim().length >= 10 && !isGeneratingFromQuery && (
              <div className="flex items-center gap-2 text-xs text-blue-600">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                <span>Ready to auto-generate podcast</span>
              </div>
            )}
            
            <Button
              onClick={handleGenerateFromQuery}
              disabled={isGeneratingFromQuery || !customQuery.trim()}
              className="w-full gap-2"
            >
              {isGeneratingFromQuery ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Generating Podcast...
                </>
              ) : (
                <>
                  <Send className="h-4 w-4" />
                  Generate Podcast from Query
                </>
              )}
            </Button>
          </div>
        </div>

        {/* Divider */}
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-border-subtle" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-background px-2 text-text-tertiary">Or</span>
          </div>
        </div>

        {/* Generate/Play Controls */}
        {audioSections.length === 0 ? (
          <div className="space-y-4">
            <div className="text-center py-6">
              <Mic className="h-12 w-12 text-text-tertiary mx-auto mb-3" />
              <h4 className="text-sm font-medium text-text-primary mb-2">
                No Audio Generated
              </h4>
              <p className="text-xs text-text-secondary mb-4">
                Generate audio summary for page {currentPage} and related content
              </p>
            </div>
            
            <Button
              onClick={handleGenerateAudio}
              disabled={isGenerating || !documentId}
              className="w-full gap-2"
            >
              {isGenerating ? (
                <>
                  <div className="h-4 w-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                  Generating Audio...
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" />
                  Generate Podcast from Current Content
                </>
              )}
            </Button>
          </div>
        ) : (
          <>
            {/* Audio Controls */}
            <div className="space-y-4">
              {/* Main Controls */}
              <div className="flex items-center justify-center gap-3">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    const newTime = Math.max(0, currentTime - 15);
                    setCurrentTime(newTime);
                  }}
                  aria-label="Skip back 15 seconds"
                >
                  <SkipBack className="h-4 w-4" />
                </Button>

                <Button
                  onClick={handlePlayPause}
                  className="h-12 w-12 rounded-full"
                  aria-label={isPlaying ? 'Pause' : 'Play'}
                >
                  {isPlaying ? (
                    <Pause className="h-5 w-5" />
                  ) : (
                    <Play className="h-5 w-5" />
                  )}
                </Button>

                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    const newTime = Math.min(duration, currentTime + 15);
                    setCurrentTime(newTime);
                  }}
                  aria-label="Skip forward 15 seconds"
                >
                  <SkipForward className="h-4 w-4" />
                </Button>
              </div>

              {/* Progress Bar */}
              <div className="space-y-2">
                <Slider
                  value={[currentTime]}
                  onValueChange={handleSeek}
                  max={duration}
                  step={1}
                  className="w-full"
                />
                
                <div className="flex justify-between text-xs text-text-tertiary">
                  <span>{formatTime(currentTime)}</span>
                  <span>{formatTime(duration)}</span>
                </div>
              </div>

              {/* Volume Control */}
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={toggleMute}
                  className="p-1"
                >
                  {isMuted || volume[0] === 0 ? (
                    <VolumeX className="h-4 w-4" />
                  ) : (
                    <Volume2 className="h-4 w-4" />
                  )}
                </Button>
                
                <Slider
                  value={isMuted ? [0] : volume}
                  onValueChange={handleVolumeChange}
                  max={1}
                  step={0.1}
                  className="flex-1"
                />
              </div>
            </div>

            {/* Current Section Info */}
            {currentSectionData && (
              <div className="p-3 bg-surface-elevated rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <Badge variant="secondary" className="text-xs">
                    {currentSectionData.type}
                  </Badge>
                  <span className="text-xs text-text-tertiary">
                    Section {currentSectionIndex + 1} of {audioSections.length}
                  </span>
                </div>
                
                <h4 className="text-sm font-medium text-text-primary mb-1">
                  {currentSectionData.title}
                </h4>
                
                <p className="text-xs text-text-secondary">
                  Duration: {formatTime(currentSectionData.duration)}
                </p>
              </div>
            )}

            {/* Transcript Toggle */}
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowTranscript(!showTranscript)}
                className="flex-1 gap-2"
              >
                <FileText className="h-4 w-4" />
                {showTranscript ? 'Hide' : 'Show'} Transcript
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => console.log('Download audio')}
                aria-label="Download audio"
              >
                <Download className="h-4 w-4" />
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => console.log('Audio settings')}
                aria-label="Audio settings"
              >
                <Settings className="h-4 w-4" />
              </Button>
            </div>
          </>
        )}
      </div>

      {/* Transcript */}
      {showTranscript && audioSections.length > 0 && (
        <div className="border-t border-border-subtle flex-1">
          <ScrollArea className="h-full">
            <div className="p-4 space-y-3">
              <h4 className="text-sm font-medium text-text-primary">
                Transcript
              </h4>
              
              {audioSections.map((section, index) => (
                <div
                  key={section.id}
                  className={`p-3 rounded-lg transition-colors ${
                    index === currentSectionIndex
                      ? 'bg-surface-selected border border-brand-primary/20'
                      : 'bg-surface-elevated'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <Badge 
                      variant={index === currentSectionIndex ? "default" : "secondary"}
                      className="text-xs"
                    >
                      {section.title}
                    </Badge>
                    <span className="text-xs text-text-tertiary">
                      {formatTime(section.duration)}
                    </span>
                  </div>
                  
                  <p className="text-sm text-text-secondary leading-relaxed">
                    {section.transcript}
                  </p>
                </div>
              ))}
            </div>
          </ScrollArea>
        </div>
      )}

      {/* Hidden Audio Element */}
      <audio
        ref={audioRef}
        preload="metadata"
        onLoadedMetadata={() => {
          if (audioRef.current) {
            setDuration(audioRef.current.duration);
            console.log('Audio loaded, duration:', audioRef.current.duration);
          }
        }}
        onTimeUpdate={() => {
          if (audioRef.current) {
            setCurrentTime(audioRef.current.currentTime);
          }
        }}
        onEnded={() => {
          setIsPlaying(false);
          setCurrentTime(0);
        }}
        onPlay={() => {
          setIsPlaying(true);
        }}
        onPause={() => {
          setIsPlaying(false);
        }}
        onError={(e) => {
          console.error('Audio error:', e);
          toast({
            title: "Audio playback error",
            description: "Unable to play the audio file. Please try again.",
            variant: "destructive"
          });
        }}
      />
    </div>
  );
}