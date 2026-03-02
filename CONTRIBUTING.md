# Contributing to Climate & Energy Intelligence Hub

Thank you for your interest in contributing! This hub is a community-driven registry of climate and energy intelligence resources.

## Ways to Contribute

### 1. Add a new model, dataset, or tool

**Via GitHub Issues (easiest):**

1. Go to [Issues](../../issues)
2. Click "New issue"
3. Select the appropriate template:
   - "Add Model" for energy system models
   - "Add Dataset" for grid/resource/socioeconomic datasets
   - "Add Pipeline" for data extraction or transformation tools
4. Fill in all required fields
5. Submit the issue

**Via Pull Request (for multiple entries):**

1. Fork the repository
2. Add your entries to the appropriate YAML file:
   - `data/models.yaml` for energy models
   - `data/datasets.yaml` for datasets
   - `data/pipelines.yaml` for pipelines
   - `data/climate_fms.yaml` for climate FMs
3. Ensure your entry follows the schema in `docs/schema.md`
4. Run `python -m yaml data/your-file.yaml` to validate
5. Create a pull request

### 2. Update existing entries

If you find incorrect or outdated information:

1. Open an issue or
2. Submit a PR with corrections directly

### 3. Improve documentation

Contributions to docs/, README, examples, and tutorials are welcome!

## Schema Compliance

All entries must follow the schema defined in `docs/schema.md`.

**Required fields for models:**
- `id` (unique slug)
- `name`
- `kind`
- `short_description`
- `domain`
- `scale`
- `model_type`
- `language`

**Required fields for datasets:**
- `id`
- `name`
- `kind`
- `short_description`
- `modality`

See the schema doc for complete reference.

## Code of Conduct

- Be respectful and constructive
- Focus on facts and citations
- Avoid self-promotion beyond factual project descriptions
- When in doubt, open an issue for discussion before submitting large changes

## Review Process

1. New entries are reviewed for schema compliance and accuracy
2. Maintainers may request additional info or corrections
3. Once approved, your PR will be merged and your entry goes live
4. The API auto-updates within minutes

## Questions?

Open a [Discussion](../../discussions) or reach out via issue.

Thank you for making energy intelligence more accessible!
