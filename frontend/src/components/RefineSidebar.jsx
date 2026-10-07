import React, { useState } from 'react';
import { Send, Wand2, History, ChevronRight, Sparkles, RefreshCw } from 'lucide-react';

export default function RefineSidebar({ project, onRefine, isRefining, isOpen, onToggle }) {
  const [tweakPrompt, setTweakPrompt] = useState('');

  const QUICK_REFINEMENTS = [
    "Add a customer testimonials grid",
    "Switch color palette to neon emerald",
    "Add an interactive FAQ accordion",
    "Make the navigation bar sticky on scroll",
    "Add a monthly / annual pricing toggle"
  ];

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!tweakPrompt.trim() || isRefining) return;
    onRefine(tweakPrompt);
    setTweakPrompt('');
  };

  if (!isOpen) {
    return (
      <button
        onClick={onToggle}
        className="fixed bottom-6 right-6 z-30 p-3.5 rounded-2xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-2xl shadow-indigo-500/30 hover:scale-105 active:scale-95 transition-all flex items-center gap-2 font-medium text-xs border border-white/20"
      >
        <Wand2 className="w-4 h-4" />
        <span>Refine with AI</span>
      </button>
    );
  }

  return (
    <aside className="w-80 md:w-96 border-l border-white/10 bg-[#0e1017] flex flex-col h-[calc(100vh-4rem)] z-20">
      {/* Top Header */}
      <div className="h-12 border-b border-white/10 px-4 flex items-center justify-between bg-white/[0.02]">
        <div className="flex items-center gap-2">
          <Wand2 className="w-4 h-4 text-indigo-400" />
          <span className="font-semibold text-xs text-white">Refine & Modify</span>
        </div>
        <button
          onClick={onToggle}
          className="text-xs text-slate-400 hover:text-white p-1 rounded hover:bg-white/5"
        >
          ✕
        </button>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {/* Project Info */}
        <div className="p-3 rounded-xl bg-white/[0.03] border border-white/5">
          <div className="text-[11px] font-semibold uppercase text-indigo-400 tracking-wider mb-1">
            Active Site
          </div>
          <h4 className="text-sm font-bold text-white mb-1 truncate">{project.title}</h4>
          <p className="text-xs text-slate-400 leading-relaxed line-clamp-3">
            {project.description}
          </p>
        </div>

        {/* Quick Tweak Chips */}
        <div>
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-purple-400" />
            <span>Quick Suggestions</span>
          </div>
          <div className="flex flex-col gap-1.5">
            {QUICK_REFINEMENTS.map((chip, idx) => (
              <button
                key={idx}
                onClick={() => setTweakPrompt(chip)}
                className="text-left text-xs p-2 rounded-lg bg-white/[0.02] hover:bg-white/[0.06] border border-white/5 hover:border-indigo-500/20 text-slate-300 hover:text-white transition flex items-center justify-between group"
              >
                <span>{chip}</span>
                <ChevronRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition" />
              </button>
            ))}
          </div>
        </div>

        {/* Revision History */}
        {project.revisions && project.revisions.length > 0 && (
          <div>
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <History className="w-3.5 h-3.5 text-indigo-400" />
              <span>Revision History ({project.revisions.length})</span>
            </div>
            <div className="space-y-1.5">
              {project.revisions.map((rev) => (
                <div
                  key={rev.id}
                  className="p-2 rounded-lg bg-white/[0.02] border border-white/5 text-xs text-slate-300"
                >
                  <div className="flex items-center justify-between text-[11px] font-semibold text-indigo-400 mb-0.5">
                    <span>Rev #{rev.revision_number}</span>
                    <span className="text-slate-500 text-[10px]">
                      {new Date(rev.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  <p className="text-slate-400 line-clamp-2 text-[11px]">{rev.prompt}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Bottom Refine Input */}
      <form onSubmit={handleSubmit} className="p-3 border-t border-white/10 bg-[#12141c]">
        <div className="relative">
          <textarea
            value={tweakPrompt}
            onChange={(e) => setTweakPrompt(e.target.value)}
            placeholder="Tell SiteForge what to change or add..."
            rows={3}
            disabled={isRefining}
            className="w-full bg-white/5 border border-white/10 rounded-xl p-2.5 text-xs text-white placeholder-slate-500 outline-none focus:border-indigo-500 transition resize-none"
          />
          <button
            type="submit"
            disabled={!tweakPrompt.trim() || isRefining}
            className="w-full mt-2 py-2 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 disabled:opacity-40 text-white text-xs font-semibold flex items-center justify-center gap-2 shadow-md shadow-indigo-500/20 transition"
          >
            {isRefining ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>Applying Changes...</span>
              </>
            ) : (
              <>
                <Send className="w-3.5 h-3.5" />
                <span>Update Site</span>
              </>
            )}
          </button>
        </div>
      </form>
    </aside>
  );
}
