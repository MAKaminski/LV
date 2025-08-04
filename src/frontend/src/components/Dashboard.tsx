import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface TopProduct {
  product_name: string;
  revenue: number;
  units_sold: number;
}

interface ProfitAnalysis {
  brand: string;
  total_profit: number;
  avg_margin: number;
}

interface AnalyticsData {
  top_by_revenue: TopProduct[];
  top_by_margin: TopProduct[];
  by_brand: ProfitAnalysis[];
  by_category: ProfitAnalysis[];
}

const Dashboard: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      const [topProductsRes, profitAnalysisRes] = await Promise.all([
        axios.get('/api/analytics/top-products'),
        axios.get('/api/analytics/profit-analysis')
      ]);

      setAnalyticsData({
        top_by_revenue: topProductsRes.data.top_by_revenue,
        top_by_margin: topProductsRes.data.top_by_margin,
        by_brand: profitAnalysisRes.data.by_brand,
        by_category: profitAnalysisRes.data.by_category
      });
    } catch (error) {
      console.error('Error fetching analytics data:', error);
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  if (loading) {
    return <div className="loading">Loading analytics...</div>;
  }

  return (
    <div className="dashboard">
      <h1>LV Project Dashboard</h1>
      
      <div className="dashboard-grid">
        {/* Top Products by Revenue */}
        <div className="chart-card">
          <h3>Top Products by Revenue</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analyticsData?.top_by_revenue}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="product_name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="revenue" fill="#0088FE" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Top Products by Margin */}
        <div className="chart-card">
          <h3>Top Products by Margin</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analyticsData?.top_by_margin}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="product_name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="margin" fill="#00C49F" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Profit by Brand */}
        <div className="chart-card">
          <h3>Profit by Brand</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={analyticsData?.by_brand}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ brand, total_profit }) => `${brand}: $${total_profit}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="total_profit"
              >
                {analyticsData?.by_brand.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Profit by Category */}
        <div className="chart-card">
          <h3>Profit by Category</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={analyticsData?.by_category}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ category, total_profit }) => `${category}: $${total_profit}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="total_profit"
              >
                {analyticsData?.by_category.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="summary-card">
          <h4>Total Revenue</h4>
          <p className="summary-value">
            ${analyticsData?.top_by_revenue.reduce((sum, product) => sum + product.revenue, 0).toFixed(2)}
          </p>
        </div>
        <div className="summary-card">
          <h4>Total Profit</h4>
          <p className="summary-value">
            ${analyticsData?.by_brand.reduce((sum, brand) => sum + brand.total_profit, 0).toFixed(2)}
          </p>
        </div>
        <div className="summary-card">
          <h4>Average Margin</h4>
          <p className="summary-value">
            {analyticsData?.by_brand.reduce((sum, brand) => sum + brand.avg_margin, 0) / (analyticsData?.by_brand.length || 1)}%
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 