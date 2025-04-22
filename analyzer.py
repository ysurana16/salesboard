import pandas as pd
import matplotlib.pyplot as plt

class SalesAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.preprocess()

    def preprocess(self):
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['Quantity'] = pd.to_numeric(self.df['Quantity'], errors='coerce')
        self.df['Unit Price'] = self.df['Unit Price'].replace({',': ''}, regex=True).astype(float)
        self.df['Cost Price'] = self.df['Cost Price'].replace({',': ''}, regex=True).astype(float)
        self.df['Credit Days'] = pd.to_numeric(self.df['Credit Days'], errors='coerce')

        self.df['Total Revenue'] = self.df['Quantity'] * self.df['Unit Price']
        self.df['Total Cost'] = self.df['Quantity'] * self.df['Cost Price']
        self.df['Profit'] = self.df['Total Revenue'] - self.df['Total Cost']
        self.df['Due Date'] = self.df['Date'] + pd.to_timedelta(self.df['Credit Days'], unit='D')
        self.df['Month'] = self.df['Date'].dt.to_period('M')

    # BASIC METRICS
    def get_summary(self):
        return {
            'Total Revenue': self.df['Total Revenue'].sum(),
            'Total Profit': self.df['Profit'].sum(),
            'Gross Margin %': (self.df['Profit'].sum() / self.df['Total Revenue'].sum()) * 100,
            'Average Order Value': self.df['Total Revenue'].sum() / len(self.df),
            'Unique Customers': self.df['Customer Name'].nunique(),
            'Unique Products': self.df['Product'].nunique(),
        }

    # PERFORMANCE & PROFITABILITY
    def best_selling_products(self, n=5):
        return self.df.groupby('Product')['Quantity'].sum().sort_values(ascending=False).head(n)

    def least_profitable_products(self, n=5):
        return self.df.groupby('Product')['Profit'].sum().sort_values().head(n)

    def profit_per_customer(self):
        return self.df.groupby('Customer Name')['Profit'].sum().sort_values(ascending=False)

    def sales_growth_rate(self):
        monthly = self.monthly_revenue()
        return monthly.pct_change().fillna(0)

    # RISK & OPERATIONS
    def aging_receivables(self):
        today = pd.Timestamp.now()
        self.df['Days Overdue'] = (today - self.df['Due Date']).dt.days
        return self.df[self.df['Days Overdue'] > 0][['Customer Name', 'Days Overdue']].groupby('Customer Name').mean()

    def credit_risk_score(self):
        return self.df.groupby('Customer Name')['Credit Days'].mean().sort_values(ascending=False)

    # ADVANCED CUSTOMER INSIGHTS
    def customer_lifetime_value(self):
        revenue = self.df.groupby('Customer Name')['Total Revenue'].sum()
        orders = self.df.groupby('Customer Name').size()
        return (revenue / orders).sort_values(ascending=False)  # avg value per order = CLV approx.

    def repeat_purchase_rate(self):
        order_counts = self.df.groupby('Customer Name').size()
        repeat_customers = order_counts[order_counts > 1].count()
        total_customers = order_counts.count()
        return repeat_customers / total_customers if total_customers > 0 else 0

    def top_regions_by_growth(self):
        monthly = self.df.groupby(['Month', 'Location'])['Total Revenue'].sum().reset_index()
        monthly['Revenue Growth'] = monthly.groupby('Location')['Total Revenue'].pct_change()
        return monthly.sort_values(by='Revenue Growth', ascending=False).dropna()

    # EXISTING ANALYTICS
    def top_customers(self, n=5):
        return self.df.groupby('Customer Name')['Total Revenue'].sum().sort_values(ascending=False).head(n)

    def product_performance(self):
        return self.df.groupby('Product')[['Total Revenue', 'Profit']].sum().sort_values(by='Total Revenue', ascending=False)

    def monthly_revenue(self):
        return self.df.groupby('Month')['Total Revenue'].sum()

    def location_performance(self):
        return self.df.groupby('Location')['Total Revenue'].sum().sort_values(ascending=False)

    def average_credit_days(self):
        return self.df.groupby('Customer Name')['Credit Days'].mean().sort_values(ascending=False)

    def raw(self):
        return self.df

    def to_json_summary(self):
        return {
            'summary': self.get_summary(),
            'top_customers': self.top_customers(5).to_dict(),
            'best_selling_products': self.best_selling_products(5).to_dict(),
            'least_profitable_products': self.least_profitable_products(5).to_dict(),
            'profit_per_customer': self.profit_per_customer().to_dict(),
            'aging_receivables': self.aging_receivables().round(1).to_dict(),
            'credit_risk_score': self.credit_risk_score().round(1).to_dict(),
            'customer_lifetime_value': self.customer_lifetime_value().round(2).to_dict(),
            'repeat_purchase_rate': round(self.repeat_purchase_rate(), 2),
            'top_regions_by_growth': self.top_regions_by_growth().to_dict(orient='records'),
            'product_performance': self.product_performance().round(2).reset_index().to_dict(orient='records'),
            'location_performance': self.location_performance().round(2).to_dict(),
            'average_credit_days': self.average_credit_days().round(1).to_dict(),
            'sales_growth_rate': self.sales_growth_rate().round(2).rename_axis(None).rename(lambda x: str(x)).to_dict(),
            'monthly_revenue': self.monthly_revenue().round(2).rename_axis(None).rename(lambda x: str(x)).to_dict()
            # 'sales_growth_rate': self.sales_growth_rate().round(1).to_dict(),
            # 'monthly_revenue': self.monthly_revenue().to_dict()
        }

    # VISUALIZATIONS
    def plot_monthly_revenue(self):
        revenue = self.monthly_revenue()
        revenue.plot(kind='line', marker='o', title='Monthly Revenue')
        plt.xlabel('Month')
        plt.ylabel('Revenue')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_top_customers(self, n=5):
        top = self.top_customers(n)
        top.plot(kind='bar', title='Top Customers by Revenue')
        plt.ylabel('Revenue')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_product_performance(self):
        perf = self.product_performance()
        perf.plot(kind='bar', figsize=(10,5), title='Product Performance')
        plt.ylabel('Amount')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
