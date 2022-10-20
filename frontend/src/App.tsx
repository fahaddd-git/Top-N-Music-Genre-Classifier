import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { AppLayout } from './components';

export default function App () {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<HomePage />} />
        </Route>
      </Routes>
    </Router>
  );
}
