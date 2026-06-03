# ⚽ FIFA World Cup 2026 for Home Assistant

Live FIFA World Cup 2026 fixtures, groups, knockout rounds, statistics, top scorers, assists and match tracking directly inside Home Assistant.

Built for Home Assistant with HACS support.

---

## 🏆 Support Development

Enjoying the integration?

Help keep the project alive and improving by supporting development.

### 💙 Donate via PayPal

👉 **https://paypal.me/graffidoodle**

Every contribution helps fund:

* ⚽ New Features
* 📊 Enhanced Statistics
* 🏟️ Match Data Improvements
* 🔧 Ongoing Maintenance
* 🏆 Dashboard Examples

**Thank you for supporting the World Cup 2026 Integration!**

---

## ✨ Features

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

* Last 32
* Last 16
* Quarter Finals
* Semi Finals
* Third Place Playoff
* Final

### Tournament Statistics

* Total Goals
* Matches Played
* Matches Remaining
* Tournament Progress
* Goals Per Match
* Current Stage
* Teams Remaining
* Eliminated Teams
* Live Goals
* Countdown to Kickoff
* Days Until Final

### Tournament Records

* Biggest Win
* Highest Scoring Match
* Latest Result
* Top Scoring Team
* Best Defence

### Player Statistics

* Top Scorer
* Top Scorers Table
* Top Assist
* Top Assists Table

---

## 📸 Screenshots

Add screenshots to your repository like this:

```text
ha-world-cup-2026/
├── screenshots/
│   ├── overview.png
│   ├── golden-boot.png
│   ├── top-assists.png
│   ├── knockout-stage.png
│   └── stats-hub.png
```

Then display them in this README using:

```markdown
## Screenshots

### Tournament Overview

![Tournament Overview](screenshots/overview.png)

### Golden Boot Race

![Golden Boot Race](screenshots/golden-boot.png)

### Top Assists

![Top Assists](screenshots/top-assists.png)

### Knockout Stage

![Knockout Stage](screenshots/knockout-stage.png)

### Stats Hub

![Stats Hub](screenshots/stats-hub.png)
```

Recommended screenshot size:

```text
1200 x 800 px
```

or normal Home Assistant mobile screenshots also work fine.

---

## 📦 Installation

### HACS

1. Open HACS
2. Go to **Integrations**
3. Click the three dots menu
4. Select **Custom Repositories**
5. Add this repository:

```text
https://github.com/Adya84/ha-world-cup-2026
```

6. Category: **Integration**
7. Install **World Cup 2026**
8. Restart Home Assistant

---

## ⚙️ Configuration

1. Obtain a free API key from Football-Data.org
2. Go to:

```text
Settings → Devices & Services → Add Integration
```

3. Search for:

```text
World Cup 2026
```

4. Enter your API key
5. Submit

---

## 🧩 Available Sensors

### Core Sensors

```text
sensor.world_cup_fixtures
sensor.world_cup_standings
sensor.world_cup_next_match
sensor.world_cup_live_matches
sensor.world_cup_today_matches
sensor.world_cup_tomorrow_matches
sensor.world_cup_completed_matches
```

### Group Sensors

```text
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

```text
sensor.world_cup_last_32
sensor.world_cup_last_16
sensor.world_cup_quarter_finals
sensor.world_cup_semi_finals
sensor.world_cup_third_place
sensor.world_cup_final
```

### Tournament Statistics Sensors

```text
sensor.world_cup_total_matches_played
sensor.world_cup_matches_remaining
sensor.world_cup_progress
sensor.world_cup_total_goals
sensor.world_cup_goals_per_match
sensor.world_cup_teams_remaining
sensor.world_cup_current_stage
sensor.world_cup_eliminated_teams
sensor.world_cup_live_goals
sensor.world_cup_countdown
sensor.world_cup_days_until_final
```

### Player Statistics Sensors

```text
sensor.world_cup_top_scorer
sensor.world_cup_top_scorers
sensor.world_cup_top_assist
sensor.world_cup_top_assists
```

### Tournament Record Sensors

```text
sensor.world_cup_biggest_win
sensor.world_cup_highest_scoring_match
sensor.world_cup_latest_result
sensor.world_cup_top_scoring_team
sensor.world_cup_best_defence
```

---

## 🏠 Example Dashboard Ideas

You can build Home Assistant dashboard cards for:

* 🏆 Tournament Overview
* ⏳ Countdown to Kickoff
* 👟 Golden Boot Race
* 🎯 Top Assists Table
* 🏆 Golden Boot Podium
* 📊 World Cup Stats Hub
* 🔥 Tournament Records
* 🌍 Group Stage Fixtures
* 🏆 Knockout Stage Tracker
* ⚽ Live Match Centre
* 📰 Latest Result Card

---

## ⚠️ State Size Note

The main fixtures sensor limits its fixture attributes to avoid Home Assistant state size issues.

Tournament progress is based on the official World Cup total of:

```text
104 matches
```

This avoids incorrect progress calculations when fixture attributes are limited.

---

## 🔄 Live Updates

Powered by Football-Data.org with automatic updates throughout the FIFA World Cup 2026 tournament.

---

## ✅ Requirements

* Home Assistant 2024.1+
* HACS
* Football-Data.org API Key

---

## ⚠️ Disclaimer

This integration is an independent community project.

It is not affiliated with FIFA, FIFA World Cup, Home Assistant, HACS or Football-Data.org.

---

Created by **Adrian Apel**.
