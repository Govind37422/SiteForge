import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import PromptConsole from './components/PromptConsole';
import PreviewViewport from './components/PreviewViewport';
import CodeViewer from './components/CodeViewer';
import RefineSidebar from './components/RefineSidebar';
import HistoryDrawer from './components/HistoryDrawer';
import GeneratingOverlay from './components/GeneratingOverlay';
import AnalyticsPanel from './components/AnalyticsPanel';
import { Sparkles, MessageSquare, Send, Cpu, Layers, Palette, Terminal } from 'lucide-react';

export default function App() {
  const [currentProject, setCurrentProject] = useState(null);
  const [projects, setProjects] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [providerInfo, setProviderInfo] = useState(null);
  
  // UI states
  const [activeTab, setActiveTab] = useState('preview'); // 'preview' | 'code'
  const [isGenerating, setIsGenerating] = useState(false);
  const [isRefining, setIsRefining] = useState(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [isRefineSidebarOpen, setIsRefineSidebarOpen] = useState(true);
  const [currentPrompt, setCurrentPrompt] = useState('');
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    fetchHealth();
    fetchTemplates();
    fetchProjects();
  }, []);

  const fetchHealth = async () => {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        setProviderInfo(data);
      }
    } catch (err) {
      console.error('Health check error:', err);
    }
  };

  const fetchTemplates = async () => {
    try {
      const res = await fetch('/api/templates');
      if (res.ok) {
        const data = await res.json();
        setTemplates(data);
      }
    } catch (err) {
      console.error('Fetch templates error:', err);
    }
  };

  const fetchProjects = async () => {
    try {
      const res = await fetch('/api/projects');
      if (res.ok) {
        const data = await res.json();
        setProjects(data);
      }
    } catch (err) {
      console.error('Fetch projects error:', err);
    }
  };

  const handleGenerate = async (promptText) => {
    setIsGenerating(true);
    setCurrentPrompt(promptText);
    setErrorMessage(null);

    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: promptText }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Generation failed');
      }

      const newProj = await res.json();
      setCurrentProject(newProj);
      setActiveTab('preview');
      fetchProjects();
    } catch (err) {
      setErrorMessage(err.message);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleRefine = async (refinePrompt) => {
    if (!currentProject) return;
    setIsRefining(true);
    setErrorMessage(null);

    try {
      const res = await fetch('/api/refine', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_id: currentProject.id,
          prompt: refinePrompt,
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Refinement failed');
      }

      const updated = await res.json();
      setCurrentProject((prev) => ({
        ...prev,
        title: updated.title,
        files: updated.files,
        revisions: [
          ...(prev.revisions || []),
          {
            id: Date.now(),
            prompt: refinePrompt,
            revision_number: updated.revision_number,
            created_at: new Date().toISOString(),
          },
        ],
      }));
    } catch (err) {
      setErrorMessage(err.message);
    } finally {
      setIsRefining(false);
    }
  };

  const handleSelectProject = async (projectId) => {
    try {
      const res = await fetch(`/api/projects/${projectId}`);
      if (res.ok) {
        const data = await res.json();
        setCurrentProject(data);
        setActiveTab('preview');
      }
    } catch (err) {
      console.error('Select project error:', err);
    }
  };

  const handleDeleteProject = async (projectId) => {
    try {
      const res = await fetch(`/api/projects/${projectId}`, { method: 'DELETE' });
      if (res.ok) {
        if (currentProject?.id === projectId) {
          setCurrentProject(null);
        }
        fetchProjects();
      }
    } catch (err) {
      console.error('Delete project error:', err);
    }
  };

  const handleExport = () => {
    if (!currentProject || !currentProject.files) return;
    const htmlContent = currentProject.files["index.html"] || "";
    const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${(currentProject.title || 'siteforge-app').toLowerCase().replace(/\s+/g, '-')}.html`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleNewSite = () => {
    setCurrentProject(null);
    setErrorMessage(null);
  };

  return (
    <div className="min-h-screen bg-[#07080d] text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Navbar */}
      <Navbar
        currentProject={currentProject}
        onNewSite={handleNewSite}
        onOpenHistory={() => setIsHistoryOpen(true)}
        historyCount={projects.length}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onExport={handleExport}
        providerInfo={providerInfo}
      />

      {/* Error Toast */}
      {errorMessage && (
        <div className="fixed top-20 right-6 z-50 bg-red-500/10 border border-red-500/30 text-red-200 px-4 py-3 rounded-xl backdrop-blur-md shadow-2xl flex items-center justify-between gap-4 max-w-md animate-fade-in">
          <span className="text-xs">{errorMessage}</span>
          <button onClick={() => setErrorMessage(null)} className="text-red-400 hover:text-white text-xs font-bold">✕</button>
        </div>
      )}

      {/* Workspace */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {!currentProject ? (
          <PromptConsole
            onGenerate={handleGenerate}
            templates={templates}
            isGenerating={isGenerating}
          />
        ) : (
          <div className="flex-1 flex overflow-hidden">
            <div className="flex-1 flex flex-col overflow-hidden">
              {activeTab === 'preview' ? (
                <PreviewViewport
                  project={currentProject}
                  onOpenInNewTab={() => window.open(`/api/preview/${currentProject.id}`, '_blank')}
                />
              ) : (
                <CodeViewer
                  project={currentProject}
                  onDownload={handleExport}
                />
              )}
            </div>

            <RefineSidebar
              project={currentProject}
              onRefine={handleRefine}
              isRefining={isRefining}
              isOpen={isRefineSidebarOpen}
              onToggle={() => setIsRefineSidebarOpen(!isRefineSidebarOpen)}
            />
          </div>
        )}
      </main>

      <AnalyticsPanel />
      
      <HistoryDrawer
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        projects={projects}
        onSelectProject={handleSelectProject}
        onDeleteProject={handleDeleteProject}
      />

      <GeneratingOverlay
        isGenerating={isGenerating}
        prompt={currentPrompt}
      />
    </div>
  );
}
