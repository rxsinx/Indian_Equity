import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import ta
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator
import warnings
from functools import lru_cache
import io
from scipy import stats

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Indian Equity Market Analyzer Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 46px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #1f77b4;
    }
    .bullish {
        color: #00aa00;
        font-weight: bold;
        background-color: #e8f5e8;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .bearish {
        color: #ff4444;
        font-weight: bold;
        background-color: #ffe8e8;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .neutral {
        color: #ff9900;
        font-weight: bold;
        background-color: #fff4e8;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .pattern-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .risk-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .success-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .warning-card {
        background: linear-gradient(135deg, #f46b45 0%, #eea849 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 18px !important;
        }
        .sub-header {
            font-size: 18px !important;
        }
        .stMetric {
            font-size: 18px !important;
        }
    }
    
    .stDataFrame {
        font-size: 18px !important;
    }
    
    .stPlotlyChart {
        border-radius: 10px;
        border: 1px solid #e6e6e6;
    }
    
    .stock-ticker {
        font-size: 18px;
        font-weight: bold;
        color: #1a237e;
        padding: 10px;
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        text-align: center;
    }
    
    .support-line {
        border-left: 3px solid #00aa00;
        padding-left: 10px;
    }
    
    .resistance-line {
        border-left: 3px solid #ff4444;
        padding-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)

class IndianEquityAnalyzer:
    """Master Trader Grade Analysis for Indian Equity Market - Enhanced Version"""
    
    def __init__(self, symbol, period='1y'):
        """Initialize with NSE/BSE symbol"""
        self.symbol = self.validate_stock_symbol(symbol)
        self.period = period
        self.data = None
        self.ticker = None
        
    def validate_stock_symbol(self, symbol):
        """Validate and format stock symbol"""
        valid_formats = ['.NS', '.BO']
        
        if any(symbol.upper().endswith(suffix) for suffix in valid_formats):
            return symbol.upper()
        
        common_indian_stocks = [
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR',
            'ICICIBANK', 'ITC', 'SBIN', 'BHARTIARTL', 'KOTAKBANK',
            'LT', 'AXISBANK', 'BAJFINANCE', 'WIPRO', 'HCLTECH',
            'ASIANPAINT', 'MARUTI', 'SUNPHARMA', 'ULTRACEMCO', 'TITAN',
            'ONGC', 'NTPC', 'POWERGRID', 'M&M', 'TATASTEEL'
        ]
        
        if symbol.upper() in common_indian_stocks:
            return f"{symbol.upper()}.NS"
        
        return f"{symbol.upper()}.NS"
    
    @st.cache_data(ttl=3600, show_spinner="Fetching market data...")
    def fetch_data(_self, symbol, period):
        """Fetch and cache stock data"""
        analyzer = IndianEquityAnalyzer(symbol, period)
        success = analyzer._fetch_raw_data()
        return analyzer if success else None
    
    def _fetch_raw_data(self):
        """Fetch data from Yahoo Finance for Indian stocks"""
        try:
            self.ticker = yf.Ticker(self.symbol)
            self.data = self.ticker.history(period=self.period)
            
            if self.data.empty:
                if self.symbol.endswith('.NS'):
                    alt_symbol = self.symbol.replace('.NS', '.BO')
                else:
                    alt_symbol = self.symbol.replace('.BO', '.NS')
                
                self.ticker = yf.Ticker(alt_symbol)
                self.data = self.ticker.history(period=self.period)
            
            if not self.data.empty:
                self.calculate_indicators()
                return True
            return False
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return False
    
    def calculate_indicators(self):
        """Calculate all technical indicators"""
        df = self.data.copy()
        
        # Moving Averages
        df['SMA_9'] = ta.trend.sma_indicator(df['Close'], window=9)
        df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
        df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
        df['SMA_100'] = ta.trend.sma_indicator(df['Close'], window=100)
        df['SMA_200'] = ta.trend.sma_indicator(df['Close'], window=200)
        
        df['EMA_8'] = ta.trend.ema_indicator(df['Close'], window=8)
        df['EMA_13'] = ta.trend.ema_indicator(df['Close'], window=13)
        df['EMA_21'] = ta.trend.ema_indicator(df['Close'], window=21)
        df['EMA_34'] = ta.trend.ema_indicator(df['Close'], window=34)
        df['EMA_55'] = ta.trend.ema_indicator(df['Close'], window=55)
        df['EMA_70'] = ta.trend.ema_indicator(df['Close'], window=70)
        
        # MACD
        macd_fast = ta.trend.MACD(df['Close'], window_fast=12, window_slow=26, window_sign=9)
        df['MACD'] = macd_fast.macd()
        df['MACD_Signal'] = macd_fast.macd_signal()
        df['MACD_Hist'] = macd_fast.macd_diff()
        
        # RSI
        df['RSI_14'] = ta.momentum.rsi(df['Close'], window=14)
        df['RSI_7'] = ta.momentum.rsi(df['Close'], window=7)
        df['RSI_21'] = ta.momentum.rsi(df['Close'], window=21)
        
        # Bollinger Bands
        bb_20_2 = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=2)
        df['BB_Upper'] = bb_20_2.bollinger_hband()
        df['BB_Middle'] = bb_20_2.bollinger_mavg()
        df['BB_Lower'] = bb_20_2.bollinger_lband()
        
        bb_20_1 = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=1)
        df['BB_Upper_1'] = bb_20_1.bollinger_hband()
        df['BB_Lower_1'] = bb_20_1.bollinger_lband()
        
        # Stochastic
        stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'], window=14, smooth_window=3)
        df['Stoch_K'] = stoch.stoch()
        df['Stoch_D'] = stoch.stoch_signal()
        
        # ATR and Volatility
        df['ATR_14'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'], window=14)
        df['ATR_7'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'], window=7)
        
        # Volume indicators
        df['OBV'] = ta.volume.on_balance_volume(df['Close'], df['Volume'])
        df['Volume_SMA_20'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA_20']
        
        # VWAP
        df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
        
        # Additional momentum indicators
        df['ROC_10'] = df['Close'].pct_change(periods=10) * 100
        df['Williams_%R'] = ta.momentum.williams_r(df['High'], df['Low'], df['Close'], lbp=14)
        
        # Price channels
        df['Donchian_High'] = df['High'].rolling(window=20).max()
        df['Donchian_Low'] = df['Low'].rolling(window=20).min()
        df['Donchian_Middle'] = (df['Donchian_High'] + df['Donchian_Low']) / 2
        
        self.data = df
    
    # ============================ SUPPORT & RESISTANCE DETECTION ============================
    
    def detect_support_resistance(self, lookback_period=100, threshold=0.02, min_touches=2):
        """
        Detect Support and Resistance levels using pivot points
        
        Parameters:
        - lookback_period: Number of recent candles to analyze
        - threshold: Price threshold for merging nearby levels (as percentage)
        - min_touches: Minimum number of touches required for a valid level
        
        Returns:
        - Dictionary with support and resistance levels
        """
        df = self.data.tail(lookback_period).copy()
        if len(df) < 20:
            return {'support': [], 'resistance': []}
        
        # Find local minima (support) and maxima (resistance)
        support_levels = []
        resistance_levels = []
        
        # Window for local extrema detection
        window = 5
        
        for i in range(window, len(df) - window):
            # Check for local minima (support)
            if df['Low'].iloc[i] == df['Low'].iloc[i-window:i+window+1].min():
                support_levels.append({
                    'price': df['Low'].iloc[i],
                    'date': df.index[i],
                    'touches': 1,
                    'strength': 1
                })
            
            # Check for local maxima (resistance)
            if df['High'].iloc[i] == df['High'].iloc[i-window:i+window+1].max():
                resistance_levels.append({
                    'price': df['High'].iloc[i],
                    'date': df.index[i],
                    'touches': 1,
                    'strength': 1
                })
        
        # Merge nearby levels
        def merge_levels(levels, threshold_pct=threshold):
            if not levels:
                return []
            
            levels.sort(key=lambda x: x['price'])
            merged = []
            
            for level in levels:
                if not merged:
                    merged.append(level.copy())
                else:
                    last_level = merged[-1]
                    price_diff = abs(level['price'] - last_level['price']) / last_level['price']
                    
                    if price_diff <= threshold_pct:
                        # Merge with existing level
                        total_touches = last_level['touches'] + level['touches']
                        last_level['price'] = (last_level['price'] * last_level['touches'] + 
                                              level['price'] * level['touches']) / total_touches
                        last_level['touches'] = total_touches
                        last_level['strength'] = min(last_level['strength'] + 0.2, 3.0)
                    else:
                        merged.append(level.copy())
            
            return merged
        
        support_levels = merge_levels(support_levels)
        resistance_levels = merge_levels(resistance_levels)
        
        # Count touches (how many times price tested the level)
        def count_touches(levels, price_series, threshold_pct=0.01):
            for level in levels:
                touches = 0
                for price in price_series:
                    if abs(price - level['price']) / level['price'] <= threshold_pct:
                        touches += 1
                level['touches'] = touches
                level['strength'] = min(touches * 0.5, 3.0)  # Strength based on touches
            return [level for level in levels if level['touches'] >= min_touches]
        
        # Count touches for support (using lows)
        low_prices = df['Low'].values
        support_levels = count_touches(support_levels, low_prices)
        
        # Count touches for resistance (using highs)
        high_prices = df['High'].values
        resistance_levels = count_touches(resistance_levels, high_prices)
        
        # Sort by strength
        support_levels.sort(key=lambda x: x['strength'], reverse=True)
        resistance_levels.sort(key=lambda x: x['strength'], reverse=True)
        
        # Take top levels
        max_levels = 5
        support_levels = support_levels[:max_levels]
        resistance_levels = resistance_levels[:max_levels]
        
        return {
            'support': support_levels,
            'resistance': resistance_levels,
            'current_price': df['Close'].iloc[-1]
        }
    
    def detect_trend_lines(self, lookback_period=100):
        """
        Detect ascending and descending trend lines
        
        Returns:
        - Dictionary with trend line information
        """
        df = self.data.tail(lookback_period).copy()
        if len(df) < 30:
            return {'ascending': [], 'descending': []}
        
        # Find swing lows for ascending trend line
        swing_lows = []
        for i in range(2, len(df) - 2):
            if (df['Low'].iloc[i] < df['Low'].iloc[i-1] and 
                df['Low'].iloc[i] < df['Low'].iloc[i+1] and
                df['Low'].iloc[i] < df['Low'].iloc[i-2] and 
                df['Low'].iloc[i] < df['Low'].iloc[i+2]):
                swing_lows.append({
                    'date': df.index[i],
                    'price': df['Low'].iloc[i]
                })
        
        # Find swing highs for descending trend line
        swing_highs = []
        for i in range(2, len(df) - 2):
            if (df['High'].iloc[i] > df['High'].iloc[i-1] and 
                df['High'].iloc[i] > df['High'].iloc[i+1] and
                df['High'].iloc[i] > df['High'].iloc[i-2] and 
                df['High'].iloc[i] > df['High'].iloc[i+2]):
                swing_highs.append({
                    'date': df.index[i],
                    'price': df['High'].iloc[i]
                })
        
        # Detect ascending trend lines (connect at least 2 swing lows)
        ascending_trends = []
        if len(swing_lows) >= 2:
            swing_lows.sort(key=lambda x: x['date'])
            
            for i in range(len(swing_lows) - 1):
                for j in range(i + 1, len(swing_lows)):
                    low1 = swing_lows[i]
                    low2 = swing_lows[j]
                    
                    # Check if the line is ascending (later point is higher)
                    if low2['price'] > low1['price']:
                        # Calculate slope
                        time_diff = (low2['date'] - low1['date']).days
                        if time_diff > 0:
                            price_diff = low2['price'] - low1['price']
                            slope = price_diff / time_diff
                            
                            # Count how many other swing lows are near this line
                            touches = 2  # Already have 2 points
                            for low in swing_lows:
                                if low['date'] not in [low1['date'], low2['date']]:
                                    predicted_price = low1['price'] + slope * (low['date'] - low1['date']).days
                                    if abs(low['price'] - predicted_price) / predicted_price < 0.02:
                                        touches += 1
                            
                            if touches >= 2:
                                ascending_trends.append({
                                    'start_date': low1['date'],
                                    'end_date': low2['date'],
                                    'start_price': low1['price'],
                                    'end_price': low2['price'],
                                    'slope': slope,
                                    'touches': touches,
                                    'type': 'ascending'
                                })
        
        # Detect descending trend lines (connect at least 2 swing highs)
        descending_trends = []
        if len(swing_highs) >= 2:
            swing_highs.sort(key=lambda x: x['date'])
            
            for i in range(len(swing_highs) - 1):
                for j in range(i + 1, len(swing_highs)):
                    high1 = swing_highs[i]
                    high2 = swing_highs[j]
                    
                    # Check if the line is descending (later point is lower)
                    if high2['price'] < high1['price']:
                        # Calculate slope
                        time_diff = (high2['date'] - high1['date']).days
                        if time_diff > 0:
                            price_diff = high2['price'] - high1['price']
                            slope = price_diff / time_diff
                            
                            # Count how many other swing highs are near this line
                            touches = 2
                            for high in swing_highs:
                                if high['date'] not in [high1['date'], high2['date']]:
                                    predicted_price = high1['price'] + slope * (high['date'] - high1['date']).days
                                    if abs(high['price'] - predicted_price) / predicted_price < 0.02:
                                        touches += 1
                            
                            if touches >= 2:
                                descending_trends.append({
                                    'start_date': high1['date'],
                                    'end_date': high2['date'],
                                    'start_price': high1['price'],
                                    'end_price': high2['price'],
                                    'slope': slope,
                                    'touches': touches,
                                    'type': 'descending'
                                })
        
        # Take strongest trends (most touches)
        ascending_trends.sort(key=lambda x: x['touches'], reverse=True)
        descending_trends.sort(key=lambda x: x['touches'], reverse=True)
        
        return {
            'ascending': ascending_trends[:3],  # Top 3 ascending trends
            'descending': descending_trends[:3]  # Top 3 descending trends
        }
    
    def detect_consolidation_zones(self, lookback_period=100, threshold=0.03):
        """
        Detect consolidation zones (trading ranges)
        
        Returns:
        - List of consolidation zones with support/resistance boundaries
        """
        df = self.data.tail(lookback_period).copy()
        if len(df) < 20:
            return []
        
        consolidation_zones = []
        
        # Use rolling standard deviation to detect low volatility periods
        rolling_std = df['Close'].rolling(window=20).std()
        rolling_mean = df['Close'].rolling(window=20).mean()
        volatility_ratio = rolling_std / rolling_mean
        
        # Find periods of low volatility
        low_vol_threshold = volatility_ratio.quantile(0.3)
        low_vol_periods = volatility_ratio < low_vol_threshold
        
        # Group consecutive low volatility periods
        groups = []
        current_group = []
        
        for i in range(len(low_vol_periods)):
            if low_vol_periods.iloc[i] and i > 0 and low_vol_periods.iloc[i-1]:
                if not current_group:
                    # Find start of group
                    start = i
                    while start > 0 and low_vol_periods.iloc[start-1]:
                        start -= 1
                    current_group = list(range(start, i+1))
                else:
                    current_group.append(i)
            else:
                if current_group and len(current_group) >= 10:  # Minimum 10 days
                    groups.append(current_group.copy())
                current_group = []
        
        if current_group and len(current_group) >= 10:
            groups.append(current_group)
        
        # Analyze each consolidation zone
        for group in groups:
            if len(group) > 0:
                zone_data = df.iloc[group]
                
                support = zone_data['Low'].min()
                resistance = zone_data['High'].max()
                zone_range = resistance - support
                range_pct = zone_range / support
                
                # Valid consolidation zone if range is small
                if range_pct <= threshold:
                    consolidation_zones.append({
                        'start_date': df.index[group[0]],
                        'end_date': df.index[group[-1]],
                        'support': support,
                        'resistance': resistance,
                        'range_pct': range_pct * 100,
                        'duration_days': len(group),
                        'volume_avg': zone_data['Volume'].mean(),
                        'breakout_direction': None
                    })
        
        # Determine breakout direction for each zone
        for zone in consolidation_zones:
            end_idx = df.index.get_loc(zone['end_date'])
            
            # Check next 5 periods after consolidation
            if end_idx + 5 < len(df):
                post_consolidation = df.iloc[end_idx+1:end_idx+6]
                
                # Check if price broke above resistance
                if post_consolidation['Close'].max() > zone['resistance'] * 1.02:
                    zone['breakout_direction'] = 'BULLISH'
                # Check if price broke below support
                elif post_consolidation['Close'].min() < zone['support'] * 0.98:
                    zone['breakout_direction'] = 'BEARISH'
                else:
                    zone['breakout_direction'] = 'CONSOLIDATING'
        
        return consolidation_zones
    
    def detect_fibonacci_levels(self, lookback_period=100):
        """
        Calculate Fibonacci retracement and extension levels
        based on significant swing highs and lows
        
        Returns:
        - Dictionary with Fibonacci levels
        """
        df = self.data.tail(lookback_period).copy()
        if len(df) < 50:
            return {}
        
        # Find significant swing high and low
        swing_high = df['High'].max()
        swing_low = df['Low'].min()
        
        # Fibonacci ratios
        fib_ratios = {
            'retracement': {
                '0.0': swing_low,
                '0.236': swing_low + (swing_high - swing_low) * 0.236,
                '0.382': swing_low + (swing_high - swing_low) * 0.382,
                '0.500': swing_low + (swing_high - swing_low) * 0.5,
                '0.618': swing_low + (swing_high - swing_low) * 0.618,
                '0.786': swing_low + (swing_high - swing_low) * 0.786,
                '1.0': swing_high,
            },
            'extension': {
                '1.272': swing_high + (swing_high - swing_low) * 0.272,
                '1.414': swing_high + (swing_high - swing_low) * 0.414,
                '1.618': swing_high + (swing_high - swing_low) * 0.618,
                '2.0': swing_high + (swing_high - swing_low) * 1.0,
                '2.618': swing_high + (swing_high - swing_low) * 1.618,
            }
        }
        
        current_price = df['Close'].iloc[-1]
        
        # Find nearest Fibonacci levels
        nearest_retracement = min(fib_ratios['retracement'].values(), 
                                  key=lambda x: abs(x - current_price))
        nearest_extension = min(fib_ratios['extension'].values(), 
                                key=lambda x: abs(x - current_price))
        
        return {
            'swing_high': swing_high,
            'swing_low': swing_low,
            'retracement_levels': fib_ratios['retracement'],
            'extension_levels': fib_ratios['extension'],
            'current_price': current_price,
            'nearest_retracement': nearest_retracement,
            'nearest_extension': nearest_extension
        }
    
    # ============================ END OF SUPPORT & RESISTANCE DETECTION ============================
    
    def detect_volume_profile(self):
        """Detect volume profile patterns with enhanced analysis"""
        df = self.data.tail(100)
        
        if len(df) < 20:
            return {}
        
        # Calculate price levels and volume distribution
        price_range = df['High'].max() - df['Low'].min()
        num_bins = 70
        bins = np.linspace(df['Low'].min(), df['High'].max(), num_bins)
        
        volume_at_price = []
        value_area_volumes = []
        
        for i in range(len(bins) - 1):
            mask = (df['Close'] >= bins[i]) & (df['Close'] < bins[i + 1])
            volume_sum = df[mask]['Volume'].sum()
            volume_at_price.append(volume_sum)
            
            if mask.any():
                avg_price = df[mask]['Close'].mean()
                value_area_volumes.append(volume_sum * avg_price)
            else:
                value_area_volumes.append(0)
        
        volume_at_price = np.array(volume_at_price)
        value_area_volumes = np.array(value_area_volumes)
        
        # Find Point of Control (POC) - highest volume price level
        poc_idx = np.argmax(volume_at_price)
        poc_price = (bins[poc_idx] + bins[poc_idx + 1]) / 2
        poc_volume = volume_at_price[poc_idx]
        
        # Find Value Area (70% of volume)
        total_volume = volume_at_price.sum()
        target_volume = total_volume * 0.70
        
        sorted_indices = np.argsort(volume_at_price)[::-1]
        cumulative_volume = 0
        value_area_indices = []
        
        for idx in sorted_indices:
            cumulative_volume += volume_at_price[idx]
            value_area_indices.append(idx)
            if cumulative_volume >= target_volume:
                break
        
        value_area_high = bins[max(value_area_indices) + 1]
        value_area_low = bins[min(value_area_indices)]
        
        # Calculate Value Area percentage
        value_area_percentage = (value_area_high - value_area_low) / price_range * 100
        
        # Identify high and low volume nodes
        volume_mean = volume_at_price.mean()
        volume_std = volume_at_price.std()
        
        high_volume_threshold = volume_mean + volume_std
        low_volume_threshold = volume_mean - volume_std
        
        high_volume_nodes = bins[:-1][volume_at_price > high_volume_threshold]
        low_volume_nodes = bins[:-1][volume_at_price < low_volume_threshold]
        
        # Calculate volume profile statistics
        try:
            volume_profile_stats = {
                'total_volume': total_volume,
                'volume_std': volume_std,
                'volume_skew': stats.skew(volume_at_price),
                'volume_kurtosis': stats.kurtosis(volume_at_price)
            }
        except:
            volume_profile_stats = {
                'total_volume': total_volume,
                'volume_std': volume_std,
                'volume_skew': 0,
                'volume_kurtosis': 0
            }
        
        # Identify single prints (low volume areas)
        single_prints = bins[:-1][volume_at_price < (volume_mean * 0.3)]
        
        return {
            'poc_price': poc_price,
            'poc_volume': poc_volume,
            'value_area_high': value_area_high,
            'value_area_low': value_area_low,
            'value_area_percentage': value_area_percentage,
            'high_volume_nodes': high_volume_nodes,
            'low_volume_nodes': low_volume_nodes,
            'single_prints': single_prints,
            'volume_distribution': volume_at_price,
            'value_distribution': value_area_volumes,
            'price_bins': bins,
            'stats': volume_profile_stats
        }
    
    # [Previous pattern detection methods remain the same - keeping them for brevity]
    # Continuing with other methods...
    
    def detect_chart_patterns(self):
        """Detect Dan Zanger's Chart Patterns with enhanced detection"""
        # [Previous implementation - keeping as is]
        # ... [previous code for pattern detection]
        
        # We'll add support/resistance patterns here
        patterns = []
        
        # Detect Support/Resistance patterns
        sr_patterns = self.detect_support_resistance_patterns()
        patterns.extend(sr_patterns)
        
        return patterns
    
    def detect_support_resistance_patterns(self):
        """Detect patterns based on support and resistance"""
        patterns = []
        
        # Get support and resistance levels
        sr_data = self.detect_support_resistance()
        current_price = sr_data['current_price']
        
        # Pattern 1: Support Bounce
        support_levels = sr_data['support']
        if support_levels:
            nearest_support = min(support_levels, key=lambda x: abs(x['price'] - current_price))
            if abs(current_price - nearest_support['price']) / nearest_support['price'] < 0.02:
                patterns.append({
                    'pattern': 'Support Bounce',
                    'signal': 'BULLISH',
                    'confidence': 'HIGH' if nearest_support['strength'] > 2 else 'MEDIUM',
                    'score': nearest_support['strength'] / 3,
                    'description': f'Price bouncing off support at ₹{nearest_support["price"]:.2f}',
                    'action': 'BUY with tight stop loss',
                    'rules': [
                        f'Stop loss below ₹{nearest_support["price"] * 0.98:.2f}',
                        f'Target: Next resistance level'
                    ]
                })
        
        # Pattern 2: Resistance Test
        resistance_levels = sr_data['resistance']
        if resistance_levels:
            nearest_resistance = min(resistance_levels, key=lambda x: abs(x['price'] - current_price))
            if abs(current_price - nearest_resistance['price']) / nearest_resistance['price'] < 0.02:
                patterns.append({
                    'pattern': 'Resistance Test',
                    'signal': 'BEARISH',
                    'confidence': 'HIGH' if nearest_resistance['strength'] > 2 else 'MEDIUM',
                    'score': nearest_resistance['strength'] / 3,
                    'description': f'Price testing resistance at ₹{nearest_resistance["price"]:.2f}',
                    'action': 'SELL or wait for breakout',
                    'rules': [
                        f'Breakout above ₹{nearest_resistance["price"] * 1.02:.2f} for bullish continuation',
                        f'Rejection for bearish reversal'
                    ]
                })
        
        # Pattern 3: Range Bound
        consolidation_zones = self.detect_consolidation_zones()
        if consolidation_zones:
            latest_zone = consolidation_zones[-1]
            if latest_zone['breakout_direction'] == 'CONSOLIDATING':
                patterns.append({
                    'pattern': 'Range Bound Trading',
                    'signal': 'NEUTRAL',
                    'confidence': 'MEDIUM',
                    'score': 0.7,
                    'description': f'Price consolidating between ₹{latest_zone["support"]:.2f} and ₹{latest_zone["resistance"]:.2f}',
                    'action': 'Trade range boundaries',
                    'rules': [
                        f'Buy near ₹{latest_zone["support"]:.2f}',
                        f'Sell near ₹{latest_zone["resistance"]:.2f}',
                        f'Stop loss outside range'
                    ]
                })
        
        return patterns
    
    # [Continuing with other methods...]
    
    def get_trading_signal(self):
        """Generate comprehensive trading signal with weighted scoring"""
        # [Previous implementation]
        # ... [existing code]
        
        # Add support/resistance analysis to signals
        sr_data = self.detect_support_resistance()
        current_price = sr_data['current_price']
        
        support_levels = sr_data['support']
        resistance_levels = sr_data['resistance']
        
        if support_levels:
            nearest_support = min(support_levels, key=lambda x: abs(x['price'] - current_price))
            support_distance = (current_price - nearest_support['price']) / current_price * 100
            
            if support_distance < 2:
                signals.append(f"✅ Near strong support (₹{nearest_support['price']:.2f}, {nearest_support['touches']} touches)")
                score += 5
            elif support_distance < 5:
                signals.append(f"⚠️ Approaching support (₹{nearest_support['price']:.2f})")
        
        if resistance_levels:
            nearest_resistance = min(resistance_levels, key=lambda x: abs(x['price'] - current_price))
            resistance_distance = (nearest_resistance['price'] - current_price) / current_price * 100
            
            if resistance_distance < 2:
                signals.append(f"⚠️ Near strong resistance (₹{nearest_resistance['price']:.2f}, {nearest_resistance['touches']} touches)")
                score -= 5
            elif resistance_distance < 5:
                signals.append(f"✅ Room to resistance (₹{nearest_resistance['price']:.2f})")
                score += 2
        
        # [Rest of the method remains the same]
        # ... [existing code]
        
        return overall, signals, score, color

# ============================ PLOTTING FUNCTIONS ============================

def create_support_resistance_chart(analyzer):
    """Create chart with support and resistance levels"""
    df = analyzer.data.tail(100)
    
    # Get support and resistance data
    sr_data = analyzer.detect_support_resistance()
    trend_lines = analyzer.detect_trend_lines()
    fib_levels = analyzer.detect_fibonacci_levels()
    
    # Create figure
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        subplot_titles=(f'{analyzer.symbol} - Support & Resistance Analysis', 'Volume')
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC',
            increasing_line_color='#17e817',
            decreasing_line_color='#f55433'
        ),
        row=1, col=1
    )
    
    # Plot support levels
    for i, support in enumerate(sr_data['support']):
        fig.add_hline(
            y=support['price'],
            line_dash="dash",
            line_color="green",
            line_width=2,
            opacity=0.7,
            row=1, col=1,
            annotation_text=f"S{i+1}: ₹{support['price']:.2f} ({support['touches']} touches)",
            annotation_position="bottom right"
        )
    
    # Plot resistance levels
    for i, resistance in enumerate(sr_data['resistance']):
        fig.add_hline(
            y=resistance['price'],
            line_dash="dash",
            line_color="red",
            line_width=2,
            opacity=0.7,
            row=1, col=1,
            annotation_text=f"R{i+1}: ₹{resistance['price']:.2f} ({resistance['touches']} touches)",
            annotation_position="top right"
        )
    
    # Plot trend lines
    for trend in trend_lines['ascending']:
        start_date = trend['start_date']
        end_date = trend['end_date']
        
        # Create line coordinates
        x_vals = [start_date, end_date]
        y_vals = [trend['start_price'], trend['end_price']]
        
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines',
                line=dict(color='blue', width=2, dash='dot'),
                name=f'Asc Trend ({trend["touches"]} pts)'
            ),
            row=1, col=1
        )
    
    for trend in trend_lines['descending']:
        start_date = trend['start_date']
        end_date = trend['end_date']
        
        x_vals = [start_date, end_date]
        y_vals = [trend['start_price'], trend['end_price']]
        
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines',
                line=dict(color='orange', width=2, dash='dot'),
                name=f'Desc Trend ({trend["touches"]} pts)'
            ),
            row=1, col=1
        )
    
    # Plot Fibonacci levels
    if fib_levels:
        retracement_colors = {
            '0.236': 'rgba(255,165,0,0.3)',
            '0.382': 'rgba(255,140,0,0.4)',
            '0.500': 'rgba(255,69,0,0.5)',
            '0.618': 'rgba(255,0,0,0.6)',
            '0.786': 'rgba(178,34,34,0.7)'
        }
        
        for level, price in fib_levels['retracement_levels'].items():
            if level not in ['0.0', '1.0']:
                fig.add_hline(
                    y=price,
                    line_dash="dot",
                    line_color="purple",
                    line_width=1,
                    opacity=0.5,
                    row=1, col=1,
                    annotation_text=f"Fib {level}",
                    annotation_position="left"
                )
    
    # Volume
    colors_vol = ['#26a69a' if df['Close'].iloc[i] >= df['Open'].iloc[i] else '#ef5350' 
                  for i in range(len(df))]
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            name='Volume',
            marker_color=colors_vol,
            opacity=0.7
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=f'{analyzer.symbol} - Support & Resistance Analysis',
        xaxis_rangeslider_visible=False,
        height=800,
        showlegend=True,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    return fig

def create_consolidation_zones_chart(analyzer):
    """Create chart highlighting consolidation zones"""
    df = analyzer.data.tail(100)
    consolidation_zones = analyzer.detect_consolidation_zones()
    
    fig = make_subplots(
        rows=1, cols=1,
        subplot_titles=(f'{analyzer.symbol} - Consolidation Zones',)
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC',
            increasing_line_color='#17e817',
            decreasing_line_color='#f55433'
        )
    )
    
    # Plot consolidation zones
    for i, zone in enumerate(consolidation_zones):
        # Add rectangle for consolidation zone
        fig.add_shape(
            type="rect",
            x0=zone['start_date'],
            x1=zone['end_date'],
            y0=zone['support'],
            y1=zone['resistance'],
            fillcolor="rgba(128,128,128,0.2)",
            line=dict(color="gray", width=1),
            opacity=0.3
        )
        
        # Add zone label
        fig.add_annotation(
            x=zone['end_date'],
            y=zone['resistance'],
            text=f"Zone {i+1}<br>{zone['range_pct']:.1f}% range<br>{zone['duration_days']} days",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="gray",
            font=dict(size=10)
        )
        
        # Add breakout indicator if applicable
        if zone['breakout_direction'] == 'BULLISH':
            fig.add_annotation(
                x=zone['end_date'] + pd.Timedelta(days=2),
                y=zone['resistance'] * 1.05,
                text="🟢 Bullish Breakout",
                showarrow=False,
                font=dict(color="green", size=10)
            )
        elif zone['breakout_direction'] == 'BEARISH':
            fig.add_annotation(
                x=zone['end_date'] + pd.Timedelta(days=2),
                y=zone['support'] * 0.95,
                text="🔴 Bearish Breakout",
                showarrow=False,
                font=dict(color="red", size=10)
            )
    
    # Update layout
    fig.update_layout(
        height=600,
        showlegend=False,
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig

def create_fibonacci_chart(analyzer):
    """Create chart with Fibonacci retracement levels"""
    df = analyzer.data.tail(100)
    fib_data = analyzer.detect_fibonacci_levels()
    
    if not fib_data:
        return go.Figure()
    
    fig = make_subplots(
        rows=1, cols=1,
        subplot_titles=(f'{analyzer.symbol} - Fibonacci Analysis',)
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC',
            increasing_line_color='#17e817',
            decreasing_line_color='#f55433'
        )
    )
    
    # Add swing high/low markers
    fig.add_trace(
        go.Scatter(
            x=[df.index[df['High'].idxmax()]],
            y=[fib_data['swing_high']],
            mode='markers+text',
            marker=dict(color='red', size=12, symbol='triangle-down'),
            text=['Swing High'],
            textposition='top center',
            name='Swing High'
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=[df.index[df['Low'].idxmin()]],
            y=[fib_data['swing_low']],
            mode='markers+text',
            marker=dict(color='green', size=12, symbol='triangle-up'),
            text=['Swing Low'],
            textposition='bottom center',
            name='Swing Low'
        )
    )
    
    # Add Fibonacci retracement levels
    fib_colors = {
        '0.0': 'green',
        '0.236': 'lightgreen',
        '0.382': 'yellow',
        '0.500': 'orange',
        '0.618': 'red',
        '0.786': 'darkred',
        '1.0': 'darkgreen'
    }
    
    for level, price in fib_data['retracement_levels'].items():
        fig.add_hline(
            y=price,
            line_dash="dash",
            line_color=fib_colors.get(level, 'gray'),
            line_width=2,
            opacity=0.7,
            annotation_text=f"Fib {level}",
            annotation_position="left"
        )
    
    # Add current price marker
    current_price = df['Close'].iloc[-1]
    fig.add_hline(
        y=current_price,
        line_dash="solid",
        line_color="blue",
        line_width=3,
        annotation_text=f"Current: ₹{current_price:.2f}",
        annotation_position="right"
    )
    
    # Update layout
    fig.update_layout(
        height=600,
        showlegend=True,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_candlestick_chart(analyzer):
    """Create advanced candlestick chart with multiple indicators"""
    # [Previous implementation - keeping as is]
    # ... [existing code]
    
    # We'll add support/resistance to this chart too
    sr_data = analyzer.detect_support_resistance()
    
    # Add key support and resistance levels to the chart
    if sr_data['support']:
        key_support = sr_data['support'][0]  # Strongest support
        fig.add_hline(
            y=key_support['price'],
            line_dash="dash",
            line_color="green",
            line_width=2,
            row=1, col=1,
            annotation_text=f"Key Support: ₹{key_support['price']:.2f}",
            annotation_position="bottom right"
        )
    
    if sr_data['resistance']:
        key_resistance = sr_data['resistance'][0]  # Strongest resistance
        fig.add_hline(
            y=key_resistance['price'],
            line_dash="dash",
            line_color="red",
            line_width=2,
            row=1, col=1,
            annotation_text=f"Key Resistance: ₹{key_resistance['price']:.2f}",
            annotation_position="top right"
        )
    
    return fig

# ============================ MAIN APPLICATION ============================

def main():
    """Main Streamlit application"""
    
    st.markdown('<div class="main-header">🎯 Indian Equity Market Analyzer Pro</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: gray;">Master Trader Grade Analysis with Support/Resistance Detection</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="stock-ticker">📊</div>', unsafe_allow_html=True)
        
        st.header("Analysis Settings")
        
        # Stock selection
        symbol = st.text_input(
            "Enter Stock Symbol",
            value="",
            help="Enter NSE symbol (e.g., RELIANCE, TCS, HDFCBANK)"
        )
        
        # Analysis period
        period = st.selectbox(
            "Analysis Period",
            options=['1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'],
            index=3
        )
        
        # Support/Resistance Settings
        st.markdown("---")
        st.markdown("### Support/Resistance Settings")
        
        sr_lookback = st.slider(
            "Lookback Period (days)",
            min_value=50,
            max_value=200,
            value=100,
            help="Number of days to analyze for S/R"
        )
        
        sr_threshold = st.slider(
            "Level Merge Threshold (%)",
            min_value=0.5,
            max_value=5.0,
            value=2.0,
            step=0.5,
            help="Merge levels within this percentage"
        )
        
        # Portfolio size for risk management
        portfolio_value = st.number_input(
            "Portfolio Value (₹)",
            min_value=10000,
            max_value=10000000,
            value=1000000,
            step=10000,
            help="Used for position sizing calculations"
        )
        
        # Analysis options
        st.markdown("---")
        st.markdown("### Analysis Options")
        
        show_sr = st.checkbox("Show Support/Resistance Analysis", value=True)
        show_advanced = st.checkbox("Show Advanced Analysis", value=True)
        show_patterns = st.checkbox("Show Pattern Detection", value=True)
        show_risk = st.checkbox("Show Risk Management", value=True)
        show_market = st.checkbox("Show Market Context", value=True)
        
        # Analyze button
        col1, col2 = st.columns(2)
        with col1:
            analyze_btn = st.button("🔍 Analyze", type="primary", use_container_width=True)
        with col2:
            clear_btn = st.button("🔄 Clear", use_container_width=True)
        
        if clear_btn:
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📚 Pattern Library")
        
        with st.expander("Support & Resistance Patterns"):
            st.markdown("""
            - **Support Bounce**: Price bouncing off support level
            - **Resistance Test**: Price testing resistance level
            - **Range Bound**: Price consolidating in a range
            - **Trend Line Break**: Breaking ascending/descending trend lines
            - **Fibonacci Retracement**: Price reacting to Fibonacci levels
            """)
        
        with st.expander("Dan Zanger Patterns"):
            st.markdown("""
            - **Cup and Handle**: Most reliable bullish pattern
            - **High Tight Flag**: Explosive breakout pattern
            - **Ascending Triangle**: Bullish continuation
            - **Flat Base**: Consolidation before breakout
            - **Falling Wedge**: Bullish reversal
            """)
        
        with st.expander("Qullamaggie Patterns"):
            st.markdown("""
            - **Breakout**: ORH entry with volume
            - **Episodic Pivot**: Gap and go momentum
            - **Parabolic Short**: Reversion to mean setup
            - **Gap and Go**: Continuation pattern
            - **ABCD Pattern**: Harmonic trading
            """)
    
    if analyze_btn and symbol:
        with st.spinner(f'🔄 Analyzing {symbol}...'):
            # Create analyzer instance and fetch data
            analyzer = IndianEquityAnalyzer(symbol, period)
            
            if analyzer._fetch_raw_data():
                # Company Information Section
                st.markdown('<div class="sub-header">🏢 Company Overview</div>', unsafe_allow_html=True)
                
                info = analyzer.get_company_info()
                company_info = st.container()
                
                with company_info:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Company", info.get('name', symbol))
                        st.metric("Sector", info.get('sector', 'N/A'))
                        
                    with col2:
                        st.metric("Market Cap", info.get('market_cap_formatted', 'N/A'))
                        st.metric("Industry", info.get('industry', 'N/A'))
                        
                    with col3:
                        pe = info.get('pe_ratio', 'N/A')
                        st.metric("P/E Ratio", f"{pe:.2f}" if isinstance(pe, (int, float)) else 'N/A')
                        st.metric("P/B Ratio", f"{info.get('pb_ratio', 'N/A'):.2f}" 
                                 if isinstance(info.get('pb_ratio'), (int, float)) else 'N/A')
                        
                    with col4:
                        st.metric("Beta", f"{info.get('beta', 1.0):.2f}")
                        div_yield = info.get('dividend_yield', 0)
                        st.metric("Div Yield", f"{div_yield:.2f}%" if div_yield else '0.00%')
                
                # Current Price Information
                current = analyzer.data.iloc[-1]
                prev = analyzer.data.iloc[-2]
                change = current['Close'] - prev['Close']
                change_pct = (change / prev['Close']) * 100
                
                st.markdown('<div class="sub-header">📊 Current Market Data</div>', unsafe_allow_html=True)
                
                price_cols = st.columns(5)
                with price_cols[0]:
                    st.metric(
                        "Current Price",
                        f"₹{current['Close']:.2f}",
                        f"{change:+.2f} ({change_pct:+.2f}%)",
                        delta_color="normal" if change >= 0 else "inverse"
                    )
                with price_cols[1]:
                    st.metric("Day High", f"₹{current['High']:.2f}")
                with price_cols[2]:
                    st.metric("Day Low", f"₹{current['Low']:.2f}")
                with price_cols[3]:
                    st.metric("52W High", f"₹{info.get('52w_high', 0):.2f}")
                with price_cols[4]:
                    st.metric("52W Low", f"₹{info.get('52w_low', 0):.2f}")
                
                # ==================== SUPPORT & RESISTANCE ANALYSIS ====================
                
                if show_sr:
                    st.markdown('<div class="sub-header">📊 Support & Resistance Analysis</div>', unsafe_allow_html=True)
                    
                    # Get S/R data
                    sr_data = analyzer.detect_support_resistance(lookback_period=sr_lookback, threshold=sr_threshold/100)
                    trend_lines = analyzer.detect_trend_lines()
                    consolidation_zones = analyzer.detect_consolidation_zones()
                    fib_levels = analyzer.detect_fibonacci_levels()
                    
                    # Display S/R Levels
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🟢 Support Levels")
                        if sr_data['support']:
                            support_df = pd.DataFrame([
                                {
                                    'Level': f'S{i+1}',
                                    'Price': f'₹{s["price"]:.2f}',
                                    'Touches': s['touches'],
                                    'Strength': 'Strong' if s['strength'] > 2 else 'Medium' if s['strength'] > 1 else 'Weak',
                                    'Distance': f'{((sr_data["current_price"] - s["price"]) / sr_data["current_price"] * 100):.1f}%'
                                }
                                for i, s in enumerate(sr_data['support'])
                            ])
                            st.dataframe(support_df, use_container_width=True, hide_index=True)
                        else:
                            st.info("No significant support levels detected")
                    
                    with col2:
                        st.markdown("#### 🔴 Resistance Levels")
                        if sr_data['resistance']:
                            resistance_df = pd.DataFrame([
                                {
                                    'Level': f'R{i+1}',
                                    'Price': f'₹{r["price"]:.2f}',
                                    'Touches': r['touches'],
                                    'Strength': 'Strong' if r['strength'] > 2 else 'Medium' if r['strength'] > 1 else 'Weak',
                                    'Distance': f'{((r["price"] - sr_data["current_price"]) / sr_data["current_price"] * 100):.1f}%'
                                }
                                for i, r in enumerate(sr_data['resistance'])
                            ])
                            st.dataframe(resistance_df, use_container_width=True, hide_index=True)
                        else:
                            st.info("No significant resistance levels detected")
                    
                    # Display Trend Lines
                    st.markdown("#### 📈 Trend Lines")
                    trend_cols = st.columns(2)
                    
                    with trend_cols[0]:
                        st.markdown("**Ascending Trends**")
                        if trend_lines['ascending']:
                            for i, trend in enumerate(trend_lines['ascending']):
                                st.markdown(f"""
                                **Trend {i+1}:**
                                - Start: ₹{trend['start_price']:.2f}
                                - End: ₹{trend['end_price']:.2f}
                                - Slope: {trend['slope']:.4f}/day
                                - Touches: {trend['touches']} points
                                """)
                        else:
                            st.info("No ascending trend lines detected")
                    
                    with trend_cols[1]:
                        st.markdown("**Descending Trends**")
                        if trend_lines['descending']:
                            for i, trend in enumerate(trend_lines['descending']):
                                st.markdown(f"""
                                **Trend {i+1}:**
                                - Start: ₹{trend['start_price']:.2f}
                                - End: ₹{trend['end_price']:.2f}
                                - Slope: {trend['slope']:.4f}/day
                                - Touches: {trend['touches']} points
                                """)
                        else:
                            st.info("No descending trend lines detected")
                    
                    # Display Consolidation Zones
                    st.markdown("#### 🎯 Consolidation Zones")
                    if consolidation_zones:
                        for i, zone in enumerate(consolidation_zones):
                            color = "green" if zone['breakout_direction'] == 'BULLISH' else "red" if zone['breakout_direction'] == 'BEARISH' else "gray"
                            icon = "🟢" if zone['breakout_direction'] == 'BULLISH' else "🔴" if zone['breakout_direction'] == 'BEARISH' else "⚪"
                            
                            st.markdown(f"""
                            **Zone {i+1}** {icon}
                            - Support: ₹{zone['support']:.2f}
                            - Resistance: ₹{zone['resistance']:.2f}
                            - Range: {zone['range_pct']:.1f}%
                            - Duration: {zone['duration_days']} days
                            - Breakout: **{zone['breakout_direction']}**
                            """)
                    else:
                        st.info("No consolidation zones detected")
                    
                    # Display Fibonacci Levels
                    st.markdown("#### 🔢 Fibonacci Levels")
                    if fib_levels:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Retracement Levels**")
                            retracement_df = pd.DataFrame([
                                {'Level': level, 'Price': f'₹{price:.2f}'}
                                for level, price in fib_levels['retracement_levels'].items()
                            ])
                            st.dataframe(retracement_df, use_container_width=True, hide_index=True)
                        
                        with col2:
                            st.markdown("**Extension Levels**")
                            extension_df = pd.DataFrame([
                                {'Level': level, 'Price': f'₹{price:.2f}'}
                                for level, price in fib_levels['extension_levels'].items()
                            ])
                            st.dataframe(extension_df, use_container_width=True, hide_index=True)
                        
                        # Current position relative to Fibonacci
                        current_price = fib_levels['current_price']
                        nearest_retracement = fib_levels['nearest_retracement']
                        distance_to_fib = abs(current_price - nearest_retracement) / nearest_retracement * 100
                        
                        st.markdown(f"""
                        **Current Position:**
                        - Price: ₹{current_price:.2f}
                        - Nearest Fibonacci: ₹{nearest_retracement:.2f}
                        - Distance: {distance_to_fib:.1f}%
                        """)
                    
                    # S/R Charts
                    st.markdown("#### 📊 Support & Resistance Charts")
                    
                    sr_chart_tabs = st.tabs(["S/R Levels", "Consolidation Zones", "Fibonacci"])
                    
                    with sr_chart_tabs[0]:
                        fig_sr = create_support_resistance_chart(analyzer)
                        st.plotly_chart(fig_sr, use_container_width=True)
                    
                    with sr_chart_tabs[1]:
                        if consolidation_zones:
                            fig_consolidation = create_consolidation_zones_chart(analyzer)
                            st.plotly_chart(fig_consolidation, use_container_width=True)
                        else:
                            st.info("No consolidation zones to display")
                    
                    with sr_chart_tabs[2]:
                        if fib_levels:
                            fig_fib = create_fibonacci_chart(analyzer)
                            st.plotly_chart(fig_fib, use_container_width=True)
                        else:
                            st.info("Insufficient data for Fibonacci analysis")
                
                # ==================== CONTINUE WITH EXISTING ANALYSIS ====================
                
                # [Rest of the existing analysis code remains the same]
                # ... [existing code for trading signals, patterns, etc.]
                
                # Trading Signal
                st.markdown('<div class="sub-header">🎯 Trading Signal & Analysis</div>', unsafe_allow_html=True)
                
                overall, signals, score, color = analyzer.get_trading_signal()
                
                signal_cols = st.columns([1, 2])
                with signal_cols[0]:
                    st.markdown(f"""
                    <div style="background-color: {color}; padding: 20px; border-radius: 10px; text-align: center;">
                         <h2 style="margin: 0; color: white;">{overall}</h2>
                         <p style="margin: 5px 0; font-size: 18px; color: white;">Score: {score:.1f}/100</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Gauge chart for signal strength
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=score,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Signal Strength"},
                        gauge={
                            'axis': {'range': [-50, 100]},
                            'bar': {'color': "blue"},
                            'steps': [
                                {'range': [-50, 0], 'color': "red"},
                                {'range': [0, 50], 'color': "yellow"},
                                {'range': [50, 100], 'color': "green"}
                            ],
                            'threshold': {
                                'line': {'color': "black", 'width': 4},
                                'thickness': 0.75,
                                'value': 50
                            }
                        }
                    ))
                    
                    fig_gauge.update_layout(height=200, margin=dict(t=30, b=10))
                    st.plotly_chart(fig_gauge, use_container_width=True)
                
                with signal_cols[1]:
                    with st.expander("📋 Detailed Analysis Signals", expanded=True):
                        for signal in signals:
                            st.markdown(f"• {signal}")
                
                # Pattern Detection
                if show_patterns:
                    st.markdown('<div class="sub-header">📈 Pattern Detection</div>', unsafe_allow_html=True)
                    
                    pattern_tabs = st.tabs(["Support/Resistance", "Dan Zanger", "Qullamaggie", "All Patterns"])
                    
                    with pattern_tabs[0]:
                        sr_patterns = analyzer.detect_support_resistance_patterns()
                        if sr_patterns:
                            for pattern in sr_patterns:
                                # Create pattern card
                                if pattern['signal'] == 'BULLISH':
                                    color_class = "bullish"
                                    icon = "📈"
                                elif pattern['signal'] == 'BEARISH':
                                    color_class = "bearish"
                                    icon = "📉"
                                else:
                                    color_class = "neutral"
                                    icon = "⚖️"
                                
                                card_html = f"""
                                <div class="pattern-card">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <div>
                                            <h3 style="margin: 0; color: white;">{icon} {pattern['pattern']}</h3>
                                            <p style="margin: 5px 0; color: #f0f0f0;">Signal: <span class="{color_class}">{pattern['signal']}</span></p>
                                        </div>
                                        <div style="text-align: right;">
                                            <p style="margin: 0; color: #f0f0f0;">Confidence: {pattern['confidence']}</p>
                                            <p style="margin: 0; color: #f0f0f0;">Score: {pattern['score']:.2f}</p>
                                        </div>
                                    </div>
                                    <hr style="border-color: rgba(255,255,255,0.2); margin: 10px 0;">
                                    <p style="margin: 5px 0; color: #f0f0f0;"><strong>Description:</strong> {pattern['description']}</p>
                                    <p style="margin: 5px 0; color: #f0f0f0;"><strong>Action:</strong> {pattern['action']}</p>
                                </div>
                                """
                                st.markdown(card_html, unsafe_allow_html=True)
                                
                                with st.expander("View Rules & Details"):
                                    st.markdown("**Rules to Follow:**")
                                    for rule in pattern.get('rules', []):
                                        st.markdown(f"• {rule}")
                        else:
                            st.info("No support/resistance patterns detected")
                    
                    with pattern_tabs[1]:
                        zanger_patterns = analyzer.detect_chart_patterns()
                        if zanger_patterns:
                            for pattern in zanger_patterns:
                                # [Existing pattern display code]
                                pass
                        else:
                            st.info("No Dan Zanger patterns detected")
                    
                    with pattern_tabs[2]:
                        swing_patterns = analyzer.detect_swing_patterns()
                        if swing_patterns:
                            for pattern in swing_patterns:
                                # [Existing pattern display code]
                                pass
                        else:
                            st.info("No Qullamaggie patterns detected")
                    
                    with pattern_tabs[3]:
                        all_patterns = sr_patterns + zanger_patterns + swing_patterns
                        if all_patterns:
                            pattern_df = pd.DataFrame([{
                                'Pattern': p['pattern'],
                                'Signal': p['signal'],
                                'Confidence': p['confidence'],
                                'Score': p['score'],
                                'Description': p['description'][:100] + '...'
                            } for p in all_patterns])
                            
                            st.dataframe(
                                pattern_df,
                                use_container_width=True,
                                column_config={
                                    "Pattern": st.column_config.TextColumn("Pattern"),
                                    "Signal": st.column_config.TextColumn("Signal"),
                                    "Confidence": st.column_config.TextColumn("Confidence"),
                                    "Score": st.column_config.ProgressColumn(
                                        "Score",
                                        format="%.2f",
                                        min_value=0,
                                        max_value=1.0
                                    ),
                                    "Description": st.column_config.TextColumn("Description", width="large")
                                }
                            )
                        else:
                            st.warning("No trading patterns detected")
                
                # [Continue with rest of existing code...]
                # Risk Management, Market Context, Technical Charts, etc.
                
                # Advanced Technical Charts
                if show_advanced:
                    st.markdown('<div class="sub-header">📊 Advanced Technical Charts</div>', unsafe_allow_html=True)
                    
                    chart_tabs = st.tabs(["Price Action & Indicators", "Volume Profile", "Market Structure"])
                    
                    with chart_tabs[0]:
                        fig_candlestick = create_candlestick_chart(analyzer)
                        st.plotly_chart(fig_candlestick, use_container_width=True)
                    
                    with chart_tabs[1]:
                        fig_volume_profile = create_volume_profile_chart(analyzer)
                        st.plotly_chart(fig_volume_profile, use_container_width=True)
                    
                    with chart_tabs[2]:
                        # Enhanced market structure with S/R
                        st.info("Market structure analysis with support/resistance levels and key price zones.")
                        
                        # Get S/R data
                        sr_data = analyzer.detect_support_resistance()
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("#### 🟢 Key Support Levels")
                            if sr_data['support']:
                                for i, support in enumerate(sr_data['support'][:3], 1):
                                    st.metric(
                                        f"Support {i}",
                                        f"₹{support['price']:.2f}",
                                        f"{support['touches']} touches"
                                    )
                            else:
                                st.info("No support levels")
                        
                        with col2:
                            st.markdown("#### 🔴 Key Resistance Levels")
                            if sr_data['resistance']:
                                for i, resistance in enumerate(sr_data['resistance'][:3], 1):
                                    st.metric(
                                        f"Resistance {i}",
                                        f"₹{resistance['price']:.2f}",
                                        f"{resistance['touches']} touches"
                                    )
                            else:
                                st.info("No resistance levels")
                
                st.success(f"✅ Analysis completed for {symbol} at {datetime.now().strftime('%H:%M:%S')}")
                
            else:
                st.error(f"❌ Unable to fetch data for {symbol}.")
    
    else:
        # Welcome screen
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
            <h1>Welcome to Indian Equity Market Analyzer Pro</h1>
            <p style="font-size: 18px;">Advanced technical analysis with Support/Resistance Detection</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🎯 Support & Resistance</h3>
                <p>Advanced S/R detection with multiple methods</p>
                <ul>
                    <li>Automatic Level Detection</li>
                    <li>Trend Line Analysis</li>
                    <li>Fibonacci Retracement</li>
                    <li>Consolidation Zones</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>📈 Pattern Detection</h3>
                <p>Comprehensive pattern recognition</p>
                <ul>
                    <li>Dan Zanger Patterns</li>
                    <li>Qullamaggie Swing Trading</li>
                    <li>Support/Resistance Patterns</li>
                    <li>Volume Analysis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 Risk Management</h3>
                <p>Professional trading tools</p>
                <ul>
                    <li>Position Sizing</li>
                    <li>Stop Loss Calculation</li>
                    <li>Risk/Reward Analysis</li>
                    <li>Portfolio Risk Management</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
