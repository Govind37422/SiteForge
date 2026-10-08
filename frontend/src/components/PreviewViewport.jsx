import React, { useState, useRef } from 'react';
import { Monitor, Laptop, Tablet, Smartphone, RotateCcw, RotateCw, ExternalLink, Check, Copy, ZoomIn, ZoomOut } from 'lucide-react';

export default function PreviewViewport({ project, onOpenInNewTab }) {
  const [device, setDevice] = useState('desktop'); // desktop | laptop | tablet | mobile
  const [orientation, setOrientation] = useState('portrait'); // portrait | landscape
  const [zoom, setZoom] = useState(100);
  const [copied, setCopied] = useState(false);
  const iframeRef = useRef(null);

  const files = project.files || {};
  const firstKey = Object.keys(files)[0];
  const htmlContent = files["index.html"] || (firstKey ? files[firstKey] : null) || project.full_code || `<!DOCTYPE html><html><body style="background:#090a0f;color:white;font-family:sans-serif;padding:40px;"><h2>${project.title || 'App Preview'}</h2><p>${project.description || ''}</p></body></html>`;

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

  const deviceConfigs = {
    desktop: { width: 'w-full', height: 'h-full', label: 'Desktop (100%)' },
    laptop: { width: 'w-[1280px]', height: 'h-[800px]', label: 'MacBook Pro (14")' },
    tablet: { width: orientation === 'portrait' ? 'w-[768px]' : 'w-[1024px]', height: orientation === 'portrait' ? 'h-[1024px]' : 'h-[768px]', label: 'iPad Pro' },
    mobile: { width: orientation === 'portrait' ? 'w-[390px]' : 'w-[844px]', height: orientation === 'portrait' ? 'h-[844px]' : 'h-[390px]', label: 'iPhone 15 Pro' }
  };

  const currentConfig = deviceConfigs[device];

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-4rem)] bg-[#07080d] overflow-hidden">
      {/* Top Advanced Responsive Toolbar */}
      <div className="h-14 border-b border-white/10 bg-[#0f111a]/80 backdrop-blur-md px-4 flex items-center justify-between z-10">
        {/* Device Switcher */}
        <div className="flex items-center gap-1 bg-white/5 p-1 rounded-xl border border-white/10">
          <button
            onClick={() => setDevice('desktop')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-all ${
              device === 'desktop' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
            title="Full Desktop View"
          >
            <Monitor className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Desktop</span>
          </button>
          <button
            onClick={() => setDevice('laptop')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-all ${
              device === 'laptop' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
            title="Laptop View"
          >
            <Laptop className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Laptop</span>
          </button>
          <button
            onClick={() => setDevice('tablet')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-all ${
              device === 'tablet' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
            title="Tablet View"
          >
            <Tablet className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Tablet</span>
          </button>
          <button
            onClick={() => setDevice('mobile')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-all ${
              device === 'mobile' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
            title="Mobile View"
          >
            <Smartphone className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Mobile</span>
          </button>
        </div>

        {/* Orientation & Zoom controls for non-desktop */}
        {device !== 'desktop' && (
          <div className="hidden md:flex items-center gap-3 bg-white/5 px-3 py-1 rounded-xl border border-white/10 text-xs">
            <button
              onClick={() => setOrientation(orientation === 'portrait' ? 'landscape' : 'portrait')}
              className="flex items-center gap-1.5 text-slate-300 hover:text-white transition"
              title="Rotate Device"
            >
              <RotateCw className="w-3.5 h-3.5 text-indigo-400" />
              <span className="capitalize">{orientation}</span>
            </button>
            <span className="text-slate-600">|</span>
            <div className="flex items-center gap-2">
              <button onClick={() => setZoom(Math.max(50, zoom - 15))} className="text-slate-400 hover:text-white">
                <ZoomOut className="w-3.5 h-3.5" />
              </button>
              <span className="font-mono text-slate-300 w-10 text-center">{zoom}%</span>
              <button onClick={() => setZoom(Math.min(150, zoom + 15))} className="text-slate-400 hover:text-white">
                <ZoomIn className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}

        {/* Project Name & Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-xs text-slate-200 transition"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span className="hidden sm:inline">{copied ? 'Copied HTML!' : 'Copy Code'}</span>
          </button>
          <button
            onClick={handleRefresh}
            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-slate-300 hover:text-white transition"
            title="Refresh Preview"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={onOpenInNewTab}
            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-slate-300 hover:text-white transition"
            title="Open in new window"
          >
            <ExternalLink className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Viewport Canvas */}
      <div className="flex-1 bg-[#040507] flex items-center justify-center p-4 md:p-8 overflow-auto">
        <div 
          style={{ transform: `scale(${zoom / 100})`, transformOrigin: 'center center' }}
          className={`transition-all duration-300 ${currentConfig.width} ${currentConfig.height} ${
            device !== 'desktop' 
              ? 'rounded-3xl border-[8px] border-slate-800 shadow-2xl overflow-hidden bg-white ring-1 ring-white/20' 
              : 'w-full h-full rounded-xl border border-white/10 shadow-2xl bg-white'
          }`}
        >
          <iframe
            ref={iframeRef}
            srcDoc={htmlContent}
            title={project.title}
            className="w-full h-full bg-white border-none"
            sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
          />
        </div>
      </div>
    </div>
  );
}
