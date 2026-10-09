import React, { useState, useEffect } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { Copy, Check, Share2, X, Smartphone, Globe, Zap } from 'lucide-react';

export default function ShareModal({ project, onClose }) {
  const [copied, setCopied] = useState(false);
  const [shareUrl, setShareUrl] = useState('');

  useEffect(() => {
    if (project?.id != null) {
      const base = window.location.origin;
      setShareUrl(`${base}/api/preview/${project.id}`);
    }
  }, [project]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(shareUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback for non-secure contexts (http tunnel links)
      const ta = document.createElement('textarea');
      ta.value = shareUrl;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (!project) return null;

  return (
    <div
      className="fixed inset-0 z-[90] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-md bg-[#0d0e14] border border-white/10 rounded-3xl shadow-2xl shadow-black/60 overflow-hidden animate-scale-in"
      >
        {/* Header */}
        <div className="relative px-6 pt-6 pb-4 bg-gradient-to-br from-indigo-600/25 via-purple-600/10 to-transparent border-b border-white/10">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-slate-400 hover:text-white transition"
          >
            <X className="w-4 h-4" />
          </button>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30">
              <Share2 className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-white text-lg leading-tight">Share this app</h3>
              <p className="text-xs text-slate-400">Anyone with the link can open it — no account needed</p>
            </div>
          </div>
        </div>

        {/* Body */}
        <div className="p-6 space-y-5">
          {/* App title */}
          <div className="text-center">
            <div className="text-sm font-semibold text-slate-200 truncate">{project.title || 'Your app'}</div>
            <div className="text-[11px] text-slate-500 mt-0.5">Generated with SiteForge</div>
          </div>

          {/* QR Code */}
          <div className="flex justify-center">
            <div className="p-4 rounded-2xl bg-white shadow-xl shadow-indigo-500/10">
              <QRCodeSVG
                value={shareUrl}
                size={168}
                level="M"
                bgColor="#ffffff"
                fgColor="#090a0f"
              />
            </div>
          </div>
          <p className="text-center text-[11px] text-slate-500 flex items-center justify-center gap-1.5">
            <Smartphone className="w-3.5 h-3.5 text-indigo-400" />
            Scan on any phone to open instantly
          </p>

          {/* Link row */}
          <div className="flex items-center gap-2 bg-white/5 border border-white/10 rounded-xl p-1.5 pl-3.5">
            <Globe className="w-4 h-4 text-indigo-400 shrink-0" />
            <input
              readOnly
              value={shareUrl}
              onFocus={(e) => e.target.select()}
              className="flex-1 bg-transparent text-xs text-slate-300 focus:outline-none min-w-0"
            />
            <button
              onClick={handleCopy}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all shrink-0 ${
                copied
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-md shadow-indigo-600/25'
              }`}
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>

          {/* Native share */}
          {typeof navigator !== 'undefined' && navigator.share && (
            <button
              onClick={() => navigator.share({ title: project.title || 'SiteForge app', url: shareUrl })}
              className="w-full flex items-center justify-center gap-2 py-3 rounded-xl border border-indigo-500/30 bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-300 text-xs font-semibold transition"
            >
              <Zap className="w-4 h-4" />
              Share via WhatsApp / More
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
