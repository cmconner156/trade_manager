class ForexPairs():
  def __init__(self):
    self._forex_pairs = {}
    self._forex_pairs['AUDUSD'] = 4
    self._forex_pairs['AUDJPY'] = 2
    self._forex_pairs['AUDNZD'] = 4
    self._forex_pairs['AUDCAD'] = 4
    self._forex_pairs['AUDCHF'] = 4
    self._forex_pairs['CADJPY'] = 2
    self._forex_pairs['CADCHF'] = 4
    self._forex_pairs['CHFJPY'] = 2
    self._forex_pairs['EURNOK'] = 4
    self._forex_pairs['EURUSD'] = 4
    self._forex_pairs['EURCHF'] = 4
    self._forex_pairs['EURTRY'] = 4
    self._forex_pairs['EURGBP'] = 4
    self._forex_pairs['EURJPY'] = 2
    self._forex_pairs['EURAUD'] = 4
    self._forex_pairs['EURCAD'] = 4
    self._forex_pairs['EURNZD'] = 4
    self._forex_pairs['EURSEK'] = 4
    self._forex_pairs['GBPJPY'] = 2
    self._forex_pairs['GBPNZD'] = 4
    self._forex_pairs['GBPAUD'] = 4
    self._forex_pairs['GBPCHF'] = 4
    self._forex_pairs['GBPUSD'] = 4
    self._forex_pairs['GBPCAD'] = 4
    self._forex_pairs['NZDCHF'] = 4
    self._forex_pairs['NZDJPY'] = 2
    self._forex_pairs['NZDUSD'] = 4
    self._forex_pairs['NZDCAD'] = 4
    self._forex_pairs['TRYJPY'] = 2
    self._forex_pairs['USDHKD'] = 4
    self._forex_pairs['USDNOK'] = 4
    self._forex_pairs['USDSEK'] = 4
    self._forex_pairs['USDZAR'] = 4
    self._forex_pairs['USDMXN'] = 4
    self._forex_pairs['USDTRY'] = 4
    self._forex_pairs['USDCAD'] = 4
    self._forex_pairs['USDCHF'] = 4
    self._forex_pairs['USDJPY'] = 2
    self._forex_pairs['USDCNH'] = 4
    self._forex_pairs['ZARJPY'] = 2
    self._forex_pairs['XAUUSD'] = 4

  def check_string_contains_pair(self, comparestring):
    for code in self._forex_pairs.keys():
      if code.lower() in comparestring.lower():
        return code, self._forex_pairs[code]
