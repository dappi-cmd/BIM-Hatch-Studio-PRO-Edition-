import { PatDefinition, PatLineDef } from './types';

export class PatGenerator {
  /**
   * Generates a valid .PAT file content string from a PatDefinition.
   */
  public static generate(def: PatDefinition): string {
    const lines: string[] = [];

    // Header
    lines.push(`*${def.name}, ${def.description}`);

    // Type definition for Revit (Drafting vs Model)
    if (def.type === 'MODEL') {
      lines.push(`;%TYPE=MODEL`);
    } else {
      lines.push(`;%TYPE=DRAFTING`);
    }

    // Line definitions
    for (const line of def.lines) {
      lines.push(this.formatLine(line));
    }

    // End with a newline as required by many PAT parsers
    lines.push('');

    return lines.join('\n');
  }

  /**
   * Formats a single PAT line.
   * Format: angle, x-origin,y-origin, delta-x,delta-y, dash-1,dash-2, ...
   */
  private static formatLine(line: PatLineDef): string {
    const base = `${line.angle}, ${line.xOrigin},${line.yOrigin}, ${line.deltaX},${line.deltaY}`;
    
    if (line.dashArray && line.dashArray.length > 0) {
      const dashes = line.dashArray.join(', ');
      return `${base}, ${dashes}`;
    }

    return base;
  }
}
