# Sources

This skill combines:

```text
GET https://geo.api.gouv.fr/communes
GET https://api.open-meteo.com/v1/forecast
```

The geographic API resolves a commune name or postal code to approximate coordinates.
Open-Meteo then returns current weather values for those coordinates.

## Values Used

- temperature at 2 meters;
- relative humidity at 2 meters;
- precipitation;
- wind speed at 10 meters.

## Limits

- Open-Meteo is used for context, not official vigilance.
- For official French alerts, check Meteo-France and competent authorities.
- Weather data must be interpreted with the time, place and operational context.
