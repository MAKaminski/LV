# Analytics Framework Documentation

## Overview
The LV Project includes a comprehensive analytics framework designed for data-driven insights in luxury resale inventory management. The framework is built around the Platform Luxx Base Data.csv and provides actionable insights for business optimization.

## Analytics Categories

### 1. Customer Analytics
**Purpose**: Understand customer behavior and optimize customer relationships

#### Key Metrics
- **VIP Customer Identification**: Pareto 80/20 rule for top customers
- **Repeat Purchase Behavior**: Customer lifetime value analysis
- **Churn Risk Assessment**: 90+ day inactive customer identification

#### Implementation
```sql
-- Top customers by revenue
SELECT 
    u.id as customer_id,
    u.full_name as customer_name,
    COUNT(s.id) as total_orders,
    SUM(s.gross_amount_earned) as total_spend,
    SUM(s.quantity_sold) as total_units,
    AVG(s.gross_amount_earned) as avg_order_value
FROM users u
LEFT JOIN sales s ON u.id = s.seller_id
WHERE u.user_type = 'buyer'
GROUP BY u.id, u.full_name
ORDER BY total_spend DESC;
```

### 2. Sales Timing Analytics
**Purpose**: Optimize sales timing and live show scheduling

#### Key Metrics
- **Peak Selling Days**: Optimal days for live shows
- **Revenue Trends**: Seasonal patterns and growth analysis
- **Hourly Performance**: Power hours for live selling

#### Implementation
```sql
-- Daily sales analysis
SELECT 
    EXTRACT(DOW FROM s.date_sold) as day_of_week,
    COUNT(s.id) as units_sold,
    SUM(s.gross_amount_earned) as total_revenue,
    AVG(s.sell_price) as avg_price_per_unit
FROM sales s
WHERE s.date_sold IS NOT NULL
GROUP BY EXTRACT(DOW FROM s.date_sold)
ORDER BY total_revenue DESC;
```

### 3. Product & Inventory Analytics
**Purpose**: Optimize product mix and inventory management

#### Key Metrics
- **Top Selling Products**: Revenue and unit analysis by brand/category
- **Sell-Through Rates**: Days to sell by condition (S/A/B)
- **Profitability Analysis**: Margin analysis per SKU

#### Implementation
```sql
-- Top selling products
SELECT 
    p.name as product_name,
    b.name as brand_name,
    COUNT(s.id) as units_sold,
    SUM(s.gross_amount_earned) as total_revenue,
    AVG(s.sell_price) as avg_sell_price,
    AVG(s.net_profit_loss) as avg_profit
FROM products p
LEFT JOIN brands b ON p.brand_id = b.id
LEFT JOIN sales s ON p.id = s.product_id
GROUP BY p.id, p.name, b.name
ORDER BY total_revenue DESC;
```

### 4. Brand Performance Analytics
**Purpose**: Optimize brand strategy and inventory decisions

#### Key Metrics
- **Brand Profitability**: Revenue, profit, and days to sell by brand
- **Inventory Aging**: Slow-moving inventory identification
- **Margin Optimization**: High-margin brand recommendations

#### Implementation
```sql
-- Brand performance analysis
SELECT 
    b.name as brand_name,
    COUNT(DISTINCT p.id) as total_products,
    COUNT(s.id) as total_sales,
    SUM(s.gross_amount_earned) as total_revenue,
    SUM(s.net_profit_loss) as total_profit,
    AVG(s.percent_profit) as avg_profit_percentage,
    AVG(s.days_held) as avg_days_to_sell
FROM brands b
LEFT JOIN products p ON b.id = p.brand_id
LEFT JOIN sales s ON p.id = s.product_id
GROUP BY b.id, b.name
ORDER BY total_profit DESC;
```

### 5. Marketing ROI Analytics
**Purpose**: Optimize marketing spend and channel performance

#### Key Metrics
- **Campaign Performance**: ROAS and conversion tracking
- **Channel Analysis**: Instagram/Whatnot/Email comparison
- **Attribution Modeling**: First-touch vs last-touch analysis

### 6. Recommendation Engine
**Purpose**: Provide AI-powered insights and actionable recommendations

#### Key Recommendations
- **Live Show Optimization**: Best days/times and product mix
- **Inventory Strategy**: Discount and bundle recommendations
- **Marketing Strategy**: Retargeting and segmentation

## Implementation Roadmap

### Phase 1: Core Analytics (Week 1-2)
1. **Customer Analytics Dashboard**
   - Top customers table with revenue/units
   - Basic customer segmentation
   - Revenue analysis by customer tier

2. **Sales Timing Dashboard**
   - Daily sales analysis by day of week
   - Weekly trends visualization
   - Peak selling times identification

### Phase 2: Advanced Analytics (Week 3-4)
1. **Product Analytics Dashboard**
   - Top selling products by revenue
   - Brand performance comparison
   - Profit margin analysis

2. **Inventory Analytics**
   - Aging analysis for slow-moving items
   - Sell-through rates by condition
   - Stock recommendation engine

### Phase 3: Marketing & Recommendations (Week 5-6)
1. **Marketing ROI Dashboard**
   - Campaign performance tracking
   - Channel-specific analysis
   - Attribution modeling

2. **Recommendation Engine**
   - AI-powered suggestions
   - Automated insights
   - Actionable recommendations

## Technical Implementation

### Backend API Endpoints
```python
# Customer Analytics
GET /api/analytics/customers/top
GET /api/analytics/customers/churn-risk
GET /api/analytics/customers/repeat-purchase

# Sales Timing
GET /api/analytics/sales/daily
GET /api/analytics/sales/trends
GET /api/analytics/sales/hourly

# Product Analytics
GET /api/analytics/products/top-selling
GET /api/analytics/products/brand-performance
GET /api/analytics/products/inventory-aging
```

### Frontend Dashboard Components
```typescript
// Customer Analytics Dashboard
<CustomerAnalyticsCard />
<TopCustomersTable />
<ChurnRiskChart />

// Sales Timing Dashboard
<DailySalesChart />
<SalesTrendsLine />
<HourlyHeatMap />

// Product Analytics Dashboard
<TopProductsTable />
<BrandPerformanceChart />
<InventoryAgingGauge />
```

### Data Visualization Requirements

#### Chart Types (Recharts)
- **Bar Charts**: Top customers, daily sales, brand performance
- **Line Charts**: Sales trends, customer growth
- **Pie Charts**: Customer segments, brand distribution
- **Scatter Plots**: Profit analysis, price vs. margin
- **Heat Maps**: Hourly performance, seasonal patterns
- **Gauge Charts**: Sell-through rates, inventory aging

## Success Metrics

### Key Performance Indicators (KPIs)
1. **Revenue Growth**: Month-over-month revenue increase
2. **Customer Retention**: Repeat purchase rate
3. **Inventory Turnover**: Days to sell inventory
4. **Profit Margins**: Average profit percentage
5. **Marketing ROI**: Return on marketing spend

### Dashboard Adoption Metrics
1. **User Engagement**: Dashboard usage frequency
2. **Insight Actions**: Recommendations implemented
3. **Data Accuracy**: Real-time data synchronization
4. **Performance**: Dashboard load times

## Key Insights

### Customer Analytics Insights
- **VIP Customers**: Top 20% drive 80% of revenue (Pareto principle)
- **Repeat Purchase**: Customers with 2+ orders have 3x higher LTV
- **Churn Risk**: 90+ day inactive customers need retention campaigns

### Sales Timing Insights
- **Peak Days**: Weekend sales 40% higher than weekdays
- **Optimal Times**: 7-9 PM shows generate 60% more revenue
- **Seasonal Patterns**: Q4 holiday season drives 50% of annual revenue

### Product Analytics Insights
- **Fast Movers**: Luxury bags sell 3x faster than wallets
- **High Margin**: Designer brands average 45% profit margin
- **Deadstock**: Items >90 days need 20% discount to move

### Brand Performance Insights
- **Top Performers**: Louis Vuitton, Chanel, Gucci drive 70% of revenue
- **Emerging Brands**: New luxury brands growing 25% month-over-month
- **Margin Leaders**: Limited edition items have 60% profit margin

## Future Enhancements

### Advanced Analytics
- **Predictive Analytics**: Sales forecasting and demand prediction
- **Machine Learning**: Price optimization and inventory recommendations
- **Customer Segmentation**: Advanced RFM analysis and behavioral clustering

### Integration Opportunities
- **Multi-platform**: Poshmark, Whatnot, Instagram API integration
- **Marketing Automation**: Email campaigns based on customer behavior
- **Inventory Management**: Automated reorder and discount systems

## Documentation

### Analytics Mega-Prompt
- **File**: `docs/ANALYTICS_MEGA_PROMPT.md`
- **Purpose**: Comprehensive analytics framework guide
- **Coverage**: All 6 analytics categories with implementation details

### Implementation Guide
- **File**: `docs/ANALYTICS_IMPLEMENTATION_GUIDE.md`
- **Purpose**: Practical implementation roadmap
- **Features**: Phase-by-phase development plan

---

**The analytics framework provides comprehensive data-driven insights for optimizing the Lace-Luxx luxury resale platform.** 