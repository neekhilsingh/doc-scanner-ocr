# Problem Statement, Scope & Target Users

## Problem Statement

Every time I've tried to snap a photo of a document and OCR it, the
results have been bad - and it's not really the OCR engine's fault. A
phone photo is basically never flat: it's angled, there's a table or
some background visible around the page, and the lighting is uneven
more often than not. Tesseract (and OCR engines in general) expect
flat, high-contrast, front-on text, so handing it a raw photo usually
gets garbled or half-missing output back.

So before OCR is even worth running, three things need to happen: find
the actual document inside the photo (and ignore the background),
straighten out the perspective so it looks like it was scanned flat
instead of shot at an angle, and clean up the lighting/contrast so the
text is actually legible.

## Scope

What this project actually does:
- finds the document's boundary in a photo using classical CV (edge
  detection + contour approximation, no trained model involved)
- fixes the perspective with a 4-point transform so the page comes
  out flat and top-down
- cleans up the flattened image with adaptive thresholding so it's
  easier for OCR to read
- runs Tesseract on it via `pytesseract` to pull the text out
- wraps all of that in a CLI so it's actually usable from the terminal

What it doesn't do (yet): no GUI, no mobile app, no batch mode for
multiple documents in one go, and no handling for upside-down or
sideways text - it assumes the photo is roughly the right way up.

## Target Users

- Students/anyone who wants to digitize notes, receipts, or handouts
  without owning an actual scanner.
- People who'd rather script this than tap through a mobile scanner
  app, especially if they've got a folder full of photos to process.
- Anyone curious about how classical (non-deep-learning) CV pipelines
  are actually put together, since the code is meant to be readable
  end to end.

## High-Level Features

- Automatic document boundary detection from a photo.
- Perspective ("bird's eye") correction to flatten the document.
- Falls back to the original image if it can't find a clean boundary,
  instead of just failing.
- Adaptive-threshold enhancement so OCR has an easier time.
- Text extraction via Tesseract - printed to console or saved to a file.
- OCR language and output paths are configurable through CLI flags.
