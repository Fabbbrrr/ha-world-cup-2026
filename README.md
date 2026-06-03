
# ⚽ FIFA World Cup 2026 Integration

---

## 🏆 Support Development

Enjoying the integration?

Help keep the project alive and improving by supporting development.

### 💙 Donate via PayPal

👉 **https://paypal.me/graffidoodle**

Every contribution helps fund:

⚽ New Features  
📊 Enhanced Statistics  
🏟️ Match Data Improvements  
🔧 Ongoing Maintenance

**Thank you for supporting the World Cup 2026 Integration!**
# ⚽ World Cup 2026 for Home Assistant

Live FIFA World Cup 2026 fixtures, groups, knockout rounds, statistics and match tracking directly inside Home Assistant.

## Features

### Fixtures

* Next Match
* Live Matches
* Today's Matches
* Tomorrow's Matches
* Completed Matches
* Full Tournament Fixture List

### Groups

* Group A
* Group B
* Group C
* Group D
* Group E
* Group F
* Group G
* Group H
* Group I
* Group J
* Group K
* Group L

### Knockout Stages

* Round of 32
* Round of 16
* Quarter Finals
* Semi Finals
* Third Place Playoff
* Final

### Statistics

* Total Goals
* Matches Played
* Teams Remaining

### Live Updates

Powered by Football-Data.org with automatic updates throughout the tournament.

---

## Installation

### HACS

1. Open HACS
2. Navigate to Integrations
3. Click the three dots menu
4. Select Custom Repositories
5. Add:

```
https://github.com/Adya84/ha-world-cup-2026
```

6. Category: Integration
7. Install World Cup 2026
8. Restart Home Assistant

---

## Configuration

1. Obtain a free API key from Football-Data.org
2. Go to:

Settings → Devices & Services → Add Integration

3. Search for:

```
World Cup 2026
```

4. Enter your API key

---

## Available Sensors

### Core Sensors

```
sensor.world_cup_fixtures
sensor.world_cup_next_match
sensor.world_cup_live_matches
sensor.world_cup_today_matches
sensor.world_cup_tomorrow_matches
sensor.world_cup_completed_matches
```

### Group Sensors

```
sensor.world_cup_group_a
sensor.world_cup_group_b
sensor.world_cup_group_c
sensor.world_cup_group_d
sensor.world_cup_group_e
sensor.world_cup_group_f
sensor.world_cup_group_g
sensor.world_cup_group_h
sensor.world_cup_group_i
sensor.world_cup_group_j
sensor.world_cup_group_k
sensor.world_cup_group_l
```

### Knockout Stage Sensors

```
sensor.world_cup_last_32
sensor.world_cup_last_16
sensor.world_cup_quarter_finals
sensor.world_cup_semi_finals
sensor.world_cup_third_place
sensor.world_cup_final
```

### Statistics Sensors

```
sensor.world_cup_total_goals
sensor.world_cup_total_matches_played
sensor.world_cup_teams_remaining
```

---

## Example Dashboard

Display:

* Upcoming fixtures
* Live scores
* Group stage matches
* Knockout bracket progression
* Tournament statistics

All data updates automatically during the FIFA World Cup 2026 tournament.

---

## Requirements

* Home Assistant 2024.1+
* HACS
* Football-Data.org API Key

---

## Disclaimer

This integration is an independent community project and is not affiliated with FIFA or Football-Data.org.

---

Created by Adrian Apel
