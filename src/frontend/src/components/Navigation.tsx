import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navigation: React.FC = () => {
  const location = useLocation();

  return (
    <nav className="nav">
      <ul>
        <li>
          <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
            Dashboard
          </Link>
        </li>
        <li>
          <Link to="/inventory" className={location.pathname === '/inventory' ? 'active' : ''}>
            Inventory
          </Link>
        </li>
        <li>
          <Link to="/products" className={location.pathname === '/products' ? 'active' : ''}>
            Products
          </Link>
        </li>
        <li>
          <Link to="/sales" className={location.pathname === '/sales' ? 'active' : ''}>
            Sales
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navigation; 