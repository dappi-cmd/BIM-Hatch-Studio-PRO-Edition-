import React from 'react';
import HatchEditor from '@/components/HatchEditor';

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-200 flex flex-col font-sans">
      {/* Top Navbar */}
      <header className="h-14 border-b border-slate-800 bg-slate-900 flex items-center justify-between px-6">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-sky-500 rounded flex items-center justify-center font-bold text-white shadow-[0_0_15px_rgba(14,165,233,0.5)]">
            B
          </div>
          <h1 className="text-xl font-semibold tracking-tight text-white">BIM Hatch Studio</h1>
        </div>
        <div className="flex items-center gap-4">
          <button className="px-4 py-1.5 text-sm bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-md transition-colors">
            Material Library
          </button>
          <button className="px-4 py-1.5 text-sm bg-sky-600 hover:bg-sky-500 text-white font-medium rounded-md shadow-lg shadow-sky-500/20 transition-all">
            Export .PAT
          </button>
        </div>
      </header>

      {/* Main Workspace */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Toolbar (Tools) */}
        <aside className="w-16 border-r border-slate-800 bg-slate-900 flex flex-col items-center py-4 gap-4">
          <div className="w-10 h-10 rounded bg-slate-800 flex items-center justify-center cursor-pointer hover:bg-slate-700 border border-slate-700 transition" title="Select">
            <span className="text-xl">↖</span>
          </div>
          <div className="w-10 h-10 rounded bg-slate-800 flex items-center justify-center cursor-pointer hover:bg-slate-700 border border-slate-700 transition" title="Line Tool">
            <span className="text-xl">╱</span>
          </div>
          <div className="w-10 h-10 rounded bg-slate-800 flex items-center justify-center cursor-pointer hover:bg-slate-700 border border-slate-700 transition" title="Rectangle">
            <span className="text-xl">□</span>
          </div>
        </aside>

        {/* Center Canvas */}
        <section className="flex-1 p-4 flex flex-col bg-slate-950">
          <HatchEditor />
        </section>

        {/* Right Sidebar (Properties & Preview) */}
        <aside className="w-80 border-l border-slate-800 bg-slate-900 flex flex-col overflow-y-auto">
          <div className="p-4 border-b border-slate-800">
            <h2 className="font-semibold text-slate-100 mb-4">Pattern Properties</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-xs text-slate-400 mb-1">Pattern Name</label>
                <input type="text" className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-sm focus:outline-none focus:border-sky-500" defaultValue="BIM_TILE_001" />
              </div>
              
              <div>
                <label className="block text-xs text-slate-400 mb-1">Type</label>
                <select className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-sm focus:outline-none focus:border-sky-500">
                  <option>Model (Scale-Aware)</option>
                  <option>Drafting (Fixed Scale)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs text-slate-400 mb-1">Grid Snap Size</label>
                <input type="number" className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-sm focus:outline-none focus:border-sky-500" defaultValue={100} />
              </div>
            </div>
          </div>

          <div className="p-4 border-b border-slate-800 flex-1">
            <h2 className="font-semibold text-slate-100 mb-4">3D Material Preview</h2>
            <div className="w-full h-48 bg-slate-950 rounded border border-slate-800 flex items-center justify-center text-slate-600 text-sm">
              [ Three.js Preview Canvas ]
            </div>
          </div>
          
          <div className="p-4">
            <h2 className="font-semibold text-slate-100 mb-2">Generated .PAT Output</h2>
            <pre className="bg-slate-950 border border-slate-800 rounded p-3 text-xs text-emerald-400 font-mono h-32 overflow-y-auto">
{`*BIM_TILE_001, Seamless Tile Pattern
;%TYPE=MODEL
0, 0,0, 0,100, 100,-100
90, 0,0, 100,0, 100,-100`}
            </pre>
          </div>
        </aside>
      </div>
    </main>
  );
}
