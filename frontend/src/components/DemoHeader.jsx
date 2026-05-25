import { useState, useEffect } from 'react';

export default function DemoHeader({ onReset, vertical }) {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <header
      role="banner"
      style={{
        background: scrolled
          ? 'rgba(10,22,40,0.96)'
          : 'rgba(10,22,40,0.92)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        color: 'white',
        padding: '0 28px',
        height: '66px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        position: 'sticky',
        top: 0,
        zIndex: 200,
        borderBottom: `1px solid ${scrolled ? 'rgba(255,255,255,0.09)' : 'rgba(255,255,255,0.06)'}`,
        boxShadow: scrolled ? '0 8px 32px rgba(0,0,0,0.4)' : '0 4px 24px rgba(0,0,0,0.25)',
        transition: 'all 0.3s ease',
      }}
    >
      {/* Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '13px' }}>
        <div style={{
          width: '40px', height: '40px',
          borderRadius: '12px',
          background: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '20px',
          boxShadow: '0 0 20px rgba(34,197,94,0.5), inset 0 1px 0 rgba(255,255,255,0.2)',
          flexShrink: 0,
          position: 'relative',
          overflow: 'hidden'
        }}>
          <span style={{ position: 'relative', zIndex: 1 }}>⚕️</span>
          <div style={{
            position: 'absolute', inset: 0,
            background: 'linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 60%)'
          }} />
        </div>
        <div>
          <div style={{
            fontSize: '19px', fontWeight: '900',
            letterSpacing: '-0.6px', lineHeight: 1,
            background: 'linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}>
            MedBridge
          </div>
          <div style={{
            fontSize: '9.5px', color: '#475569',
            letterSpacing: '1.5px', textTransform: 'uppercase',
            marginTop: '2px', fontWeight: '600'
          }}>
            {vertical ? `${vertical.icon} ${vertical.name}` : 'AI Workflow Platform'}
          </div>
        </div>
      </div>

      {/* Center */}
      <div style={{
        position: 'absolute', left: '50%', transform: 'translateX(-50%)',
        display: 'flex', alignItems: 'center', gap: '10px',
        fontSize: '13px',
      }}>
        <span style={{
          color: '#22c55e', fontWeight: '800',
          textShadow: '0 0 20px rgba(34,197,94,0.5)'
        }}>minutes.</span>
        <span style={{ color: '#1e3a5c' }}>·</span>
        <span style={{ textDecoration: 'line-through', color: '#334155', fontWeight: '500' }}>not weeks.</span>
      </div>

      {/* Right */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <div
          role="status"
          aria-label="Live demo active"
          style={{
            display: 'flex', alignItems: 'center', gap: '7px',
            background: 'rgba(34,197,94,0.1)',
            border: '1px solid rgba(34,197,94,0.3)',
            padding: '6px 14px',
            borderRadius: '100px',
            boxShadow: '0 0 12px rgba(34,197,94,0.15)',
          }}
        >
          <span style={{
            width: '7px', height: '7px', borderRadius: '50%',
            background: '#22c55e',
            display: 'inline-block',
            boxShadow: '0 0 8px rgba(34,197,94,0.8)',
            animation: 'pulse 2s infinite'
          }} />
          <span style={{ fontSize: '11px', fontWeight: '700', color: '#22c55e', letterSpacing: '1px' }}>
            LIVE DEMO
          </span>
        </div>

        {onReset && (
          <button
            onClick={onReset}
            aria-label="Start a new request"
            style={{
              background: 'rgba(255,255,255,0.07)',
              border: '1px solid rgba(255,255,255,0.13)',
              color: 'rgba(255,255,255,0.75)',
              padding: '7px 16px',
              borderRadius: '10px',
              cursor: 'pointer',
              fontSize: '12px',
              fontWeight: '600',
              transition: 'all 0.2s',
              letterSpacing: '0.3px',
              display: 'flex', alignItems: 'center', gap: '6px',
            }}
            onMouseEnter={e => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.13)';
              e.currentTarget.style.color = 'white';
              e.currentTarget.style.borderColor = 'rgba(255,255,255,0.22)';
            }}
            onMouseLeave={e => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.07)';
              e.currentTarget.style.color = 'rgba(255,255,255,0.75)';
              e.currentTarget.style.borderColor = 'rgba(255,255,255,0.13)';
            }}
          >
            <span style={{ fontSize: '14px' }}>↩</span> New Request
          </button>
        )}
      </div>
    </header>
  );
}
