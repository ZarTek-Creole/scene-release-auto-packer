/** Main App component. */

import { lazy, Suspense } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import { DebugPanel } from './components/DebugPanel';
import { ToastContainer } from './components/Toast';
import { ErrorBoundary } from './components/ErrorBoundary';
import './styles/App.css';

// Lazy load routes for code splitting
const Login = lazy(() => import('./pages/Login').then(m => ({ default: m.Login })));
const Dashboard = lazy(() => import('./pages/Dashboard').then(m => ({ default: m.Dashboard })));
const NewRelease = lazy(() => import('./pages/NewRelease').then(m => ({ default: m.NewRelease })));
const ReleasesList = lazy(() => import('./pages/ReleasesList').then(m => ({ default: m.ReleasesList })));
const ReleaseEdit = lazy(() => import('./pages/ReleaseEdit').then(m => ({ default: m.ReleaseEdit })));
const ReleaseDetail = lazy(() => import('./pages/ReleaseDetail').then(m => ({ default: m.ReleaseDetail })));
const Rules = lazy(() => import('./pages/Rules').then(m => ({ default: m.Rules })));
const Users = lazy(() => import('./pages/Users').then(m => ({ default: m.Users })));
const Roles = lazy(() => import('./pages/Roles').then(m => ({ default: m.Roles })));
const Config = lazy(() => import('./pages/Config').then(m => ({ default: m.Config })));

/**
 * Loading fallback component.
 */
function LoadingFallback() {
  return (
    <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '400px' }}>
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Chargement...</span>
      </div>
    </div>
  );
}

/**
 * Main App component with routing.
 */
function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <AuthProvider>
          <ErrorBoundary>
            <div className="app-shell">
              <Navbar />
              <main className="container-fluid">
                <Suspense fallback={<LoadingFallback />}>
                  <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route
                      path="/"
                      element={
                        <ProtectedRoute>
                          <Dashboard />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/releases/new"
                      element={
                        <ProtectedRoute>
                          <NewRelease />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/releases"
                      element={
                        <ProtectedRoute>
                          <ReleasesList />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/releases/:id/edit"
                      element={
                        <ProtectedRoute>
                          <ReleaseEdit />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/releases/:id"
                      element={
                        <ProtectedRoute>
                          <ReleaseDetail />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/rules"
                      element={
                        <ProtectedRoute>
                          <Rules />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/users"
                      element={
                        <ProtectedRoute>
                          <Users />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/roles"
                      element={
                        <ProtectedRoute>
                          <Roles />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/config"
                      element={
                        <ProtectedRoute>
                          <Config />
                        </ProtectedRoute>
                      }
                    />
                  </Routes>
                </Suspense>
              </main>
              <DebugPanel />
              <ToastContainer />
            </div>
          </ErrorBoundary>
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
