import logging

from mcp.server.fastmcp import FastMCP
from src.mcp_api.data_source_interface import FinancialDataSource
from src.mcp_api.mcp_tools.base import call_financial_data_tool

logger = logging.getLogger(__name__)


def register_financial_report_tools(app: FastMCP, active_data_source: FinancialDataSource):
    """
    向MCP应用注册财务报告相关工具

    参数:
        app: FastMCP应用实例
        active_data_source: 活跃的金融数据源
    """

    @app.tool()
    def get_profit_data(code: str, year: str, quarter: int) -> str:
        """
        获取股票的季度盈利能力数据（例如ROE，净利润率）

        参数:
            code: 股票代码（例如'sh.600000'）
            year: 4位数年份（例如'2023'）
            quarter: 季度（1, 2, 3, 或 4）

        返回:
            包含盈利能力数据的Markdown表格或错误信息
        """
        return call_financial_data_tool(
            "get_profit_data",
            active_data_source.get_profit_data,
            "Profitability",
            code, year, quarter
        )

    @app.tool()
    def get_operation_data(code: str, year: str, quarter: int) -> str:
        """
        获取股票的季度运营能力数据（例如周转率）

        参数:
            code: 股票代码（例如'sh.600000'）
            year: 4位数年份（例如'2023'）
            quarter: 季度（1, 2, 3, 或 4）

        返回:
            包含运营能力数据的Markdown表格或错误信息
        """
        return call_financial_data_tool(
            "get_operation_data",
            active_data_source.get_operation_data,
            "Operation Capability",
            code, year, quarter
        )

    @app.tool()
    def get_growth_data(code: str, year: str, quarter: int) -> str:
        """
        获取股票的季度增长能力数据（例如同比增长率）

        参数:
            code: 股票代码（例如'sh.600000'）
            year: 4位数年份（例如'2023'）
            quarter: 季度（1, 2, 3, 或 4）

        返回:
            包含增长能力数据的Markdown表格或错误信息
        """
        return call_financial_data_tool(
            "get_growth_data",
            active_data_source.get_growth_data,
            "Growth Capability",
            code, year, quarter
        )

    @app.tool()
    def get_balance_data(code: str, year: str, quarter: int) -> str:
        """
        获取股票的季度资产负债表/偿债能力数据（例如流动比率，负债率）

        参数:
            code: 股票代码（例如'sh.600000'）
            year: 4位数年份（例如'2023'）
            quarter: 季度（1, 2, 3, 或 4）

        返回:
            包含资产负债表数据的Markdown表格或错误信息
        """
        return call_financial_data_tool(
            "get_balance_data",
            active_data_source.get_balance_data,
            "Balance Sheet",
            code, year, quarter
        )

    @app.tool()
    def get_cash_flow_data(code: str, year: str, quarter: int) -> str:
        """
        获取股票的季度现金流量数据（例如经营活动现金流/营业收入比率）

        参数:
            code: 股票代码（例如'sh.600000'）
            year: 4位数年份（例如'2023'）
            quarter: 季度（1, 2, 3, 或 4）

        返回:
            包含现金流量数据的Markdown表格或错误信息
        """
        return call_financial_data_tool(
            "get_cash_flow_data",
            active_data_source.get_cash_flow_data,
            "Cash Flow",
            code, year, quarter
        )

    @app.tool()
    def get_dupont_data(code: str, year: str, quarter: int) -> str:
        """
        获取股票的季度杜邦分析数据（ROE分解）

        参数:
            code: 股票代码（例如'sh.600000'）
            year: 4位数年份（例如'2023'）
            quarter: 季度（1, 2, 3, 或 4）

        返回:
            包含杜邦分析数据的Markdown表格或错误信息
        """
        return call_financial_data_tool(
            "get_dupont_data",
            active_data_source.get_dupont_data,
            "DuPont Analysis",
            code, year, quarter
        )

    @app.tool()
    def get_performance_express_report(code: str, start_date: str, end_date: str) -> str:
        """
        获取指定日期范围内的股票业绩快报
        注意：除特定情况外，公司并非必须发布业绩快报

        参数:
            code: 股票代码（例如'sh.600000'）
            start_date: 开始日期（报告发布/更新日期），格式为'YYYY-MM-DD'
            end_date: 结束日期（报告发布/更新日期），格式为'YYYY-MM-DD'

        返回:
            包含业绩快报数据的Markdown表格或错误信息
        """
        logger.info(
            f"Tool 'get_performance_express_report' called for {code} ({start_date} to {end_date})")
        try:
            # 如果需要，可以添加日期验证
            df = active_data_source.get_performance_express_report(
                code=code, start_date=start_date, end_date=end_date)
            logger.info(
                f"Successfully retrieved performance express reports for {code}.")
            from src.mcp_api.formatting.markdown_formatter import format_df_to_markdown
            return format_df_to_markdown(df)

        except Exception as e:
            logger.exception(
                f"Exception processing get_performance_express_report for {code}: {e}")
            return f"Error: An unexpected error occurred: {e}"

    @app.tool()
    def get_forecast_report(code: str, start_date: str, end_date: str) -> str:
        """
        获取指定日期范围内的股票业绩预告
        注意：除特定情况外，公司并非必须发布业绩预告

        参数:
            code: 股票代码（例如'sh.600000'）
            start_date: 开始日期（报告发布/更新日期），格式为'YYYY-MM-DD'
            end_date: 结束日期（报告发布/更新日期），格式为'YYYY-MM-DD'

        返回:
            包含业绩预告数据的Markdown表格或错误信息
        """
        logger.info(
            f"Tool 'get_forecast_report' called for {code} ({start_date} to {end_date})")
        try:
            # 如果需要，可以添加日期验证
            df = active_data_source.get_forecast_report(
                code=code, start_date=start_date, end_date=end_date)
            logger.info(
                f"Successfully retrieved performance forecast reports for {code}.")
            from src.mcp_api.formatting.markdown_formatter import format_df_to_markdown
            return format_df_to_markdown(df)

        except Exception as e:
            logger.exception(
                f"Exception processing get_forecast_report for {code}: {e}")
            return f"Error: An unexpected error occurred: {e}"