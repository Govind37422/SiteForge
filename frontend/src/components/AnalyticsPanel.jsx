import React from 'react';
import { Activity, ShieldCheck, Database, Zap } from 'lucide-react';

export default function AnalyticsPanel() {
  return (
    <div className="flex gap-4 p-4 border-t border-white/10 bg-[#0f111a] text-slate-300 text-xs font-semibold">
      <div className="flex items-center gap-2">
        <Activity className="w-3.5 h-3.5 text-indigo-400" />
        <span>Telemetry Active</span>
      </div>
      <div className="flex items-center gap-2">
        <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
        <span>CORS / Sec Headers: Secured</span>
      </div>
      <div className="flex items-center gap-2">
        <Database className="w-3.5 h-3.5 text-amber-400" />
        <span>Atomic Storage: JSON</span>
      </div>
      <div className="flex items-center gap-2">
        <Zap className="w-3.5 h-3.5 text-cyan-400" />
        <span>Automatic Failover: Ready</span>
      </div>
    </div>
  );
}
