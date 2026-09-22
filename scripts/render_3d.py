#!/usr/bin/env python3
"""Software 3D renderer → jaw-dropping looping GIFs for the GitHub profile.

Pure numpy z-buffer rasterization + Pillow post-processing:
perspective camera, Blinn-Phong, bloom, starfield, voxel 3D text.
No SVG.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config/profile.json").read_text(encoding="utf-8"))
OUT = ROOT / "assets/generated"

FONT_BOLD = Path("C:/Windows/Fonts/segoeuib.ttf")
FONT_MONO = Path("C:/Windows/Fonts/consolab.ttf")


def normalize(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return v / np.maximum(n, 1e-9)


def _as44(m3: np.ndarray) -> np.ndarray:
    out = np.eye(4, dtype=np.float64)
    out[:3, :3] = m3
    return out


def rotation_x(a: float) -> np.ndarray:
    c, s = math.cos(a), math.sin(a)
    return _as44(np.array([[1, 0, 0], [0, c, -s], [0, s, c]], dtype=np.float64))


def rotation_y(a: float) -> np.ndarray:
    c, s = math.cos(a), math.sin(a)
    return _as44(np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], dtype=np.float64))


def rotation_z(a: float) -> np.ndarray:
    c, s = math.cos(a), math.sin(a)
    return _as44(np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=np.float64))


def scale3(s: float) -> np.ndarray:
    out = np.eye(4, dtype=np.float64)
    out[0, 0] = out[1, 1] = out[2, 2] = float(s)
    return out


def translation(t) -> np.ndarray:
    out = np.eye(4, dtype=np.float64)
    out[:3, 3] = np.asarray(t, dtype=np.float64)
    return out


def apply_transform(v: np.ndarray, m: np.ndarray) -> np.ndarray:
    if m.shape == (4, 4):
        ones = np.ones((len(v), 1), dtype=np.float64)
        hv = np.hstack([v, ones])
        return (hv @ m.T)[:, :3]
    if m.shape == (3, 4):
        return v @ m[:, :3].T + m[:, 3]
    return v @ m.T


def look_at(eye: np.ndarray, target: np.ndarray, up: np.ndarray):
    """World → view. Camera at eye looking at target (OpenGL: view forward -Z)."""
    f = normalize(target - eye)
    r = normalize(np.cross(f, up))
    u = np.cross(r, f)
    rot = np.stack([r, u, -f], axis=0)
    return rot, eye.astype(np.float64)


def face_normals(verts: np.ndarray, faces: np.ndarray) -> np.ndarray:
    v0, v1, v2 = verts[faces[:, 0]], verts[faces[:, 1]], verts[faces[:, 2]]
    return normalize(np.cross(v1 - v0, v2 - v0))


# ---------------------------------------------------------------------------
# Meshes
# ---------------------------------------------------------------------------


def box(size=(1.0, 1.0, 1.0)):
    sx, sy, sz = size
    hx, hy, hz = sx / 2, sy / 2, sz / 2
    v = np.array(
        [
            [-hx, -hy, -hz],
            [hx, -hy, -hz],
            [hx, hy, -hz],
            [-hx, hy, -hz],
            [-hx, -hy, hz],
            [hx, -hy, hz],
            [hx, hy, hz],
            [-hx, hy, hz],
        ],
        dtype=np.float64,
    )
    f = np.array(
        [
            [0, 2, 1],
            [0, 3, 2],
            [4, 5, 6],
            [4, 6, 7],
            [0, 1, 5],
            [0, 5, 4],
            [2, 3, 7],
            [2, 7, 6],
            [1, 2, 6],
            [1, 6, 5],
            [3, 0, 4],
            [3, 4, 7],
        ],
        dtype=np.int32,
    )
    return v, f


def torus(r_major=1.0, r_minor=0.28, seg_u=40, seg_v=14):
    verts = []
    for i in range(seg_u):
        u = 2 * math.pi * i / seg_u
        cu, su = math.cos(u), math.sin(u)
        for j in range(seg_v):
            v = 2 * math.pi * j / seg_v
            cv, sv = math.cos(v), math.sin(v)
            verts.append(((r_major + r_minor * cv) * cu, r_minor * sv, (r_major + r_minor * cv) * su))
    verts = np.array(verts, dtype=np.float64)
    faces = []
    for i in range(seg_u):
        for j in range(seg_v):
            a = i * seg_v + j
            b = i * seg_v + (j + 1) % seg_v
            c = ((i + 1) % seg_u) * seg_v + (j + 1) % seg_v
            d = ((i + 1) % seg_u) * seg_v + j
            faces.append([a, c, b])
            faces.append([a, d, c])
    return verts, np.array(faces, dtype=np.int32)


def icosphere(subdiv: int = 1, radius: float = 1.0):
    t = (1 + math.sqrt(5)) / 2
    raw = [
        (-1, t, 0),
        (1, t, 0),
        (-1, -t, 0),
        (1, -t, 0),
        (0, -1, t),
        (0, 1, t),
        (0, -1, -t),
        (0, 1, -t),
        (t, 0, -1),
        (t, 0, 1),
        (-t, 0, -1),
        (-t, 0, 1),
    ]
    faces = [
        [0, 5, 11],
        [0, 1, 5],
        [0, 7, 1],
        [0, 10, 7],
        [0, 11, 10],
        [1, 9, 5],
        [5, 4, 11],
        [11, 2, 10],
        [10, 6, 7],
        [7, 8, 1],
        [3, 4, 9],
        [3, 2, 4],
        [3, 6, 2],
        [3, 8, 6],
        [3, 9, 8],
        [4, 5, 9],
        [2, 11, 4],
        [6, 10, 2],
        [8, 7, 6],
        [9, 1, 8],
    ]
    verts = [normalize(np.array(v, dtype=np.float64)) for v in raw]
    for _ in range(subdiv):
        cache: dict[tuple[int, int], int] = {}
        new_faces = []
        new_verts = list(verts)

        def mid(i: int, j: int) -> int:
            key = (i, j) if i < j else (j, i)
            if key in cache:
                return cache[key]
            p = normalize(np.asarray(verts[i]) + np.asarray(verts[j]))
            new_verts.append(p)
            cache[key] = len(new_verts) - 1
            return cache[key]

        for a, b, c in faces:
            ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
            new_faces += [[a, ab, ca], [b, bc, ab], [c, ca, bc], [ab, bc, ca]]
        verts, faces = new_verts, new_faces
    return np.array(verts, dtype=np.float64) * radius, np.array(faces, dtype=np.int32)


def tube(p0, p1, r=0.06, segments=10):
    p0 = np.array(p0, dtype=np.float64)
    p1 = np.array(p1, dtype=np.float64)
    axis = p1 - p0
    length = float(np.linalg.norm(axis))
    if length < 1e-9:
        return box((r * 2, r * 2, r * 2))
    axis_n = axis / length
    tmp = np.array([0.0, 1.0, 0.0])
    if abs(float(np.dot(tmp, axis_n))) > 0.9:
        tmp = np.array([1.0, 0.0, 0.0])
    n1 = normalize(np.cross(axis_n, tmp))
    n2 = np.cross(axis_n, n1)
    verts = []
    for i in range(segments):
        a = 2 * math.pi * i / segments
        off = math.cos(a) * n1 + math.sin(a) * n2
        verts.append(p0 + off * r)
        verts.append(p1 + off * r)
    verts = np.array(verts, dtype=np.float64)
    faces = []
    for i in range(segments):
        j = (i + 1) % segments
        a0, a1, b0, b1 = 2 * i, 2 * i + 1, 2 * j, 2 * j + 1
        faces.append([a0, b1, b0])
        faces.append([a0, a1, b1])
    return verts, np.array(faces, dtype=np.int32)


def voxel_text_mask(text: str, font_path: Path, px_per_voxel: int = 7, max_width: int = 780):
    font = ImageFont.truetype(str(font_path), 72)
    tmp = Image.new("L", (2400, 220), 0)
    ImageDraw.Draw(tmp).text((30, 50), text, fill=255, font=font)
    bbox = tmp.getbbox()
    if not bbox:
        return np.zeros((1, 1), dtype=bool)
    crop = tmp.crop(bbox)
    w = min(crop.width, max_width)
    h = max(8, int(crop.height * w / max(crop.width, 1)))
    small = crop.resize((max(8, w // px_per_voxel), max(3, h // px_per_voxel)), Image.Resampling.BILINEAR)
    return np.array(small, dtype=np.uint8) > 110


def voxels_to_mesh(mask: np.ndarray, voxel: float = 1.0, depth_layers: int = 3):
    rows, cols = mask.shape
    if rows == 0 or cols == 0:
        return np.zeros((0, 3)), np.zeros((0, 3), dtype=np.int32)
    verts: list[list[float]] = []
    faces: list[list[int]] = []
    index: dict[tuple[int, int, int, str], int] = {}

    def vid(x: int, y: int, z: int, corner: str) -> int:
        key = (x, y, z, corner)
        if key not in index:
            index[key] = len(verts)
            verts.append([x * voxel, y * voxel, z * voxel])
        return index[key]

    dz = int(depth_layers)

    def quad(a, b, c, d):
        faces.append([a, b, c])
        faces.append([a, c, d])

    solid = mask
    for y in range(rows):
        for x in range(cols):
            if not solid[y, x]:
                continue
            x0, x1 = x, x + 1
            y0, y1 = rows - y - 1, rows - y
            z0, z1 = 0, dz
            # front (+z) facing +z — CCW when viewed from +z
            quad(vid(x0, y0, z1, "a"), vid(x1, y0, z1, "b"), vid(x1, y1, z1, "c"), vid(x0, y1, z1, "d"))
            # back
            quad(vid(x0, y0, z0, "a"), vid(x0, y1, z0, "d"), vid(x1, y1, z0, "c"), vid(x1, y0, z0, "b"))
            if y == 0 or not solid[y - 1, x]:
                quad(vid(x0, y1, z0, "d"), vid(x1, y1, z0, "c"), vid(x1, y1, z1, "c"), vid(x0, y1, z1, "d"))
            if y == rows - 1 or not solid[y + 1, x]:
                quad(vid(x0, y0, z0, "a"), vid(x0, y0, z1, "a"), vid(x1, y0, z1, "b"), vid(x1, y0, z0, "b"))
            if x == 0 or not solid[y, x - 1]:
                quad(vid(x0, y0, z0, "a"), vid(x0, y1, z0, "d"), vid(x0, y1, z1, "d"), vid(x0, y0, z1, "a"))
            if x == cols - 1 or not solid[y, x + 1]:
                quad(vid(x1, y0, z0, "b"), vid(x1, y0, z1, "b"), vid(x1, y1, z1, "c"), vid(x1, y1, z0, "c"))

    if not verts:
        return np.zeros((0, 3)), np.zeros((0, 3), dtype=np.int32)
    v = np.array(verts, dtype=np.float64)
    v -= v.mean(axis=0)
    width = float(v[:, 0].max() - v[:, 0].min()) or 1.0
    v *= 4.4 / width
    return v, np.array(faces, dtype=np.int32)


# ---------------------------------------------------------------------------
# Renderer
# ---------------------------------------------------------------------------


class Renderer:
    def __init__(self, w: int, h: int, ssaa: int = 2, fov_deg: float = 48.0):
        self.w, self.h, self.ssaa = w, h, ssaa
        self.rw, self.rh = w * ssaa, h * ssaa
        self.zbuf = np.full((self.rh, self.rw), np.inf, dtype=np.float32)
        self.color = np.zeros((self.rh, self.rw, 3), dtype=np.float32)
        self.focal = 0.5 * self.rw / math.tan(math.radians(fov_deg) / 2)
        # lights in view space
        self.l1 = normalize(np.array([0.4, 0.75, 0.55], dtype=np.float64))
        self.l2 = normalize(np.array([-0.55, 0.2, 0.4], dtype=np.float64))

    def reset(self):
        self.zbuf.fill(np.inf)
        yy = np.linspace(0.0, 1.0, self.rh, dtype=np.float32)[:, None, None]
        top = np.array([0.008, 0.02, 0.055], dtype=np.float32)
        bot = np.array([0.02, 0.09, 0.15], dtype=np.float32)
        self.color[:] = top * (1 - yy) + bot * yy

    def _shade(self, n: np.ndarray, base, specular: float, shininess: float, emissive: float) -> np.ndarray:
        nv = normalize(n)
        # camera looks -Z; toward camera is +Z
        ndl1 = max(0.0, float(nv @ self.l1))
        ndl2 = max(0.0, float(nv @ self.l2))
        halfway = normalize(self.l1 + np.array([0.0, 0.0, 1.0]))
        ndh = max(0.0, float(nv @ halfway))
        # wrap diffuse slightly + strong ambient for smooth spheres
        ndl1 = (ndl1 + 0.15) / 1.15
        ndl2 = (ndl2 + 0.1) / 1.1
        spec = specular * (ndh ** shininess) if ndl1 > 0.05 else 0.0
        lum = 0.32 + 0.55 * ndl1 + 0.22 * ndl2 + spec
        col = np.asarray(base, dtype=np.float32)
        return np.clip(col * lum + col * emissive, 0.0, 1.0)

    def draw_mesh(
        self,
        verts_local: np.ndarray,
        faces: np.ndarray,
        model,
        eye: np.ndarray,
        rot_view: np.ndarray,
        color,
        specular=0.55,
        shininess=48.0,
        emissive=0.0,
        cull=True,
    ):
        if len(verts_local) == 0 or len(faces) == 0:
            return
        vw = apply_transform(verts_local, model)
        fnw = face_normals(vw, faces)
        vv = (vw - eye) @ rot_view.T
        fnv = fnw @ rot_view.T

        for i in range(len(faces)):
            n_view = fnv[i]
            if cull and n_view[2] <= 0.02:
                continue
            a, b, c = vv[faces[i, 0]], vv[faces[i, 1]], vv[faces[i, 2]]
            d0, d1, d2 = -a[2], -b[2], -c[2]
            eps = 0.08
            if d0 < eps and d1 < eps and d2 < eps:
                continue
            d0e, d1e, d2e = max(d0, eps), max(d1, eps), max(d2, eps)
            s0 = (self.rw * 0.5 + a[0] * self.focal / d0e, self.rh * 0.5 - a[1] * self.focal / d0e, d0e)
            s1 = (self.rw * 0.5 + b[0] * self.focal / d1e, self.rh * 0.5 - b[1] * self.focal / d1e, d1e)
            s2 = (self.rw * 0.5 + c[0] * self.focal / d2e, self.rh * 0.5 - c[1] * self.focal / d2e, d2e)
            rgb = self._shade(n_view if n_view[2] > 0 else -n_view, color, specular, shininess, emissive)
            self._raster_tri(s0, s1, s2, rgb)

    def _raster_tri(self, p0, p1, p2, rgb: np.ndarray):
        x0, y0, z0 = p0
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        minx = int(max(0, math.floor(min(x0, x1, x2))))
        maxx = int(min(self.rw - 1, math.ceil(max(x0, x1, x2))))
        miny = int(max(0, math.floor(min(y0, y1, y2))))
        maxy = int(min(self.rh - 1, math.ceil(max(y0, y1, y2))))
        if minx > maxx or miny > maxy:
            return
        area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        if abs(area) < 1e-8:
            return
        ys, xs = np.mgrid[miny : maxy + 1, minx : maxx + 1]
        px = xs.astype(np.float32) + 0.5
        py = ys.astype(np.float32) + 0.5
        # barycentric weights for vertices 0,1,2
        w0 = ((x1 - px) * (y2 - py) - (x2 - px) * (y1 - py)) / area
        w1 = ((x2 - px) * (y0 - py) - (x0 - px) * (y2 - py)) / area
        w2 = 1.0 - w0 - w1
        eps = -0.001
        mask = (w0 >= eps) & (w1 >= eps) & (w2 >= eps)
        if not mask.any():
            return
        zpix = w0 * z0 + w1 * z1 + w2 * z2
        zpix = np.where(mask, zpix, np.inf)
        region = self.zbuf[miny : maxy + 1, minx : maxx + 1]
        ok = mask & (zpix < region)
        if not ok.any():
            return
        cur = self.color[miny : maxy + 1, minx : maxx + 1]
        cur[ok] = rgb
        region[ok] = zpix[ok]

    def project(self, pts: np.ndarray, eye: np.ndarray, rot_view: np.ndarray):
        vv = (pts - eye) @ rot_view.T
        depth = np.maximum(-vv[:, 2], 1e-3)
        sx = self.rw * 0.5 + vv[:, 0] * self.focal / depth
        sy = self.rh * 0.5 - vv[:, 1] * self.focal / depth
        return sx, sy, depth

    def draw_glow_points(self, pts, eye, rot_view, color, radius=3.0, intensity=1.0):
        if len(pts) == 0:
            return
        pts = np.atleast_2d(np.asarray(pts, dtype=np.float64))
        sx, sy, d = self.project(pts, eye, rot_view)
        col = np.asarray(color, dtype=np.float32)
        for i in range(len(pts)):
            if d[i] <= 0.1:
                continue
            x, y = float(sx[i]), float(sy[i])
            r = radius * self.ssaa * (2.2 / d[i])
            r = float(np.clip(r, 1.5, 48))
            x0, x1 = int(max(0, x - r)), int(min(self.rw, x + r + 2))
            y0, y1 = int(max(0, y - r)), int(min(self.rh, y + r + 2))
            if x0 >= x1 or y0 >= y1:
                continue
            ys, xs = np.mgrid[y0:y1, x0:x1]
            dist2 = (xs - x) ** 2 + (ys - y) ** 2
            fall = np.exp(-dist2 / (0.4 * r * r + 1e-6)).astype(np.float32)
            fall *= intensity * (1.15 / d[i])
            z = float(d[i])
            zb = self.zbuf[y0:y1, x0:x1]
            write = (z < zb + 0.2) & (fall > 0.02)
            if not write.any():
                continue
            cur = self.color[y0:y1, x0:x1]
            add = col * fall[..., None]
            cur[write] = np.clip(cur[write] + add[write], 0, 1)

    def draw_line_3d(self, a, b, eye, rot_view, color, width=1.2, n_samples=28):
        ts = np.linspace(0.0, 1.0, n_samples)
        a = np.asarray(a, dtype=np.float64)
        b = np.asarray(b, dtype=np.float64)
        pts = a[None, :] * (1 - ts[:, None]) + b[None, :] * ts[:, None]
        self.draw_glow_points(pts, eye, rot_view, color, radius=width, intensity=0.8)

    def finalize(self) -> Image.Image:
        img = np.clip(self.color, 0, 1)
        if self.ssaa > 1:
            img = img.reshape(self.h, self.ssaa, self.w, self.ssaa, 3).mean(axis=(1, 3))
        img = np.clip(img, 0, 1) ** 0.9
        return Image.fromarray((img * 255).astype(np.uint8), "RGB")


def bloom(pil_img: Image.Image, threshold=0.5, radius=12, strength=0.6) -> Image.Image:
    arr = np.asarray(pil_img, dtype=np.float32) / 255.0
    lum = arr.mean(axis=2, keepdims=True)
    bright = np.where(lum > threshold, arr, 0.0)
    bright_img = Image.fromarray((np.clip(bright, 0, 1) * 255).astype(np.uint8), "RGB")
    blurred = bright_img.filter(ImageFilter.GaussianBlur(radius))
    b = np.asarray(blurred, dtype=np.float32) / 255.0
    out = np.clip(arr + b * strength, 0, 1)
    return Image.fromarray((out * 255).astype(np.uint8), "RGB")


def vignette(pil_img: Image.Image, power=0.35) -> Image.Image:
    w, h = pil_img.size
    y, x = np.mgrid[0:h, 0:w]
    dist = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
    mask = np.clip(1.0 - power * dist**1.6, 0.4, 1.0).astype(np.float32)
    arr = np.asarray(pil_img, dtype=np.float32) * mask[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def draw_hud(img: Image.Image, lines: list[str]) -> Image.Image:
    d = ImageDraw.Draw(img, "RGBA")
    try:
        font = ImageFont.truetype(str(FONT_MONO), 13)
        font_s = ImageFont.truetype(str(FONT_MONO), 11)
    except OSError:
        font = ImageFont.load_default()
        font_s = font
    d.text((18, 14), lines[0], font=font, fill=(120, 240, 255, 235))
    if len(lines) > 1:
        d.text((18, 34), lines[1], font=font_s, fill=(130, 160, 180, 205))
    w, h = img.size
    d.text((w - 14, 14), "SOFTWARE · 3D · PYTHON", font=font_s, fill=(110, 140, 160, 185), anchor="ra")
    c, L = (56, 230, 255, 210), 18
    for x, y, dx, dy in [(10, 10, 1, 1), (w - 10, 10, -1, 1), (10, h - 10, 1, -1), (w - 10, h - 10, -1, -1)]:
        d.line([(x, y), (x + dx * L, y)], fill=c, width=2)
        d.line([(x, y), (x, y + dy * L)], fill=c, width=2)
    return img


def starfield(n=160, seed=0):
    rng = np.random.default_rng(seed)
    pts = rng.uniform(-9, 9, size=(n, 3))
    pts[:, 2] = rng.uniform(-6, -1.5, size=n)
    return pts


# ---------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------


def render_hero(n_frames: int = 36, w: int = 960, h: int = 420) -> list[Image.Image]:
    name = CFG["identity"]["name"].upper()
    mask = voxel_text_mask(name, FONT_BOLD, px_per_voxel=7, max_width=780)
    text_v, text_f = voxels_to_mesh(mask, voxel=1.0, depth_layers=3)

    core_v, core_f = icosphere(subdiv=2, radius=0.75)
    ring_v, ring_f = torus(r_major=1.4, r_minor=0.07, seg_u=48, seg_v=12)
    ring2_v, ring2_f = torus(r_major=1.75, r_minor=0.04, seg_u=48, seg_v=10)

    cubes = []
    for i in range(8):
        bv, bf = box((0.3, 0.3, 0.3))
        cubes.append((bv, bf, 2 * math.pi * i / 8, i))

    stars = starfield(170, seed=42)
    gy = -1.55
    grid_segs = []
    for i in range(-6, 7):
        grid_segs.append((np.array([i * 0.75, gy, -4.0]), np.array([i * 0.75, gy, 3.5])))
        grid_segs.append((np.array([-4.5, gy, i * 0.6]), np.array([4.5, gy, i * 0.6])))

    R = Renderer(w, h, ssaa=2)
    frames = []
    t0 = time.time()
    cube_colors = [
        (0.95, 0.45, 0.55),
        (0.4, 0.7, 1.0),
        (0.5, 1.0, 0.7),
        (1.0, 0.8, 0.4),
        (0.8, 0.5, 1.0),
        (0.4, 0.95, 0.95),
        (1.0, 0.6, 0.85),
        (0.7, 0.85, 1.0),
    ]
    rng = np.random.default_rng(1)
    particles = rng.uniform(-3.2, 3.2, size=(45, 3))
    particles[:, 1] = rng.uniform(-1.3, 2.0, size=45)

    for f in range(n_frames):
        th = 2 * math.pi * f / n_frames
        R.reset()
        eye = np.array([math.sin(th * 0.35) * 0.9, 0.55 + math.sin(th * 2) * 0.06, 7.6])
        target = np.array([0.0, -0.15, 0.0])
        rot_view, eye = look_at(eye, target, np.array([0.0, 1.0, 0.0]))

        R.draw_glow_points(stars, eye, rot_view, (0.65, 0.88, 1.0), radius=1.1, intensity=0.5)
        for a, b in grid_segs:
            R.draw_line_3d(a, b, eye, rot_view, (0.1, 0.5, 0.7), width=1.0)

        # core
        model = rotation_y(th * 1.25) @ rotation_x(0.45 + th * 0.2)
        R.draw_mesh(core_v, core_f, model, eye, rot_view, (0.15, 0.72, 0.95), specular=0.5, shininess=40, cull=True)

        # rings
        R.draw_mesh(
            ring_v,
            ring_f,
            rotation_x(math.radians(70)) @ rotation_z(th * 0.9),
            eye,
            rot_view,
            (0.68, 0.5, 1.0),
            specular=0.55,
            shininess=48,
            cull=True,
        )
        R.draw_mesh(
            ring2_v,
            ring2_f,
            rotation_x(math.radians(-52)) @ rotation_y(-th * 1.15),
            eye,
            rot_view,
            (0.2, 0.95, 0.75),
            specular=0.5,
            shininess=42,
            cull=True,
        )

        # orbit cubes
        for bv, bf, ang, i in cubes:
            a = ang + th
            pos = np.array([math.cos(a) * 2.5, math.sin(a * 2 + i) * 0.55, math.sin(a) * 2.5])
            model = translation(pos) @ rotation_y(a * 2.2) @ rotation_x(a + i * 0.3)
            R.draw_mesh(bv, bf, model, eye, rot_view, cube_colors[i], specular=0.45, shininess=32, cull=True)

        # name slab — fully in frame
        bob = math.sin(th * 2) * 0.05
        tilt = rotation_x(-0.22 + math.sin(th) * 0.04) @ rotation_y(math.sin(th * 0.5) * 0.12)
        model = translation([0.0, -1.05 + bob, 1.6]) @ tilt @ scale3(0.78)
        R.draw_mesh(text_v, text_f, model, eye, rot_view, (0.88, 0.99, 1.0), specular=0.55, shininess=40, cull=False)

        # near particles
        pp = particles.copy()
        pp[:, 0] += np.sin(th + particles[:, 1]) * 0.12
        R.draw_glow_points(pp, eye, rot_view, (0.35, 0.95, 1.0), radius=2.0, intensity=0.65)

        img = R.finalize()
        img = bloom(img, threshold=0.48, radius=14, strength=0.7)
        img = vignette(img, 0.42)
        img = draw_hud(img, ["◆ K S CHANNALLI // IDENTITY CORE", "numpy z-buffer · Blinn-Phong · seamless loop"])
        frames.append(img)
        if f == 0:
            print(f"  hero first frame: {time.time() - t0:.2f}s")
    print(f"  hero: {n_frames} frames in {time.time() - t0:.1f}s")
    return frames


def render_automation(n_frames: int = 32, w: int = 960, h: int = 340) -> list[Image.Image]:
    steps = ["TRIGGER", "UNDERSTAND", "DECIDE", "EXECUTE", "VERIFY", "RESULT"]
    colors = [
        (0.22, 0.9, 1.0),
        (0.38, 0.65, 1.0),
        (0.66, 0.55, 1.0),
        (0.96, 0.45, 0.7),
        (0.98, 0.75, 0.3),
        (0.2, 0.85, 0.6),
    ]
    n = len(steps)
    xs = np.linspace(-3.6, 3.6, n)
    sphere_v, sphere_f = icosphere(subdiv=2, radius=1.0)
    tubes = []
    for i in range(n - 1):
        tubes.append(tube([xs[i], 0, 0], [xs[i + 1], 0, 0], r=0.05, segments=12))
    card_v, card_f = box((1.2, 0.36, 0.1))
    stars = starfield(90, seed=7)
    rng = np.random.default_rng(3)

    R = Renderer(w, h, ssaa=2, fov_deg=42.0)
    frames = []
    t0 = time.time()
    for f in range(n_frames):
        th = 2 * math.pi * f / n_frames
        R.reset()
        eye = np.array([math.sin(th * 0.3) * 0.7, 1.1, 7.8])
        target = np.array([0.0, -0.2, 0.0])
        rot_view, eye = look_at(eye, target, np.array([0.0, 1.0, 0.0]))

        R.draw_glow_points(stars, eye, rot_view, (0.6, 0.85, 1.0), radius=1.0, intensity=0.45)
        for i in range(-5, 6):
            R.draw_line_3d(
                [i * 0.85, -1.3, -2.5],
                [i * 0.85, -1.3, 2.5],
                eye,
                rot_view,
                (0.08, 0.38, 0.52),
                width=1.0,
            )

        for tv, tf in tubes:
            R.draw_mesh(tv, tf, np.eye(4), eye, rot_view, (0.1, 0.32, 0.48), specular=0.35, shininess=28, cull=True)

        pulse_pos = -3.6 + (f / n_frames) * 7.2
        for i in range(n):
            x = float(xs[i])
            heat = math.exp(-((x - pulse_pos) ** 2) / 0.7)
            base = colors[i]
            col = tuple(min(1.0, base[j] * (0.65 + 0.55 * heat) + 0.2 * heat) for j in range(3))
            s = 0.30 * (1.0 + 0.06 * math.sin(th * 3 + i) + 0.12 * heat)
            model = translation([x, 0, 0]) @ (rotation_y(th + i * 0.7) @ rotation_x(th * 0.8)) @ scale3(s)
            R.draw_mesh(
                sphere_v,
                sphere_f,
                model,
                eye,
                rot_view,
                col,
                specular=0.45,
                shininess=36,
                emissive=0.25 * heat,
                cull=True,
            )
            R.draw_mesh(
                card_v,
                card_f,
                translation([x, -0.72, 0.15]) @ rotation_x(-0.12),
                eye,
                rot_view,
                (0.05, 0.12, 0.2),
                specular=0.25,
                shininess=18,
                cull=True,
            )
            R.draw_glow_points(
                [[x, -0.72, 0.28]],
                eye,
                rot_view,
                base,
                radius=3.0 + 5 * heat,
                intensity=0.35 + 0.65 * heat,
            )
            # step number particles rising when hot
            if heat > 0.45:
                rise = np.array([[x + rng.normal(0, 0.1), 0.35 + heat * 0.7, 0.18]])
                R.draw_glow_points(rise, eye, rot_view, base, radius=2.5, intensity=0.55 * heat)

        ox = pulse_pos
        R.draw_glow_points([[ox, 0, 0]], eye, rot_view, (1.0, 1.0, 1.0), radius=7, intensity=1.1)
        trail = np.linspace(max(-3.6, ox - 1.7), ox, 22)
        tpts = np.stack([trail, np.zeros_like(trail), np.zeros_like(trail)], axis=1)
        R.draw_glow_points(tpts, eye, rot_view, (0.4, 0.95, 1.0), radius=2.5, intensity=0.45)

        # step labels as HUD-like projected dots only (geometry cards stay subtle)
        img = R.finalize()
        img = bloom(img, threshold=0.42, radius=16, strength=0.75)
        img = vignette(img, 0.36)
        img = draw_hud(img, ["◆ AUTOMATION PIPELINE // LIVE", "TRIGGER · UNDERSTAND · DECIDE · EXECUTE · VERIFY · RESULT"])
        frames.append(img)
    print(f"  automation: {n_frames} frames in {time.time() - t0:.1f}s")
    return frames


def save_gif(frames: list[Image.Image], path: Path, duration_ms: int = 85):
    if not frames:
        raise RuntimeError("no frames")
    mid = frames[len(frames) // 2]
    pal = mid.quantize(colors=160, method=Image.Quantize.MEDIANCUT)
    conv = [fr.quantize(palette=pal, dither=Image.Dither.NONE) for fr in frames]
    path.parent.mkdir(parents=True, exist_ok=True)
    conv[0].save(
        path,
        save_all=True,
        append_images=conv[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"  wrote {path.name}: {path.stat().st_size / 1024:.0f} KB, {len(conv)} frames")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("Rendering hero-3d.gif …")
    save_gif(render_hero(36, 960, 420), OUT / "hero-3d.gif", duration_ms=90)
    print("Rendering automation-3d.gif …")
    save_gif(render_automation(32, 960, 340), OUT / "automation-3d.gif", duration_ms=85)
    for name in (
        "hero-3d.svg",
        "automation-3d.svg",
        "hero-depth.svg",
        "technology-field.svg",
        "project-constellation.svg",
        "opero-loop.svg",
    ):
        p = OUT / name
        if p.exists():
            p.unlink()
            print(f"  removed {name}")
    print("Done.")


if __name__ == "__main__":
    main()
