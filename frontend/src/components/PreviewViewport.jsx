import React, { useState, useRef } from 'react';
import { Monitor, Tablet, Smartphone, RotateCcw, ExternalLink, Check, Copy } from 'lucide-react';

export default function PreviewViewport({ project, onOpenInNewTab }) {
  const [device, setDevice] = useState('desktop'); // desktop | tablet | mobile
  const [copied, setCopied] = useState(false);
  const iframeRef = useRef(null);

  const files = project.files || { "index.html": project.full_code || "" };
  const htmlContent = files["index.html"] || "<h1>No HTML found</h1>";

  const handleRefresh = () => {
    if (iframeRef.current) {
      iframeRef.current.srcdoc = htmlContent;
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(htmlContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const deviceWidths = {
    desktop: 'w-full',
    tablet: 'w-[768px]',
    mobile: 'w-[390px]'
  };

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-4rem)] bg-[#090a0f] overflow-hidden">
      {/* Top Device & Control Bar */}
      <div className="h-12 border-b border-white/10 bg-[#12141c]/60 px-4 flex items-center justify-between">
        {/* Device Viewport Switcher */}
        <div className="flex items-center gap-1 bg-white/5 p-1 rounded-lg border border-white/5">
          <button
            onClick={() => setDevice('desktop')}
            className={`p-1.5 rounded-md transition-all ${
              device === 'desktop' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'
            }`}
            title="Desktop (100%)"
          >
            <Monitor className="w-4 h-4" />
          </button>
          <button
            onClick={() => setDevice('tablet')}
            className={`p-1.5 rounded-md transition-all ${
              device === 'tablet' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'
            }`}
            title="Tablet (768px)"
          >
            <Tablet className="w-4 h-4" />
          </button>
          <button
            onClick={() => setDevice('mobile')}
            className={`p-1.5 rounded-md transition-all ${
              device === 'mobile' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'
            }`}
            title="Mobile (390px)"
          >
            <Smartphone className="w-4 h-4" />
          </button>
        </div>

        {/* Project Title & Status */}
        <div className="hidden sm:flex items-center gap-2 text-xs text-slate-300">
          <span className="font-semibold text-white truncate max-w-xs">{project.title}</span>
          <span className="text-slate-600">•</span>
          <span className="text-slate-400 text-[11px]">Emergent Full-Stack Preview</span>
        </div>

        {/* Quick controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md bg-white/5 hover:bg-white/10 border border-white/10 text-slate-300 transition"
            title="Copy index.html to clipboard"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span className="hidden md:inline">{copied ? 'Copied!' : 'Copy HTML'}</span>
          </button>
          <button
            onClick={handleRefresh}
            className="p-1.5 rounded-md bg-white/5 hover:bg-white/10 border border-white/10 text-slate-300 transition"
            title="Reload Frame"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={onOpenInNewTab}
            className="p-1.5 rounded-md bg-white/5 hover:bg-white/10 border border-white/10 text-slate-300 transition"
            title="Open in new window"
          >
            <ExternalLink className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Viewport Frame Area */}
      <div className="flex-1 bg-[#050608] flex items-center justify-center p-2 md:p-4 overflow-auto">
        <div 
          className={`h-full transition-all duration-300 ${deviceWidths[device]} ${
            device !== 'desktop' 
              ? 'rounded-2xl border-4 border-slate-800 shadow-2xl overflow-hidden ring-1 ring-white/10' 
              : 'rounded-xl border border-white/10 shadow-lg'
          }`}
        >
          <iframe
            ref={iframeRef}
            srcDoc={htmlContent}
            title={project.title}
            className="w-full h-full bg-white rounded-lg"
            sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
          />
        </div>
      </div>
    </div>
  );
}
