# Job Enriquez learning portfolio

ITC-C508 eportfolio featuring activities, reports, notebooks, reflections, and term takeaways from Prelims to Finals.

Live website: https://russeruuuu.github.io/eportfolio/

## Local preview

Run `python3 -m http.server 4173` from this directory and open http://localhost:4173.

## Updating content

- Original files are in `ACTIVITIES/`.
- Activity reflections are in `content/reflections.json`.
- Term takeaways are in `content/takeaways.json`.
- Run `python3 scripts/build_catalog.py` after changing the catalog or content.
- Run `python3 scripts/build_notebooks.py` after updating notebook files.

Notebook previews display code and saved results without executing cells. Interactive widgets require the original notebook in Jupyter or Colab.

The site uses two fonts, Inter and Space Grotesk, and is served as static files with GitHub Pages.
