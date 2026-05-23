"use client";

import React, { useState, useRef, useEffect } from 'react';
import { Stage, Layer, Line, Circle, Rect } from 'react-konva';

export default function HatchEditor() {
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      setDimensions({
        width: containerRef.current.offsetWidth,
        height: containerRef.current.offsetHeight,
      });
    }
    
    const handleResize = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.offsetWidth,
          height: containerRef.current.offsetHeight,
        });
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="w-full h-full bg-slate-900 border border-slate-700 rounded-lg overflow-hidden flex flex-col">
      <div className="bg-slate-800 p-2 flex justify-between items-center border-b border-slate-700 text-slate-300 text-sm font-medium">
        <span>Workspace (Infinite Canvas)</span>
        <div className="flex gap-2">
          <button className="px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs transition">Grid Snap</button>
          <button className="px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs transition">Draw Line</button>
        </div>
      </div>
      <div ref={containerRef} className="flex-1 w-full relative">
        <Stage width={dimensions.width} height={dimensions.height}>
          <Layer>
            {/* Background Grid */}
            <Rect 
              x={0} 
              y={0} 
              width={dimensions.width} 
              height={dimensions.height} 
              fill="#0f172a" 
            />
            {/* Grid Lines Placeholder */}
            {Array.from({ length: 50 }).map((_, i) => (
              <React.Fragment key={i}>
                <Line points={[0, i * 20, dimensions.width, i * 20]} stroke="#1e293b" strokeWidth={1} />
                <Line points={[i * 20, 0, i * 20, dimensions.height]} stroke="#1e293b" strokeWidth={1} />
              </React.Fragment>
            ))}
            
            {/* Example Vector Line */}
            <Line
              points={[100, 100, 300, 300]}
              stroke="#38bdf8"
              strokeWidth={3}
              draggable
            />
          </Layer>
        </Stage>
      </div>
    </div>
  );
}
