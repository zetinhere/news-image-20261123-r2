# news-image-20261123-r2

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/zetinhere/news-image-20261123-r2/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/zetinhere/news-image-20261123-r2/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

The World in One Day — Monday 23 November 2026: a program that draws one image summing up the day's world news — COP31 climate talks collapse in Antalya with no deal on fossil fuels; Iran strikes Bahrain and tankers are hit near the Strait of Hormuz; a Russian drone destroys flats in Dymer, Ukraine, leaving 14 missing; Mexico captures cartel boss 'El Chapo Isidro'; the World Court rules Myanmar guilty of genocide against the Rohingya; a factory fire in Indonesia kills 3 with 36 workers missing; and Democrats take their largest House majority since 1992.

## Run it

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`draw.py` draws `entry.png` from scratch with PIL (no network, no downloaded images); `main.ts` copies it to the output directory, world-readable.

---

<sub>Entered on [make.fun](https://make.fun/?ref=jc69fpy6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
