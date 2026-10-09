import React from 'react';
import { Sparkles, History, Code2, Download, ExternalLink, Plus, Layers, Flame, Share2 } from 'lucide-react';

export default function Navbar({ 
  currentProject, 
  onNewSite, 
  onOpenHistory, 
  historyCount, 
  activeTab, 
  setActiveTab,
  onExport,
  onShare,
  providerInfo
}) {
  return (
    <header className="h-16 border-b border-white/10 bg-[#090a0f]/80 backdrop-blur-md sticky top-0 z-40 px-4 md:px-6 flex items-center justify-between">
      {/* Brand */}
      <div className="flex items-center gap-3">
        <div 
          onClick={onNewSite} 
          className="flex items-center gap-2.5 cursor-pointer group"
        >
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 p-0.5 shadow-lg shadow-indigo-500/25 transition-transform group-hover:scale-105">
            <div className="w-full h-full bg-[#090a0f] rounded-[10px] flex items-center justify-center">
              <Flame className="w-5 h-5 text-indigo-400 fill-indigo-400/20" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
                SiteForge
              </span>
              <span className="text-[10px] font-semibold uppercase px-1.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 tracking-wider">
                v2.0
              </span>
            </div>
          </div>
        </div>

        {/* Engine status pill */}
        <div className="hidden lg:flex items-center gap-2 pl-4 border-l border-white/10 text-xs text-slate-400">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Engine: <strong className="text-slate-200">{providerInfo?.provider?.toUpperCase() || 'GROQ'}</strong> ({providerInfo?.model || 'Llama 3.3'})</span>
        </div>
      </div>

      {/* Center Tabs (when project is active) */}
      {currentProject && (
        <div className="flex items-center bg-white/5 p-1 rounded-xl border border-white/10 text-xs font-medium">
          <button
            onClick={() => setActiveTab('preview')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all ${
              activeTab === 'preview' 
                ? 'bg-indigo-600 text-white shadow-sm' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            Live Preview
          </button>
          <button
            onClick={() => setActiveTab('code')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all ${
              activeTab === 'code' 
                ? 'bg-indigo-600 text-white shadow-sm' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Code2 className="w-3.5 h-3.5" />
            Code Inspector
          </button>
        </div>
      )}

      {/* Right Action buttons */}
      <div className="flex items-center gap-2">
        <button
          onClick={onOpenHistory}
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/10 hover:border-white/20 bg-white/5 text-xs text-slate-300 hover:text-white transition"
          title="Past Projects"
        >
          <History className="w-3.5 h-3.5 text-slate-400" />
          <span className="hidden sm:inline">History</span>
          {historyCount > 0 && (
            <span className="px-1.5 py-0.2 rounded-full bg-indigo-500/20 text-indigo-300 text-[10px] font-bold">
              {historyCount}
            </span>
          )}
        </button>

        {currentProject && (
          <>
            <button
              onClick={onShare}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-indigo-500/20 to-purple-600/20 hover:from-indigo-500/30 hover:to-purple-600/30 border border-indigo-500/40 text-xs text-indigo-200 hover:text-white transition font-semibold"
              title="Share public link & QR"
            >
              <Share2 className="w-3.5 h-3.5" />
              <span className="hidden md:inline">Share</span>
            </button>
            <button
              onClick={onExport}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-xs text-slate-200 transition"
              title="Download HTML"
            >
              <Download className="w-3.5 h-3.5 text-indigo-400" />
              <span className="hidden md:inline">Download</span>
            </button>
            <a
              href={`/api/preview/${currentProject.id}`}
              target="_blank"
              rel="noreferrer"
              className="p-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-slate-300 hover:text-white transition"
              title="Open full-screen in new tab"
            >
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </>
        )}

        <button
          onClick={onNewSite}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white text-xs font-semibold shadow-md shadow-indigo-500/20 transition-all hover:scale-[1.02]"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>New Site</span>
        </button>
      </div>
    </header>
  );
}
