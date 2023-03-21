# Diary of a Fat Slob

**Under development! Some links may not work and archive is very incomplete.**

This is an archive of Doug Holland's blog <https://www.itsdougholland.com/>. If you want to access the current version of the archive, head over to the [wiki](https://github.com/dfs-archiver/dfs-archive/wiki). Should you encounter any errors, [submit an issue](https://github.com/dfs-archiver/dfs-archive/issues) (requires a GitHub account).

## Motivation

I am a big fan of Doug Holland's work and want to preserve it. His website will not last forever and I am trying to archive it in a more long-lived format, which can easily be distributed and stored locally.

## Methodology

Archiving the blog consists of several (automatic) steps:

  1. Cloning the entire website using [wget](https://www.gnu.org/software/wget/).
  2. Removing all files that are not needed for further processing (e.g. `.js` files).
  3. Building indexes of the various series (e.g. _Pathetic Life_, _Breakfast at the Diner_).
  4. Formatting each post to a clean and minimal `XHTML` format.
  5. Reformatting each post based on the series (e.g. moving entry dates to the top of each page).
  6. Cleaning up the content by removing disclaimers, series titles, etc.
  7. Packing posts into files based on the series.
  8. Converting links.
  9. _(Optional: Converting `XHTML` to `MD`.)_

## Specification

All posts are converted into strict `XHTML` and `MD` formats.

```text
TODO: write specifications and tests for them
```
