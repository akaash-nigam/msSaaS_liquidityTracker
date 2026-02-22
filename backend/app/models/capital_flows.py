from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func
from app.database import Base


class CapitalFlow(Base):
    __tablename__ = "capital_flows"

    id = Column(Integer, primary_key=True, index=True)
    flow_date = Column(Date, nullable=False, index=True)
    source_country = Column(String(5))
    destination_country = Column(String(5))
    region_from = Column(String(50))
    region_to = Column(String(50))
    flow_type = Column(String(50), nullable=False)  # portfolio_equity, portfolio_debt, official, other
    asset_class = Column(String(50))  # equity, debt
    sector = Column(String(50))  # government, non_bank_financial
    direction = Column(String(10))  # net, inflow, outflow
    amount_usd = Column(Numeric(20, 4))  # in billions USD
    amount_local = Column(Numeric(20, 4))
    currency = Column(String(5), default="USD")
    data_source = Column(String(50))
    series_id = Column(String(50))
    frequency = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())


class CapitalFlowIndex(Base):
    __tablename__ = "capital_flow_index"

    id = Column(Integer, primary_key=True, index=True)
    index_date = Column(Date, nullable=False, unique=True, index=True)
    total_global_flows = Column(Numeric(20, 4))
    dm_to_em_flows = Column(Numeric(20, 4))
    em_to_dm_flows = Column(Numeric(20, 4))
    us_net_flows = Column(Numeric(20, 4))
    risk_appetite_score = Column(Numeric(10, 4))
    dollar_strength_index = Column(Numeric(10, 4))
    capital_flight_index = Column(Numeric(10, 4))
    created_at = Column(DateTime, server_default=func.now())


class USTreasuryTIC(Base):
    __tablename__ = "us_treasury_tic"

    id = Column(Integer, primary_key=True, index=True)
    report_date = Column(Date, nullable=False, index=True)
    country_code = Column(String(5), nullable=False, index=True)
    country_name = Column(String(100))
    treasury_bonds = Column(Numeric(20, 4))
    treasury_bills = Column(Numeric(20, 4))
    total_treasuries = Column(Numeric(20, 4))
    agency_bonds = Column(Numeric(20, 4))
    corporate_bonds = Column(Numeric(20, 4))
    equities = Column(Numeric(20, 4))
    total_holdings = Column(Numeric(20, 4))
    mom_change = Column(Numeric(20, 4))
    yoy_change = Column(Numeric(20, 4))
    series_id = Column(String(50))
    data_source = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())


class BalanceOfPayments(Base):
    __tablename__ = "balance_of_payments"

    id = Column(Integer, primary_key=True, index=True)
    report_date = Column(Date, nullable=False, index=True)
    country_code = Column(String(5), nullable=False, index=True)
    country_name = Column(String(100))
    current_account_balance = Column(Numeric(20, 4))
    trade_balance = Column(Numeric(20, 4))
    goods_exports = Column(Numeric(20, 4))
    goods_imports = Column(Numeric(20, 4))
    services_balance = Column(Numeric(20, 4))
    primary_income = Column(Numeric(20, 4))
    secondary_income = Column(Numeric(20, 4))
    capital_account_balance = Column(Numeric(20, 4))
    financial_account_balance = Column(Numeric(20, 4))
    direct_investment_abroad = Column(Numeric(20, 4))
    direct_investment_inward = Column(Numeric(20, 4))
    net_direct_investment = Column(Numeric(20, 4))
    portfolio_investment_assets = Column(Numeric(20, 4))
    portfolio_investment_liabilities = Column(Numeric(20, 4))
    net_portfolio_investment = Column(Numeric(20, 4))
    other_investment_assets = Column(Numeric(20, 4))
    other_investment_liabilities = Column(Numeric(20, 4))
    net_other_investment = Column(Numeric(20, 4))
    reserve_assets = Column(Numeric(20, 4))
    net_errors_omissions = Column(Numeric(20, 4))
    series_id = Column(String(50))
    data_source = Column(String(50))
    frequency = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())


class BISBankingFlows(Base):
    __tablename__ = "bis_banking_flows"

    id = Column(Integer, primary_key=True, index=True)
    report_date = Column(Date, nullable=False, index=True)
    reporting_country = Column(String(5), nullable=False)
    counterparty_country = Column(String(5))
    currency = Column(String(5))
    cross_border_claims = Column(Numeric(20, 4))
    cross_border_liabilities = Column(Numeric(20, 4))
    net_flows = Column(Numeric(20, 4))
    data_source = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
