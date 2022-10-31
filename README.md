# BSI (Black Swan Indicator) Notes & README

## VIX tl;dr

`The volatility index has a strong negative correlation to the S&P 500. Generally when markets fall, the volatility index climbs and vice versa.`





## VIX Investing Highlights

`Investing in the VIX generally requires the use of derivatives. As a result of this investment style there is a decay on all volatility related ETF's. In this example we are analyzing 'UVXY' a fund which attempts to mimic 2X the performance on the volatility index. Because of this, that decay factor is dramatically increased. With that leverage comes the burden of paying interest on borrowed funds and management fees. For this reason, UVXY was chosen for this analysis as a "short" opportunity to capitalize on the decay factor when it is also likely that UVXY will fall. Generall investing in UVXY requires options or a straight "short" position. With options the results are more profitable but should only be used during a "sell" trigger. With shorting, this can be done at almost any time the volatility index isn't well below its standard (roughly 17 handle) value. This program primarily deals with the options trading portion but finding an entry point to "short" the fund is also useful with "buy" and "sell" triggers.`

## UVXY (Volatility Index 2X Performance ETF) Calculation Notes

`UVXY's heavy decay factor means the 30 day MACD calculation will not mean much because the further we get into the data the more of a drop off we are going to see which will heavilty influence the MACD line to trigger us to "BUY" when no such trigger should be given. This is because it does not realize the artificial "dropoffs" are more of a result of decay than of market movements. For this reason a 5 day MACD is the only useable time period for UVXY swing trading.`

- Given the short-term nature of UVXY it should never be held for longer than a week.
- Intra day MACD lines are far more valuable in analyzing UVXY for day trading than Weekly MACD lines for swing trading
    - This program does not focus on day trading but rather on opportunities to short UVXY and capitalize on both market movements and the decay factor. For this reason, intra-day data has not been gathered and will not be gathered.
