---
title: 'mwarp1d: Manual one-dimensional data warping in Python and PyQt'
tags:
  - Python
  - PyQt
  - biomechanics
  - dynamics
  - kinematics
  - electromyography
authors:
  - name: Todd C. Pataky
    orcid: 0000-0002-8292-7189
    affiliation: 1
  - name: Hanaa Naouma
    affiliation: "1, 2"
  - name: Cyril J. Donnelly
    affiliation: 3
affiliations:
 - name: Kyoto University, Department of Human Health Sciences
   index: 1
 - name: Shinshu University, Department of Bioengineering
   index: 2
 - name: Nanyang Technological University, Rehabilitation Research Institute of Singapore
   index: 3
date: 11 October 2019
bibliography: refs.bib

---

# Summary

"Warping" is a mathematical/computational process that transforms a domain like time or space so that its nodes (i.e., points in time or space) are unqeuallty spaced. For one-dimensional (1D) domains like time, warping involves translating nodes forward or backward (in time). The goal of warping is usually "registration", or the alignment of homologous events/features. An example is shown in Fig.1 below; an original 1D observation is warped to more closely match a template 1D observation.

Warping 1D data has been shown to be necessary for minimizing variability in a variety of applications, yet only a few open-source algorithms, and no manual techniques, exist for 1D registration. It has separately been shown that, for 2D data, manual registration can perform as well as, and in some cases better than algorithmic registration. Manual registration may also be necessary when algorithmic registration fails.

``mwarp1d`` is a tool for 1D manual warping, both via Python scripting and via a PyQt graphical user interface. Two warping procedures are implemented: `landmark` and `manual`. Landmark registration was introduced to the literature more than 20 years ago, involving homologous point digitizing and subsequent piecewise interpolation. While simple, landmark registration was implemented as a comparative baseline. The `manual` registration scheme is novel, involving domain warps through manually adjustable, globally-constrained asymmetric Gaussian warping kernels.


# Statement of need

`mwarp1d` allows users to manually warp 1D data with the purpose of achieveing registration amongst multiple 1D observations (i.e., homologous 1D event alignment). This software solves the problem of algorithmically poor registration performance, allowing users to define arbitrarily complex warps without algoritmic limitations. As far as we are aware, no other manual, GUI-based software exists for manual 1D data warping. The target audience is anyone working with or analyzing registerable 1D data, especially researchers in the human and animal movement sciences.

# Figures

<center>
<img src="ss0.png" width="400"/>

Figure 1: Example 1D warp.
</center>

# References

[@Adler:1976]