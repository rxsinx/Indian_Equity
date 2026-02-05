# 📖 User Guide - Indian Equity Market Analyzer

## Table of Contents
1. [Getting Started](#getting-started)
2. [Understanding the Interface](#understanding-the-interface)
3. [Reading the Analysis](#reading-the-analysis)
4. [Pattern Recognition Guide](#pattern-recognition-guide)
5. [Risk Management Guide](#risk-management-guide)
6. [Example Use Cases](#example-use-cases)
7. [Best Practices](#best-practices)

---

## 1. Getting Started

### Accessing the Application

#### Option 1: Online (Streamlit Cloud)
- Open your browser
- Navigate to the deployed URL
- No installation required!

#### Option 2: Local Installation
1. Install Python 3.8+
2. Clone repository
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `streamlit run app.py`
5. Open `http://localhost:8501`

### First Time Use

1. **Enter Stock Symbol**
   - Type NSE symbol WITHOUT `.NS` suffix
   - Examples: `RELIANCE`, `TCS`, `INFY`, `HDFCBANK`
   
2. **Select Time Period**
   - For swing trading: 3-6 months
   - For position trading: 1-2 years
   - For long-term analysis: 2-5 years

3. **Click "Analyze Stock"**
   - Wait 5-10 seconds for data fetching
   - Analysis will be displayed automatically

---

## 2. Understanding the Interface

### Main Sections

#### A. Company Overview (Top Section)
**Displays:**
- Company name and sector
- Market capitalization
- Industry classification
- Key ratios (P/E, P/B, Beta)
- Dividend yield
- Current price metrics

**How to Read:**
- **Market Cap:** Larger = more stable, smaller = more volatile
- **P/E Ratio:** Compare with sector average
- **Beta:** >1 = more volatile than market, <1 = less volatile
- **Dividend Yield:** Income generation potential

#### B. Trading Signal (Second Section)
**Components:**
- Overall signal (Strong Buy to Strong Sell)
- Signal strength score (out of 7)
- Individual indicator signals
- Detailed breakdown

**Signal Colors:**
- 🟢 Green = Bullish/Buy signals
- 🔴 Red = Bearish/Sell signals
- 🟡 Yellow = Neutral/Hold signals
- ⚠️ Warning = Caution required

#### C. Risk Management Parameters
**Key Metrics:**
- **Entry Price:** Current market price
- **Stop Loss:** Where to exit if trade goes wrong
- **Target 1 & 2:** Profit-taking levels
- **Risk/Reward Ratios:** Expected gain vs potential loss
- **Risk per Share:** Amount at risk per share

#### D. Pattern Detection
**Two Tabs:**

**Tab 1: Dan Zanger Patterns**
- Cup and Handle
- High Tight Flag
- Ascending Triangle
- Flat Base
- Falling Wedge

**Tab 2: Qullamaggie Patterns**
- Breakout (VDU)
- Episodic Pivot (EP)
- Parabolic Short

#### E. Technical Charts
**Two Tabs:**

**Tab 1: Price Action & Indicators**
- Candlestick chart
- Moving averages (SMA 20/50/200, EMA 10/20)
- Bollinger Bands
- VWAP
- MACD histogram
- RSI indicator
- Volume bars

**Tab 2: Volume Profile**
- Horizontal volume distribution
- Point of Control (POC)
- Value Area (70% volume zone)
- High/Low Volume Nodes

---

## 3. Reading the Analysis

### Understanding Trading Signals

#### Strong Buy (Score: 4-7)
**Characteristics:**
- Price above all major moving averages
- MACD bullish crossover
- RSI in healthy range (40-60)
- Above average volume
- Multiple bullish patterns detected

**Action:**
- Consider initiating long position
- Set stop loss as indicated
- Target profits at specified levels
- Follow position sizing rules (1% risk)

#### Buy (Score: 2-3)
**Characteristics:**
- Price above some moving averages
- Mixed indicator signals
- Some bullish patterns present
- Moderate volume

**Action:**
- Potential entry but with caution
- Tighter stop loss recommended
- Smaller position size
- Monitor closely

#### Hold (Score: -1 to 1)
**Characteristics:**
- Neutral technical setup
- Conflicting signals
- Consolidation phase
- No clear pattern

**Action:**
- If holding: maintain position
- If not in: wait for better setup
- Monitor for breakout
- No rush to enter

#### Sell (Score: -3 to -2)
**Characteristics:**
- Price below key moving averages
- MACD bearish crossover
- Weakening momentum
- Below average volume

**Action:**
- Consider exiting long positions
- Avoid new long entries
- Protect profits
- Watch for support levels

#### Strong Sell (Score: -7 to -4)
**Characteristics:**
- Price below all moving averages
- Multiple bearish signals
- High RSI (overbought) or parabolic move
- Distribution pattern

**Action:**
- Exit all long positions
- Consider short positions (if allowed)
- Stay in cash
- Wait for stabilization

---

## 4. Pattern Recognition Guide

### Cup and Handle Pattern

**Visual Characteristics:**
```
         ____
        /    \____  ← Handle (consolidation)
       /          \
      /            \  ← Cup (U-shape)
     /              \
────/                \────
    ↑                ↑
  Start            Bottom
```

**What to Look For:**
1. **Cup Formation:** 7-8 weeks minimum
2. **Depth:** 12-33% decline from high
3. **Handle:** 1-4 weeks, tight consolidation
4. **Volume:** Decreasing in handle
5. **Breakout:** Must be with 3x volume

**Trading Rules:**
- Entry: Above handle resistance
- Stop: Below handle low
- Target: Cup depth added to breakout
- Hold: Minimum 4-8 weeks

**Example:**
```
Stock: RELIANCE
Cup: ₹2400 → ₹1800 → ₹2350 (8 weeks)
Handle: ₹2350 → ₹2250 → ₹2330 (3 weeks)
Breakout: ₹2360 with high volume
Target: ₹2960 (₹600 cup depth + ₹2360)
Stop: ₹2230 (below handle)
```

### High Tight Flag

**Visual Characteristics:**
```
       ╱╱╱
      ╱╱╱     ← Tight flag (3-5 weeks)
     ╱╱╱
    ╱╱
   ╱╱         ← Pole (strong uptrend)
  ╱╱
 ╱╱
──
```

**What to Look For:**
1. **Pole:** 20%+ gain in 4-8 weeks
2. **Flag:** <15% pullback, tight range
3. **Duration:** 3-5 weeks consolidation
4. **Volume:** Drying up in flag
5. **Breakout:** Explosive volume

**Trading Rules:**
- Entry: Above flag high
- Stop: 2% below entry
- Target: 30-50% from breakout
- Hold: 4-12 weeks

**Example:**
```
Stock: TCS
Pole: ₹3000 → ₹3700 (+23% in 6 weeks)
Flag: ₹3700 → ₹3550 → ₹3650 (4 weeks)
Breakout: ₹3720 with massive volume
Target 1: ₹4640 (+25% from ₹3720)
Target 2: ₹5580 (+50% from ₹3720)
Stop: ₹3645 (-2% from ₹3720)
```

### Episodic Pivot (EP)

**Visual Characteristics:**
```
              ___
             |   |  ← Gap up
    ____     |   |
   |    |____|   |
___|            Volume spike ↑↑↑
```

**What to Look For:**
1. **Catalyst:** News, earnings, sector rotation
2. **Gap:** 2-5% gap up at open
3. **Volume:** 10x+ normal in first 15 min
4. **ORH:** Opening Range High established
5. **Follow-through:** Price stays above ORH

**Trading Rules:**
- Entry: Above ORH after 1-5 min
- Stop: Loss of day (LOD)
- Target: 3-5% intraday
- Hold: 3-5 days max

**Example:**
```
Stock: INFY (Earnings Beat)
Previous Close: ₹1500
Opening: ₹1575 (5% gap)
ORH (first 5 min): ₹1585
Entry: ₹1590 above ORH
Stop: ₹1520 (LOD)
Target: ₹1640 (3% from entry)
Exit: Day 3 at ₹1625
```

### Parabolic Short Setup

**Visual Characteristics:**
```
          ╱  ← Extended from moving avg
         ╱
        ╱
       ╱
      ╱
──────EMA────────  ← 10/20 EMA far below
```

**What to Look For:**
1. **Vertical Move:** >15% from 10/20 EMA
2. **Duration:** Unsustainable pace
3. **Volume:** Climactic (very high)
4. **Sentiment:** Euphoria, news coverage
5. **First Crack:** Break of previous low

**Trading Rules:**
- Entry: First close below prev day low
- Stop: Above recent high
- Target: 10/20 EMA (mean reversion)
- Hold: 2-5 days

**Example:**
```
Stock: TATAMOTORS
Price: ₹1000
10 EMA: ₹850 (15% below)
20 EMA: ₹820 (18% below)
First Crack: Close at ₹980 (below ₹990)
Entry: ₹975 next morning
Stop: ₹1020 (recent high)
Target: ₹850 (10 EMA)
Exit: ₹870 after 4 days
```

---

## 5. Risk Management Guide

### Position Sizing

**The 1% Rule:**
Never risk more than 1% of your portfolio on a single trade.

**Calculation:**
```
Portfolio: ₹10,00,000
Max Risk per Trade: ₹10,000 (1%)
Stock Price: ₹500
Stop Loss: ₹475 (5% below entry)
Risk per Share: ₹25

Position Size = Max Risk ÷ Risk per Share
Position Size = ₹10,000 ÷ ₹25 = 400 shares
Total Investment = 400 × ₹500 = ₹2,00,000
```

### Stop Loss Strategy

**Types of Stops:**

1. **ATR-based Stop** (Dynamic)
   - Stop = Entry - (2 × ATR)
   - Adjusts to volatility
   - Wider for volatile stocks

2. **Percentage Stop** (Fixed)
   - Stop = Entry × 0.98 (2% stop)
   - Simple and consistent
   - Dan Zanger's 8% absolute rule

3. **Support-based Stop** (Technical)
   - Stop below key support
   - Pattern-specific
   - Example: Below handle in cup pattern

**Use the WIDER of:**
- ATR stop
- Percentage stop
- Technical stop

### Profit Targets

**Conservative Strategy:**
```
Entry: ₹1000
Target 1: ₹1150 (15% gain)
Target 2: ₹1300 (30% gain)

Action:
- Sell 50% at Target 1
- Sell 25% at Target 2
- Trail remaining 25% with 10/20 SMA
```

**Aggressive Strategy:**
```
Entry: ₹1000
Target 1: ₹1200 (20% gain)
Target 2: ₹1500 (50% gain)

Action:
- Sell 33% at Target 1
- Sell 33% at Target 2
- Hold 34% for home run (trail with stop)
```

### Trade Management Examples

**Example 1: Successful Trade**
```
Entry: ₹500 (200 shares = ₹1,00,000)
Stop: ₹475 (Risk = ₹5,000)
Target 1: ₹575 (15%)
Target 2: ₹650 (30%)

Execution:
Day 1: Buy 200 shares @ ₹500
Day 15: Hits ₹575 - Sell 100 shares (₹7,500 profit)
Day 30: Hits ₹650 - Sell 50 shares (₹7,500 profit)
Day 45: Trail 50 shares to ₹700, exit @ ₹680 (₹9,000 profit)

Total Profit: ₹24,000 (24% on ₹1,00,000)
Risk/Reward: 24% gain vs 5% risk = 4.8:1
```

**Example 2: Stopped Out**
```
Entry: ₹500 (200 shares = ₹1,00,000)
Stop: ₹475
Target: ₹575

Execution:
Day 1: Buy 200 shares @ ₹500
Day 3: Drops to ₹475 - Stop triggered
Exit: Sell 200 shares @ ₹475

Total Loss: ₹5,000 (5% loss)
Impact on Portfolio: 0.5% (assuming ₹10L portfolio)
```

---

## 6. Example Use Cases

### Use Case 1: Momentum Trading

**Objective:** Capture 20-30% gains in 4-8 weeks

**Process:**
1. Run analyzer on high-momentum stocks
2. Look for Cup & Handle or High Tight Flag
3. Confirm with STRONG BUY signal
4. Check volume profile for breakout zones
5. Enter on breakout with 3x volume
6. Set stop at -8% (Zanger's rule)
7. Target 20-30% gain
8. Exit 50% at +20%, trail rest

**Example:**
- Stock: RELIANCE
- Pattern: Cup and Handle
- Signal: STRONG BUY (Score: 6)
- Entry: ₹2500 on breakout
- Stop: ₹2300 (8% stop)
- Target 1: ₹3000 (20%)
- Target 2: ₹3250 (30%)
- Result: Exit at ₹3100 (24% gain in 6 weeks)

### Use Case 2: Swing Trading

**Objective:** Quick 5-15% gains in 3-5 days

**Process:**
1. Scan for Episodic Pivot patterns
2. Wait for gap up with huge volume
3. Enter above Opening Range High
4. Set tight stop at Loss of Day
5. Target 5-10% intraday to 3-day
6. Exit quickly, don't overstay

**Example:**
- Stock: INFY (Earnings)
- Pattern: Episodic Pivot
- Gap: 4% up at open
- Entry: ₹1585 above ORH
- Stop: ₹1520 (LOD)
- Target: ₹1650 (4%)
- Result: Exit Day 2 at ₹1635 (3.2% gain)

### Use Case 3: Mean Reversion

**Objective:** Profit from overextended moves

**Process:**
1. Find stocks with Parabolic Short setup
2. Wait for "first crack" signal
3. Enter short or reduce long exposure
4. Target reversion to 10/20 EMA
5. Exit on mean reversion or bounce

**Example:**
- Stock: XYZ (Parabolic move)
- Setup: 18% above 20 EMA
- Entry: ₹1000 (after first crack)
- Stop: ₹1050 (recent high)
- Target: ₹850 (20 EMA)
- Result: Exit at ₹870 (13% gain in 5 days)

---

## 7. Best Practices

### Before Trading

✅ **DO:**
- Analyze multiple stocks
- Compare signals across timeframes
- Check volume profile
- Verify pattern quality
- Calculate position size
- Set stop loss BEFORE entry
- Have profit target plan
- Check market conditions

❌ **DON'T:**
- Trade based on single indicator
- Ignore volume
- Trade without stop loss
- Risk more than 1% per trade
- Chase stocks already extended
- Trade during high volatility without plan
- Ignore risk/reward ratio

### During Trade

✅ **DO:**
- Follow your plan
- Use stop loss religiously
- Take partial profits
- Trail winners
- Keep emotions in check
- Journal your trades
- Monitor market conditions

❌ **DON'T:**
- Move stop loss away from entry
- Add to losing positions
- Panic sell on minor dips
- Get greedy and skip profits
- Ignore exit signals
- Trade on emotion
- Revenge trade after loss

### After Trade

✅ **DO:**
- Review what worked/didn't work
- Journal entry/exit reasoning
- Calculate actual R:R achieved
- Learn from mistakes
- Update strategy if needed
- Track win rate and avg gain
- Celebrate disciplined execution

❌ **DON'T:**
- Dwell on losses
- Get overconfident after wins
- Forget to update journal
- Repeat same mistakes
- Ignore what data shows
- Trade to recover losses

---

## 8. Quick Reference Checklist

### Pre-Trade Checklist
```
□ Stock shows clear pattern
□ Trading signal is BUY or STRONG BUY
□ Volume profile supports move
□ Entry point identified
□ Stop loss calculated
□ Position size determined (1% rule)
□ Profit targets set
□ Risk/Reward > 2:1
□ Market conditions favorable
□ Emotional state checked
```

### Trade Execution Checklist
```
□ Entered at planned price
□ Stop loss order placed
□ Profit target alert set
□ Trade logged in journal
□ Portfolio allocation within limits
□ Can afford to lose this amount
□ Have reviewed trade plan
```

### Trade Management Checklist
```
□ Monitor daily (not hourly)
□ Honor your stop loss
□ Take profits as planned
□ Trail winners systematically
□ Don't add to losers
□ Update stop to breakeven when up 5%
□ Review weekly performance
```

---

## Keyboard Shortcuts

- `Ctrl + R` - Refresh analysis
- `Ctrl + S` - Save current view (browser)
- `Ctrl + P` - Print report
- `F5` - Reload page

---

## Tips for Success

1. **Start Small:** Begin with 1-2 stocks, master the patterns
2. **Paper Trade First:** Test strategies without real money
3. **Follow the Rules:** Discipline beats strategy
4. **Be Patient:** Wait for high-quality setups
5. **Journal Everything:** Learn from every trade
6. **Manage Risk First:** Profits will follow
7. **Never Stop Learning:** Markets evolve, so should you

---

## Common Mistakes to Avoid

1. ❌ **Not using stop losses**
2. ❌ **Position size too large**
3. ❌ **Chasing extended stocks**
4. ❌ **Ignoring volume**
5. ❌ **Trading during low liquidity**
6. ❌ **Not having exit plan**
7. ❌ **Emotional decision making**
8. ❌ **Overtrading**
9. ❌ **Revenge trading**
10. ❌ **Not learning from mistakes**

---

**Remember:** This tool provides analysis, not advice. Always do your own research and trade responsibly!

---

For more help, refer to:
- README.md - General information
- DEPLOYMENT_GUIDE.md - Technical setup
- GitHub Issues - Community support
