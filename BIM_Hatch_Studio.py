import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math

class HatchStudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BIM Hatch Studio - Advanced Pro Edition")
        self.root.geometry("1400x900")
        
        # Dark Theme Colors
        self.bg_color = "#0f172a"
        self.panel_color = "#1e293b"
        self.text_color = "#f8fafc"
        self.accent_color = "#0ea5e9"
        self.grid_color = "#334155"
        self.line_color = "#38bdf8"
        self.preview_bg = "#0b1120"
        
        self.root.configure(bg=self.bg_color)
        
        # State
        self.lines = [] # list of (x1, y1, x2, y2)
        self.current_shape_id = None
        self.start_x = 0
        self.start_y = 0
        
        self.current_tool = tk.StringVar(value="LINE") # LINE, RECT, CIRCLE
        self.grid_size_mm = tk.IntVar(value=100) # Grid snap in mm
        self.canvas_width_mm = tk.IntVar(value=1000)
        self.canvas_height_mm = tk.IntVar(value=1000)
        
        # 1 pixel = 1 mm for simplicity, but we scale view if needed. Let's assume 1px = 1mm for direct drafting.
        # But to fit a 1000x1000 canvas on screen, we might need a scale factor.
        self.scale = 1.0 
        
        self.pattern_name = tk.StringVar(value="BIM_PATTERN_PRO")
        self.pattern_type = tk.StringVar(value="MODEL")
        
        self.setup_ui()
        self.draw_grid()

    def setup_ui(self):
        # Top Header
        header = tk.Frame(self.root, bg=self.panel_color, height=60)
        header.pack(side=tk.TOP, fill=tk.X)
        
        title = tk.Label(header, text="BIM Hatch Studio [PRO]", fg=self.text_color, bg=self.panel_color, font=("Segoe UI", 16, "bold"))
        title.pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_export = tk.Button(header, text="Export .PAT", bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold"), 
                               relief=tk.FLAT, padx=15, command=self.export_pat)
        btn_export.pack(side=tk.RIGHT, padx=20, pady=15)
        
        btn_clear = tk.Button(header, text="Clear Canvas", bg="#ef4444", fg="white", font=("Segoe UI", 10, "bold"), 
                              relief=tk.FLAT, padx=15, command=self.clear_canvas)
        btn_clear.pack(side=tk.RIGHT, padx=10, pady=15)

        # Main Workspace Split
        workspace = tk.Frame(self.root, bg=self.bg_color)
        workspace.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left Toolbar (Tools)
        toolbar = tk.Frame(workspace, bg=self.panel_color, width=60)
        toolbar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Tool Buttons
        tools = [("Line", "LINE", "╱"), ("Rect", "RECT", "□"), ("Circle", "CIRCLE", "○")]
        for (name, val, icon) in tools:
            btn = tk.Radiobutton(toolbar, text=icon, variable=self.current_tool, value=val,
                                 indicatoron=0, bg=self.panel_color, fg=self.text_color, 
                                 selectcolor=self.accent_color, font=("Segoe UI", 18), width=3, relief=tk.FLAT)
            btn.pack(pady=5, padx=5)

        # Canvas Area
        self.canvas_frame = tk.Frame(workspace, bg=self.panel_color, bd=1, relief=tk.SUNKEN)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.canvas = tk.Canvas(self.canvas_frame, bg=self.bg_color, highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        # Floating Dimension Label
        self.dim_label = tk.Label(self.canvas, text="0,0 mm", bg="#000000", fg="#ffffff", font=("Consolas", 8))
        self.dim_label.place(x=-100, y=-100) # Hide initially
        
        # Right Properties Panel
        sidebar = tk.Frame(workspace, bg=self.panel_color, width=400)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Properties
        prop_label = tk.Label(sidebar, text="Design Properties", fg=self.text_color, bg=self.panel_color, font=("Segoe UI", 12, "bold"))
        prop_label.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Size Controls
        size_frame = tk.Frame(sidebar, bg=self.panel_color)
        size_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(size_frame, text="Canvas Size (mm)", fg="#94a3b8", bg=self.panel_color, font=("Segoe UI", 9)).grid(row=0, column=0, sticky=tk.W, columnspan=3)
        tk.Entry(size_frame, textvariable=self.canvas_width_mm, width=8, bg=self.bg_color, fg=self.text_color, font=("Consolas", 10), insertbackground="white", relief=tk.FLAT).grid(row=1, column=0, pady=5)
        tk.Label(size_frame, text="x", fg="#94a3b8", bg=self.panel_color).grid(row=1, column=1)
        tk.Entry(size_frame, textvariable=self.canvas_height_mm, width=8, bg=self.bg_color, fg=self.text_color, font=("Consolas", 10), insertbackground="white", relief=tk.FLAT).grid(row=1, column=2, pady=5)
        
        tk.Label(size_frame, text="Grid Snap (mm)", fg="#94a3b8", bg=self.panel_color, font=("Segoe UI", 9)).grid(row=2, column=0, sticky=tk.W, columnspan=3, pady=(10,0))
        tk.Entry(size_frame, textvariable=self.grid_size_mm, width=8, bg=self.bg_color, fg=self.text_color, font=("Consolas", 10), insertbackground="white", relief=tk.FLAT).grid(row=3, column=0, pady=5)
        
        # Binding updates
        self.canvas_width_mm.trace_add("write", lambda *args: self.draw_grid())
        self.canvas_height_mm.trace_add("write", lambda *args: self.draw_grid())
        self.grid_size_mm.trace_add("write", lambda *args: self.draw_grid())
        
        tk.Label(sidebar, text="Pattern Name", fg="#94a3b8", bg=self.panel_color, font=("Segoe UI", 9)).pack(anchor=tk.W, padx=15, pady=(10,0))
        name_entry = tk.Entry(sidebar, textvariable=self.pattern_name, bg=self.bg_color, fg=self.text_color, font=("Consolas", 10), insertbackground="white", relief=tk.FLAT)
        name_entry.pack(fill=tk.X, padx=15, pady=(0, 10), ipady=5)
        
        # Seamless Preview Window
        prev_label = tk.Label(sidebar, text="Seamless Preview (3x3 Tiling)", fg=self.text_color, bg=self.panel_color, font=("Segoe UI", 10, "bold"))
        prev_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        self.preview_canvas = tk.Canvas(sidebar, bg=self.preview_bg, height=200, highlightthickness=1, highlightbackground=self.grid_color)
        self.preview_canvas.pack(fill=tk.X, padx=15, pady=5)
        
        # Live PAT Output
        output_label = tk.Label(sidebar, text="Live .PAT Output", fg=self.text_color, bg=self.panel_color, font=("Segoe UI", 10, "bold"))
        output_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        self.text_output = tk.Text(sidebar, bg=self.bg_color, fg="#34d399", font=("Consolas", 9), relief=tk.FLAT, insertbackground="white", wrap=tk.WORD)
        self.text_output.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Trace var to update code when name changes
        self.pattern_name.trace_add("write", lambda *args: self.generate_pat())
        self.pattern_type.trace_add("write", lambda *args: self.generate_pat())
        
        self.generate_pat()

    def get_grid_size(self):
        try:
            return max(10, self.grid_size_mm.get())
        except:
            return 100

    def get_canvas_dims(self):
        try:
            w = max(100, self.canvas_width_mm.get())
            h = max(100, self.canvas_height_mm.get())
            return w, h
        except:
            return 1000, 1000

    def draw_grid(self):
        self.canvas.delete("grid")
        self.canvas.delete("bounds")
        grid = self.get_grid_size()
        cw, ch = self.get_canvas_dims()
        
        # Draw design boundaries
        self.canvas.create_rectangle(0, 0, cw, ch, outline="#475569", width=2, dash=(4,4), tags="bounds")
        
        for i in range(0, cw + 1, grid):
            self.canvas.create_line(i, 0, i, ch, fill=self.grid_color, tags="grid")
        for i in range(0, ch + 1, grid):
            self.canvas.create_line(0, i, cw, i, fill=self.grid_color, tags="grid")
            
        self.canvas.tag_lower("grid")
        self.canvas.tag_lower("bounds")
        self.update_preview()

    def snap(self, val):
        grid = self.get_grid_size()
        return round(val / grid) * grid
        
    def on_mouse_move(self, event):
        x = self.snap(event.x)
        y = self.snap(event.y)
        self.dim_label.config(text=f"{x}mm, {y}mm")
        self.dim_label.place(x=event.x + 15, y=event.y + 15)

    def on_press(self, event):
        self.start_x = self.snap(event.x)
        self.start_y = self.snap(event.y)
        
        tool = self.current_tool.get()
        if tool == "LINE":
            self.current_shape_id = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, fill=self.line_color, width=2, capstyle=tk.ROUND)
        elif tool == "RECT":
            self.current_shape_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline=self.line_color, width=2)
        elif tool == "CIRCLE":
            self.current_shape_id = self.canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y, outline=self.line_color, width=2)

    def on_drag(self, event):
        if self.current_shape_id:
            end_x = self.snap(event.x)
            end_y = self.snap(event.y)
            
            self.dim_label.config(text=f"{end_x}mm, {end_y}mm")
            self.dim_label.place(x=event.x + 15, y=event.y + 15)
            
            tool = self.current_tool.get()
            if tool == "LINE" or tool == "RECT":
                self.canvas.coords(self.current_shape_id, self.start_x, self.start_y, end_x, end_y)
            elif tool == "CIRCLE":
                r = math.hypot(end_x - self.start_x, end_y - self.start_y)
                self.canvas.coords(self.current_shape_id, self.start_x - r, self.start_y - r, self.start_x + r, self.start_y + r)

    def on_release(self, event):
        if self.current_shape_id:
            end_x = self.snap(event.x)
            end_y = self.snap(event.y)
            tool = self.current_tool.get()
            
            if self.start_x != end_x or self.start_y != end_y:
                if tool == "LINE":
                    self.lines.append((self.start_x, self.start_y, end_x, end_y))
                elif tool == "RECT":
                    self.lines.append((self.start_x, self.start_y, end_x, self.start_y))
                    self.lines.append((end_x, self.start_y, end_x, end_y))
                    self.lines.append((end_x, end_y, self.start_x, end_y))
                    self.lines.append((self.start_x, end_y, self.start_x, self.start_y))
                elif tool == "CIRCLE":
                    r = math.hypot(end_x - self.start_x, end_y - self.start_y)
                    # Convert circle to 16 line segments for .PAT
                    segments = 16
                    pts = []
                    for i in range(segments + 1):
                        ang = 2 * math.pi * i / segments
                        px = self.start_x + r * math.cos(ang)
                        py = self.start_y + r * math.sin(ang)
                        pts.append((px, py))
                    for i in range(segments):
                        self.lines.append((pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1]))
            else:
                self.canvas.delete(self.current_shape_id)
            
            self.current_shape_id = None
            self.redraw_all()
            self.generate_pat()

    def redraw_all(self):
        self.canvas.delete("all")
        self.draw_grid()
        for (x1, y1, x2, y2) in self.lines:
            self.canvas.create_line(x1, y1, x2, y2, fill=self.line_color, width=2, capstyle=tk.ROUND)

    def update_preview(self):
        self.preview_canvas.delete("all")
        cw, ch = self.get_canvas_dims()
        if cw == 0 or ch == 0: return
        
        # Scale preview to fit in 350x200 window
        prev_w = 350
        prev_h = 200
        
        # We tile 3x3, so total size is 3*cw by 3*ch
        scale_x = prev_w / (cw * 3)
        scale_y = prev_h / (ch * 3)
        scale = min(scale_x, scale_y) * 0.9 # 90% to leave margin
        
        offset_x = (prev_w - (cw * 3 * scale)) / 2
        offset_y = (prev_h - (ch * 3 * scale)) / 2
        
        # Draw 3x3 tiles
        for row in range(3):
            for col in range(3):
                tx = offset_x + col * cw * scale
                ty = offset_y + row * ch * scale
                
                # Tile bounds
                self.preview_canvas.create_rectangle(tx, ty, tx + cw * scale, ty + ch * scale, outline="#1e293b", dash=(2,2))
                
                # Draw lines
                for (x1, y1, x2, y2) in self.lines:
                    self.preview_canvas.create_line(
                        tx + x1 * scale, ty + y1 * scale, 
                        tx + x2 * scale, ty + y2 * scale, 
                        fill="#38bdf8", width=1
                    )

    def clear_canvas(self):
        self.lines.clear()
        self.redraw_all()
        self.generate_pat()

    def generate_pat(self):
        code = f"*{self.pattern_name.get()}, Generated by BIM Hatch Studio PRO\n"
        code += f";%TYPE={self.pattern_type.get()}\n"
        
        cw, ch = self.get_canvas_dims()
        
        for (x1, y1, x2, y2) in self.lines:
            dx = x2 - x1
            dy = y2 - y1
            
            if dx == 0 and dy == 0: continue
            
            # Calculate angle
            angle = math.degrees(math.atan2(-dy, dx)) # Tkinter Y is inverted relative to standard cartesian
            if angle < 0:
                angle += 360
                
            length = math.sqrt(dx**2 + dy**2)
            
            # Formatting as required by PAT specifications: angle, x, y, deltax, deltay, dash1, dash2
            # Here we provide repeating offsets based on canvas width/height to make it seamless
            repeat_x = cw if dx == 0 else 0
            repeat_y = ch if dy == 0 else 0
            
            # Very basic repeating representation. True seamless math requires complex projection
            code += f"{angle:.2f}, {x1:.2f},{-y1:.2f}, {repeat_x:.2f},{repeat_y:.2f}, {length:.2f},-{length:.2f}\n"
            
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, code)
        self.update_preview()

    def export_pat(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pat",
            initialfile=f"{self.pattern_name.get()}.pat",
            filetypes=[("AutoCAD/Revit Pattern", "*.pat"), ("All Files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'w') as f:
                    f.write(self.text_output.get("1.0", tk.END).strip())
                messagebox.showinfo("Success", f"Pattern successfully exported to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HatchStudioApp(root)
    root.mainloop()
