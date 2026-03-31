# Zenodo Preprint Submission Guide

## Overview

Both papers are submitted simultaneously to Zenodo as preprints to secure DOIs.

| Paper | PDF | Metadata |
|-------|-----|----------|
| Paper 1 (Optics) | `../drafts/paper1_optics/main.pdf` | `paper1_metadata.json` |
| Paper 2 (Surface Tension) | `../drafts/paper2_surface_tension/main.pdf` | `paper2_metadata.json` |

## Submission Steps (Web UI)

1. Go to https://zenodo.org and sign in (GitHub login works)
2. Click **"New Upload"**
3. Upload the PDF file
4. Fill in metadata from the corresponding JSON file:
   - **Resource type**: Publication > Preprint
   - **Title**: from `metadata.title`
   - **Authors**: Miyauchi, Kazuyoshi / Independent researcher
   - **Description**: from `metadata.description`
   - **Keywords**: from `metadata.keywords`
   - **License**: Creative Commons Attribution 4.0 International (CC-BY-4.0)
   - **Related identifiers**: GitHub repo URL, relation "is supplemented by"
5. Click **"Save"** to save draft
6. **"Get a DOI now!"** to reserve DOI before publishing
7. Review everything, then click **"Publish"**

## Important Notes

- Once published, the record **cannot be deleted** (DOI is permanent)
- You **can** upload new versions later (each gets its own DOI)
- Add the DOI back to the paper PDF and GitHub README after publishing
- Consider adding ORCID to author metadata for discoverability

## After Publishing

1. Update README.md with DOI badges
2. Update paper tex files with DOI in header
3. Cold-email relevant researchers with DOI + GitHub URL
4. Submit to journal (PRB / JCP) with Zenodo DOI as preprint reference

## API Upload (Alternative)

If you prefer programmatic upload, use the Zenodo REST API:
- Get a personal access token at https://zenodo.org/account/settings/applications/
- See https://developers.zenodo.org/ for documentation
- The metadata JSON files are already in the correct format for the API
