# Railway build failure analysis

## Symptom

The build stopped after `apply_supplied_artwork.py` with:

`FAIL: supplied artwork missing or unexpectedly small`

## Root cause

The WebP repository object was not a valid binary image. It contained Base64 text instead of decoded WebP bytes, so its stored size was below the validator threshold and browsers could not reliably render it.

## Fix

- replace the malformed blob with an actual binary WebP asset;
- retain deterministic existence, minimum-size and alt-text checks;
- verify the WebP RIFF/WEBP signature in the build validator.

This is an asset-encoding defect, not a Railway, Docker, Caddy or application-runtime defect.
