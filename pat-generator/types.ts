export type PatPatternType = 'MODEL' | 'DRAFTING';

export interface PatLineDef {
  angle: number;
  xOrigin: number;
  yOrigin: number;
  deltaX: number;
  deltaY: number;
  dashArray: number[]; // e.g., [100, -100] for 100 on, 100 off. Empty array means solid line.
}

export interface PatDefinition {
  name: string;
  description: string;
  type: PatPatternType;
  lines: PatLineDef[];
}
