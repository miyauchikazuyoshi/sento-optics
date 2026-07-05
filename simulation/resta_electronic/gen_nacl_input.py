"""実験F-2: NaCl 2x2x2 conventional スーパーセル (64原子) の SCF 入力生成"""
A = 5.64                      # NaCl 格子定数 (Å)
L = 2 * A                     # スーパーセル一辺 11.28 Å
CELLDM = L / 0.529177210903   # Bohr

na_base = [(0, 0, 0), (.5, .5, 0), (.5, 0, .5), (0, .5, .5)]
cl_base = [(.5, 0, 0), (0, .5, 0), (0, 0, .5), (.5, .5, .5)]
na, cl = [], []
for i in range(2):
    for j in range(2):
        for k in range(2):
            for b in na_base:
                na.append(((b[0] + i) / 2, (b[1] + j) / 2, (b[2] + k) / 2))
            for b in cl_base:
                cl.append(((b[0] + i) / 2, (b[1] + j) / 2, (b[2] + k) / 2))
assert len(na) == 32 and len(cl) == 32

lines = f"""&CONTROL
    calculation   = 'scf'
    prefix        = 'NaCl'
    outdir        = './tmp'
    pseudo_dir    = '../surface_tension/qe_slab/pseudo/'
    verbosity     = 'low'
/
&SYSTEM
    ibrav         = 1
    celldm(1)     = {CELLDM:.6f}
    nat           = 64
    ntyp          = 2
    ecutwfc       = 50.0
    ecutrho       = 400.0
    occupations   = 'fixed'
    nbnd          = 260
/
&ELECTRONS
    conv_thr      = 1.0d-8
    mixing_beta   = 0.7
    mixing_ndim   = 4
    diago_david_ndim = 2
/
ATOMIC_SPECIES
 Na  22.98976928  Na.pbe-spn-kjpaw_psl.1.0.0.UPF
 Cl  35.453       Cl.pbe-n-kjpaw_psl.1.0.0.UPF

K_POINTS gamma

ATOMIC_POSITIONS crystal
"""
for p in na:
    lines += f" Na  {p[0]:.10f}  {p[1]:.10f}  {p[2]:.10f}\n"
for p in cl:
    lines += f" Cl  {p[0]:.10f}  {p[1]:.10f}  {p[2]:.10f}\n"

with open("NaCl_scf.in", "w") as f:
    f.write(lines)
print(f"生成: NaCl_scf.in (64原子, L={L} Å, celldm={CELLDM:.4f} Bohr, "
      f"ecut 50/400, nbnd=260, 占有256)")
