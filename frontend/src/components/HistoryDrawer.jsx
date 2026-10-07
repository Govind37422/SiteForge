import React from 'react';
import { History, X, Trash2, ArrowUpRight, Clock, FileCode } from 'lucide-react';

export default function HistoryDrawer({ isOpen, onClose, projects, onSelectProject, onDeleteProject }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Backdrop */}
      <div 
        onClick={onClose} 
        className="fixed inset-0 bg-black/60 backdrop-blur-sm transition-opacity" 
      />

      {/* Drawer */}
      <div className="relative w-full max-w-md bg-[#0f1118] border-l border-white/10 h-full flex flex-col z-10 shadow-2xl animate-fade-in">
        {/* Header */}
        <div className="h-16 px-6 border-b border-white/10 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <History className="w-5 h-5 text-indigo-400" />
            <h3 className="font-bold text-sm text-white">Project History</h3>
            <span className="text-xs px-2 py-0.5 rounded-full bg-white/10 text-slate-300 font-mono">
              {projects.length}
            </span>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {projects.length === 0 ? (
            <div className="h-64 flex flex-col items-center justify-center text-center p-6 text-slate-500">
              <History className="w-10 h-10 mb-2 opacity-30" />
              <p className="text-sm font-medium">No saved websites yet</p>
              <p className="text-xs text-slate-600 mt-1">Generate your first site to start building your history.</p>
            </div>
          ) : (
            projects.map((proj) => (
              <div
                key={proj.id}
                className="group relative p-4 rounded-xl bg-white/[0.02] hover:bg-white/[0.06] border border-white/5 hover:border-indigo-500/30 transition-all cursor-pointer"
                onClick={() => {
                  onSelectProject(proj.id);
                  onClose();
                }}
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <h4 className="text-sm font-semibold text-slate-200 group-hover:text-white truncate">
                    {proj.title}
                  </h4>
                  <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDeleteProject(proj.id);
                      }}
                      className="p-1 rounded hover:bg-red-500/20 text-slate-400 hover:text-red-400 transition"
                      title="Delete"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                    <div className="p-1 text-indigo-400">
                      <ArrowUpRight className="w-3.5 h-3.5" />
                    </div>
                  </div>
                </div>

                <p className="text-xs text-slate-400 line-clamp-2 mb-3 leading-relaxed">
                  {proj.prompt}
                </p>

                <div className="flex items-center justify-between text-[11px] text-slate-500 font-mono">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {new Date(proj.created_at).toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </span>
                  <span className="text-[10px] uppercase font-semibold text-indigo-400/80 bg-indigo-500/10 px-1.5 py-0.5 rounded">
                    {proj.model || 'AI Model'}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
