import React, { useState, useEffect } from 'react';
import { Sparkles, Code2, Palette, ShieldCheck, Cpu } from 'lucide-react';

export default function GeneratingOverlay({ isGenerating, prompt }) {
  const [stepIndex, setStepIndex] = useState(0);

  const STEPS = [
    { title: "Analyzing Concept & Requirements", desc: "Parsing design intent, target persona, and section structure...", icon: Sparkles },
    { title: "Architecting Design System", desc: "Generating color harmonies, CSS variables, typography, and spacing...", icon: Palette },
    { title: "Synthesizing Interactive Components", desc: "Assembling navigation, hero banner, feature grids, and forms...", icon: Code2 },
    { title: "Injecting Responsive Logic & Vanilla JS", desc: "Calibrating mobile viewports, touch menus, and scroll animations...", icon: Cpu },
    { title: "Finalizing Production-Ready Bundle", desc: "Polishing standalone HTML, closing tags, and optimizing layout...", icon: ShieldCheck }
  ];

  useEffect(() => {
    if (!isGenerating) {
      setStepIndex(0);
      return;
    }

    const interval = setInterval(() => {
      setStepIndex((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 2800);

    return () => clearInterval(interval);
  }, [isGenerating]);

  if (!isGenerating) return null;

  const currentStep = STEPS[stepIndex];
  const CurrentIcon = currentStep.icon;

  return (
    <div className="fixed inset-0 z-50 bg-[#090a0f]/90 backdrop-blur-xl flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-[#12141c] border border-white/10 rounded-2xl p-6 md:p-8 shadow-2xl text-center relative overflow-hidden">
        {/* Glow behind */}
        <div className="absolute -top-24 -left-24 w-48 h-48 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -right-24 w-48 h-48 bg-purple-500/20 rounded-full blur-3xl pointer-events-none" />

        {/* Icon Sphere */}
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-500 to-purple-500 p-0.5 mx-auto mb-6 shadow-xl shadow-indigo-500/20 animate-pulse">
          <div className="w-full h-full bg-[#12141c] rounded-[14px] flex items-center justify-center">
            <CurrentIcon className="w-8 h-8 text-indigo-400" />
          </div>
        </div>

        {/* Title */}
        <h3 className="text-xl font-bold text-white mb-2 tracking-tight">
          {currentStep.title}
        </h3>
        <p className="text-xs text-slate-400 mb-6 leading-relaxed">
          {currentStep.desc}
        </p>

        {/* Prompt snippet */}
        <div className="p-3 rounded-xl bg-white/[0.03] border border-white/5 text-[11px] text-slate-300 italic mb-6 line-clamp-2">
          "{prompt}"
        </div>

        {/* Step dots */}
        <div className="flex items-center justify-center gap-2 mb-2">
          {STEPS.map((_, i) => (
            <div
              key={i}
              className={`h-1.5 rounded-full transition-all duration-500 ${
                i === stepIndex 
                  ? 'w-8 bg-indigo-500' 
                  : i < stepIndex 
                  ? 'w-2 bg-emerald-500' 
                  : 'w-2 bg-white/10'
              }`}
            />
          ))}
        </div>
        <div className="text-[10px] uppercase tracking-wider font-semibold text-slate-500">
          Step {stepIndex + 1} of {STEPS.length}
        </div>
      </div>
    </div>
  );
}
