import sys
import time
import numpy as np
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, 
    QWidget, QSpinBox, QPushButton, QGroupBox, QDoubleSlider
)

# ==========================================
# 50 FRACTAL VARIATIONS
# ==========================================
def v0_linear(x, y, r2, r, a): return x, y
def v1_sinusoidal(x, y, r2, r, a): return np.sin(x), np.sin(y)
def v2_spherical(x, y, r2, r, a): return x/(r2+1e-6), y/(r2+1e-6)
def v3_swirl(x, y, r2, r, a): return x*np.sin(r2) - y*np.cos(r2), x*np.cos(r2) + y*np.sin(r2)
def v4_horseshoe(x, y, r2, r, a): return (x-y)*(x+y)/(r+1e-6), 2*x*y/(r+1e-6)
def v5_polar(x, y, r2, r, a): return a/np.pi, r - 1.0
def v6_handkerchief(x, y, r2, r, a): return np.sin(a+r)*r, np.cos(a-r)*r
def v7_heart(x, y, r2, r, a): return np.sin(r*x)*r, -np.cos(r*y)*r
def v8_disc(x, y, r2, r, a): return np.sin(r*np.pi)*y/np.pi, np.cos(r*np.pi)*x/np.pi
def v9_spiral(x, y, r2, r, a): return (np.cos(r) + np.sin(r)/r)*x/r, (np.sin(r) - np.cos(r)/r)*y/r
def v10_hyperbolic(x, y, r2, r, a): return np.sin(a)/r, np.cos(a)*r
def v11_diamond(x, y, r2, r, a): return np.sin(a)*np.cos(r), np.cos(a)*np.sin(r)
def v12_ex(x, y, r2, r, a): return r*np.cos(a*x*x), r*np.sin(a*x*x)
def v13_julia(x, y, r2, r, a): return np.sqrt(r)*np.cos(a/2 + np.pi/2), np.sqrt(r)*np.sin(a/2 + np.pi/2)
def v14_waves(x, y, r2, r, a): return x + np.sin(y), y + np.sin(x)
def v15_fisheye(x, y, r2, r, a): return 2/(r+1)*y, 2/(r+1)*x
def v16_popcorn(x, y, r2, r, a): return x + np.sin(np.sin(3*y)), y + np.sin(np.sin(3*x))
def v17_exponential(x, y, r2, r, a): return np.exp(x-1)*np.cos(np.pi*y), np.exp(x-1)*np.sin(np.pi*y)
def v18_power(x, y, r2, r, a): return np.cos(a)*r**np.sin(a), np.sin(a)*r**np.sin(a)
def v19_cosine(x, y, r2, r, a): return np.cos(np.pi*x)*np.cosh(y), -np.sin(np.pi*x)*np.sinh(y)
def v20_rings(x, y, r2, r, a): return (r - 2*np.sin(r*np.pi)) * np.cos(a), (r - 2*np.sin(r*np.pi)) * np.sin(a)
def v21_fan(x, y, r2, r, a): return np.sin(a+np.pi) * r, np.cos(a-np.pi) * r
def v22_eyefish(x, y, r2, r, a): return 2/(r+1)*x, 2/(r+1)*y
def v23_bubble(x, y, r2, r, a): return 4 / (r2 + 4) * x, 4 / (r2 + 4) * y
def v24_cylinder(x, y, r2, r, a): return np.sin(x), y
def v25_tangent(x, y, r2, r, a): return np.sin(x)/np.cos(y), np.tan(y)
def v26_square(x, y, r2, r, a): return np.sin(x) - np.cos(y), np.sin(y) - np.cos(x)
def v27_cross(x, y, r2, r, a): return np.sqrt(1/(x*x*y*y+1e-6)) * x, np.sqrt(1/(x*x*y*y+1e-6)) * y
def v28_gaussian(x, y, r2, r, a): return np.random.normal(size=x.shape)*x, np.random.normal(size=y.shape)*y
def v29_rays(x, y, r2, r, a): return np.tan(a)/(r+1e-6), np.tan(a)
def v30_blade(x, y, r2, r, a): return x * (np.cos(a+r) + np.sin(a-r)), x * (np.cos(a-r) - np.sin(a+r))
def v31_secant(x, y, r2, r, a): return 1/np.cos(x), 1/np.sin(y)
def v32_twintrian(x, y, r2, r, a): return np.sin(a)*x + np.cos(a)*y, np.cos(a)*x - np.sin(a)*y
def v33_auger(x, y, r2, r, a): return x + np.sin(y) - np.cos(x), y + np.sin(x) - np.cos(y)
def v34_flower(x, y, r2, r, a): return np.sin(r) * np.cos(a), np.sin(r) * np.sin(a)
def v35_conic(x, y, r2, r, a): return r * (1 - 0.5*np.cos(2*a)) * np.cos(a), r * (1 - 0.5*np.cos(2*a)) * np.sin(a)
def v36_parabola(x, y, r2, r, a): return np.sin(y*y)/np.sin(x+1e-6), np.sin(x*x)/np.cos(y+1e-6)
def v37_bent(x, y, r2, r, a): return np.where(x>=0, x, 2*x), np.where(y>=0, y, y/2)
def v38_wedge(x, y, r2, r, a): return x + np.sin(a)*r, y + np.cos(a)*r
def v39_scry(x, y, r2, r, a): return x/(r2*r+1e-6), y/(r2*r+1e-6)
def v40_elliptic(x, y, r2, r, a): return np.sin(a) * np.cosh(r), np.cos(a) * np.sinh(r)
def v41_bipolar(x, y, r2, r, a): return np.arctan2(y, x-1), np.arctan2(y, x+1)
def v42_butterfly(x, y, r2, r, a): return np.sin(x*y) * x, np.sin(x*y) * y
def v43_cell(x, y, r2, r, a): return np.mod(x, 2)-1, np.mod(y, 2)-1
def v44_cpow(x, y, r2, r, a): return np.cos(a/2)*r**0.5, np.sin(a/2)*r**0.5
def v45_lazysusan(x, y, r2, r, a): return x*np.cos(r) + y*np.sin(r), y*np.cos(r) - x*np.sin(r)
def v46_board(x, y, r2, r, a): return np.floor(x), np.floor(y)
def v47_felix(x, y, r2, r, a): return np.sin(x*y), np.cos(x*y)
def v48_post_mirror(x, y, r2, r, a): return -x, y
def v49_circleblur(x, y, r2, r, a): return r*x, r*y

VARIATIONS = [
    v0_linear, v1_sinusoidal, v2_spherical, v3_swirl, v4_horseshoe, v5_polar, v6_handkerchief, 
    v7_heart, v8_disc, v9_spiral, v10_hyperbolic, v11_diamond, v12_ex, v13_julia, v14_waves, 
    v15_fisheye, v16_popcorn, v17_exponential, v18_power, v19_cosine, v20_rings, v21_fan, 
    v22_eyefish, v23_bubble, v24_cylinder, v25_tangent, v26_square, v27_cross, v28_gaussian, 
    v29_rays, v30_blade, v31_secant, v32_twintrian, v33_auger, v34_flower, v35_conic, 
    v36_parabola, v37_bent, v38_wedge, v39_scry, v40_elliptic, v41_bipolar, v42_butterfly, 
    v43_cell, v44_cpow, v45_lazysusan, v46_board, v47_felix, v48_post_mirror, v49_circleblur
]

# Helper to generate random multi-harmonic procedural parameters
def make_harmonics():
    return {
        'a1': np.random.uniform(0.2, 0.8), 'w1': np.random.uniform(0.2, 1.5), 'p1': np.random.uniform(0, np.pi),
        'a2': np.random.uniform(0.1, 0.4), 'w2': np.random.uniform(1.5, 3.5), 'p2': np.random.uniform(0, np.pi)
    }

def eval_harmonics(t, h):
    # Creates complex, evolving Lissajous-like curves
    return h['a1'] * np.sin(t * h['w1'] + h['p1']) + h['a2'] * np.cos(t * h['w2'] + h['p2'])


# ==========================================
# FRACTAL GENERATOR THREAD
# ==========================================
class FlameFractalGenerator(QThread):
    image_ready = Signal(QImage)

    def __init__(self, width=600, height=600, parent=None):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.running = True
        self.t = 0.0
        
        self.total_iterations = 30_000_000
        self.num_transforms = 4
        self.morph_speed = 1.0
        self.color_speed = 1.0
        
        self.pending_iters = self.total_iterations
        self.pending_transforms = self.num_transforms
        self.pending_morph = self.morph_speed
        self.pending_color = self.color_speed
        self.needs_update = True
        
        self.transforms = []

    def update_settings(self, total_iters, num_transforms, morph_speed, color_speed):
        self.pending_iters = total_iters
        self.pending_transforms = num_transforms
        self.pending_morph = morph_speed
        self.pending_color = color_speed
        self.needs_update = True

    def randomize_transforms(self):
        self.transforms = []
        for _ in range(self.num_transforms):
            # Procedurally blend between TWO variations over time
            var1 = np.random.randint(0, len(VARIATIONS))
            var2 = np.random.randint(0, len(VARIATIONS))
            
            params = {
                'var1': var1, 'var2': var2,
                'var_blend_speed': np.random.uniform(0.1, 0.8),
                'var_blend_phase': np.random.uniform(0, np.pi),
                
                # Procedural multi-harmonic animations for affine matrices
                'ax_h': make_harmonics(), 'bx_h': make_harmonics(), 'cx_h': make_harmonics(),
                'dy_h': make_harmonics(), 'ey_h': make_harmonics(), 'fy_h': make_harmonics(),
                
                # Procedural color animation parameters (HSV)
                'col_hue': np.random.uniform(0, 1.0),
                'col_hue_speed': np.random.uniform(-0.2, 0.2),
                'col_sat': np.random.uniform(0.7, 1.0),
                'col_val': np.random.uniform(0.8, 1.0)
            }
            self.transforms.append(params)

    def run(self):
        while self.running:
            if self.needs_update:
                self.total_iterations = self.pending_iters
                self.num_transforms = self.pending_transforms
                self.morph_speed = self.pending_morph
                self.color_speed = self.pending_color
                self.steps = max(20, self.total_iterations // 1_000_000)
                self.batch_size = self.total_iterations // self.steps
                self.randomize_transforms()
                self.needs_update = False
            
            start_time = time.time()
            
            hist_r, hist_g, hist_b = self.generate_frame(self.t)
            img_data = self.apply_colormap(hist_r, hist_g, hist_b)
            
            h, w, _ = img_data.shape
            img_data = np.ascontiguousarray(img_data)
            qimg = QImage(img_data.data, w, h, 3 * w, QImage.Format_RGB888)
            
            self.image_ready.emit(qimg.copy())
            
            self.t += 0.05 * self.morph_speed
            
            elapsed = time.time() - start_time
            sleep_time = max(0, 0.033 - elapsed)
            self.msleep(int(sleep_time * 1000))

    def generate_frame(self, t):
        x = np.random.uniform(-1, 1, self.batch_size)
        y = np.random.uniform(-1, 1, self.batch_size)
        
        # Color accumulation buffers per point
        col_r = np.zeros(self.batch_size)
        col_g = np.zeros(self.batch_size)
        col_b = np.zeros(self.batch_size)
        
        for step in range(self.steps):
            choices = np.random.randint(0, self.num_transforms, self.batch_size)
            new_x = np.copy(x)
            new_y = np.copy(y)
            new_r, new_g, new_b = np.copy(col_r), np.copy(col_g), np.copy(col_b)
            
            for i, tr in enumerate(self.transforms):
                mask = (choices == i)
                if not np.any(mask): continue
                
                sub_x = np.clip(x[mask], -10, 10)
                sub_y = np.clip(y[mask], -10, 10)
                
                r2 = sub_x*sub_x + sub_y*sub_y + 1e-6
                r = np.sqrt(r2)
                a = np.arctan2(sub_y, sub_x)
                
                # 1. Calculate Animated Affine Matrix using multi-harmonic functions
                ax = 0.5 + eval_harmonics(t, tr['ax_h'])
                bx = eval_harmonics(t, tr['bx_h'])
                cx = eval_harmonics(t, tr['cx_h']) * 1.5
                
                dy = eval_harmonics(t, tr['dy_h'])
                ey = 0.5 + eval_harmonics(t, tr['ey_h'])
                fy = eval_harmonics(t, tr['fy_h']) * 1.5
                
                aff_x = ax * sub_x + bx * sub_y + cx
                aff_y = dy * sub_x + ey * sub_y + fy
                
                # 2. Procedurally blend variations
                blend = 0.5 + 0.5 * np.sin(t * tr['var_blend_speed'] + tr['var_blend_phase'])
                
                v1_func = VARIATIONS[tr['var1']]
                v2_func = VARIATIONS[tr['var2']]
                
                vx1, vy1 = v1_func(aff_x, aff_y, r2, r, a)
                vx2, vy2 = v2_func(aff_x, aff_y, r2, r, a)
                
                vx = vx1 * blend + vx2 * (1.0 - blend)
                vy = vy1 * blend + vy2 * (1.0 - blend)
                
                new_x[mask] = vx * 0.5
                new_y[mask] = vy * 0.5
                
                # 3. Procedural Color Animation (HSV to RGB)
                hue = (tr['col_hue'] + t * tr['col_hue_speed'] * self.color_speed) % 1.0
                rgb = self.hsv_to_rgb(hue, tr['col_sat'], tr['col_val'])
                
                # Smoothly lerp point colors towards the transform's current color
                new_r[mask] = col_r[mask] * 0.6 + rgb[0] * 0.4
                new_g[mask] = col_g[mask] * 0.6 + rgb[1] * 0.4
                new_b[mask] = col_b[mask] * 0.6 + rgb[2] * 0.4
                
            x, y = new_x, new_y
            col_r, col_g, col_b = new_r, new_g, new_b
            
        # Weighted histograms for smooth color blending
        hist_r, _, _ = np.histogram2d(x, y, bins=[self.width, self.height], range=[[-2, 2], [-2, 2]], weights=col_r)
        hist_g, _, _ = np.histogram2d(x, y, bins=[self.width, self.height], range=[[-2, 2], [-2, 2]], weights=col_g)
        hist_b, _, _ = np.histogram2d(x, y, bins=[self.width, self.height], range=[[-2, 2], [-2, 2]], weights=col_b)
        
        return hist_r.T, hist_g.T, hist_b.T

    def hsv_to_rgb(self, h, s, v):
        # Vectorized HSV to RGB conversion
        i = np.floor(h * 6).astype(int)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        i = i % 6
        r = np.choose(i, [v, q, p, p, t, v])
        g = np.choose(i, [t, v, v, q, p, p])
        b = np.choose(i, [p, p, t, v, v, q])
        return r, g, b

    def apply_colormap(self, hist_r, hist_g, hist_b):
        # Logarithmic tone mapping per channel
        log_r = np.log1p(np.abs(hist_r))
        log_g = np.log1p(np.abs(hist_g))
        log_b = np.log1p(np.abs(hist_b))
        
        max_val = max(log_r.max(), log_g.max(), log_b.max())
        if max_val > 0:
            norm_r = (log_r / max_val * 255).astype(np.uint8)
            norm_g = (log_g / max_val * 255).astype(np.uint8)
            norm_b = (log_b / max_val * 255).astype(np.uint8)
        else:
            norm_r = norm_g = norm_b = np.zeros_like(hist_r, dtype=np.uint8)
            
        img_data = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        img_data[..., 0] = norm_r
        img_data[..., 1] = norm_g
        img_data[..., 2] = norm_b
        
        # Apply a slight gamma curve to brighten mid-tones
        img_data = np.clip(img_data * 1.2, 0, 255).astype(np.uint8)
        return img_data

    def stop(self):
        self.running = False


# ==========================================
# CUSTOM SLIDER FOR FLOATS
# ==========================================
class QDoubleSlider(QWidget):
    def __init__(self, min_val, max_val, init_val, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        from PySide6.QtWidgets import QSlider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)
        self.min_val = min_val
        self.max_val = max_val
        
        self.label = QLabel(f"{init_val:.2f}")
        self.label.setFixedWidth(30)
        
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.label)
        
        self.set_value(init_val)
        self.slider.valueChanged.connect(self.on_change)

    def on_change(self, val):
        val_f = self.min_val + (val / 1000.0) * (self.max_val - self.min_val)
        self.label.setText(f"{val_f:.2f}")
        
    def set_value(self, val):
        val_int = int((val - self.min_val) / (self.max_val - self.min_val) * 1000)
        self.slider.setValue(val_int)
        
    def value(self):
        val_f = self.min_val + (self.slider.value() / 1000.0) * (self.max_val - self.min_val)
        return val_f


# ==========================================
# MAIN APPLICATION WINDOW
# ==========================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Procedural Flame Fractal - 50 Variations & Animation")
        self.resize(1000, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # --- Left Sidebar ---
        sidebar = QVBoxLayout()
        sidebar.setAlignment(Qt.AlignTop)
        
        # Settings Group
        settings_group = QGroupBox("Fractal Settings")
        settings_layout = QVBoxLayout()
        
        settings_layout.addWidget(QLabel("Total Iterations:"))
        self.iterations_spin = QSpinBox()
        self.iterations_spin.setRange(1_000_000, 100_000_000)
        self.iterations_spin.setSingleStep(1_000_000)
        self.iterations_spin.setValue(30_000_000)
        self.iterations_spin.setSuffix(" pts")
        settings_layout.addWidget(self.iterations_spin)
        
        settings_layout.addWidget(QLabel("Number of Transforms:"))
        self.transforms_spin = QSpinBox()
        self.transforms_spin.setRange(2, 12)
        self.transforms_spin.setValue(4)
        settings_layout.addWidget(self.transforms_spin)
        
        settings_layout.addWidget(QLabel("Morph Speed:"))
        self.morph_slider = QDoubleSlider(0.0, 3.0, 1.0)
        settings_layout.addWidget(self.morph_slider)
        
        settings_layout.addWidget(QLabel("Color Shift Speed:"))
        self.color_slider = QDoubleSlider(0.0, 3.0, 1.0)
        settings_layout.addWidget(self.color_slider)
        
        self.apply_btn = QPushButton("Apply & Regenerate Procedural Paths")
        self.apply_btn.clicked.connect(self.apply_settings)
        settings_layout.addWidget(self.apply_btn)
        
        settings_group.setLayout(settings_layout)
        sidebar.addWidget(settings_group)
        
        info_group = QGroupBox("Status")
        info_layout = QVBoxLayout()
        self.info_label = QLabel("Variations: 50\nProcedural Animation: Active")
        self.info_label.setStyleSheet("color: #888;")
        info_layout.addWidget(self.info_label)
        info_group.setLayout(info_layout)
        sidebar.addWidget(info_group)
        
        # --- Right Display Area ---
        self.display_label = QLabel()
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setStyleSheet("background-color: black;")
        self.display_label.setMinimumSize(700, 700)
        
        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.display_label, 4)
        
        # Setup and start the background generator thread
        self.generator = FlameFractalGenerator(width=700, height=700)
        self.generator.image_ready.connect(self.update_image)
        self.apply_settings()
        self.generator.start()

    def apply_settings(self):
        iters = self.iterations_spin.value()
        transforms = self.transforms_spin.value()
        morph = self.morph_slider.value()
        color = self.color_slider.value()
        
        self.generator.update_settings(iters, transforms, morph, color)
        self.info_label.setText(f"Variations: 50\nTransforms: {transforms}\nMorph: {morph:.2f}x\nColor: {color:.2f}x")

    def update_image(self, qimg):
        pixmap = QPixmap.fromImage(qimg)
        self.display_label.setPixmap(pixmap.scaled(
            self.display_label.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        ))

    def closeEvent(self, event):
        self.generator.stop()
        self.generator.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow { background-color: #1e1e1e; }
        QGroupBox { 
            color: #ddd; 
            border: 1px solid #444; 
            border-radius: 4px; 
            margin-top: 10px; 
            padding-top: 15px; 
        }
        QGroupBox::title { 
            subcontrol-origin: margin; 
            left: 10px; 
            padding: 0 3px; 
        }
        QLabel { color: #aaa; }
        QSpinBox, QPushButton { 
            background-color: #2a2a2a; 
            color: #fff; 
            border: 1px solid #555; 
            padding: 4px; 
            border-radius: 3px; 
        }
        QPushButton:hover { background-color: #3a3a3a; border: 1px solid #888; }
        QSlider::groove:horizontal { border: 1px solid #555; height: 4px; background: #2a2a2a; }
        QSlider::handle:horizontal { background: #00aaff; width: 10px; margin: -4px 0; border-radius: 5px; }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())