# beamer-AMSUniBo-template

> A ready-to-use presentation skeleton for the
> [AMSUniBo Beamer style](https://github.com/andreaomicini/beamer-AMSUniBo)

## author

* Andrea Omicini

## requirements

* A TeX distribution providing `pdflatex`, `latexmk` and `bibtex` (TeX Live).
* The font packages the style loads, all from TeX Live: `merriweather`,
  `inconsolata`, `newtxsf` and `anyfontsize`. The first three are in
  `collection-fontsextra`, the last in `collection-latexextra`; both are in
  `scheme-full`, neither in a minimal installation such as BasicTeX, where
  `tlmgr install merriweather inconsolata newtxsf anyfontsize` is enough.

The style itself needs no separate installation: the `.style` submodule pins the
release this template was built against, and the symbolic links in the repository
root reach it.

## usage

Clone the repository **with its submodule**, since the style is pulled in that way:

```bash
git clone --recurse-submodules https://github.com/andreaomicini/beamer-AMSUniBo-template.git
```

If you have already cloned without `--recurse-submodules`:

```bash
git submodule update --init .style
```

Then edit `AMSUniBo-template.tex` and build it as usual, e.g.

```bash
latexmk -pdf AMSUniBo-template.tex
```

The most recent build of the template is attached to every
[release](https://github.com/andreaomicini/beamer-AMSUniBo-template/releases).

### the `apice` option

The template's preamble enables the style's `apice` option:

```latex
\documentclass[presentation,apice]{beamer}\mode<presentation>{\usetheme{AMSUniBo}}
```

With it, an `apice` field in a BibTeX entry is displayed as a small `(APICe)`
marker linking to the corresponding page of the
[APICe](https://apice.unibo.it/) Wiki:

```bibtex
@manual{bibtex-patashnik88,
    ...
    apice = {BibtexPatashnik88},
}
```

Drop the option and nothing else has to change: `\apicepar` is still defined,
but expands to nothing, so the same `.bib` and the same slides keep working
with the markers simply absent.

The template's own slides demonstrate the option, and the bibliography shows
the marker in place.

### the `bologna` and `cesena` options

The style watermarks every slide with a seal in the lower-right corner, cropped by
the page edge. `bologna` selects the seal of the *Alma Mater Studiorum* as a whole
and is the default, so the option can be left out; `cesena` selects the seal of the
*Campus di Cesena* instead:

```latex
\documentclass[presentation,cesena]{beamer}\mode<presentation>{\usetheme{AMSUniBo}}
```

The two are told apart by the border — solid for the Campus, an outline for the
Ateneo — which is what an eye in the Alma Mater reads first. Nothing else in a deck
changes, and saying `bologna` explicitly is identical to saying nothing.

This template leaves the option out, so its slides carry the Ateneo seal.

## relation to beamer-AMSBolognaFC-template

This is
[beamer-AMSBolognaFC-template](https://github.com/andreaomicini/beamer-AMSBolognaFC-template)
with the AMSUniBo style in place of the AMSBolognaFC one. The frames, the
structure and the demonstrations are the same, with two differences:

* the `Colours` frame documents the AMSUniBo palette and where each value comes
  from;
* in the `Citations` frame each weight is demonstrated on a header it can
  actually be read on. `\ccite` and `\cccite` are **both** light — a citation
  marker's usual home is a block header, which is dark — so `\ccite` sits on the
  `block` header and `\cccite`, the lighter of the two, on the `alertblock` one.
  The original template put `\cccite` on a light header, where it cannot be seen.

## structure

The style itself lives in the `.style` submodule, which tracks the `main`
branch of [beamer-AMSUniBo](https://github.com/andreaomicini/beamer-AMSUniBo).
The style files in the repository root are symbolic links into `.style`, so
there is exactly one copy of each file.

To move the template onto a newer style release:

```bash
git submodule update --remote .style
git add .style
git commit -m "Update style submodule"
```

## versioning

The template version is declared in `AMSUniBo-template.tex` as
`\templatemajor` / `\templateminor` / `\templatepatch`, giving
`Major.Minor[.Patch]`. `\templatepatch` is optional: comment it out to release
as `Major.Minor`.

Releases are tagged `Major.Minor[.Patch]-<UTC time-stamp>`, with the time-stamp
appended automatically by the CI at release time.

The template is versioned independently of the style: it changes sometimes
together with the style and sometimes on its own.

## licence

The template is released into the public domain under
[CC0 1.0 Universal](LICENSE). Use it, adapt it and build on it freely, with no
obligation to credit or to carry any notice into your own presentations.

This applies to the template itself. The style files reached through the
`.style` submodule are covered by their own licence — the
[LaTeX Project Public License](https://github.com/andreaomicini/beamer-AMSUniBo/blob/main/LICENSE),
version 1.3c or later — and `apalike-AMS.bst` remains subject to Oren
Patashnik's terms. The colours are the Alma Mater Studiorum's institutional
ones, and their use is governed by the Ateneo's own rules.
