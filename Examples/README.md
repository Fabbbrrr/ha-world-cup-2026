# Example World Cup 2026 Dashboard

This folder contains a ready-to-copy Home Assistant dashboard example.

## File

- `world_cup_dashboard.yaml` — full dashboard example with:
  - Group Stage page
  - Fixtures & Results page
  - Knockout Stage page
  - Neon card styling
  - Background image support

## Before You Start

Install these first:

1. Home Assistant
2. HACS
3. World Cup 2026 integration
4. card-mod from HACS Frontend

Then add the World Cup 2026 integration in Home Assistant and enter your own Football-Data.org API key.

## Importing the Dashboard

1. In Home Assistant, go to **Settings → Dashboards**.
2. Create a new dashboard called **World Cup 2026**.
3. Open the new dashboard.
4. Click **Edit Dashboard**.
5. Open the **Raw configuration editor**.
6. Copy the contents of `world_cup_dashboard.yaml`.
7. Paste it into the raw editor.
8. Save.

## Important Notes

### Background Images

The example YAML includes background image references from the original dashboard, such as:

```yaml
media-source://image_upload/...
```

These will not exist on another Home Assistant system.

If the backgrounds do not show:

1. Edit the dashboard.
2. Open each view's background settings.
3. Upload your own World Cup background image.
4. Save.

### Required Entities

This dashboard expects World Cup entities such as:

```text
sensor.world_cup_fixtures
sensor.world_cup_next_match
sensor.world_cup_live_matches
sensor.world_cup_today_matches
sensor.world_cup_tomorrow_matches
sensor.world_cup_completed_matches
sensor.world_cup_total_goals
sensor.world_cup_total_matches_played
sensor.world_cup_teams_remaining
```

If you are using older dashboard code that references `sensor.world_cup_standings`, make sure your integration/version also provides standings data, or replace those group-table cards with the newer group fixture sensors.

## Recommended Dashboard Layout

- **Page 1:** Group Stage
- **Page 2:** Fixtures & Results
- **Page 3:** Knockout Stage

## Optional Extras

For the best look, install:

- card-mod
- layout-card
- mushroom cards

