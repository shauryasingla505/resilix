export interface SensorNode {
  id: string;
  name: string;
  lat: number;
  lng: number;
  water_level_m: number;
  risk_score: number;
}

export function calculateSystemMetrics(nodes: SensorNode[], rainfall: number, drainageCapacity: number) {
  if (!nodes || nodes.length === 0) {
    return { avgRisk: 0, criticalCount: 0, normalCount: 0, systemStatus: 'NOMINAL' };
  }

  const totalRisk = nodes.reduce((acc, node) => acc + node.risk_score, 0);
  const avgRisk = Math.round(totalRisk / nodes.length);
  
  const criticalNodes = nodes.filter((node) => node.risk_score > 60);
  const normalCount = nodes.length - criticalNodes.length;

  let systemStatus = 'NOMINAL';
  if (avgRisk > 60 || criticalNodes.length >= 2) {
    systemStatus = 'CRITICAL OVERFLOW ALERT';
  } else if (avgRisk > 35) {
    systemStatus = 'ELEVATED WATCH';
  }

  return {
    avgRisk,
    criticalCount: criticalNodes.length,
    normalCount,
    systemStatus,
    adjustedFlowEfficiency: Math.max(0, drainageCapacity - rainfall * 0.15)
  };
}