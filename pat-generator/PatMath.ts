import { PatLineDef } from './types';

export class PatMath {
  /**
   * Converts a standard line segment (p1 -> p2) into a repeating PAT line definition.
   * This is a simplified mathematical conversion.
   */
  public static segmentToPatLine(
    x1: number, 
    y1: number, 
    x2: number, 
    y2: number, 
    repeatOffsetX: number, 
    repeatOffsetY: number
  ): PatLineDef {
    
    const dx = x2 - x1;
    const dy = y2 - y1;
    
    // Calculate angle in degrees
    let angle = Math.atan2(dy, dx) * (180 / Math.PI);
    if (angle < 0) angle += 360;

    // Calculate length of the segment
    const length = Math.sqrt(dx * dx + dy * dy);

    // If it's a solid line that repeats perfectly, dash array is empty or length/-gap
    // For now, we return a simple representation
    return {
      angle: parseFloat(angle.toFixed(4)),
      xOrigin: parseFloat(x1.toFixed(4)),
      yOrigin: parseFloat(y1.toFixed(4)),
      deltaX: repeatOffsetX,
      deltaY: repeatOffsetY,
      dashArray: [parseFloat(length.toFixed(4)), -parseFloat(length.toFixed(4))] 
    };
  }
}
