# Published sources

Hemond et al. (2008), Distinct classes of pyramidal cells exhibit mutually
exclusive firing patterns in hippocampal area CA3b.
Code: https://github.com/ModelDBRepository/101629
ModelDB: https://modeldb.science/101629

Start with ca3b-cell1zr.hoc and the fig9d procedure. Geometry is in
geo-cell1zr.hoc. Kinetics are in na3n.mod, kdrca1.mod, kaprox.mod, h.mod,
and calcium mechanisms. Preserve original files separately when downloading.
The published code is not bundled or executed in this starter.

Meeks & Mennerick (2007), Action potential initiation and propagation in
CA3 pyramidal axons. https://doi.org/10.1152/jn.01288.2006
Useful for AIS initiation and propagation constraints; not the source of
this demo's geometry.

This starter uses a passive subset of Hemond reference constants, not a
reproduction of its Figure 9D. Leak reversal is fixed for the passive demo;
the original actively balances resting currents. The reference has no
separate AIS section. No validated AIS or chandelier parameters are supplied.
