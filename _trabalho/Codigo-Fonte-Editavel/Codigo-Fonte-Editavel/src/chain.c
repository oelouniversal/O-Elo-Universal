// Raymarcher de uma corrente de 7 elos (stadium-torus) em ouro polido.
// Saida: arquivo float32 RGBA+depth (premultiplicado): w*h*5 floats  (r,g,b,alpha,depth)
// Uso: chain W H SS out.raw  zdeg xdeg ydeg  tx ty tz  fovdeg  spin0deg
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

typedef struct { float x, y, z; } v3;
static inline v3 V(float x, float y, float z) { v3 r = {x, y, z}; return r; }
static inline v3 add(v3 a, v3 b) { return V(a.x + b.x, a.y + b.y, a.z + b.z); }
static inline v3 sub(v3 a, v3 b) { return V(a.x - b.x, a.y - b.y, a.z - b.z); }
static inline v3 mul(v3 a, float s) { return V(a.x * s, a.y * s, a.z * s); }
static inline float dot(v3 a, v3 b) { return a.x * b.x + a.y * b.y + a.z * b.z; }
static inline float len(v3 a) { return sqrtf(dot(a, a)); }
static inline v3 nrm(v3 a) { float l = len(a); return l > 0 ? mul(a, 1.f / l) : a; }
static inline float clampf(float x, float a, float b) { return x < a ? a : (x > b ? b : x); }
static inline float sat(float x) { return clampf(x, 0.f, 1.f); }

#define NL 7
static const float RT = 1.0f;   // raio do tubo
static const float RS = 2.35f;  // meia-largura da linha central
static const float AH = 1.55f;  // meio comprimento reto

typedef struct { float m[9]; v3 t; } xf;  // q = m * (p - t)
static xf links[NL];
static v3 chainT; static float chainR;

static void matmul(const float *a, const float *b, float *o) {
  for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) {
    float s = 0; for (int k = 0; k < 3; k++) s += a[i * 3 + k] * b[k * 3 + j]; o[i * 3 + j] = s; }
}
static void rotx(float a, float *m) { float c = cosf(a), s = sinf(a); float r[9] = {1,0,0, 0,c,-s, 0,s,c}; memcpy(m, r, sizeof r); }
static void roty(float a, float *m) { float c = cosf(a), s = sinf(a); float r[9] = {c,0,s, 0,1,0, -s,0,c}; memcpy(m, r, sizeof r); }
static void rotz(float a, float *m) { float c = cosf(a), s = sinf(a); float r[9] = {c,-s,0, s,c,0, 0,0,1}; memcpy(m, r, sizeof r); }
static void transp(const float *a, float *o) { for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) o[i * 3 + j] = a[j * 3 + i]; }
static v3 mulv(const float *m, v3 p) { return V(m[0]*p.x + m[1]*p.y + m[2]*p.z, m[3]*p.x + m[4]*p.y + m[5]*p.z, m[6]*p.x + m[7]*p.y + m[8]*p.z); }

static inline float link_sd(const xf *L, v3 p) {
  v3 q = mulv(L->m, sub(p, L->t));
  float yy = q.y - clampf(q.y, -AH, AH);
  float d2 = sqrtf(q.x * q.x + yy * yy);
  float ring = d2 - RS;
  return sqrtf(ring * ring + q.z * q.z) - RT;
}
static inline float scene(v3 p, int *idx) {
  float best = 1e9f; int bi = 0;
  for (int i = 0; i < NL; i++) { float d = link_sd(&links[i], p); if (d < best) { best = d; bi = i; } }
  if (idx) *idx = bi; return best;
}
static v3 link_normal(const xf *L, v3 p) {
  v3 q = mulv(L->m, sub(p, L->t));
  float cy = clampf(q.y, -AH, AH);
  float yy = q.y - cy;
  float d2 = sqrtf(q.x * q.x + yy * yy); if (d2 < 1e-6f) d2 = 1e-6f;
  v3 c = V(q.x / d2 * RS, cy + yy / d2 * RS, 0.f);
  v3 nl = nrm(sub(q, c));
  float mt[9]; transp(L->m, mt);
  return nrm(mulv(mt, nl));
}

static v3 env(v3 r) {
  v3 K = nrm(V(-0.55f, 0.62f, -0.56f));
  v3 S = nrm(V(0.88f, 0.10f, -0.40f));
  v3 B = nrm(V(-0.25f, 0.25f, 0.93f));
  float k = powf(fmaxf(dot(r, K), 0.f), 14.f);
  float k2 = powf(fmaxf(dot(r, K), 0.f), 90.f);
  float s = powf(fmaxf(dot(r, S), 0.f), 34.f) * (1.f - 0.5f * fabsf(r.y));
  float b = powf(fmaxf(dot(r, B), 0.f), 10.f);
  float up = r.y * 0.5f + 0.5f;
  v3 base = V(0.010f + 0.040f * up, 0.010f + 0.043f * up, 0.012f + 0.050f * up);
  float floorb = powf(fmaxf(-r.y, 0.f), 1.6f);
  v3 c = base;
  c = add(c, V(floorb * 0.22f, floorb * 0.14f, floorb * 0.07f));
  c = add(c, V(k * 2.3f + k2 * 8.f, k * 1.9f + k2 * 6.6f, k * 1.35f + k2 * 5.f));
  c = add(c, V(s * 1.0f, s * 1.4f, s * 1.8f));
  c = add(c, V(b * 1.6f, b * 1.05f, b * 0.4f));
  return c;
}

int main(int argc, char **argv) {
  if (argc < 13) { fprintf(stderr, "args\n"); return 1; }
  int W = atoi(argv[1]), H = atoi(argv[2]), SS = atoi(argv[3]);
  const char *out = argv[4];
  float zd = atof(argv[5]) * M_PI / 180, xd = atof(argv[6]) * M_PI / 180, yd = atof(argv[7]) * M_PI / 180;
  v3 T = V(atof(argv[8]), atof(argv[9]), atof(argv[10]));
  float fov = atof(argv[11]) * M_PI / 180;
  float spin0 = atof(argv[12]) * M_PI / 180;
  float pitch = 2.f * (AH + RS - RT) * 0.985f;

  float Rz[9], Rx[9], Ry[9], t1[9], Rc[9], RcT[9];
  rotz(zd, Rz); rotx(xd, Rx); roty(yd, Ry);
  matmul(Rz, Rx, t1); matmul(t1, Ry, Rc); transp(Rc, RcT);
  for (int i = 0; i < NL; i++) {
    float yc = (i - (NL - 1) * 0.5f) * pitch;
    v3 c = V(0, yc, 0);
    v3 tw = add(T, mulv(Rc, c));
    float th = spin0 + (i % 2 ? M_PI * 0.5f : 0.f);
    float Rl[9]; roty(-th, Rl);
    matmul(Rl, RcT, links[i].m);
    links[i].t = tw;
  }
  chainT = T; chainR = ((NL - 1) * 0.5f * pitch) + AH + RS + RT + 1.0f;

  float *buf = (float *)calloc((size_t)W * H * 5, sizeof(float));
  float tanf2 = tanf(fov * 0.5f);
  float aspect = (float)W / H;
  v3 cam = V(0, 0, 0);

#pragma omp parallel for schedule(dynamic, 4)
  for (int y = 0; y < H; y++) {
    for (int x = 0; x < W; x++) {
      float R = 0, G = 0, B = 0, A = 0, D = 0;
      for (int sy = 0; sy < SS; sy++) for (int sx = 0; sx < SS; sx++) {
        float u = ((x + (sx + 0.5f) / SS) / W * 2.f - 1.f) * aspect * tanf2;
        float v = (1.f - (y + (sy + 0.5f) / SS) / H * 2.f) * tanf2;
        v3 rd = nrm(V(u, v, 1.f));
        // esfera englobante
        v3 oc = sub(cam, chainT);
        float bq = dot(oc, rd), cq = dot(oc, oc) - chainR * chainR;
        float disc = bq * bq - cq;
        if (disc < 0) continue;
        float sq = sqrtf(disc);
        float t = fmaxf(-bq - sq, 0.f), tmax = -bq + sq;
        int hit = 0; v3 p = cam; int idx = 0;
        for (int it = 0; it < 220; it++) {
          p = add(cam, mul(rd, t));
          float d = scene(p, &idx);
          float eps = 0.0006f * t;
          if (d < eps) { hit = 1; break; }
          t += d * 0.92f;
          if (t > tmax) break;
        }
        if (!hit) continue;
        v3 n = link_normal(&links[idx], p);
        float ndv = dot(n, mul(rd, -1.f));
        if (ndv < 0) { n = mul(n, -1.f); ndv = -ndv; }
        v3 r = sub(rd, mul(n, 2.f * dot(rd, n)));
        v3 e = env(r);
        // leve "rugosidade": media de 4 amostras do ambiente
        v3 ta = nrm(V(n.y, -n.x, 0.f) ); if (len(ta) < 0.1f) ta = V(1, 0, 0);
        v3 e2 = V(0, 0, 0);
        for (int k = 0; k < 4; k++) {
          float ang = k * 1.5707963f + 0.4f;
          v3 jit = add(mul(ta, cosf(ang) * 0.10f), mul(nrm(V(n.y * 0.3f, n.x * 0.3f, 1.f)), sinf(ang) * 0.10f));
          e2 = add(e2, env(nrm(add(r, jit))));
        }
        e2 = mul(e2, 0.25f);
        e = add(mul(e, 0.45f), mul(e2, 0.55f));
        float fr = powf(1.f - sat(ndv), 5.f);
        v3 F0 = V(1.0f, 0.73f, 0.30f);
        v3 F = V(F0.x + (1 - F0.x) * fr, F0.y + (1 - F0.y) * fr, F0.z + (1 - F0.z) * fr);
        // AO
        float ao = 0.f, w = 1.f;
        for (int k = 1; k <= 5; k++) {
          float h = 0.22f * k;
          float dd = scene(add(p, mul(n, h)), NULL);
          ao += (h - dd) * w; w *= 0.62f;
        }
        ao = clampf(1.f - 0.62f * ao, 0.12f, 1.f);
        v3 col = V(F.x * e.x * ao, F.y * e.y * ao, F.z * e.z * ao);
        // leve brilho difuso quente (patina)
        float dif = fmaxf(dot(n, nrm(V(-0.5f, 0.7f, -0.5f))), 0.f);
        col = add(col, V(0.030f * dif * ao, 0.020f * dif * ao, 0.008f * dif * ao));
        R += col.x; G += col.y; B += col.z; A += 1.f; D += t;
      }
      float inv = 1.f / (SS * SS);
      size_t o = ((size_t)y * W + x) * 5;
      float a = A * inv;
      buf[o + 0] = R * inv; buf[o + 1] = G * inv; buf[o + 2] = B * inv; buf[o + 3] = a;
      buf[o + 4] = A > 0 ? D / A : 0.f;
    }
  }
  FILE *f = fopen(out, "wb"); fwrite(buf, sizeof(float), (size_t)W * H * 5, f); fclose(f);
  return 0;
}
