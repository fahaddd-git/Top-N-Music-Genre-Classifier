import { Outlet } from 'react-router-dom';
import { Header } from './Header';

/**
 * Appwide layout component. Should be used as the root element for react-router-dom's
 * base <Route>
 */
export const AppLayout = () => (
  <>
    <Header />
    <Outlet />
  </>
);
