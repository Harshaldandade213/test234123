import React from 'react';

interface LogoProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
}

export function Logo({ className = '', size = 'md', showText = true }: LogoProps) {
  const sizes = {
    sm: { icon: 20, text: 'text-lg', gap: 2 },
    md: { icon: 24, text: 'text-2xl', gap: 3 },
    lg: { icon: 32, text: 'text-3xl', gap: 4 }
  };

  const currentSize = sizes[size];

  return (
    <div className={`flex items-center gap-${currentSize.gap} ${className}`}>
      {/* Adobe+ Logo Icon */}
              <svg
          width={currentSize.icon}
          height={currentSize.icon}
          viewBox="0 0 64 64"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          role="img"
          aria-label="Adobe Plus"
          className="drop-shadow-sm"
        >
        <defs>
          <linearGradient id="aplus_gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="var(--aplus-warm, #ff7a3d)" />
            <stop offset="50%" stopColor="var(--aplus-mid, #ff4fb0)" />
            <stop offset="100%" stopColor="var(--aplus-cool, #5b6cff)" />
          </linearGradient>
          <filter id="logoShadow">
            <feDropShadow dx="0" dy="1" stdDeviation="2" floodOpacity="0.15"/>
          </filter>
        </defs>
        
        {/* Rounded heart/A shape with soft corner radius */}
        <path 
          d="M32 8c-7.5 0-13.5 6-13.5 13.5 0 4.5 2.2 8.5 5.8 11L32 56l7.7-23.5c3.6-2.5 5.8-6.5 5.8-11.2C45.5 14 39.5 8 32 8z" 
          fill="url(#aplus_gradient)" 
          filter="url(#logoShadow)"
          rx="2"
        />
        
        {/* Small warm dot at top-left */}
        <circle 
          cx="20" 
          cy="18" 
          r="3" 
          fill="var(--aplus-warm, #ff7a3d)" 
          opacity="0.9"
        />
        
        {/* Plus cutout — uses header bg color so it "knocks out" cleanly */}
        <rect 
          x="28" 
          y="22" 
          width="16" 
          height="6" 
          rx="3" 
          fill="var(--surface-1, #111)" 
          opacity="0.95"
        />
        <rect 
          x="34" 
          y="16" 
          width="6" 
          height="18" 
          rx="3" 
          fill="var(--surface-1, #111)" 
          opacity="0.95"
        />
      </svg>

      {showText && (
        <div className="flex flex-col">
          <h1 className={`font-black ${currentSize.text} bg-gradient-to-r from-aplus-warm via-aplus-mid to-aplus-cool bg-clip-text text-transparent drop-shadow-sm`}>
            Adobe+
          </h1>
          {size !== 'sm' && (
            <span className="text-xs text-muted-foreground font-semibold tracking-wider uppercase bg-muted/30 px-2 py-0.5 rounded-full">
              Intelligent PDF Reading
            </span>
          )}
        </div>
      )}
    </div>
  );
}