import { useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useClientStore } from '@/store/clientStore';

const ACTIVITY_EVENTS: (keyof WindowEventMap)[] = [
  'mousemove',
  'keypress',
  'click',
  'scroll',
  'touchstart',
];

const CHECK_INTERVAL_MS = 30_000; // check every 30 seconds

/**
 * Monitors user activity and logs out the portal session
 * after `timeoutMs` milliseconds of inactivity (default 30 min).
 * Only active when isPortalAuthenticated is true.
 */
export const useSessionTimeout = (
  timeoutMs: number = 30 * 60 * 1000,
): void => {
  const navigate = useNavigate();
  const isPortalAuthenticated = useClientStore((s) => s.isPortalAuthenticated);
  const lastActivity = useClientStore((s) => s.lastActivity);
  const resetActivity = useClientStore((s) => s.resetActivity);
  const portalLogout = useClientStore((s) => s.portalLogout);

  const handleActivity = useCallback(() => {
    resetActivity();
  }, [resetActivity]);

  useEffect(() => {
    if (!isPortalAuthenticated) return;

    // Register activity listeners
    ACTIVITY_EVENTS.forEach((evt) =>
      window.addEventListener(evt, handleActivity, { passive: true }),
    );

    // Periodic expiry check
    const intervalId = window.setInterval(() => {
      const elapsed = Date.now() - useClientStore.getState().lastActivity;
      if (elapsed > timeoutMs) {
        portalLogout();
        navigate('/cliente/login');
      }
    }, CHECK_INTERVAL_MS);

    return () => {
      ACTIVITY_EVENTS.forEach((evt) =>
        window.removeEventListener(evt, handleActivity),
      );
      window.clearInterval(intervalId);
    };
  }, [isPortalAuthenticated, timeoutMs, handleActivity, portalLogout, navigate]);
};
