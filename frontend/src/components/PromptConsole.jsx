import React, { useState } from 'react';
import { Sparkles, ArrowRight, Wand2, Compass } from 'lucide-react';

export default function PromptConsole({ onGenerate, templates, isGenerating }) {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!prompt.trim() || isGenerating) return;
    onGenerate(prompt);
  };

  const handleKeyDown = (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      handleSubmit();
    }
  };

  const handleSelectTemplate = (templatePrompt) => {
    setPrompt(templatePrompt);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12 md:py-20 text-center animate-fade-in">
      {/* Glow Badge */}
      <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold mb-6 shadow-sm shadow-indigo-500/10">
        <Sparkles className="w-3.5 h-3.5" />
        <span>Next-Generation AI Website Synthesis</span>
      </div>

      {/* Main Title */}
      <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-white mb-6 leading-tight">
        Build high-end websites with <br className="hidden sm:block" />
        <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400 bg-clip-text text-transparent">
          pure natural language
        </span>
      </h1>

      <p className="text-slate-400 text-base sm:text-lg max-w-2xl mx-auto mb-10 leading-relaxed">
        Describe your concept. SiteForge crafts responsive, production-ready websites with stunning glassmorphic UI, animations, and zero configuration.
      </p>

      {/* Input Console */}
      <form onSubmit={handleSubmit} className="relative max-w-3xl mx-auto mb-10">
        <div className="relative rounded-2xl p-1 bg-gradient-to-b from-white/15 to-white/5 shadow-2xl shadow-indigo-500/10 focus-within:from-indigo-500/40 focus-within:to-purple-500/40 transition-all duration-300">
          <div className="bg-[#12141c] rounded-[14px] p-2 flex flex-col sm:flex-row items-stretch gap-2">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="e.g. A futuristic dark-mode landing page for an AI cyber-security platform with glowing metrics, interactive threat scanner card, client badges, and pricing tiers..."
              rows={3}
              className="w-full bg-transparent text-slate-100 placeholder-slate-500 text-sm p-3 outline-none resize-none"
            />
            
            <div className="flex sm:flex-col justify-between items-end gap-2 p-1">
              <span className="text-[11px] text-slate-500 hidden sm:block whitespace-nowrap">
                Ctrl + Enter
              </span>
              <button
                type="submit"
                disabled={!prompt.trim() || isGenerating}
                className="w-full sm:w-auto px-5 py-3 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-medium text-sm flex items-center justify-center gap-2 shadow-lg shadow-indigo-500/25 transition-all hover:scale-105 active:scale-95"
              >
                <Wand2 className="w-4 h-4" />
                <span>Forge Site</span>
              </button>
            </div>
          </div>
        </div>
      </form>

      {/* Pre-engineered Inspirations */}
      {templates && templates.length > 0 && (
        <div className="max-w-3xl mx-auto text-left">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 px-1">
            <Compass className="w-3.5 h-3.5 text-indigo-400" />
            <span>Curated Inspirations</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {templates.map((tpl) => (
              <button
                key={tpl.id}
                onClick={() => handleSelectTemplate(tpl.prompt)}
                className="group p-3.5 rounded-xl bg-white/[0.03] hover:bg-white/[0.08] border border-white/5 hover:border-indigo-500/30 text-left transition-all duration-200"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[11px] font-semibold text-indigo-400 uppercase tracking-wider">
                    {tpl.category}
                  </span>
                  <ArrowRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition-all" />
                </div>
                <h4 className="text-sm font-semibold text-slate-200 group-hover:text-white mb-1">
                  {tpl.title}
                </h4>
                <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                  {tpl.prompt}
                </p>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
