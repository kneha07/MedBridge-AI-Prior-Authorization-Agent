import { useState, useEffect, useRef } from 'react';
import DemoHeader from './components/DemoHeader';
import VerticalSelector from './components/VerticalSelector';
import WorkflowForm from './components/WorkflowForm';
import AgentProgress from './components/AgentProgress';
import ResultCard from './components/ResultCard';

const API = 'http://localhost:8000';
const TERMINAL = new Set(['submitted', 'approved', 'denied', 'needs_info']);

export default function App() {
  const [view, setView]             = useState('select');   // select | form | progress | result
  const [verticals, setVerticals]   = useState([]);
  const [vertical, setVertical]     = useState(null);
  const [loading, setLoading]       = useState(false);
  const [workflowId, setWorkflowId] = useState(null);
  const [workflowData, setWorkflowData] = useState(null);
  const [startTime, setStartTime] = useState(null);
  const pollRef = useRef(null);

  useEffect(() => {
    fetch(`${API}/api/verticals`).then(r => r.json()).then(setVerticals).catch(() => {});
  }, []);

  const stopPolling = () => { if (pollRef.current) { clearInterval(pollRef.current); pollRef.current = null; } };

  const startPolling = (id) => {
    stopPolling();
    pollRef.current = setInterval(async () => {
      try {
        const res = await fetch(`${API}/api/workflow/${id}/status`);
        if (!res.ok) return;
        const data = await res.json();
        setWorkflowData(data);
        if (TERMINAL.has(data.status)) { stopPolling(); setView('result'); }
      } catch {}
    }, 1500);
  };

  useEffect(() => () => stopPolling(), []);

  const handleSelectVertical = (v) => { setVertical(v); setView('form'); };

  const handleSubmit = async (formData, aiProvider) => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/workflow/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vertical_id: vertical.id, ai_provider: aiProvider, form_data: formData })
      });
      if (!res.ok) throw new Error('Submission failed');
      const data = await res.json();
      setWorkflowId(data.workflow_id);
      setStartTime(Date.now());
      setView('progress');
      startPolling(data.workflow_id);
    } catch (err) {
      alert('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    stopPolling();
    try { await fetch(`${API}/api/demo/reset`, { method: 'POST' }); } catch {}
    setView('select'); setVertical(null); setWorkflowId(null); setWorkflowData(null); setStartTime(null);
  };

  const handleBack = () => { setView('select'); setVertical(null); };

  return (
    <div style={{ minHeight: '100vh' }}>
      <DemoHeader onReset={view !== 'select' ? handleReset : null} vertical={vertical} />

      {/* ── VERTICAL SELECTOR ── */}
      {view === 'select' && (
        <VerticalSelector verticals={verticals} onSelect={handleSelectVertical} />
      )}

      {/* ── FORM ── */}
      {view === 'form' && vertical && (
        <WorkflowForm
          vertical={vertical}
          onSubmit={handleSubmit}
          onBack={handleBack}
          loading={loading}
        />
      )}

      {/* ── PROGRESS ── */}
      {view === 'progress' && (
        <div>
          <div style={{
            background: 'linear-gradient(135deg, #060e1a 0%, #0a1628 40%, #0f2240 100%)',
            padding: '40px 24px', textAlign: 'center', color: 'white',
            borderBottom: '1px solid rgba(255,255,255,0.06)',
            position: 'relative', overflow: 'hidden',
          }}>
            <div style={{ position: 'absolute', top: '-40px', left: '20%', width: '200px', height: '200px', borderRadius: '50%', background: `radial-gradient(circle, ${vertical?.color || '#3b82f6'}20, transparent 70%)` }} />
            <div style={{ position: 'relative', zIndex: 1 }}>
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: '7px', background: 'rgba(59,130,246,0.12)', border: '1px solid rgba(59,130,246,0.3)', padding: '5px 14px', borderRadius: '100px', marginBottom: '14px' }}>
                <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#60a5fa', boxShadow: '0 0 8px rgba(96,165,250,0.8)', display: 'inline-block', animation: 'pulse 1.5s infinite' }} />
                <span style={{ fontSize: '10px', fontWeight: '700', color: '#60a5fa', letterSpacing: '1.3px', textTransform: 'uppercase' }}>
                  {vertical?.icon} {vertical?.name} Agent
                </span>
              </div>
              <h2 style={{ margin: '0 0 10px', fontSize: '28px', fontWeight: '900', letterSpacing: '-0.6px' }}>
                Handling Your Request
              </h2>
              <p style={{ margin: 0, color: '#475569', fontSize: '14px', fontWeight: '500' }}>
                Sit back — all 5 steps are being handled automatically
              </p>
            </div>
          </div>
          <AgentProgress steps={workflowData?.steps || []} status={workflowData?.status} workflowId={workflowId} vertical={vertical} startTime={startTime} />
        </div>
      )}

      {/* ── RESULT ── */}
      {view === 'result' && (
        <div>
          <div style={{
            background: 'linear-gradient(135deg, #052e16 0%, #14532d 40%, #166534 100%)',
            padding: '40px 24px', textAlign: 'center', color: 'white',
            borderBottom: '1px solid rgba(255,255,255,0.08)',
            position: 'relative', overflow: 'hidden',
          }}>
            <div style={{ position: 'absolute', top: '-40px', right: '20%', width: '200px', height: '200px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(34,197,94,0.15), transparent 70%)' }} />
            <div style={{ position: 'relative', zIndex: 1 }}>
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: '7px', background: 'rgba(34,197,94,0.15)', border: '1px solid rgba(34,197,94,0.35)', padding: '5px 14px', borderRadius: '100px', marginBottom: '14px', boxShadow: '0 0 16px rgba(34,197,94,0.2)' }}>
                <span>✓</span>
                <span style={{ fontSize: '10px', fontWeight: '700', color: '#4ade80', letterSpacing: '1.3px', textTransform: 'uppercase' }}>All 5 Steps Complete</span>
              </div>
              <h2 style={{ margin: '0 0 10px', fontSize: '28px', fontWeight: '900', letterSpacing: '-0.6px' }}>
                Successfully Submitted
              </h2>
              <p style={{ margin: 0, color: 'rgba(255,255,255,0.55)', fontSize: '14px', fontWeight: '500' }}>
                Your request has been processed and submitted — tracking is active
              </p>
            </div>
          </div>
          <AgentProgress steps={workflowData?.steps || []} status={workflowData?.status} workflowId={workflowId} vertical={vertical} startTime={startTime} />
          <ResultCard workflowData={workflowData} vertical={vertical} onStartNew={handleReset} />
        </div>
      )}
    </div>
  );
}
