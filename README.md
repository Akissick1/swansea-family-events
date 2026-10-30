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

## Weather

`tools/weather.html` is added to the website by `tools/build_site.py` (not to the Claude guide). It fetches forecasts live in the visitor's browser from Open-Meteo (free, CC BY 4.0, Met Office data) and stores nothing on the device.
- Header pill: Swansea, now. Tap for today's range, rain chance and wind.
- Event panel: a Weather line for the venue's area, on the event's day. Hourly at the start time up to 5 days ahead, daily summary for days 6 to 10, "Forecast from <date>" beyond that. Indoor events show it as "For the journey".
- Venues are matched to 31 places by keywords in the venue and area; coordinates came from Open-Meteo's geocoding service. A new town not in the list falls back to Swansea: add it to PLACES and RULES.

## Save to your calendar

`tools/calendar.html` (added by `tools/build_site.py`, website only) replaces the guide's Google/Outlook row:
- Asks "Which date are you going?" when an event has several upcoming dates (chips up to 8, a list beyond), unless the event was opened from a day in the Calendar tab.
- iPhone, iPad and Mac: one "Add to my calendar" button that opens Apple Calendar. Android: the same button offers Google Calendar, Phone calendar (Samsung and others) and Outlook. Computers: Google, Outlook, Apple or other.
- Apple and phone calendars get a calendar file from `netlify/functions/ics.mjs` with reminders at 6pm the evening before and 2 hours before the published start. Google and Outlook links cannot carry reminders.
- Times are saved only when the organiser published one clear start and finish, otherwise all day (same rule as the guide).
