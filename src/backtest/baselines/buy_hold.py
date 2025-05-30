import pandas as pd
from .base_strategy import BaseStrategy, Signal, Portfolio

class BuyHoldStrategy(BaseStrategy):
    """
    买入持有策略
    经典的长期投资基准策略
    """
    
    def __init__(self, allocation_ratio: float = 1.0, **kwargs):
        # Extract name from kwargs if provided, otherwise use default
        name = kwargs.pop('name', 'Buy-and-Hold')
        super().__init__(name, **kwargs)
        self.allocation_ratio = allocation_ratio  # 资金配置比例
        self.initial_purchase_made = False
        
    def generate_signal(self, data: pd.DataFrame, portfolio: Portfolio, 
                       current_date: str, **kwargs) -> Signal:
        """
        买入持有策略逻辑：
        - 第一次交易时买入并持有
        - 之后所有时间都持有
        """
        if not self.initial_purchase_made and portfolio.cash > 0:
            # 第一次投资：买入
            current_price = data.iloc[-1]['close']
            max_shares = int((portfolio.cash * self.allocation_ratio) / current_price)
            
            if max_shares > 0:
                self.initial_purchase_made = True
                return Signal(
                    action='buy',
                    quantity=max_shares,
                    confidence=1.0,
                    reasoning="Initial buy-and-hold purchase",
                    metadata={'allocation_ratio': self.allocation_ratio}
                )
        
        # 已投资或无法投资：持有
        return Signal(
            action='hold',
            quantity=0,
            confidence=1.0,
            reasoning="Buy-and-hold strategy maintains position"
        )