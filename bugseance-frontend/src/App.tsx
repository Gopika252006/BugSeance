import { useState } from 'react';
import type { FormEvent, ChangeEvent } from 'react';

interface AnalyzeResponse {
  ghost_message: string;
  problem_summary: string;
  root_cause: string;
  evidence: string;
  proposed_fix: string;
  code_patch?: string;
  verification_steps: string;
  confidence: string;
  limitations?: string;
}

export default function App() {
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input_text: code })
      });
      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.detail || 'Server error');
      }
      const data = (await resp.json()) as AnalyzeResponse;
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>🐛 BugSéance – The Last Words of a Bug</h1>
      <form onSubmit={handleSubmit} className="bug-form">
        <textarea
          placeholder="Paste your code, error log, or stack trace here…"
          value={code}
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) => setCode(e.target.value)}
          rows={10}
          required
        />
        {loading ? <div className="spinner"></div> : <button type="submit" disabled={loading}>🪄 Summon the Ghost</button>}
      </form>
      {error && <p className="error">❗ {error}</p>}
      {result && (
        <div className="result">
          <h2>{result.ghost_message}</h2>
          <section><strong>Problem Summary:</strong> {result.problem_summary}</section>
          <section><strong>Root Cause:</strong> {result.root_cause}</section>
          <section><strong>Evidence:</strong> {result.evidence}</section>
          <section><strong>Proposed Fix:</strong> {result.proposed_fix}</section>
          {result.code_patch && (
            <section>
              <strong>Code Patch:</strong>
              <pre>{result.code_patch}</pre>
            </section>
          )}
          <section><strong>Verification Steps:</strong> {result.verification_steps}</section>
          <section><strong>Confidence:</strong> {result.confidence}</section>
          {result.limitations && (<section><strong>Limitations:</strong> {result.limitations}</section>)}
        </div>
      )}
    </div>
  );
}
