import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface Product {
  id: string;
  name: string;
  revenue: number;
  margin: number;
}

interface AnalyticsData {
  topProducts: Product[];
  profitAnalysis: {
    byBrand: Array<{ brand: string; profit: number }>;
    byCategory: Array<{ category: string; profit: number }>;
  };
  summary: {
    totalRevenue: number;
    totalProfit: number;
    totalProducts: number;
    totalSales: number;
  };
}

const Dashboard: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch analytics data from backend
        const [topProductsRes, profitAnalysisRes] = await Promise.all([
          fetch('http://localhost:8000/api/analytics/top-products'),
          fetch('http://localhost:8000/api/analytics/profit-analysis')
        ]);

        const topProducts = await topProductsRes.json();
        const profitAnalysis = await profitAnalysisRes.json();

        // Mock summary data (in real app, this would come from backend)
        const summary = {
          totalRevenue: 125000,
          totalProfit: 45000,
          totalProducts: 150,
          totalSales: 89
        };

        setData({
          topProducts: topProducts.top_by_revenue || [],
          profitAnalysis,
          summary
        });
      } catch (error) {
        console.error('Error fetching data:', error);
        // Use mock data if API is not available
        setData({
          topProducts: [
            { id: '1', name: 'Product A', revenue: 25000, margin: 35 },
            { id: '2', name: 'Product B', revenue: 22000, margin: 28 },
            { id: '3', name: 'Product C', revenue: 18000, margin: 42 }
          ],
          profitAnalysis: {
            byBrand: [
              { brand: 'Brand A', profit: 15000 },
              { brand: 'Brand B', profit: 12000 },
              { brand: 'Brand C', profit: 8000 }
            ],
            byCategory: [
              { category: 'Category A', profit: 18000 },
              { category: 'Category B', profit: 14000 },
              { category: 'Category C', profit: 3000 }
            ]
          },
          summary: {
            totalRevenue: 125000,
            totalProfit: 45000,
            totalProducts: 150,
            totalSales: 89
          }
        });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (!data) {
    return <div className="loading">Error loading data</div>;
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div className="dashboard">
      <h1>LV Project Dashboard</h1>
      
      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="summary-card">
          <h4>Total Revenue</h4>
          <p className="summary-value">${data.summary.totalRevenue.toLocaleString()}</p>
        </div>
        <div className="summary-card">
          <h4>Total Profit</h4>
          <p className="summary-value">${data.summary.totalProfit.toLocaleString()}</p>
        </div>
        <div className="summary-card">
          <h4>Total Products</h4>
          <p className="summary-value">{data.summary.totalProducts}</p>
        </div>
        <div className="summary-card">
          <h4>Total Sales</h4>
          <p className="summary-value">{data.summary.totalSales}</p>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="dashboard-grid">
        {/* Top Products Chart */}
        <div className="chart-card">
          <h3>Top Products by Revenue</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.topProducts}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="revenue" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Profit by Brand */}
        <div className="chart-card">
          <h3>Profit by Brand</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={data.profitAnalysis.byBrand}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ brand, percent }) => `${brand} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="profit"
              >
                {data.profitAnalysis.byBrand.map((entry, index) => (
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
            <BarChart data={data.profitAnalysis.byCategory}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="profit" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Revenue Trend */}
        <div className="chart-card">
          <h3>Revenue Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data.topProducts}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="revenue" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 