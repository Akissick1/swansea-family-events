# Swansea Family Events website

The public website for the Swansea Family Events guide, hosted on Netlify at
https://swansea-family-events.netlify.app/

## What is in here

- `index.html`: the whole guide (events, calendar, indoor places, sources). Built from the Claude version of the guide by `tools/build_site.py`. Do not edit it by hand: the twice weekly refresh overwrites it.
- `og-image.png`: the preview picture shown when the link is shared on WhatsApp, Facebook and similar.
- `netlify.toml`: tells Netlify there is no build step and that browsers must always check for the latest copy.
- `robots.txt`: lets search engines index the site.
- `tools/build_site.py`: turns the guide's page into a normal web page (proper title, description, sharing preview).

## How it updates

The scheduled refresh (Mondays and Thursdays, early morning) updates the guide on Claude, then runs
`python3 tools/build_site.py <page> index.html`, commits `index.html` here and pushes to `main`.
Netlify publishes every push to `main` automatically, usually within a minute.

## Visitor analytics

`tools/build_site.py` adds PostHog (EU cloud, project "Default project", id 302061) to the website only, in cookieless mode: no cookies or local storage, so no consent banner. It records page views plus these events: event_opened, listing_opened, calendar_added, event_shared, tab_viewed, search_used, season_button, post_event_email. The Claude version of the guide carries no analytics.
