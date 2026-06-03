## Example Dashboard

A complete Home Assistant World Cup dashboard example is included in this repository.

### Included Example

```text
examples/world_cup_dashboard.yaml
```

The example dashboard includes:

- Group Stage page
- Fixtures & Results page
- Knockout Stage page
- Live match cards
- Latest results cards
- Tournament countdown
- Tournament progress
- Neon World Cup styling

### How To Use

1. Install the World Cup 2026 integration through HACS.
2. Add the integration in Home Assistant.
3. Enter your own Football-Data.org API key.
4. Install `card-mod` from HACS Frontend.
5. Create a new dashboard in Home Assistant.
6. Open the raw configuration editor.
7. Paste the contents of:

```text
examples/world_cup_dashboard.yaml
```

8. Save the dashboard.

### Background Images

The example dashboard may include `media-source://image_upload/...` background references from the original setup. These are local to each Home Assistant install.

If the background images do not show, upload your own World Cup background images through the Home Assistant dashboard editor.
