# Find similar startups

This is a demo of [startupradar.co](https://startupradar.co)'s API 
combined with OpenAI embeddings
to find similar startups.

The code works as follows:
1. load the list of startup domains in `domains.txt`
2. fetch descriptions of these startups with startupradar's API
3. create embeddings for all startups with OpenAI
4. compute cosine similarities between all pairs
5. output a similarity matrix as `similarity_matrix.csv`

The formatted output looks like this:

![](.github/screenshot.png)

and the provided sample can be found in a [public Google Sheet](https://docs.google.com/spreadsheets/d/1WGsrq6eUC3bdFoV7pMVgbqqbyaBtjxl2cr_dMV0TVHA/).


## Installation and Usage

Install the dependencies into a virtual environment.

```commandline
pip install -r requirements.txt
```

Create a `config.py` file and add the credentials for startupradar and OpenAI:

```python
STARTUPRADAR_API_KEY = "your-key-here"

OPENAI_API_KEY = "your-key-here"
OPENAI_ENGINE = "text-similarity-davinci-001"
```

An API key for OpenAI can be created online.
Please note that embedding a lot of startups can result in significant charges.
Make sure to set budgets upfront!

Run with

```commandline
python cli.py run
```

## Competitor and Lookalikes API

Looking for a ready-to-use solution? 
Skip the setup and get instant results with our [Competitor and Lookalikes API](https://markets.apistemic.com).

### Why use our API instead of building your own?
This demo shows the technical approach, but running it yourself means:

- Managing OpenAI API costs and rate limits
- Maintaining startup data freshness
- Handling embedding computation at scale
- Building your own similarity algorithms

Our API handles all of this for you with a simple REST endpoint.

### What you get

- Instant competitor detection - Submit any company domain or identifier
- Fresh startup data - Always up-to-date company information
- Pre-computed similarities - No waiting for embeddings or calculations
- Multiple similarity types - Find direct competitors and lookalikes
- Scalable pricing - Pay only for what you use

Examples:

- [Uber](https://markets.apistemic.com/companies/uber-com-ojj2j)
- [Crunchbase](https://markets.apistemic.com/companies/crunchbase-ay7e7)
- [Lufthansa](https://markets.apistemic.com/companies/lufthansa-e93bz)
- [OpenAI](https://markets.apistemic.com/companies/openai-je9z5)

### Use cases

- Market research - Quickly map competitive landscapes
- Investment analysis - Find comparable companies for valuation
- Sales prospecting - Identify similar companies as potential customers
- Partnership discovery - Find complementary businesses
- Competitive intelligence - Stay updated on similar companies

### Get started
Sign up at [markets.apistemic.com](https://markets.apistemic.com) 
and start finding similar companies in seconds, not hours.
