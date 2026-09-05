"use client";

import dynamic from "next/dynamic";
import { useState } from "react";

import {
  Activity,
  AlertOctagon,
  Radio,
  Sliders,
  Layers,
  Cpu,
  CheckCircle2,
  MapPin,
} from "lucide-react";

const DeckGLMap = dynamic(() => import("@/components/DeckGLMap"), {
  ssr: false,
});

export default function Home() {
  const [rainfall, setRainfall] = useState(45);
  const [drainageCapacity, setDrainageCapacity] = useState(80);

  const drainageFactor = drainageCapacity / 80;

  const nodes = [
    {
      id: "NODE-01",
      name: "Fort Basin Outflow",
      lat: 12.9165,
      lng: 79.1325,
      water_level_m: Number(
        (1.2 + (rainfall * 0.04) / drainageFactor).toFixed(1)
      ),
      risk_score: Math.min(
        99,
        Math.round((30 + rainfall * 1.1) / drainageFactor)
      ),
    },

    {
      id: "NODE-02",
      name: "Subterranean Canal C2",
      lat: 12.9692,
      lng: 79.1559,
      water_level_m: Number(
        (0.8 + (rainfall * 0.02) / drainageFactor).toFixed(1)
      ),
      risk_score: Math.min(
        99,
        Math.round((15 + rainfall * 0.6) / drainageFactor)
      ),
    },

    {
      id: "NODE-03",
      name: "Junction Sector 4 Outflow",
      lat: 12.9734,
      lng: 79.1384,
      water_level_m: Number(
        (1.5 + (rainfall * 0.05) / drainageFactor).toFixed(1)
      ),
      risk_score: Math.min(
        99,
        Math.round((45 + rainfall * 0.9) / drainageFactor)
      ),
    },

    {
      id: "NODE-04",
      name: "Katpadi North Sluice",
      lat: 12.9811,
      lng: 79.1412,
      water_level_m: Number(
        (0.5 + (rainfall * 0.01) / drainageFactor).toFixed(1)
      ),
      risk_score: Math.min(
        99,
        Math.round((10 + rainfall * 0.4) / drainageFactor)
      ),
    },

    {
      id: "NODE-05",
      name: "Southern Intake Channel",
      lat: 12.905,
      lng: 79.121,
      water_level_m: Number(
        (2.0 + (rainfall * 0.06) / drainageFactor).toFixed(1)
      ),
      risk_score: Math.min(
        99,
        Math.round((55 + rainfall * 1.0) / drainageFactor)
      ),
    },
  ];

  const criticalNodes = nodes.filter((n) => n.risk_score > 60);

  const avgRisk = Math.round(
    nodes.reduce((acc, curr) => acc + curr.risk_score, 0) / nodes.length
  );

  return (
    <div className="h-screen w-screen bg-[#0b0f19] text-slate-300 flex flex-col p-3 gap-3 overflow-hidden select-none font-sans">

      {/* Header */}

      <header className="h-14 bg-slate-900/70 backdrop-blur-md border border-slate-800/80 rounded-lg px-4 flex items-center justify-between shrink-0 shadow-sm">

        <div className="flex items-center gap-4">

          <div className="p-2 bg-slate-950/60 border border-slate-800 rounded-md">
            <Cpu className="w-5 h-5 text-slate-400" />
          </div>

          <div>
            <div className="flex items-center gap-2">

              <h1 className="text-sm font-semibold tracking-wide text-slate-200 uppercase">
                RESILIX AI{" "}
                <span className="text-slate-500 font-normal">
                  | COMMAND & TELEMETRY HUB
                </span>
              </h1>

              <span className="px-1.5 py-0.5 text-[9px] bg-slate-800/60 text-slate-400 border border-slate-700/50 rounded">
                v2.4-PROD
              </span>

            </div>

            <p className="text-[10px] text-slate-500 uppercase tracking-tight">
              Real-time Spatial Intelligence & Multi-Hazard Predictive Modeling
            </p>
          </div>

        </div>

        <div className="flex items-center gap-6 text-xs">

          <div className="flex items-center gap-2">
            <span className="text-slate-500 text-[10px] uppercase">
              Telemetry Relay:
            </span>

            <span className="flex items-center gap-1.5 font-medium text-emerald-400/90">
              <Radio className="w-3.5 h-3.5 text-emerald-400" />
              SIMULATION LIVE
            </span>
          </div>

          <div className="h-4 w-px bg-slate-800" />

          <div className="flex items-center gap-2">
            <span className="text-slate-500 text-[10px] uppercase">
              System Risk Index:
            </span>

            <span
              className={`px-2 py-0.5 font-medium rounded text-[11px] ${
                avgRisk > 50
                  ? "bg-amber-950/40 text-amber-300/90 border border-amber-900/50"
                  : "bg-emerald-950/40 text-emerald-300/90 border border-emerald-900/50"
              }`}
            >
              {avgRisk}% AVG
            </span>
          </div>

        </div>
      </header>

      {/* Main */}

      <div className="flex-1 w-full grid grid-cols-12 gap-3 min-h-0">

        {/* LEFT */}

        <div className="col-span-3 flex flex-col gap-3 h-full overflow-hidden">

          <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/80 p-3 rounded-lg flex flex-col gap-2 shrink-0">

            <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <Activity className="w-3.5 h-3.5 text-slate-400" />
              Sensor Network Metrics
            </span>

            <div className="grid grid-cols-3 gap-2 pt-1 text-center">

              <div className="p-2 bg-slate-950/40 border border-slate-800/60 rounded-md">
                <span className="text-[10px] text-slate-500 block">
                  Total
                </span>

                <span className="text-sm font-semibold text-slate-300">
                  {nodes.length}
                </span>
              </div>

              <div className="p-2 bg-slate-950/40 border border-slate-800/60 rounded-md">
                <span className="text-[10px] text-slate-500 block">
                  Normal
                </span>

                <span className="text-sm font-semibold text-emerald-400/90">
                  {nodes.length - criticalNodes.length}
                </span>
              </div>

              <div className="p-2 bg-slate-950/40 border border-slate-800/60 rounded-md">
                <span className="text-[10px] text-slate-500 block">
                  Critical
                </span>

                <span className="text-sm font-semibold text-amber-400/90">
                  {criticalNodes.length}
                </span>
              </div>

            </div>
          </div>

          <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/80 p-3 rounded-lg flex-1 flex flex-col gap-2 min-h-0 overflow-hidden">

            <div className="flex justify-between items-center pb-2 border-b border-slate-800/60 shrink-0">

              <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <MapPin className="w-3.5 h-3.5 text-slate-400" />
                Live Sensor Feed
              </span>

              <span className="text-[9px] text-slate-500">
                {nodes.length} Active Points
              </span>

            </div>

            <div className="flex-1 overflow-y-auto flex flex-col gap-2 pr-1">

              {nodes.map((node) => (
                <div
                  key={node.id}
                  className={`p-2.5 rounded-md border flex flex-col gap-1 shrink-0 transition-all ${
                    node.risk_score > 60
                      ? "bg-amber-950/20 border-amber-900/40"
                      : node.risk_score > 35
                      ? "bg-slate-950/60 border-slate-800/80"
                      : "bg-slate-950/40 border-slate-800/60"
                  }`}
                >

                  <div className="flex justify-between items-center text-xs">

                    <span className="font-medium text-slate-300">
                      {node.name}
                    </span>

                    <span
                      className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${
                        node.risk_score > 60
                          ? "bg-amber-950/60 text-amber-300 border border-amber-900/50"
                          : "bg-slate-800/80 text-slate-400"
                      }`}
                    >
                      {node.risk_score}%
                    </span>

                  </div>

                  <div className="flex justify-between items-center text-[10px] text-slate-500">

                    <span>ID: {node.id}</span>

                    <span>
                      Depth:{" "}
                      <strong className="text-slate-400">
                        {node.water_level_m}m
                      </strong>
                    </span>

                  </div>

                </div>
              ))}

            </div>
          </div>

        </div>

        {/* CENTER MAP */}

        <div className="col-span-6 flex flex-col h-full relative min-h-0">

          <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/80 rounded-lg w-full h-full relative overflow-hidden shadow-sm">

            <div className="absolute top-3 left-3 z-20 flex items-center gap-2 px-3 py-1.5 bg-slate-950/80 backdrop-blur border border-slate-800 rounded-md text-[11px] shadow-sm pointer-events-none">

              <Layers className="w-3.5 h-3.5 text-slate-400" />

              <span className="text-slate-300 font-medium">
                Subterranean Hydrological Layer
              </span>

            </div>

            <div className="absolute inset-0 w-full h-full">
              <DeckGLMap
                telemetry={{
                  timestamp: new Date().toISOString(),
                  storm_category: 2,
                  nodes,
                }}
              />
            </div>

            <div className="absolute bottom-3 left-3 right-3 z-20 px-3 py-2 bg-slate-950/80 backdrop-blur border border-slate-800 rounded-md flex justify-between items-center text-[10px] text-slate-500 pointer-events-none">

              <div className="flex items-center gap-4">

                <span>
                  Projection:{" "}
                  <strong className="text-slate-400">
                    EPSG:3857
                  </strong>
                </span>

                <span>
                  Coordinates:{" "}
                  <strong className="text-slate-400">
                    12.9165° N, 79.1325° E
                  </strong>
                </span>

              </div>

              <span className="text-emerald-400/90 flex items-center gap-1">

                <CheckCircle2 className="w-3 h-3 text-emerald-400" />

                Spatial Engine Ready

              </span>

            </div>

          </div>

        </div>

        {/* RIGHT */}

        <div className="col-span-3 flex flex-col gap-3 h-full overflow-hidden">

          <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/80 p-3.5 rounded-lg flex flex-col gap-3 shrink-0">

            <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-800/60 pb-2">

              <Sliders className="w-3.5 h-3.5 text-slate-400" />

              Predictive Stress Tuning

            </span>

            <div className="flex flex-col gap-1.5">

              <div className="flex justify-between text-xs">

                <span className="text-slate-400">
                  Precipitation Rate
                </span>

                <span className="font-medium text-slate-300">
                  {rainfall} mm/h
                </span>

              </div>

              <input
                type="range"
                min="5"
                max="100"
                value={rainfall}
                onChange={(e) =>
                  setRainfall(Number(e.target.value))
                }
                className="accent-slate-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
              />

            </div>

            <div className="flex flex-col gap-1.5">

              <div className="flex justify-between text-xs">

                <span className="text-slate-400">
                  Sluice Gate Efficiency
                </span>

                <span className="font-medium text-slate-300">
                  {drainageCapacity}%
                </span>

              </div>

              <input
                type="range"
                min="10"
                max="100"
                value={drainageCapacity}
                onChange={(e) =>
                  setDrainageCapacity(Number(e.target.value))
                }
                className="accent-slate-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
              />

            </div>

          </div>

          <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/80 p-3.5 rounded-lg flex-1 flex flex-col gap-2 min-h-0 overflow-hidden">

            <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-800/60 pb-2 shrink-0">

              <AlertOctagon className="w-3.5 h-3.5 text-slate-400" />

              Real-time System Warnings

            </span>

            <div className="flex-1 overflow-y-auto flex flex-col gap-2 pr-1 pt-1 text-[11px]">

              {criticalNodes.length > 0 ? (
                criticalNodes.map((cNode) => (

                  <div
                    key={cNode.id}
                    className="p-2.5 bg-slate-950/60 border border-slate-800/80 rounded-md flex flex-col gap-1 shrink-0"
                  >

                    <div className="flex justify-between font-medium text-slate-300">

                      <span>{cNode.name}</span>

                      <span className="text-amber-400/90 text-[10px]">
                        ELEVATED
                      </span>

                    </div>

                    <p className="text-[10px] text-slate-500">

                      Threshold near depth{" "}
                      {cNode.water_level_m}m. Model tracking closely.

                    </p>

                  </div>

                ))
              ) : (

                <div className="p-3 bg-slate-950/40 border border-slate-800/60 rounded-md text-slate-500 text-[10px] text-center">

                  All active nodes operating within defined safe thresholds.

                </div>

              )}

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}