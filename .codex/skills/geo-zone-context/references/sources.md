# Sources

This skill uses the French public geographic API:

```text
GET https://geo.api.gouv.fr/communes
```

The request searches by commune name or postal code and asks for:

- commune name;
- INSEE code;
- postal codes;
- population;
- department;
- region;
- commune center coordinates.

## Limits

- Coordinates are approximate and represent the commune center.
- Population values depend on the source freshness.
- This context is useful for orientation, not for field-level operational mapping.
