import React, { useState } from 'react';
import { Copy, Check, Download, FileCode, CheckCircle2 } from 'lucide-react';

export default function CodeViewer({ project, onDownload }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(project.full_code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const codeLines = project.full_code.split('\n');

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-4rem)] bg-[#0c0d14] font-mono text-xs overflow-hidden">
      {/* Top Header */}
      <div className="h-12 border-b border-white/10 bg-[#12141c] px-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <FileCode className="w-4 h-4 text-indigo-400" />
          <span className="text-slate-200 font-semibold text-xs">index.html</span>
          <span className="text-slate-500 text-[11px]">({codeLines.length} lines)</span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-slate-200 transition font-sans"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-emerald-400">Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5 text-slate-400" />
                <span>Copy Code</span>
              </>
            )}
          </button>
          
          <button
            onClick={onDownload}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition font-sans shadow-sm"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download</span>
          </button>
        </div>
      </div>

      {/* Code Text Area with Line Numbers */}
      <div className="flex-1 overflow-auto p-4 flex gap-4 text-slate-300 select-text">
        <div className="select-none text-slate-600 text-right pr-3 border-r border-white/5 font-mono">
          {codeLines.map((_, i) => (
            <div key={i} className="leading-5">{i + 1}</div>
          ))}
        </div>
        <pre className="flex-1 leading-5 overflow-x-auto text-slate-200 whitespace-pre">
          <code>{project.full_code}</code>
        </pre>
      </div>
    </div>
  );
}
