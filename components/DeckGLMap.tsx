"use client";

import React, { useEffect, useRef, useState } from "react";
import dynamic from "next/dynamic";

const MapContainer = dynamic(
  () => import("react-leaflet").then((mod) => mod.MapContainer),
  { ssr: false }
);

const TileLayer = dynamic(
  () => import("react-leaflet").then((mod) => mod.TileLayer),
  { ssr: false }
);

const Marker = dynamic(
  () => import("react-leaflet").then((mod) => mod.Marker),
  { ssr: false }
);

const Popup = dynamic(
  () => import("react-leaflet").then((mod) => mod.Popup),
  { ssr: false }
);

interface NodeItem {
  id: string;
  name: string;
  lat: number;
  lng: number;
  water_level_m: number;
  risk_score: number;
}

interface TelemetryPayload {
  timestamp: string;
  storm_category?: number;
  nodes: NodeItem[];
}

export default function DeckGLMap({
  telemetry,
}: {
  telemetry: TelemetryPayload | null;
}) {
  const [isMounted, setIsMounted] = useState(false);
  const [leaflet, setLeaflet] = useState<any>(null);
  const mapRef = useRef<any>(null);

  useEffect(() => {
    setIsMounted(true);

    import("leaflet").then((L) => {
      setLeaflet(L);
    });
  }, []);

  useEffect(() => {
    if (!mapRef.current) return;

    const timer = setTimeout(() => {
      mapRef.current.invalidateSize();
    }, 200);

    return () => clearTimeout(timer);
  }, [isMounted]);

  const nodes = telemetry?.nodes ?? [];

  if (!isMounted || !leaflet) {
    return (
      <div className="w-full h-full bg-[#0b0f19] flex items-center justify-center text-xs text-slate-500 font-mono">
        INITIALIZING...
      </div>
    );
  }

  const createCustomIcon = (risk: number) => {
    const color = risk > 60 ? "#fbbf24" : "#10b981";

    return leaflet.divIcon({
      className: "custom-leaflet-marker",
      html: `
        <div
          style="
            background-color: ${color};
            width: 16px;
            height: 16px;
            border-radius: 50%;
            border: 2px solid #0b0f19;
            box-shadow: 0 0 10px ${color};
          "
        ></div>
      `,
      iconSize: [16, 16],
      iconAnchor: [8, 8],
    });
  };

  return (
    <div className="absolute inset-0 w-full h-full bg-[#0b0f19]">
      <style jsx global>{`
        .leaflet-container {
          width: 100% !important;
          height: 100% !important;
          background: #0b0f19 !important;
          position: absolute !important;
          inset: 0 !important;
          z-index: 0;
        }

        .leaflet-tile-pane {
          filter: brightness(0.6) invert(1) contrast(3) hue-rotate(200deg) saturate(0.3) !important;
        }

        .leaflet-control-zoom {
          border: 1px solid #334155 !important;
        }

        .leaflet-control-zoom a {
          background: #0f172a !important;
          color: #cbd5e1 !important;
          border-color: #334155 !important;
        }

        .leaflet-control-zoom a:hover {
          background: #1e293b !important;
        }

        .leaflet-popup-content-wrapper {
          background: #f8fafc;
          color: #0f172a;
          border-radius: 6px;
        }

        .leaflet-popup-tip {
          background: #f8fafc;
        }
      `}</style>

      <MapContainer
        ref={mapRef}
        center={[12.9165, 79.1325]}
        zoom={13}
        scrollWheelZoom={true}
        style={{
          width: "100%",
          height: "100%",
          position: "absolute",
          inset: 0,
        }}
        attributionControl={false}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          maxZoom={19}
        />

        {nodes.map((node) => (
          <Marker
            key={node.id}
            position={[node.lat, node.lng]}
            icon={createCustomIcon(node.risk_score)}
          >
            <Popup>
              <div className="p-1 text-slate-900 font-sans">
                <strong className="block text-xs font-bold">
                  {node.name}
                </strong>

                <span className="text-[10px] text-slate-600">
                  ID: {node.id}
                </span>

                <div className="mt-1 text-[11px]">
                  Depth: <b>{node.water_level_m}m</b> | Risk:{" "}
                  <span
                    className={
                      node.risk_score > 60
                        ? "text-amber-600 font-bold"
                        : "text-emerald-600 font-bold"
                    }
                  >
                    {node.risk_score}%
                  </span>
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}